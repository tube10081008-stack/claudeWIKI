"""
⑩ 생성: 검색 청크를 컨텍스트로 인용 강제 답변.

generate(query, contexts) → {answer, citations, low_confidence}
  - 인용 강제 프롬프트: 모든 사실 주장에 [source] 인용을 붙이도록 지시.
  - LLM provider 미설정(config.LLM_PROVIDER is None) 시 stub 생성기로 폴백:
    검색 컨텍스트에서 질의 관련 문장을 추출/요약해 인용과 함께 답한다(무인증 실행).
  - low_confidence=True 이면 "자료에 없음" 폴백 응답(가드레일 §7).
"""

from __future__ import annotations

import re
import sys
from pathlib import Path
from typing import Dict, List

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import config

# 인용 강제 시스템 프롬프트(운영 LLM 경로에서 사용).
CITATION_SYSTEM_PROMPT = """\
너는 사내 위키 검색 어시스턴트다. 아래 '컨텍스트'에 있는 내용만 근거로 답하라.
규칙:
1) 모든 사실 주장 끝에 반드시 출처를 [source] 형식으로 인용하라.
2) 컨텍스트에 없는 내용은 절대 지어내지 말고 "자료에 없음"이라고 답하라.
3) 한국어로 간결하게 답하라.
"""


def _build_prompt(query: str, contexts: List[Dict]) -> str:
    """LLM 호출용 사용자 프롬프트(컨텍스트 + 질의) 구성."""
    blocks = []
    for c in contexts:
        blocks.append(f"[{c['source']}] ({c['section']})\n{c['text']}")
    ctx = "\n\n---\n\n".join(blocks)
    return f"컨텍스트:\n{ctx}\n\n질문: {query}\n\n답변(모든 사실에 [source] 인용):"


def _fallback_answer(sources: List[str]) -> Dict:
    """무근거/저신뢰 폴백 응답(가드레일: 단정 금지)."""
    return {
        "answer": "자료에 없음 — 제공된 위키 컨텍스트에서 근거를 찾지 못했습니다.",
        "citations": sources,
        "low_confidence": True,
    }


def _split_sentences(text: str) -> List[str]:
    """한국어/영어 혼용 단순 문장 분리."""
    parts = re.split(r"(?<=[.!?。])\s+|\n+", text)
    return [p.strip(" -*•\t") for p in parts if p.strip(" -*•\t")]


def _stub_generate(query: str, contexts: List[Dict]) -> Dict:
    """
    LLM 미설정 시 폴백 생성기.
    질의 토큰과 겹침이 큰 문장을 컨텍스트에서 추출해 인용과 함께 묶는다.
    (의미 생성은 아니지만, 인용 강제 계약과 무인증 실행을 보장.)
    """
    q_tokens = set(re.findall(r"[0-9a-z]+|[가-힣]+", query.lower()))
    scored = []
    for c in contexts:
        for sent in _split_sentences(c["text"]):
            st = set(re.findall(r"[0-9a-z]+|[가-힣]+", sent.lower()))
            overlap = len(q_tokens & st)
            if overlap > 0:
                scored.append((overlap, sent, c["source"]))
    scored.sort(key=lambda x: -x[0])

    if not scored:
        # 겹치는 문장이 없으면 최상위 컨텍스트 첫 문장으로라도 근거 제시.
        top = contexts[0]
        first = _split_sentences(top["text"])[:1]
        if not first:
            return _fallback_answer([c["source"] for c in contexts])
        scored = [(0, first[0], top["source"])]

    # 상위 3개 문장을 인용과 함께 합성.
    picked = scored[:3]
    lines = [f"- {sent} [{src}]" for _, sent, src in picked]
    citations = list(dict.fromkeys(src for _, _, src in picked))  # 순서 보존 중복제거
    answer = "관련 근거:\n" + "\n".join(lines)
    return {"answer": answer, "citations": citations, "low_confidence": False}


def _llm_generate(query: str, contexts: List[Dict]) -> Dict:
    """
    운영 LLM provider 경로(스텁).
    config.LLM_PROVIDER 설정 시 여기서 실제 호출을 구현한다.
    PoC에서는 미구현 → stub로 위임(무인증 실행 유지).
    """
    # 예시(운영 구현 자리):
    #   prompt = _build_prompt(query, contexts)
    #   resp = call_provider(config.LLM_PROVIDER, CITATION_SYSTEM_PROMPT, prompt)
    #   return parse_answer_and_citations(resp)
    return _stub_generate(query, contexts)


def generate(query: str, contexts: List[Dict],
             low_confidence: bool = False) -> Dict:
    """
    답변 생성 진입점.
    low_confidence=True 또는 컨텍스트 없음 → 무근거 폴백.
    그 외에는 provider(있으면) 또는 stub로 인용 강제 답변.
    """
    sources = list(dict.fromkeys(c["source"] for c in contexts))
    if low_confidence or not contexts:
        return _fallback_answer(sources)

    if config.LLM_PROVIDER:
        return _llm_generate(query, contexts)
    return _stub_generate(query, contexts)
