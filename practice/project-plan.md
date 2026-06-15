# 🛠️ 실습 기획 — "나만의 AI 1인 기업 MVP 만들기"

> **목표:** 7강의 이론을 **실제 동작하는 결과물**로. 끝나면 *나만의 페르소나 AI + 단기/장기 기억 + 에이전트*를 갖게 된다.
> **원칙:** 강의 철학대로 **최대한 무료(Colab·HuggingFace·LM Studio·Ollama)**. 작게 시작해 매일 1개씩 키운다.
> **연결:** 각 단계는 [실습 기록(practice)](./README.md)의 항목 A~T와 [개념 사전](../concepts/)에 매핑됨.

---

## 🎯 최종 산출물 (Definition of Done)
- [ ] 내 페르소나로 답하는 **파인튜닝 모델** (HF에 업로드, LM Studio/Ollama에서 구동)
- [ ] 내 지식이 연결된 **단기기억(RAG/GitHub)** + **장기기억(데이터셋/HF)**
- [ ] 위 두뇌를 쓰는 **에이전트 1개** (하이브리드로 비용 절감)
- [ ] 매주 데이터를 늘리는 **데이터 축적 루프** 가동

---

## 📅 7단계 로드맵 (총 2~3주, 하루 30~90분)

| Phase | 목표 | 매핑 실습 | 예상 |
| --- | --- | --- | --- |
| 0 | 준비 & 니치 결정 | — | 1일 |
| 1 | 페르소나 데이터셋 30개 | M | 1~2일 |
| 2 | Colab 파인튜닝 | F·M | 1일 |
| 3 | 디버깅 & 배포 | N·O | 1일 |
| 4 | 단기기억(RAG) 연결 | A~E·Q·R | 1~2일 |
| 5 | 에이전트화 | H~L·S | 2~3일 |
| 6 | 데이터 축적 루프 | P | 지속(평생) |
| 7 (확장) | 멀티에이전트·특화 두뇌 | T | 추후 |

---

## 📍 Phase 0 — 준비 & 니치 결정 (1일)
**목표:** 환경 세팅 + "무엇을 만들지" 한 문장으로 확정.

- [ ] 계정: Google(Colab) · Hugging Face · (선택)LM Studio/Ollama 설치
- [ ] Colab `런타임 → T4 GPU` 확인 (`!nvidia-smi`)
- [ ] **니치 한 문장 정하기:** "나는 `___` 분야의 `___`를 돕는 AI를 만든다."
  - 예: "반려견 영양 상담", "소상공인 마케팅 카피", "주식 초보 용어 해설"
- **완료기준:** 니치 한 문장 + Colab GPU 연결 확인.
> 💡 니치는 **내 지식·경험이 있는 곳**이 좋다 (데이터를 직접 만들 수 있어야 함).

## 📍 Phase 1 — 페르소나 데이터셋 30개 (1~2일)
**목표:** HF 표준 형식 Q&A 30개. 개념: [데이터 자산화](../concepts/data-as-asset.md)

- [ ] **카테고리 황금비율**로 배분: 정체성20% · 전문40% · 태도20% · 사례15% · 잡담5%
- [ ] 같은 의미 **다른 표현 5개+**씩 (과적합·echo 방지)
- [ ] 형식: `{"conversations":[{"role":"user",...},{"role":"assistant",...}]}`
- [ ] AI 증강으로 1개 → 6개 부풀리기 (짧은/정중/반말/상황/헷갈리는용)
- **완료기준:** 균형 잡힌 30개(가능하면 50개) JSON.
> ⚠️ 가장 흔한 실수: 정체성만 50개(다른 질문에 페르소나 X) / 전문만 100개("안녕"에 학술답변).

## 📍 Phase 2 — Colab 파인튜닝 (1일)
**목표:** Unsloth로 LoRA 학습, Loss **0.2~0.5**. 개념: [파인튜닝·LoRA](../concepts/finetuning-lora.md) · [학습 파라미터](../concepts/training-params.md)

- [ ] `FastModel.from_pretrained("unsloth/gemma-4-E2B-it", load_in_4bit=True, full_finetuning=False)`
- [ ] 핵심 3파라미터: `learning_rate=3e-4` · `max_steps=60` · `lora_alpha=32`
- [ ] Response-only masking 적용 → `trainer.train()`
- [ ] 학습 전/후 **베이스라인 질문** 비교
- **완료기준:** Loss 0.2~0.5, 페르소나 질문에 내 톤으로 응답.

## 📍 Phase 3 — 디버깅 & 배포 (1일)
**목표:** 3대 함정 통과 + 로컬 구동. 개념: [파인튜닝 디버깅](../concepts/finetuning-debugging.md)

- [ ] [5단계 체크리스트](../concepts/finetuning-debugging.md): `<bos>` 토큰 / 과적합·다양성 / GGUF RAM
- [ ] `push_to_hub_gguf(..., quantization_method="q4_k_m")` → HF 업로드
- [ ] **LM Studio**(Discover 검색) 또는 **Ollama**(`ollama run hf.co/<id>/<model>`)로 구동
- **완료기준:** 인터넷 없이 내 PC에서 내 모델과 대화 성공.

## 📍 Phase 4 — 단기기억(RAG) 연결 (1~2일)
**목표:** 검색형 지식 붙이기. 개념: [단기 vs 장기 기억](../concepts/short-vs-long-term-memory.md)

- [ ] NotebookLM/Gemini로 내 문서 RAG 체험(비교·Source Grounding) — 실습 A
- [ ] (도구 사용 시) Connect AI/ezerai 두뇌에 **GitHub(단기) 연동** — 실습 Q·R
- [ ] 내 지식 문서 몇 개를 단기기억에 주입 → 답변 변화 관찰
- **완료기준:** 외부 지식이 답변에 반영됨(없을 때 vs 있을 때 차이 확인).

## 📍 Phase 5 — 에이전트화 (2~3일)
**목표:** 두뇌를 쓰는 에이전트 + 하이브리드 비용절감. 개념: [Antigravity SDK](../concepts/antigravity-sdk.md) · [하이브리드](../concepts/hybrid-cost-optimization.md)

- [ ] venv + SDK 설치, `GEMINI_API_KEY` 세팅 — 실습 H
- [ ] Hello World 에이전트 → 안전 가드(rm 차단) — 실습 I·J
- [ ] **하이브리드 연결:** LM Studio 서버(`127.0.0.1:1234`)를 도구로 — 실습 K
- [ ] 내 목적의 에이전트 1개(예: 콘텐츠 초안/상담) 만들기 — 실습 L·S
- **완료기준:** 에이전트가 내 로컬 두뇌로 작업 수행, 권한 제어 동작.

## 📍 Phase 6 — 데이터 축적 루프 (지속) ⭐
**목표:** 자산을 매주 키운다. 개념: [데이터 자산화](../concepts/data-as-asset.md)

- [ ] Google Sheets(`날짜·카테고리·질문·답변·출처·상태`) 개설 — 실습 P
- [ ] **주 30분 루프:** 질문수집 → AI증강 → 추가·균형점검 → 실사용 피드백
- [ ] **2주마다** 재학습 → 새 GGUF 배포 / 데이터셋 HF 백업(`private=True`)
- **완료기준:** 1주차 데이터 +N개, 루프가 습관화. (30→100→700→1500개+)

## 📍 Phase 7 — 멀티에이전트·특화 두뇌 (확장)
- [ ] 카테고리별 특화 모델(코더·디자이너·사업) 분리 학습 — 실습 T
- [ ] 공유 게시판/환경으로 지식 공유 → [지식 공유 패턴](../concepts/knowledge-sharing-patterns.md)

---

## 🚦 이번 주 추천 스타트 (3세션)
1. **세션 1 (오늘):** Phase 0 — 니치 한 문장 + Colab GPU 확인.
2. **세션 2:** Phase 1 — 정체성/인사 10개부터 작성 (황금비율 시작).
3. **세션 3:** Phase 2 — Colab 파인튜닝 1회 돌려 Loss 곡선 보기.

> 막히면? 각 단계 옆 **개념 링크 → 5단계 체크리스트**부터. arxiv 등 막힌 자료는 텍스트로 주면 내가 정리.

---

## ✅ 진행 트래커
| Phase | 상태 | 메모 |
| --- | --- | --- |
| 0 준비·니치 | ⬜ | 니치: ________________ |
| 1 데이터셋 30개 | ⬜ | |
| 2 파인튜닝 | ⬜ | Loss: ____ |
| 3 디버깅·배포 | ⬜ | |
| 4 RAG 연결 | ⬜ | |
| 5 에이전트화 | ⬜ | |
| 6 데이터 루프 | ⬜ | 누적: ____개 |
| 7 멀티에이전트 | ⬜ | |

→ [실습 기록](./README.md) · [전체 강의 캡스톤](../lectures/course-summary.md)
