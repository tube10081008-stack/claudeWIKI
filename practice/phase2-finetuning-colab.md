# 📍 Phase 2 — Colab 파인튜닝 가이드 (Unsloth × Gemma)

> **목표:** Phase 1에서 만든 데이터셋으로 페르소나를 **진짜 모델 두뇌에 학습**시킨다.
> **도구:** [Unsloth](../concepts/unsloth.md) + Gemma E2B + Colab 무료 T4.
> **노트북:** [`finetune_persona.ipynb`](./finetune_persona.ipynb) — 5명 전부 재사용(맨 위 `AGENT`만 변경).

---

## 🚀 빠른 시작 (코라부터)

1. **노트북 열기** — `finetune_persona.ipynb`를 [Colab](https://colab.research.google.com)에 업로드
2. **런타임 → 런타임 유형 변경 → T4 GPU**
3. 셀 0에서 `AGENT = "cora"` 확인
4. 위에서부터 셀 차례로 실행 (▶)
5. 4번 셀에서 `cora.jsonl` 업로드
6. 6번 셀에서 학습 → **Loss 0.2~0.5** 확인
7. 7번 셀에서 코라 말투 나오면 🎉 성공
8. 나머지 4명은 `AGENT` 값만 바꿔 반복

---

## 🎯 핵심 파라미터 (감 잡기)

| 파라미터 | 의미(비유) | 시작값 | 조절 |
| --- | --- | --- | --- |
| `learning_rate` | 학습 속도 | `2e-4` | 너무 크면 불안정, 작으면 느림 |
| `max_steps` | 학습 횟수 | `60` | Loss 보며 ↑/↓ |
| `batch×accum` | 한 번에 보는 양 | `2×4=8` | T4 메모리 한계 내에서 |
| `r` (LoRA rank) | 학습할 행렬 크기 | `8` | 클수록 표현력↑·과적합 위험↑ |

> 강의 핵심: **이 파라미터 조절 '감'이 곧 비즈니스 경쟁력.** 정답은 없고 실험으로 찾는다.

### Loss 해석 ([디버깅 문서](../concepts/finetuning-debugging.md))
| Loss | 의미 | 조치 |
| --- | --- | --- |
| `> 1.0` | 학습 부족 | `max_steps` ↑ |
| **`0.2~0.5`** | ✅ 이상적 | 그대로 |
| `< 0.01` | ⚠️ 과적합 | `max_steps` ↓ |

---

## ⚠️ 3대 함정 (이 노트북에 미리 방어됨)

| # | 증상 | 원인 | 노트북의 방어 |
| --- | --- | --- | --- |
| ① **`<bos>` 토큰** | Loss는 낮은데 페르소나 X | 학습/추론 형식 1토큰 차이 | `ask()`에서 중복 bos 제거 |
| ② **echo·과적합** | 질문을 따라 하거나 밋밋 | 데이터 다양성 부족 | `train_on_responses_only`(답변만 학습) + 데이터 표현 5개+ |
| ③ **GGUF 커널 사망** | 변환 중 런타임 죽음 | GPU 아닌 **시스템 RAM** 부족 | 8번 셀 주석 — Pro/HF 변환 안내 |

---

## 📈 결과가 안 좋을 때

- **말투가 안 나온다** → 데이터를 30 → 50개+로 늘리기(특히 정체성을 다른 표현으로), `max_steps` 살짝 ↑
- **질문을 echo한다** → 과적합. `max_steps` ↓, 같은 의미 다른 표현 데이터 보강
- **아무 질문에나 한 가지 답만** → 과적합 심함. step 크게 ↓
- **Loss가 안 떨어진다** → `learning_rate` 점검, 데이터 형식(chat template) 확인

> 💡 30개는 강의에서도 "부족"하다고 한 수치 — **되는지 확인용**. 본격 운영은 100개+ 권장.

---

## 🔜 다음 단계
1. 5명 각각 LoRA 학습 → `.zip` 다운로드
2. **GGUF 변환** → LM Studio / Ollama에 올려 로컬에서 내 분신 구동
3. (선택) 지오를 라우터로 둔 [멀티 에이전트 오케스트레이션](../agents/orchestration-blueprint.md) 연결

→ 개념: [파인튜닝·LoRA](../concepts/finetuning-lora.md) · [학습 파라미터](../concepts/training-params.md) · [과적합·과소적합](../concepts/overfitting-underfitting.md) · [양자화](../concepts/quantization.md) · [디버깅](../concepts/finetuning-debugging.md)
