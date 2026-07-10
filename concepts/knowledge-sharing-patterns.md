# 멀티에이전트 지식 공유 패턴 (3종)

**한 줄 정의:** 에이전트가 많아질수록 멍청해지는 문제를 푸는 3가지 지식 공유 방식. 단계적으로 진화한다.

## ① Shared Message Pool (블랙보드) — MetaGPT / AutoGen GroupChat
- 1:1 대화 대신 **가운데 공유 게시판** 하나를 두고 일함.
- **Publish-Subscribe:** 산출물을 게시판에 발행 → 필요한 에이전트가 구독해 업데이트.
- **표준 운영 절차(SOP)** 기반. → 100개로 늘어도 안 꼬이고 **Single Source of Truth** 공유, 토큰↓.
- 논문: https://arxiv.org/pdf/2308.00352

## ② Shared Environment & Memory — AgentVerse / Generative Agents
- 에이전트들을 **하나의 가상 데이터 공간(Environment)**에 함께 넣음.
- A가 행동 → 공유 환경 DB에 기록 → 다른 에이전트가 **관찰(Observation)**하다 자동 흡수.
- **위키 동시 편집**·소문 전파와 유사 (단, 데이터 공유는 왜곡 없이 빠름).
- 논문: https://arxiv.org/abs/2308.10848

## ③ Exchange of Thought (EoT) — Multi-Agent Debate / ChatEval
- 완성 지식이 아니라 **추론 과정(컨텍스트) 자체**를 실시간 공유.
- A의 생각을 B가 받아 보완 → 서로의 프롬프트 메모리를 엮음.
- 개별 편향·할루시네이션이 **필터링** → 혼자선 불가능한 **집단지성** 형성.
- 논문: https://arxiv.org/pdf/2308.07201

## 구현 로드맵
Step1 공유 지식 만들기(SOP) → Step2 모두가 함께 갖기 → Step3 평가·추론·개선(EoT).

## 관련 개념
[멀티에이전트](./multi-agent.md) · [Self-RAG](./self-rag.md) · [오케스트레이션](./agent-orchestration.md)
