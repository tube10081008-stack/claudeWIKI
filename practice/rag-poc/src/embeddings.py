"""
임베딩 추상화 (ingest/retrieve 공용).

핵심 안전장치:
  sentence-transformers 미설치 또는 모델 다운로드(네트워크) 실패 시,
  결정론적 **해시 기반 더미 임베딩**으로 자동 폴백한다.
  → 무거운 모델 없이도 전체 파이프라인이 최소 동작(스모크 테스트 가능).
  더미 임베딩은 의미를 모르지만, 같은 텍스트엔 같은 벡터를 주므로
  인덱스/검색 경로의 정합성 검증에는 충분하다.
"""

from __future__ import annotations

import hashlib
from typing import List

import numpy as np

import config

# 더미 임베딩 차원(실모델과 무관하게 고정; 인덱스 내부 일관성만 지키면 됨).
_DUMMY_DIM = 256

_real_model = None        # 지연 로딩된 SentenceTransformer 인스턴스
_use_dummy = None         # True=더미, False=실모델, None=미결정


def _try_load_real_model():
    """sentence-transformers 실모델 로딩 시도. 실패하면 None."""
    global _real_model
    try:
        from sentence_transformers import SentenceTransformer  # 지연 import
        _real_model = SentenceTransformer(config.EMBED_MODEL)
        return _real_model
    except Exception as e:  # 미설치·네트워크·OOM 등 모두 폴백 처리
        print(f"[embeddings] 실모델 로딩 실패 → 더미 임베딩 폴백: {e}")
        return None


def _ensure_backend():
    """백엔드(실모델/더미)를 1회 결정한다."""
    global _use_dummy
    if _use_dummy is not None:
        return
    model = _try_load_real_model()
    _use_dummy = model is None
    if not _use_dummy:
        print(f"[embeddings] 실모델 사용: {config.EMBED_MODEL}")


def using_dummy() -> bool:
    """현재 더미 임베딩 경로인지 여부(보고/디버깅용)."""
    _ensure_backend()
    return bool(_use_dummy)


def _dummy_embed_one(text: str) -> np.ndarray:
    """
    해시 기반 결정론적 더미 임베딩.
    텍스트를 공백 토큰으로 쪼개 각 토큰을 해시→차원 인덱스에 누적(bag-of-hashed-tokens).
    L2 정규화하여 코사인 유사도가 의미를 갖도록 한다.
    """
    vec = np.zeros(_DUMMY_DIM, dtype=np.float32)
    for tok in text.lower().split():
        h = int(hashlib.md5(tok.encode("utf-8")).hexdigest(), 16)
        vec[h % _DUMMY_DIM] += 1.0
    norm = np.linalg.norm(vec)
    if norm > 0:
        vec /= norm
    return vec


def embed_passages(texts: List[str]) -> np.ndarray:
    """문서(passage) 임베딩. (N, D) float32 배열, L2 정규화."""
    _ensure_backend()
    if _use_dummy:
        return np.vstack([_dummy_embed_one(t) for t in texts])
    # e5 계열 관례: passage 프리픽스.
    prefixed = [f"passage: {t}" for t in texts]
    emb = _real_model.encode(prefixed, normalize_embeddings=True,
                             convert_to_numpy=True, show_progress_bar=False)
    return np.asarray(emb, dtype=np.float32)


def embed_query(text: str) -> np.ndarray:
    """질의 임베딩. (D,) float32 벡터, L2 정규화."""
    _ensure_backend()
    if _use_dummy:
        return _dummy_embed_one(text)
    emb = _real_model.encode([f"query: {text}"], normalize_embeddings=True,
                             convert_to_numpy=True, show_progress_bar=False)
    return np.asarray(emb[0], dtype=np.float32)
