# 📦 Week 1 — Step 1: RAG 4부작 종합 정리

> **한 문장 요약:** AI 1인 기업의 핵심은 '지식이 탑재된 AI'. RAG로 지식을 연결하고,
> Self-RAG·Graph RAG로 정교화하며, Agentic RAG로 추론·자율성을 더하고, 파인튜닝으로 두뇌를 특화한다.

| Day | 주제 | 핵심 키워드 | 노트 |
| --- | --- | --- | --- |
| **1** | 뿌리 찾기 | RAG, 할루시네이션, 파라/논파라 메모리, 인코더·벡터, MIPS | [day1](./day1-RAG.md) |
| **2** | 진화 (의심·연결) | Self-RAG(4기준), Graph RAG(태그·6단계) | [day2](./day2-self-rag-graph-rag.md) |
| **3** | 현재 (Agentic) | 추론(Chain/Tree/Graph), 오케스트레이션, HuggingFace, 로컬 vs 클라우드 | [day3](./day3-agentic-rag.md) |
| **4** | 미래 (파인튜닝) | RAG vs 파인튜닝, LoRA, 과적합, 학습 파라미터, SLM+RAG | [day4](./day4-finetuning-lora.md) |

---

## 🧠 전체 서사 (한 흐름으로)

```
일반 LLM (할루시네이션)
   │ 외부 지식을 붙이자
   ▼
RAG (오픈북 검색)                         ← Day 1
   │ 막 검색하니 'AI 슬롭'이 생김
   ▼
Self-RAG (스스로 의심·검증)               ← Day 2
   │ 점(點) 검색만으론 전체 맥락을 못 봄
   ▼
Graph RAG (점→선, 태그로 연결)            ← Day 2
   │ 추론·자율성·도구가 필요해짐
   ▼
Agentic RAG (생각→검색, 오케스트레이션)   ← Day 3
   │ 모델 자체를 내 것으로 만들고 싶음
   ▼
파인튜닝 / LoRA (두뇌 특화)               ← Day 4
   │ 비용·보안 문제
   ▼
미래: SLM + RAG (온프레미스 경량화)       ← Day 4
```

---

## 🎯 핵심 개념 치트시트

| 개념 | 한 줄 |
| --- | --- |
| **RAG** | 외부에서 찾아와(R) 강화해(A) 생성(G) |
| **할루시네이션** | 확률 모델이라 모르면 지어냄 |
| **파라/논파라 메모리** | 머릿속 지식 vs 외부 지식 창고 |
| **인코더·벡터** | 글자 → 수백 차원 좌표 (의미 비슷하면 가까이) |
| **MIPS** | 가장 비슷한 벡터를 광속 검색 |
| **Self-RAG** | isRetrieve/isRelevant/isSupported/isUseful 4기준 자가검증 |
| **Graph RAG** | 점→선 연결, 태그 기반, 6단계(청킹→엔티티→그래프→커뮤니티→요약→Map-Reduce) |
| **Agentic RAG** | RAG + 추론 + 자율성, "생각하고 검색" |
| **RAG vs 파인튜닝** | 검색해 오기(오픈북) vs 두뇌 자체 변경 |
| **LoRA** | y=wx+b의 끝 행렬만(~0.29%) 변경 = 저비용 특화 |
| **과적합/과소적합** | 너무 많이 학습=꼰대 / 너무 적게=인식 실패 |
| **SLM + RAG** | 경량 모델 + 강력 RAG = 2027 주류 (보안·비용) |

---

## 🛠️ 도구 맵

| 도구 | 역할 |
| --- | --- |
| NotebookLM / Gemini | 문서 기반 RAG 체험 |
| Google OPAL | 멀티소스 지식 연결 |
| Antigravity | 마크다운 지식 + 모델 연결, 코드/웹 생성 |
| Hugging Face | 모델 앱스토어 (258만 개) |
| Unsloth | 무료·저사양 파인튜닝 |
| Ollama / LM Studio | 로컬 모델 실행 |
| Connect AI | 로컬 모델을 에이전트로 연결 |
| GitHub | 온라인 지식 메모리 (동기화) |

---

## 💼 비즈니스 기회 (Day 4)

1. 로컬 LLM 자동화 에이전트 구축 · 2. 두뇌 파인튜닝 판매 · 3. Physical AI ·
4. On-device AI · 5. 맞춤형 로컬 LLM 구축 스타트업

> 진입 장벽 = **AI 지식 + 바이브 코딩 + 사업 능력** 3박자. 그래서 기회가 크다.

---

→ 개념 사전: [`../../concepts/`](../../concepts/) · 실습 기록: [`../../practice/`](../../practice/) · 오케스트레이션: [`../../agents/`](../../agents/)
