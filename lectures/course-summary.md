# 🎓 AI 1인 기업 — 전체 강의 종합 (완강 캡스톤)

> **단 하나의 메시지:** 인공지능 모델은 소비재, **데이터는 자산**.
> 모델은 6개월마다 바뀌지만, 검증·축적한 데이터는 대체 불가능한 평생 자산이 된다.

이 문서는 1~7강 전체를 하나로 꿰는 마스터 정리입니다.
세부는 각 [Day 노트](./)와 [개념 사전](../concepts/)으로 링크됩니다.

---

## 🧭 전체 서사 (Day 1 → Day 7)

```
              ┌──────────────── Step 1: RAG (지능 구축) ────────────────┐
일반 LLM ─► RAG ─► Self-RAG ─► Graph RAG ─► Agentic RAG ─► 파인튜닝/LoRA ─► (미래) SLM+RAG
(할루시)   (검색)  (의심)      (연결)       (추론·자율)    (두뇌 특화)        (온프레미스)
 Day1 ───────────── Day2 ────────── Day3 ────────────── Day4 ─────────────────────┘
                                                                  │
              ┌──────────────── Step 2: Agent (자동화 실행) ───────┴───────┐
        SDK 연결 ────────► 장기기억·데이터 자산화 ────────► 멀티에이전트·집단지성
       (로컬↔클라우드)       (모델 소비재/데이터 자산)         (지식 공유로 똑똑해짐)
         Day5 ──────────────── Day6 ───────────────────────── Day7
```

### 두 기둥, 하나의 다리
| | **단기기억** | **장기기억** |
| --- | --- | --- |
| 정체 | **RAG** (검색해 쓰는 외부 지식) | **파인튜닝** (두뇌에 각인) |
| 저장소 | GitHub | Hugging Face (데이터셋·모델) |
| 강의 | Day 1~4 | Day 6 |
| 다리 | — **Day 5 (에이전트 SDK)** 가 둘을 연결 — | |
| 확장 | — **Day 7 (멀티에이전트)** 가 여러 두뇌를 공유 — | |

---

## 📚 강의별 한 줄 요약

| Day | 제목 | 한 줄 | 노트 |
| --- | --- | --- | --- |
| 1 | RAG의 뿌리 | 외부에서 찾아와(R) 강화해(A) 생성(G) → 할루시네이션 해결 | [day1](./week1/day1-RAG.md) |
| 2 | 진화 | Self-RAG(스스로 의심) + Graph RAG(점→선 연결, 태그) | [day2](./week1/day2-self-rag-graph-rag.md) |
| 3 | Agentic RAG | 생각하고 검색, 추론·자율성, 오케스트레이션, HuggingFace | [day3](./week1/day3-agentic-rag.md) |
| 4 | 미래·파인튜닝 | RAG vs 파인튜닝, LoRA(0.6% 학습), SLM+RAG, 비즈니스 5종 | [day4](./week1/day4-finetuning-lora.md) |
| 5 | 에이전트 SDK | CLI=사용자/SDK=생산자, 권한·보안 코드 제어, 하이브리드 98% 절감 | [day5](./week2/day5-antigravity-sdk.md) |
| 6 | 데이터 자산화 ⭐ | 단기/장기 기억, 3대 디버깅 함정, "모델은 소비재 데이터는 자산" | [day6](./week2/day6-data-as-asset.md) |
| 7 | 멀티에이전트 | 지식 공유(MetaGPT/AgentVerse/EoT), 집단지성, 특화 두뇌 | [day7](./week2/day7-multi-agent.md) |

---

## 🗂️ 마스터 개념 치트시트 (29개)

**RAG 기초(Day1)** — [RAG](../concepts/rag.md) · [할루시네이션](../concepts/hallucination.md) · [파라/논파라 메모리](../concepts/memory-types.md) · [인코더·벡터](../concepts/encoder-vector.md) · [MIPS](../concepts/mips.md)
**진화(Day2)** — [Self-RAG](../concepts/self-rag.md) · [Graph RAG](../concepts/graph-rag.md)
**Agentic(Day3)** — [Agentic RAG](../concepts/agentic-rag.md) · [추론](../concepts/reasoning.md) · [오케스트레이션](../concepts/agent-orchestration.md) · [Hugging Face](../concepts/huggingface.md) · [로컬 vs 클라우드](../concepts/local-vs-cloud-llm.md) · [양자화](../concepts/quantization.md) · [파인튜닝·LoRA](../concepts/finetuning-lora.md)
**미래·파인튜닝(Day4)** — [RAG vs 파인튜닝](../concepts/rag-vs-finetuning.md) · [과적합·과소적합](../concepts/overfitting-underfitting.md) · [학습 파라미터](../concepts/training-params.md) · [Unsloth](../concepts/unsloth.md) · [미래 RAG & BM](../concepts/future-rag.md)
**SDK 연결(Day5)** — [Antigravity SDK](../concepts/antigravity-sdk.md) · [에이전트 자율성·가드레일](../concepts/agent-autonomy.md) · [하이브리드 비용 최적화](../concepts/hybrid-cost-optimization.md)
**데이터 자산(Day6)** — [단기 vs 장기 기억](../concepts/short-vs-long-term-memory.md) · [데이터 자산화](../concepts/data-as-asset.md) · [파인튜닝 디버깅](../concepts/finetuning-debugging.md)
**멀티에이전트(Day7)** — [멀티에이전트](../concepts/multi-agent.md) · [지식 공유 패턴](../concepts/knowledge-sharing-patterns.md) · [학습 패러다임](../concepts/learning-paradigms.md) · [스페셜리스트 vs 제너럴리스트](../concepts/specialist-vs-generalist.md)

---

## 🏆 관통하는 핵심 원칙

1. **모델은 소비재, 데이터는 자산** — 차별화는 나만의 검증·축적된 데이터에서 나온다.
2. **지식 구조화가 먼저** — 데이터를 쏟아붓지 말고 네트워크로 설계 (단기 → 필터링 → 장기).
3. **목적에 맞는 모델 + 컴퓨테이션 효율** — 60km 차에 페라리 엔진 넣지 않기. 에이전트별 특화 두뇌.
4. **하이브리드** — 무거운 처리는 무료 로컬, 최종 추론만 클라우드 → 비용 ~98% 절감.
5. **소수만 아는 코어를 안다** — 단기/장기, GitHub/HF, SFT/RLHF의 본질을 이해해야 진짜 에이전트를 만든다.
6. **집단지성** — 에이전트는 많아질수록 멍청해진다. 답은 지식 공유.
7. **생산자 마인드** — 소비자(쓰는 사람)가 아니라 만들어 파는 생산자가 된다.

---

## 🛠️ 도구 스택 전체 맵

| 단계 | 도구 | 역할 |
| --- | --- | --- |
| 지식(단기) | NotebookLM·Gemini·OPAL·**GitHub** | RAG 지식 연결·동기화 |
| 모델 탐색 | **Hugging Face** | 모델 앱스토어(258만), Apache 2.0 상업 가능 |
| 학습(장기) | **Unsloth + Colab** | 무료 LoRA 파인튜닝 → GGUF |
| 실행 | **LM Studio · Ollama** | 로컬 모델 구동 (인터넷 X) |
| 에이전트 | **Antigravity SDK** | 권한·보안 코드 제어, 에이전트 제작 |
| 통합 | **Connect AI / ezerai** | 단기+장기 두뇌, 멀티에이전트 연결 |

---

## 💼 비즈니스 모델 (생산자의 길)

1. 로컬 LLM 자동화 에이전트 구축 · 2. 두뇌 파인튜닝 판매 · 3. Physical AI ·
4. On-device AI · 5. 맞춤형 로컬 LLM 구축 스타트업 · **+ 커뮤니티 지식 네트워크**

> 진입 장벽 = **AI 지식 + 바이브 코딩 + 사업 능력** 3박자 → 다 갖춘 사람이 드물어서 기회가 크다.

---

## 🚀 완강 후 액션 로드맵

```
[오늘]            [1개월]           [6개월]            [1년]
30개 데이터       100개             700개              1500개+
페르소나 SFT      DPO(선호학습)     RAG+SFT 프로덕션    대체 불가 디지털 분신
─────────────────────────────────────────────────────────────────
주 30분 루프: 질문수집 → AI증강 → 데이터셋 추가·균형 → 실사용 피드백
2주마다: 재학습 → 새 GGUF 배포
```

### 지금 바로 할 것 (실습 체크리스트)
- [ ] [실습 A~E] RAG 체험 (NotebookLM/Gemini/OPAL/Antigravity/HuggingFace) — [practice](../practice/)
- [ ] [실습 F·M] Unsloth로 페르소나 파인튜닝 (3파라미터 + 황금비율 + Loss 0.2~0.5)
- [ ] [실습 N] 3대 함정 디버깅(`<bos>`/과적합/RAM)
- [ ] [실습 O] GGUF → HF → LM Studio/Ollama 배포
- [ ] [실습 H~L] 에이전트 SDK + 하이브리드 로컬 연결
- [ ] [실습 P] 데이터 축적 시스템(Google Sheets) 시작 — **평생 과제**
- [ ] [실습 Q~T] 멀티에이전트 두뇌 연동·특화 두뇌

---

## 🎯 한 문단 결론

> AI 1인 기업의 본질은 화려한 자동화가 아니라 **'지식이 탑재된 AI'**다.
> 외부 지식을 검색하는 **단기기억(RAG)**, 그중 검증된 핵심을 각인하는 **장기기억(파인튜닝)**,
> 이를 연결·공유하는 **에이전트(SDK·멀티에이전트)** — 이 세 축으로 **나만의 두뇌**를 키운다.
> 모델은 갈아끼워도, 그렇게 쌓은 **데이터셋이야말로 평생 자산**이다. 그리고 그 자산을 만들 수 있는 소수가 곧 생산자다.

→ 인덱스: [README](../README.md) · [개념 사전](../concepts/) · [실습](../practice/) · [오케스트레이션 청사진](../agents/orchestration-blueprint.md)
