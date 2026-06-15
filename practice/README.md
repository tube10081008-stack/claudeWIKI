# 🛠️ 실습 기록 (Practice Log)

강의 실습을 직접 해보고 결과·깨달음을 기록하는 공간입니다.

---

## Week 1 · Day 1 실습 4종

### [실습 1] RAG 맛보기 — "내 문서를 읽는 똑똑한 뇌"
- **도구:** NotebookLM & Gemini
- **데이터:** *Natural Language Processing with Transformers* (Hugging Face, PDF)
- **할 일:**
  1. **비교 체험:** 일반 Gemini "트랜스포머 원리 설명해줘" vs NotebookLM에 PDF 넣고 "이 책 저자가 말하는 RAG 핵심은?"
  2. **Source Grounding:** 답변이 몇 페이지를 참고했는지 확인 → 할루시네이션 제어 과정 관찰
  3. **지식 재구성:** 가이드북/FAQ 기능으로 교재를 '비즈니스 요약본'으로 변환
- **상태:** ⬜ 미완료
- **기록:** _(여기에 결과·캡처·느낀 점 작성)_

### [실습 2] Google OPAL 기반 지식 확장
- **도구:** Google OPAL
- **핵심:** 멀티소스(드라이브·문서·유튜브) 연결로 논파라메트릭 메모리 구체화
- **포인트:** Generator가 텍스트뿐 아니라 **이미지·영상 생성**으로도 다양해짐
- **상태:** ⬜ 미완료

### [실습 3] Antigravity + 클라우드 모델 연결
- **할 일:**
  1. 실습1에서 만든 지식을 마크다운(`day1.md`)으로 저장
  2. Antigravity 프로젝트에 넣고 `@day1` 지식 참조로 코드/웹 생성
  3. 로컬 폴더 ↔ GitHub 동기화로 온라인 메모리 구축
- **상태:** ⬜ 미완료

### [실습 4] Connect AI — 로컬 LLM(Gemma) 연결
- **할 일:** 클라우드가 아닌 로컬 LLM(Gemma 4 등)에 지식 주입, GitHub 동기화
- **핵심:** 클라우드(오른쪽) vs 로컬(왼쪽) 하이브리드 사용법 체득
- **상태:** ⬜ 미완료

---

> 💡 실습하며 "뭔가 부족하다"고 느낀 지점을 메모해두면, 다음 단계(Graph RAG)에서 해소됩니다.

---

## Week 1 · Day 2 실습 (Self-RAG & Graph RAG)

### [실습 A] Self-RAG '자가 검증' 체험
- **도구:** 커넥트 AI (전용 파일 2.5 버전 설치 → `Ctrl+Shift+P → Install from VSIX`)
- **할 일:** AI 1인 기업 모드에서 에이전트가 모은 지식에 **'자가 검증 켜기'** 적용 →
  [4기준(isRetrieve/isRelevant/isSupported/isUseful)](../concepts/self-rag.md)으로 걸러지는지 관찰
- **상태:** ⬜ 미완료

### [실습 B] 지식 네트워크(Graph) 시각화 관찰
- **도구:** 안티그래비티 / 옵시디언 '지식 네트워크 보기'
- **할 일:** `raw`(내가 주입) vs `agent`(에이전트가 모음) 폴더가 어떻게 연결됐는지,
  **루트 커뮤니티 vs 서브 커뮤니티** 패턴 관찰 → "왜 이렇게 연결됐지?" 탐구
- **상태:** ⬜ 미완료

---

## Week 1 · Day 3 실습 (Agentic RAG · 로컬 모델)

### [실습 C] 이미지 생성 로컬 모델 (Hugging Face + Colab)
- **모델:** `JSCPPProgrammer/z-anime-distill8-gradio-zerogpu` (애니메이션 증류 모델)
- **권장 설정:** Steps **8** / CFG **1.0~1.5** / Sampler **Euler_a** / Scheduler **Beta** / Denoise **1.0** / **FP8**
  - ⚠️ Steps·CFG를 일반값(7.0+)으로 올리면 색상 붕괴(이미지 타버림)
- **할 일:** Space에서 프롬프트 생성 → `Use this model → Colab`에서 T4 GPU(무료)로 실행 →
  큰 모델 실패 시 [양자화](../concepts/quantization.md)/Least-parameters 버전으로 대체
- **링크:** https://huggingface.co/spaces/JSCPPProgrammer/z-anime-distill8-gradio-zerogpu
- **상태:** ⬜ 미완료

### [실습 D] 음악 생성 모델 테스트
- **모델:** `ACE-Step/acestep-v15-xl-turbo` (핫한 음악 생성)
- **상태:** ⬜ 미완료

### [실습 E] 상업 가능 모델 찾기 (Apache 2.0)
- **할 일:** Hugging Face에서 라이선스 **Apache 2.0** 필터 → 수익화 가능한 모델(약 44만 개, Gemma 4 등) 탐색
- **상태:** ⬜ 미완료

---

## Week 1 · Day 4 실습 (Unsloth로 파인튜닝) ⭐숙제

> 오늘은 **실습보다 숙제가 더 중요**. 답이 없는 미래 영역이라 직접 실험해봐야 한다.

### [실습 F] Gemma 4 LoRA 파인튜닝 (Colab 무료)
- **도구:** Unsloth + Google Colab (런타임 → T4 GPU 무료)
- **단계:**
  1. 학습 전 **베이스라인 질문** 던져 모델이 모르는지 확인
  2. **나만의 데이터** 만들기 — HF 표준(role/user-assistant, JSON) 질문-답변 모범답안 (30→100→1000개+, AI로 생성)
  3. chat template 적용 → 학습 실행
  4. **Loss 줄이기** 목표 — 평균 감소 확인 (너무 적으면 과소적합/많으면 과적합)
  5. learning_rate·max_steps·batch_size·데이터 수를 **막 실험**
  6. `.py` 다운로드 → 안티그래비티에서 분석·개선
- **숙제:** 내가 하고 싶은 사업(병원/금융/호텔 등)의 베이스라인 질문에 답하는 **특화 모델** 만들기
- **실습 자료:** https://colab.research.google.com/drive/1mE2Q4adkqAYNegGeAN3v-7BjO0GSEV2u
- **상태:** ⬜ 미완료

### [실습 G] (다음 주 예고) 학습한 두뇌 연결
- 파인튜닝한 모델을 **LM Studio / Ollama / Connect AI**에 올려 자동화 에이전트의 두뇌로 연결
- **상태:** ⬜ 예정

---

## Week 2 · Day 5 실습 (Antigravity SDK · 하이브리드)

### [실습 H] 가상환경 + SDK 설치
```bash
python3 -m venv venv && source venv/bin/activate
pip install --upgrade pip
pip install google-antigravity uvicorn sse-starlette starlette
export GEMINI_API_KEY="발급받은_키"   # Windows: set GEMINI_API_KEY=...
```
- **상태:** ⬜ 미완료

### [실습 I] Hello World 에이전트
- `Agent` + `LocalAgentConfig`로 첫 에이전트 구동 → "오케이" 응답 확인
- **상태:** ⬜ 미완료

### [실습 J] 안전 가드 에이전트 (Policy/Hook)
- `policy.deny("run_command", when=check_command_danger)`로 `rm` 등 위험 명령 자동 차단
- **상태:** ⬜ 미완료

### [실습 K] 하이브리드 로컬 AI 연결 ⭐
- LM Studio 모델 Load → `http://127.0.0.1:1234` 서버 → 에이전트 도구로 연결
- 목표 체감: 클라우드 30만 토큰 → 하이브리드 5천 토큰 (**~98% 절감**)
- **상태:** ⬜ 미완료

### [실습 L] SDK 예제 Fork → 나만의 에이전트
- SDK 저장소 Fork/gfork → 예제 분석 → "유튜브/웹사이트 관리 에이전트 개발" → 권한·삭제금지 설정 실험
- 저장소: https://github.com/google-antigravity/antigravity-sdk-python
- **상태:** ⬜ 미완료

---

## Week 2 · Day 6 실습 (페르소나 파인튜닝 & 데이터 자산화) ⭐

### [실습 M] Gemma 4 페르소나 파인튜닝 (Colab)
- Unsloth로 30개 Q&A 학습 → 나만의 페르소나 AI
- 핵심 3파라미터 실험: `learning_rate=3e-4` · `max_steps=60` · `lora_alpha=32`
- **카테고리 황금비율** 지키기(정체성20/전문40/태도20/사례15/잡담5) + 같은 의미 다른 표현 5개+
- 목표 Loss **0.2~0.5** (과적합<0.01 주의)
- 실습 Colab: https://colab.research.google.com/drive/1pbV4tmNRiLUgC5kVu3eSRacsakoPKGEW
- **상태:** ⬜ 미완료

### [실습 N] 3대 함정 디버깅
- `<bos>` 토큰 일관성 / 과적합·다양성 / GGUF 변환 RAM → [5단계 체크리스트](../concepts/finetuning-debugging.md)로 점검
- **상태:** ⬜ 미완료

### [실습 O] 배포: GGUF → HF → LM Studio/Ollama
- `push_to_hub_gguf(..., quantization_method="q4_k_m")` → LM Studio Discover 검색 / `ollama run hf.co/<id>/<model>`
- **상태:** ⬜ 미완료

### [실습 P] 데이터 축적 시스템 구축 (장기 과제)
- Google Sheets(`날짜·카테고리·질문·답변·출처·상태`) → 주 30분 루프 → 2주마다 재학습
- 데이터셋 HF 백업(`private=True`) → 새 모델에 1줄 재학습
- **목표:** 30개 → 100 → 700 → 1500개+ (대체 불가 디지털 분신)
- **상태:** ⬜ 진행 중(평생)

---

## Week 2 · Day 7 실습 (멀티에이전트 · 단기→장기 통합)

### [실습 Q] 두뇌 연동 설정 (단기/장기)
- Connect AI/ezerai 두뇌 → 연동에서 **GitHub(단기)** + **Hugging Face(장기)** 토큰 설정
- 도구: https://www.ezerai.xyz/download
- **상태:** ⬜ 미완료

### [실습 R] J브레인 코어 지식 받기
- 단기기억에 검증된 코어 지식 28개 가져오기
- 저장소: `https://github.com/wonseokjung/jay-brain.git` (password: `jaybrain2026`)
- **상태:** ⬜ 미완료

### [실습 S] 단기 → 장기 학습 (SFT + AI 자동 피드백)
- 단기 지식 → **학습 데이터 변환 + 증강** → HF 데이터셋 업로드
- learning_rate 강도(안전/기본/강하게) 선택 → 자동 학습 노트북 실행 → 모델 HF 업로드
- AI 자동 피드백(강화학습): 좋은 답(+)/나쁜 답(−) 생성으로 품질 학습
- **상태:** ⬜ 미완료

### [실습 T] 카테고리별 특화 두뇌 만들기
- 마케팅/코딩/사업/일반으로 분류 → 에이전트별(코더·디자이너·사업) 특화 모델 따로 학습·연결
- **상태:** ⬜ 미완료
