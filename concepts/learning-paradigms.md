# 머신러닝 3대 학습 패러다임

**한 줄 정의:** AI를 학습시키는 세 가지 큰 방식. 사람이 학습하는 방법을 기계에 적용한 것.

| 패러다임 | 방식 | 예시 |
| --- | --- | --- |
| **Supervised Learning (지도)** | 정답을 주입 (= SFT) | "이건 커피야" × N / "1+1=2" 반복 |
| **Unsupervised Learning (비지도)** | 정답 없이 스스로 패턴 찾아 분류 | 사진 100장 → 컵/종이 자동 구분 |
| **Reinforcement Learning (강화)** | 보상(+)/벌점(−) 피드백으로 학습 | 맞으면 +1, 틀리면 −1 (사람 학습과 가장 닮음) |

## 파인튜닝과의 관계
- **SFT (Supervised Fine-Tuning)** = 지도학습 기반 주입식 교육 = 가장 기본적인 [파인튜닝](./finetuning-lora.md).
- **AI 자동 피드백** = 강화학습 기반, 좋은 답/나쁜 답을 스스로 만들어 품질 학습 (cf. [RLHF](./short-vs-long-term-memory.md)).

## 관련 개념
[파인튜닝·LoRA](./finetuning-lora.md) · [단기 vs 장기 기억](./short-vs-long-term-memory.md) · [추론](./reasoning.md)
