"""
⑦ 하이브리드 검색(Dense + BM25, RRF 융합) + ⑧ 재랭킹.

load_index() 로 eval/index.pkl 를 읽고,
hybrid_search(query, k) 가 [{chunk_id, text, source, section, score}] 를 반환.
  - Dense: 코사인 유사도 top-CANDIDATE_K
  - Sparse: BM25 top-CANDIDATE_K
  - 융합: RRF(Reciprocal Rank Fusion)
  - 선택: CrossEncoder 재랭킹(있으면; 없으면 RRF 순서 유지)
"""

from __future__ import annotations

import pickle
import re
import sys
from pathlib import Path
from typing import Dict, List, Optional

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import config
from src.embeddings import embed_query

_index = None         # 로딩된 인덱스 캐시
_bm25 = None          # BM25Okapi 인스턴스 캐시
_reranker = None      # CrossEncoder 캐시
_reranker_tried = False


def load_index(path: Optional[Path] = None) -> Dict:
    """인덱스(pickle) 로드 + BM25 구성(1회 캐시)."""
    global _index, _bm25
    if _index is not None:
        return _index
    path = path or config.INDEX_PATH
    if not Path(path).exists():
        raise FileNotFoundError(
            f"인덱스가 없습니다: {path}\n먼저 `python src/ingest.py` 를 실행하세요.")
    with open(path, "rb") as f:
        _index = pickle.load(f)

    # BM25 구성(미설치 시 None → sparse 축 비활성, dense만으로 동작).
    try:
        from rank_bm25 import BM25Okapi
        _bm25 = BM25Okapi(_index["bm25_corpus"])
    except Exception as e:
        print(f"[retrieve] rank_bm25 사용 불가 → dense-only: {e}")
        _bm25 = None
    return _index


def _tokenize(text: str) -> List[str]:
    """BM25 질의 토크나이저(ingest와 동일 규칙: 라틴/한글 분리)."""
    return re.findall(r"[0-9a-z]+|[가-힣]+", text.lower())


def _dense_rank(query: str, k: int) -> List[int]:
    """코사인 유사도 상위 k 청크 인덱스(내림차순)."""
    idx = load_index()
    emb = idx["embeddings"]              # (N, D), 정규화됨
    q = embed_query(query)               # (D,), 정규화됨
    sims = emb @ q                       # 정규화 가정 → 내적=코사인
    return list(np.argsort(-sims)[:k])


def _sparse_rank(query: str, k: int) -> List[int]:
    """BM25 상위 k 청크 인덱스. BM25 없으면 빈 리스트."""
    if _bm25 is None:
        return []
    scores = _bm25.get_scores(_tokenize(query))
    return list(np.argsort(-scores)[:k])


def _rrf_fuse(ranked_lists: List[List[int]], k_const: int) -> List[tuple]:
    """
    RRF: 각 리스트에서의 순위(rank) 역수를 합산.
      score(d) = Σ 1 / (k_const + rank_i(d))
    반환: [(chunk_idx, rrf_score), ...] 내림차순.
    """
    fused: Dict[int, float] = {}
    for ranked in ranked_lists:
        for rank, doc_idx in enumerate(ranked):
            fused[doc_idx] = fused.get(doc_idx, 0.0) + 1.0 / (k_const + rank)
    return sorted(fused.items(), key=lambda x: -x[1])


def _maybe_rerank(query: str, candidates: List[Dict]) -> List[Dict]:
    """
    ⑧ CrossEncoder 재랭킹. 모델 로딩 실패 시 입력 순서(RRF) 유지.
    재랭킹 점수는 'rerank_score'로 추가하고 그 순으로 정렬.
    """
    global _reranker, _reranker_tried
    if not config.RERANK or not candidates:
        return candidates
    if not _reranker_tried:
        _reranker_tried = True
        try:
            from sentence_transformers import CrossEncoder
            _reranker = CrossEncoder(config.RERANK_MODEL)
            print(f"[retrieve] 리랭커 사용: {config.RERANK_MODEL}")
        except Exception as e:
            print(f"[retrieve] 리랭커 사용 불가 → RRF 순서 유지: {e}")
            _reranker = None
    if _reranker is None:
        return candidates
    pairs = [(query, c["text"]) for c in candidates]
    scores = _reranker.predict(pairs)
    for c, s in zip(candidates, scores):
        c["rerank_score"] = float(s)
    return sorted(candidates, key=lambda c: -c["rerank_score"])


def hybrid_search(query: str, k: Optional[int] = None) -> List[Dict]:
    """
    하이브리드 검색 진입점.
    반환: 상위 k개 [{chunk_id, text, source, section, score}]
      score: RRF 융합 점수(재랭킹 시 rerank_score도 포함).
    """
    idx = load_index()
    k = k or config.TOP_K
    cand_k = config.CANDIDATE_K
    chunks = idx["chunks"]

    dense = _dense_rank(query, cand_k)
    sparse = _sparse_rank(query, cand_k)
    fused = _rrf_fuse([dense, sparse], config.RRF_K)

    # 재랭킹은 융합 상위 후보군에만 적용(비용 절감).
    top_candidates = fused[:cand_k]
    results: List[Dict] = []
    for doc_idx, rrf in top_candidates:
        c = chunks[doc_idx]
        results.append({
            "chunk_id": c["chunk_id"],
            "text": c["text"],
            "source": c["source"],
            "section": c["section"],
            "title": c["title"],
            "score": float(rrf),
        })

    results = _maybe_rerank(query, results)
    return results[:k]


if __name__ == "__main__":
    # 간단 수동 점검: python src/retrieve.py "질의"
    q = sys.argv[1] if len(sys.argv) > 1 else "LoRA가 뭐야?"
    for i, r in enumerate(hybrid_search(q), 1):
        print(f"{i}. [{r['source']} :: {r['section']}] score={r['score']:.4f}")
        print(f"   {r['text'][:80]}...")
