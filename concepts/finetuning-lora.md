# 사전훈련 · 파인튜닝 · LoRA

**한 줄 정의:** 인공지능 모델을 내 목적에 맞게 만드는 3가지 수준의 방법.

| 방법 | 설명 | 우리에게 |
| --- | --- | --- |
| **Pretraining (사전훈련)** | 모델을 처음부터 학습 | 컴퓨팅 막대 → 어려움 (구글/OpenAI 영역) |
| **Fine-tuning (미세조정)** | 기존 모델을 조금 수정 (예: 특정 강아지 사진 1000장 학습으로 더 잘 인식) | 현실적으로 가능 |
| **LoRA** | 가벼운 비법노트만 얹어 즉각 실력 향상 | 가장 가벼움, 저비용 |

## Full Fine-tuning vs LoRA
- 모델은 수학 모델: **y = w·x + b**, 여기서 **W(가중치)**가 핵심 숫자.
- **Full Fine-tuning:** W 전체를 다 바꿈 → 컴퓨팅 막대.
- **LoRA (Low-Rank Adaptation):** 끝의 **작은 행렬만** 바꿈 → 전체의 약 **0.29%만 학습**해도 충분한 성능.
  - Linear Regression 비유: 선을 바꾸는 방법 중 맨 끝 값(위아래)만 조정 → 계산 적음.
  - 논문: *LoRA: Low-Rank Adaptation of Large Language Models* — https://arxiv.org/abs/2106.09685

## 비유
- 파인튜닝: 강아지를 잘 인식하는 모델에 **내 강아지 사진**을 학습시켜 특화.
- LoRA: 모델 본체는 그대로 두고 **얇은 노트**만 추가.

## 관련 개념
[RAG vs 파인튜닝](./rag-vs-finetuning.md) · [학습 파라미터](./training-params.md) · [과적합·과소적합](./overfitting-underfitting.md) · [Unsloth](./unsloth.md) · [양자화](./quantization.md)
