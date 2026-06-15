# 🧠 claudeWIKI — AI 1인 기업 지식 뇌 (Knowledge Brain)

> **"외부에서 정보를 찾아와(Retrieval), 능력을 강화해(Augmented), 답변을 만든다(Generation)."**

이 저장소는 **AI 1인 기업가 과정**의 학습 내용을 구조화하여 축적하는 **나만의 지식 네트워크**입니다.
강의에서 배운 RAG의 핵심 원리("논파라메트릭 메모리 = 외부 지식 창고")를 그대로 실천합니다.

- **로컬 메모리** = 내 컴퓨터의 작업 공간
- **온라인 메모리** = 이 GitHub 저장소 (동기화로 항상 최신 상태 유지)

이렇게 지식을 구조화해두면, 어떤 AI 모델(Gemini, Claude, Gemma 등)을 쓰더라도
이 지식을 불러와 **나만의 독창적인 결과물**을 생성할 수 있습니다.

---

## 🗺️ 저장소 지도 (Index)

| 폴더 | 내용 |
| --- | --- |
| [`curriculum/`](./curriculum/) | 8주 전체 커리큘럼 개요 |
| [`lectures/`](./lectures/) | 날짜별 강의 학습 노트 |
| [`concepts/`](./concepts/) | 핵심 개념 사전 (RAG, 인코더, 벡터, MIPS 등) |
| [`practice/`](./practice/) | 실습 코드 & 결과 기록 |
| [`agents/`](./agents/) | AI 에이전트 워크플로우 청사진 (오케스트레이션 설계도) |

---

## 📚 학습 진행 현황

| 주차 | 단계 | 주제 | 상태 |
| --- | --- | --- | --- |
| 1~4주 | **Step 1: RAG** | 지능 구축 (지식 네트워크) | ✅ Day 1~4 완료 (Step 1 이론 완결) |
| 5~8주 | **Step 2: Agent** | 자동화 실행 (자율 에이전트) | 🟡 진행 중 (Day 5 완료) |

### 완료한 강의
- [x] [Week 1 · Day 1 — RAG의 뿌리 찾기](./lectures/week1/day1-RAG.md)
- [x] [Week 1 · Day 2 — 진화의 시작: Self-RAG & Graph RAG](./lectures/week1/day2-self-rag-graph-rag.md)
- [x] [Week 1 · Day 3 — Agentic RAG: 추론과 자율성](./lectures/week1/day3-agentic-rag.md)
- [x] [Week 1 · Day 4 — 미래 예상 & 파인튜닝/LoRA](./lectures/week1/day4-finetuning-lora.md)
- [x] [Week 2 · Day 5 — 로컬→클라우드 에이전트 연결 (Antigravity SDK)](./lectures/week2/day5-antigravity-sdk.md)

> 🎯 **Step 1(RAG) 4부작 완결:** 뿌리(Day1) → 진화(Day2) → 현재(Day3) → 미래(Day4)
> 📦 **[Week 1 종합 정리 & 치트시트](./lectures/week1/README.md)**
> 🚀 **Step 2 진입:** Day5 — 에이전트를 코드로 직접 만들기 (SDK) + 하이브리드 비용 절감

---

## 🧭 황금 3법칙 (이 저장소의 운영 원칙)

1. **지식 구조화가 먼저** — 데이터를 쏟아붓지 말고 네트워크로 설계한다.
2. **목적에 맞는 모델 선택** — 작업 성격에 맞는 AI 모델을 RAG와 결합한다.
3. **에이전트화** — 찾은 정보로 AI가 스스로 다음 단계를 실행하게 만든다.

---

## 🔄 동기화 워크플로우

```
[로컬 작업] → git commit → git push → [GitHub 온라인 메모리]
                                            │
                          다음 세션의 AI가 이 지식을 다시 불러옴 (RAG)
```

> 세션은 임시(ephemeral)이므로, 학습한 지식은 반드시 커밋·푸시하여 영속화합니다.
