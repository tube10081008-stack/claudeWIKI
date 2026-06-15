# 📔 개념 사전 (Concept Glossary)

강의에서 등장한 핵심 개념을 RAG처럼 "찾아 쓰기 좋게" 정리한 색인입니다.

## 🟢 Day 1 — RAG 기초
| 개념 | 한 줄 정의 |
| --- | --- |
| [RAG](./rag.md) | 외부 지식을 찾아와 능력을 강화해 답변을 생성하는 기술 |
| [할루시네이션](./hallucination.md) | 확률 모델인 LLM이 모르면 그럴듯하게 지어내는 현상 |
| [파라메트릭 vs 논파라메트릭 메모리](./memory-types.md) | AI의 머릿속 지식 vs 외부 지식 창고 |
| [인코더 & 벡터](./encoder-vector.md) | 글자를 고차원 숫자 좌표로 번역하는 장치와 그 좌표 |
| [MIPS](./mips.md) | 가장 유사한 벡터를 광속으로 찾는 검색 기술 |

## 🟡 Day 2 — 진화 (의심 & 연결)
| 개념 | 한 줄 정의 |
| --- | --- |
| [Self-RAG](./self-rag.md) | AI 스스로 모은 지식을 4기준으로 검증해 좋은 것만 남김 |
| [Graph RAG](./graph-rag.md) | 점이 아닌 선으로 지식을 연결해 전체 맥락(숲)을 봄 |

## 🟠 Day 3 — Agentic RAG
| 개념 | 한 줄 정의 |
| --- | --- |
| [Agentic RAG](./agentic-rag.md) | RAG + 추론 + 자율성, 2026년 최전선 |
| [추론 (Reasoning)](./reasoning.md) | 단계별 사고(Chain/Tree/Graph)로 복잡한 문제 풀기 |
| [에이전트 오케스트레이션](./agent-orchestration.md) | 여러 에이전트를 지휘자처럼 조율 (수직/수평) |
| [Hugging Face](./huggingface.md) | AI계의 GitHub, 258만 모델 무료 공유 |
| [로컬 vs 클라우드 LLM](./local-vs-cloud-llm.md) | 내 컴퓨터 vs 남의 서버, 모델 선택 원칙 |
| [양자화 (Quantization)](./quantization.md) | 지능 유지하며 모델 크기 압축 |
| [사전훈련·파인튜닝·LoRA](./finetuning-lora.md) | 모델을 내 목적에 맞게 만드는 3가지 방법 |

## 🔴 Day 4 — 미래 & 파인튜닝
| 개념 | 한 줄 정의 |
| --- | --- |
| [RAG vs 파인튜닝](./rag-vs-finetuning.md) | 검색해 가져오기 vs 두뇌 자체 바꾸기 (보완 관계) |
| [과적합·과소적합](./overfitting-underfitting.md) | 학습량이 과하면 꼰대화, 부족하면 인식 실패 |
| [학습 파라미터](./training-params.md) | 가중치·로스·learning rate·max steps·batch size |
| [Unsloth](./unsloth.md) | 무료·저사양에서 LLM 파인튜닝하는 오픈소스 도구 |
| [미래 RAG & 비즈니스 모델](./future-rag.md) | Knowledge Runtime·SLM+RAG·스타트업 5종 |

## 🔵 Day 5 — 에이전트 SDK & 연결 (Step 2 진입)
| 개념 | 한 줄 정의 |
| --- | --- |
| [Antigravity SDK](./antigravity-sdk.md) | 에이전트를 코드로 정밀 제작 (CLI=사용자, SDK=생산자) |
| [에이전트 자율성·가드레일](./agent-autonomy.md) | 자율성 수준 + 위험 행동 차단(policy/hook) |
| [하이브리드 비용 최적화](./hybrid-cost-optimization.md) | 로컬로 요약·클라우드로 최종 → ~98% 절감 |

## 🟣 Day 6 — 데이터 자산화 & 장기기억 (핵심)
| 개념 | 한 줄 정의 |
| --- | --- |
| [단기 vs 장기 기억](./short-vs-long-term-memory.md) | RAG(단기) vs 파인튜닝(장기), RLHF 필터링 |
| [데이터 자산화](./data-as-asset.md) | "모델은 소비재, 데이터는 자산" 축적 시스템 |
| [파인튜닝 디버깅](./finetuning-debugging.md) | 3대 함정(bos·과적합·RAM) + 5단계 체크리스트 |

> 새 강의를 들을 때마다 개념이 추가됩니다.
