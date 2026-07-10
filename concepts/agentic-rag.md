# Agentic RAG

**한 줄 정의:** RAG에 **추론(Reasoning)**과 **자율성(Autonomy)**을 더한 2026년 최전선의 RAG.

## 진화 흐름
1. **RAG** — 지식 주입(오픈북)으로 지식 부재 해결.
2. **+ Reasoning** — [Chain of Thought](./reasoning.md)로 논리 붕괴 해결.
3. **+ Autonomy** — 여러 에이전트가 스스로 판단·협업.

## 핵심 전환: 생각 → 검색
- 부정확한 검색이 추론을 오염시킨다 → **먼저 생각하고(어떤 키워드로 검색할지) 그다음 검색.**
- 루프: 복잡한 질문을 **작게 쪼개기** → 검색 → 필요한 것만 재조합 → [Self-RAG](./self-rag.md) 반성 → 생성.

## 복잡도 폭발 → 오케스트레이션
- 검색·추론·멀티모달 도구가 늘며 복잡 → [에이전트 오케스트레이션](./agent-orchestration.md)으로 조율.
- 추론 구조: [Chain / Tree / Graph](./reasoning.md), 그리고 강화학습.

## 시대 인식
> **2026년은 혼란(Chaos)의 시기.** 논문들도 "다 써보는 단계"다. 이 혼란을 직접 느껴야 다음으로 성장한다.

## 기반 논문
- Two-world Agentic RAG with deep reasoning — https://arxiv.org/pdf/2507.09477
- Medical Graph RAG (의료 할루시네이션) — https://arxiv.org/pdf/2408.04187v1

## 관련 개념
[RAG](./rag.md) · [Self-RAG](./self-rag.md) · [Graph RAG](./graph-rag.md) · [추론](./reasoning.md) · [오케스트레이션](./agent-orchestration.md)
