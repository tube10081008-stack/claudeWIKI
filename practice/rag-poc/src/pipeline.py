"""
질의 파이프라인 전체 흐름 (⑤ 라우팅 → ⑦ 검색 → ⑧ 재랭킹 → ⑪ 자가검증 → ⑩ 생성).

answer(query) → {
    query, answer, citations, contexts, low_confidence, confidence, retrieved
}

CLI:  python src/pipeline.py "<질의>"
"""

from __future__ import annotations

import sys
from pathlib import Path
from typing import Dict

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import config
from src.retrieve import hybrid_search
from src.generate import generate
from src.selfrag import should_retrieve, grade_contexts, is_low_confidence


def answer(query: str) -> Dict:
    """단일 질의에 대한 전체 RAG 흐름."""
    # ⑤ 라우팅: 인사/잡담은 검색 스킵.
    if not should_retrieve(query):
        return {
            "query": query,
            "answer": "안녕하세요! 위키 내용에 대해 무엇이든 물어보세요.",
            "citations": [],
            "contexts": [],
            "low_confidence": False,
            "confidence": None,
            "retrieved": False,
        }

    # ⑦⑧ 하이브리드 검색 + (선택) 재랭킹.
    contexts = hybrid_search(query, k=config.TOP_K)

    # ⑪ 자가검증: 관련성 채점 → 저신뢰면 폴백.
    confidence = grade_contexts(query, contexts)
    low_conf = is_low_confidence(confidence)

    # ⑩ 인용 강제 생성(저신뢰 시 무근거 폴백).
    gen = generate(query, contexts, low_confidence=low_conf)

    return {
        "query": query,
        "answer": gen["answer"],
        "citations": gen["citations"],
        "contexts": contexts,
        "low_confidence": gen["low_confidence"],
        "confidence": confidence,
        "retrieved": True,
    }


def _print_result(res: Dict) -> None:
    """CLI 출력(인용 포함)."""
    print("=" * 70)
    print(f"질의: {res['query']}")
    print("-" * 70)
    print(res["answer"])
    print("-" * 70)
    if res.get("confidence") is not None:
        flag = " (low_confidence)" if res["low_confidence"] else ""
        print(f"관련성 confidence: {res['confidence']}{flag}")
    if res["citations"]:
        print("인용 출처:")
        for src in res["citations"]:
            print(f"  - {src}")
    if res.get("contexts"):
        print(f"검색 컨텍스트 {len(res['contexts'])}개:")
        for c in res["contexts"]:
            print(f"  · [{c['source']} :: {c['section']}] score={c['score']:.4f}")
    print("=" * 70)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print('사용법: python src/pipeline.py "<질의>"')
        sys.exit(0)
    query = " ".join(sys.argv[1:])
    _print_result(answer(query))
