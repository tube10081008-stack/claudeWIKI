"""
RAGAS 평가 + CI 임계 게이트 (③ RAGAS 하니스 / §3.4 게이트).

골든셋(eval/golden_set.jsonl)으로 파이프라인을 돌려 4지표를 측정하고,
config.RAGAS_THRESHOLDS 미달 시 exit code 1(머지 차단).

  - RAGAS + LLM 자격증명이 있으면 진짜 RAGAS 4지표를 계산.
  - 미설치/무인증(stub·더미 임베딩 환경) 시 **오프라인 근사 지표**로 폴백해
    파이프라인 정합성과 게이트 로직만이라도 검증한다(주석으로 명시).

실행:  python eval/evaluate.py
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path
from typing import Dict, List

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import config
from src.pipeline import answer

GOLDEN_PATH = config.EVAL_DIR / "golden_set.jsonl"


def load_golden() -> List[Dict]:
    """골든셋(1줄 1 JSON) 로드."""
    items = []
    for line in GOLDEN_PATH.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if line:
            items.append(json.loads(line))
    return items


def run_pipeline(items: List[Dict]) -> List[Dict]:
    """각 골든 질의를 파이프라인에 통과시켜 답/컨텍스트 수집."""
    rows = []
    for it in items:
        res = answer(it["question"])
        rows.append({
            "question": it["question"],
            "ground_truth": it["ground_truth"],
            "answer": res["answer"],
            "contexts": [c["text"] for c in res.get("contexts", [])],
            "context_sources": [c["source"] for c in res.get("contexts", [])],
            "evidence_sources": [e["source"] for e in it.get("evidence", [])],
            "type": it["type"],
            "low_confidence": res.get("low_confidence", False),
        })
    return rows


# ───────────────────── RAGAS 경로 ─────────────────────

def evaluate_with_ragas(rows: List[Dict]) -> Dict[str, float]:
    """진짜 RAGAS 4지표. 실패 시 RuntimeError 발생 → 호출부에서 폴백."""
    from datasets import Dataset
    from ragas import evaluate
    from ragas.metrics import (
        faithfulness, answer_relevancy,
        context_precision, context_recall,
    )

    ds = Dataset.from_dict({
        "question": [r["question"] for r in rows],
        "answer": [r["answer"] for r in rows],
        "contexts": [r["contexts"] or [""] for r in rows],
        "ground_truth": [r["ground_truth"] for r in rows],
    })
    result = evaluate(ds, metrics=[
        faithfulness, answer_relevancy, context_precision, context_recall,
    ])
    # ragas 결과를 평이한 dict로 정규화.
    return {k: float(v) for k, v in dict(result).items()}


# ───────────────── 오프라인 근사 폴백 ─────────────────

def _toks(text: str) -> set:
    return set(re.findall(r"[0-9a-z]+|[가-힣]+", text.lower()))


def evaluate_offline(rows: List[Dict]) -> Dict[str, float]:
    """
    RAGAS/LLM 없이 동작하는 **근사 지표**(스모크/CI 골격 검증용).
    실제 RAGAS 점수와 다르므로 운영 게이트로 쓰면 안 됨(주석 명시).
      - faithfulness ≈ 답변 토큰이 컨텍스트로 뒷받침되는 비율
      - answer_relevancy ≈ 답변-질문 토큰 자카드
      - context_precision ≈ 가져온 출처 중 evidence에 속한 비율
      - context_recall ≈ evidence 출처를 컨텍스트가 커버한 비율
    refusal/adversarial은 evidence가 없으므로 검색 회피/저신뢰면 만점 처리.
    """
    f, ar, cp, cr = [], [], [], []
    for r in rows:
        a_tok, q_tok = _toks(r["answer"]), _toks(r["question"])
        ctx_tok = _toks(" ".join(r["contexts"]))
        no_evidence = len(r["evidence_sources"]) == 0

        # faithfulness: 답변 토큰의 컨텍스트 뒷받침 비율
        if no_evidence:
            f.append(1.0 if (r["low_confidence"] or "자료에 없음" in r["answer"]) else 0.5)
        else:
            f.append(len(a_tok & ctx_tok) / len(a_tok) if a_tok else 0.0)

        # answer_relevancy: 답변-질문 겹침
        ar.append(len(a_tok & q_tok) / len(q_tok) if q_tok else 0.0)

        srcs = set(r["context_sources"])
        ev = set(r["evidence_sources"])
        if no_evidence:
            cp.append(1.0); cr.append(1.0)  # 거절류는 검색 정밀/재현 평가 제외(만점 간주)
        else:
            cp.append(len(srcs & ev) / len(srcs) if srcs else 0.0)
            cr.append(len(srcs & ev) / len(ev) if ev else 0.0)

    n = max(len(rows), 1)
    return {
        "faithfulness": sum(f) / n,
        "answer_relevancy": sum(ar) / n,
        "context_precision": sum(cp) / n,
        "context_recall": sum(cr) / n,
    }


# ───────────────────── 게이트 ─────────────────────

def gate(scores: Dict[str, float]) -> bool:
    """RAGAS 임계 게이트. 모두 통과면 True."""
    ok = True
    print("\n=== RAGAS 게이트 ===")
    for metric, thresh in config.RAGAS_THRESHOLDS.items():
        val = scores.get(metric, 0.0)
        passed = val >= thresh
        ok = ok and passed
        mark = "PASS" if passed else "FAIL"
        print(f"  {metric:20s} {val:.3f}  (>= {thresh})  [{mark}]")
    print(f"=== 결과: {'PASS' if ok else 'FAIL (머지 차단)'} ===")
    return ok


def main() -> int:
    items = load_golden()
    print(f"[evaluate] 골든셋 {len(items)}개 로드")
    rows = run_pipeline(items)

    try:
        scores = evaluate_with_ragas(rows)
        print("[evaluate] RAGAS 실측 사용")
    except Exception as e:
        print(f"[evaluate] RAGAS 사용 불가 → 오프라인 근사 폴백: {e}")
        print("           (근사 지표는 골격 검증용 — 운영 게이트로 쓰지 말 것)")
        scores = evaluate_offline(rows)

    passed = gate(scores)
    return 0 if passed else 1


if __name__ == "__main__":
    sys.exit(main())
