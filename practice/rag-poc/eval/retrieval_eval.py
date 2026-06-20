"""
검색 품질 평가 (LLM-free) — 골든셋의 근거 '출처(source)'를 정답으로 사용.

RAGAS의 context_precision/recall 축에 해당하는 부분을 LLM 없이 직접 측정한다.
세 가지 검색 구성을 같은 골든셋으로 비교:
  - dense_only : 임베딩 코사인만 (현 환경은 더미 임베딩 → P0 베이스라인)
  - bm25_only  : BM25 키워드만 (실제 lexical 신호)
  - hybrid     : Dense+BM25 RRF 융합 (블루프린트 권장 = P1)

지표(answerable 질의 대상, refusal/adversarial 제외):
  - Hit@1   : top-1 청크의 출처가 정답 출처에 포함된 비율
  - Recall@k: top-k 안에 정답 출처 청크가 하나라도 있는 비율
  - MRR     : 정답 출처가 처음 등장하는 순위의 역수 평균

실행: python eval/retrieval_eval.py
"""
from __future__ import annotations

import json
import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import config
from src import retrieve


def norm(src: str) -> str:
    """출처 경로를 파일명만으로 정규화(절대/상대/파일명 차이 흡수)."""
    return os.path.basename(str(src)).strip().lower()


def load_golden():
    items = []
    with open(config.EVAL_DIR / "golden_set.jsonl", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            o = json.loads(line)
            # answerable = 근거 출처가 있는 항목만(검색 평가 대상)
            srcs = {norm(e["source"]) for e in o.get("evidence", []) if e.get("source")}
            if o.get("type") in ("refusal",) or not srcs:
                continue
            items.append({"q": o["question"], "gold": srcs, "type": o["type"]})
    return items


def chunks_for(indices, idx):
    return [idx["chunks"][i] for i in indices]


def ranked_sources(query: str, mode: str, k: int):
    """구성별 top-k 청크의 출처 리스트(순위 순)."""
    idx = retrieve.load_index()
    if mode == "dense_only":
        ch = chunks_for(retrieve._dense_rank(query, k), idx)
    elif mode == "bm25_only":
        ranks = retrieve._sparse_rank(query, k)
        ch = chunks_for(ranks, idx) if ranks else []
    else:  # hybrid
        ch = retrieve.hybrid_search(query, k)
    return [norm(c["source"]) for c in ch]


def evaluate(mode: str, items, k: int):
    hit1 = rec = mrr = 0.0
    for it in items:
        srcs = ranked_sources(it["q"], mode, k)
        gold = it["gold"]
        if srcs and srcs[0] in gold:
            hit1 += 1
        if any(s in gold for s in srcs):
            rec += 1
        rr = 0.0
        for rank, s in enumerate(srcs, 1):
            if s in gold:
                rr = 1.0 / rank
                break
        mrr += rr
    n = len(items)
    return {"Hit@1": hit1 / n, f"Recall@{k}": rec / n, "MRR": mrr / n}


def main():
    k = config.TOP_K
    items = load_golden()
    print(f"평가 대상 answerable 질의: {len(items)}개 (refusal 제외), k={k}")
    print(f"임베딩 백엔드: {os.getenv('RAG_EMBED_MODEL', config.EMBED_MODEL)} "
          f"(HF 미접속 시 더미 임베딩으로 폴백됨)\n")

    rows = {}
    for mode in ("dense_only", "bm25_only", "hybrid"):
        rows[mode] = evaluate(mode, items, k)

    cols = ["Hit@1", f"Recall@{k}", "MRR"]
    print(f"{'구성':<12}" + "".join(f"{c:>12}" for c in cols))
    print("-" * (12 + 12 * len(cols)))
    for mode, m in rows.items():
        print(f"{mode:<12}" + "".join(f"{m[c]*100:>11.1f}%" if c != 'MRR'
                                      else f"{m[c]:>12.3f}" for c in cols))

    base = rows["dense_only"][f"Recall@{k}"]
    p1 = rows["hybrid"][f"Recall@{k}"]
    delta = (p1 - base) * 100
    print(f"\nΔ Recall@{k}: dense_only(P0) {base*100:.1f}% → hybrid(P1) {p1*100:.1f}% "
          f"({'+' if delta>=0 else ''}{delta:.1f}%p)")
    print("※ 현 환경은 더미 임베딩이라 dense 축이 약함. sentence-transformers 실모델"
          " 사용 시 dense·hybrid 모두 추가 상승(코드 변경 0).")


if __name__ == "__main__":
    main()
