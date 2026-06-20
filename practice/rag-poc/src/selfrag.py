"""
⑪ Self/CRAG-lite: 검색 필요여부 판단 + 검색 결과 관련성 채점.

  - should_retrieve(query): ⑤ 라우팅 보조. 아주 짧은 인사/잡담이면 검색 스킵.
  - grade_contexts(query, contexts): 검색 결과의 관련성 confidence(0~1) 산출.
    임계(config.RELEVANCE_THRESHOLD) 미만이면 파이프라인이 low_confidence 처리.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path
from typing import Dict, List

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import config

# 검색 없이 바로 응대할 짧은 인사/잡담 패턴(⑤ 라우팅).
_SMALLTALK = {
    "안녕", "안녕하세요", "하이", "헬로", "hello", "hi", "hey",
    "고마워", "고맙습니다", "감사", "감사합니다", "thanks", "thank you",
    "잘가", "바이", "bye", "ㅎㅇ", "ㄳ",
}


def should_retrieve(query: str) -> bool:
    """
    검색이 필요한 질의인가?
    매우 짧고(<=12자) 인사/잡담 키워드로만 이뤄지면 False(검색 스킵).
    그 외에는 보수적으로 True(놓치는 것보다 검색하는 게 안전).
    """
    q = query.strip().lower()
    if not q:
        return False
    normalized = re.sub(r"[^0-9a-z가-힣 ]", "", q).strip()
    if normalized in _SMALLTALK:
        return False
    tokens = normalized.split()
    if len(normalized) <= 12 and tokens and all(t in _SMALLTALK for t in tokens):
        return False
    return True


def _overlap_score(query: str, text: str) -> float:
    """질의-청크 토큰 자카드 유사도(휴리스틱 관련성). 0~1."""
    qt = set(re.findall(r"[0-9a-z]+|[가-힣]+", query.lower()))
    ct = set(re.findall(r"[0-9a-z]+|[가-힣]+", text.lower()))
    if not qt:
        return 0.0
    inter = len(qt & ct)
    return inter / len(qt)


def grade_contexts(query: str, contexts: List[Dict]) -> float:
    """
    검색 결과 관련성 confidence(0~1) 산출.
    두 신호를 결합한다:
      (a) 상위 컨텍스트의 질의-토큰 겹침(휴리스틱 — 더미 임베딩에도 견고)
      (b) 검색 점수(rerank_score 있으면 우선, 없으면 RRF score)의 존재
    더미 임베딩 환경에서도 동작하도록 (a)에 무게를 둔다.
    """
    if not contexts:
        return 0.0
    top = contexts[:3]
    overlaps = [_overlap_score(query, c["text"]) for c in top]
    best_overlap = max(overlaps) if overlaps else 0.0

    # 검색 점수 신호: 후보가 실제로 잡혔는지(0/약간). 정규화는 단순화.
    has_signal = 1.0 if any(c.get("score", 0) > 0 for c in top) else 0.0

    confidence = 0.8 * best_overlap + 0.2 * has_signal
    return round(min(confidence, 1.0), 4)


def is_low_confidence(confidence: float) -> bool:
    """임계 미만이면 low_confidence(무근거 폴백 대상)."""
    return confidence < config.RELEVANCE_THRESHOLD
