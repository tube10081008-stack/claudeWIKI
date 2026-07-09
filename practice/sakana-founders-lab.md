# 🐟 Sakana 창업자 3인 실습랩 — 논문을 손으로 굴린다

> **컨셉:** [Day8 강의](../lectures/week3/day8-collective-intelligence-sakana.md)의 세 창업자, 각자의 **대표 아이디어·논문을 1개씩 직접 실습**한다.
> Jones = *뇌를 이해하고* → Ha = *뇌를 합치고* → Ito = *뇌를 판다*. 마지막에 셋을 묶어 **"나만의 Fugu"** 캡스톤.
> 원칙: 전부 **0원(Colab 무료/로컬)**, 기존 자산(코라 LoRA·분신팀·RAG PoC·골든셋) 재사용.

---

## 🗺️ 전체 로드맵

| 모듈 | 창업자 | 대표 아이디어/논문 | 실습 한 줄 | 시간 |
| --- | --- | --- | --- | --- |
| 1 | **Llion Jones** (CTO) | *Attention Is All You Need* (2017) | 어텐션을 **눈으로 보고**, 모델 성격을 **조종**해본다 | 반나절 |
| 2 | **David Ha** (CEO) | *Evolutionary Optimization of Model Merging Recipes* (2024, EvoLLM-JP) + 집단지성 서베이 | 두 모델을 **합쳐**(mergekit) 새 모델을 만들고 **측정으로 선택** | 반나절~1일 |
| 3 | **Ren Ito** (COO) | 논문 대신 **스케일업 플레이북** (前 Stability AI COO) | Marlin-lite **자율 전략임원** + 내 상품 **가격표** | 반나절 |
| ★ | 캡스톤 | Fugu 구조 (Thinker→Worker→Verifier) | 셋을 묶어 **나만의 Fugu 오케스트라** | 1일 |

> 순서 의미: **이해(1) 없이 합치면(2) 미신이 되고, 합쳐도 못 팔면(3) 취미로 끝난다.**

---

## 🧠 Module 1 — Llion Jones: "어텐션을 눈으로 본다"

### 이론 배경
- **Attention Is All You Need** (Vaswani, …, **Jones**, … 2017): RNN 없이 **셀프어텐션만으로** 시퀀스를 처리 — 오늘날 GPT·Claude·Qwen·코라의 공통 조상.
- 핵심 수식 한 줄: `Attention(Q,K,V) = softmax(QKᵀ/√d)·V` — *"각 단어가 다른 단어를 얼마나 쳐다보는가"*.

### 실습 단계
1. **손계산 미니 노트북** — 토큰 4개짜리 문장으로 Q·K·V 행렬을 numpy로 직접 곱해 어텐션 맵 산출 (수식 체감, 30분).
2. **코라의 뇌 열어보기** — Colab에서 `transformer_lens`로 Qwen2.5 로드 → *"슬픔을 다 식은 국밥에"* 같은 코라 문장 입력 → 레이어별 어텐션 히트맵 시각화. "어느 헤드가 조사(을/를)를 보고, 어느 헤드가 비유를 잇는가" 관찰.
3. **성격 조종(activation steering) 맛보기** — "차분한 문장 − 들뜬 문장" 활성 벡터 차이를 추출해 residual stream에 더하기 → **파인튜닝 없이** 말투가 기우는지 확인. (Day8 강의의 `성격조종 steering` 항목)

### 산출물 & 성공 기준
- [ ] 어텐션 히트맵 이미지 3장 + 관찰 노트 (`practice/labs/jones-attention.md`)
- [ ] steering 전/후 같은 프롬프트 출력 비교 1쌍
- 성공: *"코라가 왜 그렇게 말하는지, 헤드 단위로 한 가지 이상 설명할 수 있다"*

---

## 🧬 Module 2 — David Ha: "AI 연금술 — 진화 병합" ⭐ 오늘의 미착수 조각

### 이론 배경
- **Evolutionary Optimization of Model Merging Recipes** (Akiba, Shing, Tang, Sun, **Ha** — Sakana, 2024): 수십만 오픈소스 모델을 **재학습 없이** 섞되, *어떻게 섞을지(레시피)*를 사람이 아니라 **진화 알고리즘(자연선택)**이 찾게 함. 결과물 **EvoLLM-JP** = "추가 학습 없이, 진화만으로 수학 잘하는 일본어 모델".
  - 두 공간에서 섞음: **파라미터 공간**(레이어 가중치 비율) + **데이터 흐름 공간**(레이어 배치 경로) — 강의의 "디지털 DNA 교배" 그림.
- 배경 계보: *World Models*(1998년생 아이디어의 2018 부활, Ha & Schmidhuber) · *Weight Agnostic NN* · **Collective Intelligence for Deep Learning 서베이**(Ha & Tang 2022) — 전부 "크게 키우기 대신 여럿·진화".

### 실습 단계 (Colab 무료 T4 기준)
1. **mergekit 기본 병합** — 같은 계열 소형 모델 2개(예: Qwen2.5-1.5B instruct 변형들)를 `slerp`로 병합:
   ```yaml
   # merge-slerp.yaml (mergekit)
   slices:
     - sources:
         - model: 모델A   # 예: 대화 특화
         - model: 모델B   # 예: 코딩/수학 특화
   merge_method: slerp
   base_model: 모델A
   parameters:
     t: 0.5              # 섞는 비율 — 이게 '레시피'
   dtype: bfloat16
   ```
2. **task arithmetic 체험** — `TIES`/`task_arithmetic` 방식으로 "능력 더하고 빼기": (코라 LoRA를 병합해 넣기 = *내 데이터 능력을 벡터로 더한다*).
3. **미니 진화 루프 (핵심)** — Sakana처럼 CMA-ES까진 아니어도, **레시피 파라미터 `t`를 0.2/0.35/0.5/0.65/0.8로 5마리 만들고** → 우리 **RAG 골든셋/코라 테스트 질문**으로 채점 → **최고 점수만 생존** → 그 주변 값으로 2세대 반복. *"자연선택을 손으로 돌려본다."*
   - 채점기는 이미 있음: `practice/rag-poc/eval/`의 골든셋 + 코라 페르소나 질문 10개 (톤 유지·한국어·거절 처리).
4. (심화) 병합 모델 vs 원본 vs 코라LoRA **3자 비교표** 작성.

### 산출물 & 성공 기준
- [ ] 병합 모델 1개(GGUF 변환까지 하면 보너스) + **세대별 점수표** (`practice/labs/ha-evolution-merge.md`)
- 성공: *"레시피(t)에 따라 점수가 달라짐을 표로 보여주고, 왜 그 개체가 생존했는지 한 문단으로 설명"*
- ⚠️ 함정 예고: 다른 계열(토크나이저 다른) 모델끼리 병합 시도 → 깨짐. **같은 베이스 계열**부터.

---

## 💼 Module 3 — Ren Ito: "프론티어를 상품으로"

### 이론 배경 (논문 대신 플레이북)
- Ito는 연구자가 아니라 **스케일 담당** — 前 Stability AI COO, 글로벌 비즈니스 확장. Sakana의 교훈: *기술(Fugu)만큼 중요한 게 **패키징과 가격**($20/$100/$200, Marlin ¥15만/월).*
- 강의 7장 그대로: ① AI 한 개만 쓰지 마라 ② 나만의 모델 ③ 자율로 일하게 ④ 0원부터.

### 실습 단계
1. **Marlin-lite 만들기** — 지오(지휘)+분신팀으로 "자율 전략임원" 흉내: 주제 하나를 던지면 `가설 수립(지오) → 리서치(핀) → 모순 검증(RAG 골든셋식 근거 확인) → 반복 2회 → 전략 보고서 초안` 을 사람이 개입 없이 완주하는 프롬프트 체인 설계. (Claude/로컬 모델로 실행)
2. **가격표 설계** — 핀과 함께 내 분신팀 서비스의 3단 요금제(Fugu 벤치마킹: 무료체험/개인/프로) + "무엇이 로컬·0원 해자인지" 한 줄 포지셔닝.
3. **랜딩 한 장** — 상품명·타깃·가격·데모 문구를 담은 한 페이지(마크다운 또는 노션).

### 산출물 & 성공 기준
- [ ] 자동 생성된 전략 보고서 1부 + 요금표 + 랜딩 초안 (`practice/labs/ito-productize.md`)
- 성공: *"남에게 링크 하나로 보여줄 수 있는 '상품' 형태가 존재한다"*

---

## 🏆 캡스톤 — "나만의 Fugu"

세 모듈을 한 파이프라인으로:
```
사용자 질문
   ↓
Thinker  = 지오 (분해·계획)          ← Module 3의 오케스트레이션
Worker   = Module 2의 병합 모델 + 분신들 (실행)
Verifier = RAG 근거 검증 + 골든셋식 채점   ← Module 1의 이해가 디버깅 무기
   ↓
인용 달린 최종 답변  (실패 시 재시도 1회)
```
- 성공 기준: 골든셋 10문항에서 **단일 모델 vs 나의 Fugu** 점수 비교표 — *"팀워크 > 개별"을 Sakana처럼 숫자로 재현*.
- 강의의 그 문장을 실증하는 것: **"Sakana가 논문으로 내는 걸, 우리는 코드로 굴린다."**

---

## 🧰 공통 준비물
| 항목 | 내용 |
| --- | --- |
| 환경 | Colab 무료 T4 (병합·steering), 로컬 Ollama/LM Studio (캡스톤 서빙) |
| 설치 | `mergekit`, `transformer_lens`, (기존) `finetune_persona.ipynb` 스택 |
| 재사용 자산 | 코라 LoRA · 분신팀 데이터셋 · `rag-poc/eval/golden_set.jsonl` · 페르소나 로스터 |
| 비용 | **0원** |

## 📅 일정 제안
- **집중형(3일):** Day1 Jones → Day2 Ha → Day3 Ito+캡스톤
- **주말형(3주):** 주말마다 모듈 1개, 마지막 주말 캡스톤

## ✅ 랩 전체 완료 체크리스트
- [ ] M1: 히트맵+steering 비교 산출
- [ ] M2: 병합 모델 + **세대별 생존 점수표** (핵심)
- [ ] M3: 보고서·요금표·랜딩
- [ ] 캡스톤: 단일 vs Fugu 비교표
- [ ] 각 랩 노트를 `practice/labs/`에 기록 (측정 없인 완료 아님)

→ 관련: [Day8 강의](../lectures/week3/day8-collective-intelligence-sakana.md) · [멀티에이전트](../concepts/multi-agent.md) · [파인튜닝·LoRA](../concepts/finetuning-lora.md) · [성숙한 RAG 설계도](../concepts/mature-rag-blueprint.md) · [세션 회고](./session-retrospective.md)
