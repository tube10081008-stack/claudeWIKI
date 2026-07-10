# Unsloth

**한 줄 정의:** 저사양·무료 환경(Colab 등)에서도 LLM을 최적화해 빠르게 학습(파인튜닝)시킬 수 있는 오픈소스 도구.

## 왜 쓰나
- Hugging Face에서 직접 학습하려면 GPU/TPU가 많이 필요 → 무료 환경에선 어려움.
- Unsloth가 최적화해줘서 **저비용으로 파인튜닝** 가능. (예: `unsloth/gemma-4-E2B`)

## 핵심 설정 5가지
| 설정 | 의미 |
| --- | --- |
| **model name** | 사용할 모델 |
| **max_sequence_length** | 한 번에 생성할 토큰 수 (예: 1024) |
| **load_in_4bit** | True = [양자화](./quantization.md)(압축·고속) |
| **full_finetuning** | True=전체 변경 / False=LoRA(일부) |
| (추론) **temperature/top_p/top_k** | 생성 방식 제어 |

## 학습 데이터 형식
- Hugging Face 표준: `role`(user/assistant) 기반 **질문-답변 모범답안**(JSON).
- 30개는 부족 → **100~1000개+**. AI로 생성하는 게 효율적.

## 실습 링크
- Text(Finetuning): https://colab.research.google.com/github/unslothai/notebooks/blob/main/nb/Gemma4_(E2B)-Text.ipynb
- Vision: https://colab.research.google.com/github/unslothai/notebooks/blob/main/nb/Gemma4_(E2B)-Vision.ipynb

## 관련 개념
[파인튜닝·LoRA](./finetuning-lora.md) · [학습 파라미터](./training-params.md) · [양자화](./quantization.md) · [Hugging Face](./huggingface.md)
