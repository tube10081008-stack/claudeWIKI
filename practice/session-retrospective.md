# 🪞 세션 회고 — "쓰는 사람에서 만드는 사람으로"

> 하루 동안 **페르소나 파인튜닝 → 멀티에이전트 설계 → 성숙한 RAG 구현**까지 한 줄로 달린 기록.
> 핵심 한 줄: *"개념을 코드로, 코드를 측정으로 — 느낌이 아니라 숫자로 끝냈다."*

---

## 1. 무엇을 만들었나 (3대 줄기)

### 🎭 줄기 A — 나를 닮은 AI 분신팀 (파인튜닝)
- **5에이전트 팀** 설계: 지오(총괄·분신) / 코라(시적 글쓰기) / 핀(AI수익화) / 오피(솔로프리너) / 리나(커뮤니티) + 분야별 시그니처 표현.
- **데이터셋**: 코라 103 · 핀 30 · 오피 32 · 리나 34 · 지오 30 (총 ~229개).
- **Colab 파인튜닝**(Unsloth): Gemma 3n 멀티모달 충돌 → **Qwen2.5-3B 텍스트 모델로 전환**.
- **코라를 직접 구워 "감"을 잡음** → `cora_lora` 구글드라이브 백업.
- 산출물: `persona-roster.md` · `datasets/*.jsonl` · `finetune_persona.ipynb` · `phase2-finetuning-colab.md` · `dataset-scaling-log.md`

### 🎰 줄기 B — 도박중독 디지털치료제(DTx) 설계 조직
- **6에이전트 유기체**: 오케스트레이터 + System Architect / Frontend-UX / Backend-Data / Native Integration / Clinical & Safety / Knowledge-RAG.
- **논문 3편 RAG 심화**: RAG(2020) · MedGraphRAG · Agentic RAG Survey → `knowledge-rag.md` + `references.md` + `verification-report.md`.
- **PoC 코드**: Flutter 앱(충동 파도타기 UI) + Django REST 백엔드(실행·검증 완료).
- 위치: `projects/dtx-gambling/` *(claudeWIKI와 분리 권장 — tarball·git 번들 보유, 분리는 보류 상태)*

### 🔎 줄기 C — 성숙한 RAG 파일링 시스템 (설계→코드→측정)
- **설계도**: `concepts/mature-rag-blueprint.md` — 런타임 루프 + **평가(RAGAS) 루프** 2축, 레시피 합성 매트릭스.
- **실행 PoC**: `practice/rag-poc/` — 하이브리드(RRF)·재랭킹·인용강제·Self/CRAG·RAGAS 게이트.
- **골든셋 50개** + **검색 실측**(LLM-free).
- 개념 보강: `concepts/why-finetuning-needs-little-data.md`

---

## 2. 가장 값진 깨달음 (오늘의 교훈 5)

| # | 깨달음 | 어디서 |
| --- | --- | --- |
| 1 | **파인튜닝 "감"은 4번 만에 잡힌다** — 30개(과적합 0.05) → 103개·1.28(부족) → 0.056(과함) → **90스텝·0.55(딱)** | 코라 |
| 2 | **모델 뇌는 이미 완성** — 우리는 0.96%만 덧칠해 *역할*을 입힌다(배우 캐스팅) | why-finetuning 문서 |
| 3 | **닫힌 모델(Opus/Gemini)은 weight 파인튜닝 X** → 프롬프트+RAG가 유일 레버 / 열린 모델(Qwen)만 LoRA | 모델별 특화 논의 |
| 4 | **LoRA+RAG 기법은 이미 상식(commodity)** — 차별점은 *데이터·니치·실행·평가*. NotebookLM의 프론티어도 알고리즘이 아니라 *경험·통합* | 시장 성숙도 논의 |
| 5 | **측정이 "하이브리드 맹신"을 깼다** — 더미 dense 노이즈가 RRF로 BM25를 끌어내려 `hybrid(68%) < bm25(89%)` | 검색 실측 |

> ⭐ 관통하는 메타교훈: **"느낌상 좋아졌다"는 미숙, "숫자로 회귀를 본다"가 성숙.** 파인튜닝의 Loss도, RAG의 RAGAS도 결국 같은 원리.

---

## 3. 실측 결과 스냅샷

### 코라 파인튜닝 (Qwen2.5-3B)
```
30개·15ep  → Loss 0.05  과적합(일본어 새고 붕괴)
103개·시스템프롬프트·90스텝 → Loss 0.55  ✅ 자연스러운 한국어 + 거절 처리
```

### RAG 검색 품질 (골든셋 44 answerable, k=5)
| 구성 | Hit@1 | Recall@5 | MRR |
|---|---|---|---|
| dense_only (더미) | 25.0% | 45.5% | 0.326 |
| **bm25_only** | **61.4%** | **88.6%** | **0.732** |
| hybrid | 36.4% | 68.2% | 0.501 |
> 교훈: 한 축(dense)이 망가지면 순진한 하이브리드는 *손해*. 실 임베딩(e5) 투입 시 역전 예상(로컬 재현 가능).

---

## 4. 막혔던 것 & 우회 (정직한 기록)
| 벽 | 우회 |
| --- | --- |
| Gemma 3n 멀티모달이 텍스트 작업과 충돌 | Qwen2.5-3B 텍스트 모델로 교체 |
| Colab 셀 순서 혼동 → `NameError` 반복 | "①번부터 순서대로" 원칙 정립 |
| 과적합 ↔ 과소적합 진동 | 데이터↑ + 시스템프롬프트 + 스텝 미세조정 |
| HuggingFace egress 차단 → e5 다운로드 불가 | 더미 임베딩 + **LLM-free 검색 평가**로 실측 |
| Google Drive egress 차단 → 4번째 논문 못 받음 | 직접 첨부 요청(`[R4]` 자리 예약) |
| 레포 권한(403) → 새 깃허브 레포 생성 불가 | tarball + git 번들로 분리 자료 전달 |

---

## 5. 현재 레포 상태
```
claudeWIKI/
├── lectures/ · concepts/ · curriculum/   ← 강의 위키(기존)
├── concepts/ 신규: why-finetuning-needs-little-data, mature-rag-blueprint
├── practice/
│   ├── persona-roster · datasets/*.jsonl · finetune_persona.ipynb
│   ├── phase1/phase2 가이드 · dataset-scaling-log
│   └── rag-poc/   ← 설계도의 실행본(코드+골든셋+평가)
└── projects/dtx-gambling/   ← DTx 설계조직+PoC (분리 권장, 보류)
```
전부 커밋·푸시됨 (브랜치 `claude/laughing-bohr-a5h1c4`).

---

## 6. 다음 스텝 (이어서 할 것)
- [ ] **코라 외 4명 학습** (핀·오피·리나·지오) — 90스텝 기준 동일 반복
- [ ] **로컬 연결** — LM Studio/Ollama (집 PC에서, GGUF 변환)
- [ ] **RAG 실모델** — 로컬에서 `sentence-transformers` 붙여 dense·hybrid 재측정
- [ ] **RAG×페르소나 통합** — 말투(파인튜닝) + 지식(RAG) 결합
- [ ] **DTx 분리** — 별도 레포로 (번들/타르볼 보유)
- [ ] **풀 RAGAS** — LLM judge 붙여 faithfulness/answer_relevancy까지

---

## 🔑 한 문장 결론
> **오늘 ChatGPT를 "쓰는 사람"에서 "만들고·측정하는 사람"이 됐다.** 데이터를 빚고(코라), 조직을 설계하고(DTx), 검색을 측정했다(RAG) — 셋 다 *남이 못 가진 데이터 × 측정 루프*가 핵심이었다.

→ 관련: [persona-roster](./persona-roster.md) · [mature-rag-blueprint](../concepts/mature-rag-blueprint.md) · [why-finetuning-needs-little-data](../concepts/why-finetuning-needs-little-data.md) · [DTx](../projects/dtx-gambling/README.md)
