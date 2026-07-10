# 파인튜닝 실전 디버깅 (3대 함정 + 5단계 체크리스트)

**한 줄 정의:** 파인튜닝이 실패할 때 1~3시간을 날리는 단골 함정들과, 99%를 잡아내는 5단계 점검 순서.

## Loss 해석 가이드
| Loss | 의미 | 조치 |
| --- | --- | --- |
| > 1.0 | 학습 부족 | step ↑ |
| **0.2~0.5** | ✅ 이상적 | 그대로 |
| < 0.01 | ⚠️ 과적합 | step ↓ |

## 3대 함정
### ① `<bos>` 토큰 (Loss는 떨어졌는데 페르소나 없음)
- 학습 시 `<bos>` 없음 / 추론 시 자동 추가 → **1 토큰 차이로 LoRA 효과 100%→0%**.
- 해결: 추론 시 첫 토큰이 bos면 제거.
  ```python
  if inp["input_ids"][0,0].item() == tokenizer.bos_token_id:
      inp["input_ids"] = inp["input_ids"][:, 1:]
      inp["attention_mask"] = inp["attention_mask"][:, 1:]
  ```
- 교훈: **학습 형식 = 추론 형식.**

### ② 과적합 & 답변 반복 (다양성 부족)
- 증상: 질문을 echo하거나 페르소나 미작동.
- 해결: 설정 완화(`max_steps↓`, `lr↓`, 목표 loss 0.2~0.4) + **같은 의미 다른 표현** 5개+.
- 교훈: 신경망은 "표현"을 외우지 "의미"를 외우지 않는다.

### ③ GGUF 변환 중 커널 사망 (System RAM)
- 원인: **GPU가 아니라 시스템 RAM 부족** (T4 RAM 12.7GB < 변환 ~15GB).
- 해결: Colab Pro(L4+고RAM) / `push_to_hub_merged` 후 HF Space 변환 / LoRA만 푸시.
- 교훈: 메모리는 GPU만이 아니다.

## 5단계 디버깅 체크리스트
1. 토큰 형식 일치 · 2. 마스킹 정상(답변만) · 3. LoRA 학습됨(norm≠0) · 4. 추론 모드 전환 · 5. **`<bos>` 일관성**(가장 흔함)
> ✅ 99%의 학습 실패는 이 5개 중 하나에서 잡힌다.

## 관련 개념
[학습 파라미터](./training-params.md) · [과적합·과소적합](./overfitting-underfitting.md) · [파인튜닝·LoRA](./finetuning-lora.md) · [Unsloth](./unsloth.md)
