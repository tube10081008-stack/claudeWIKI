# 하이브리드 비용 최적화 (Hybrid Cost Optimization)

**한 줄 정의:** 단순 처리·요약은 무료 로컬 AI에, 고도 추론·최종 결정만 값비싼 클라우드 AI에 맡겨 비용·성능을 동시에 잡는 패턴.

## 원리
1. 로컬 AI(LM Studio)가 무거운 원문을 **짧은 요약본**으로 축소 (무료).
2. 요약본만 클라우드(Gemini)에 넘겨 **최종 결과** 생성.

## 비용 시뮬레이션 (쇼츠 10개, 각 30,000토큰)
| 방식 | 클라우드 청구 토큰 |
| --- | --- |
| 🔴 100% 클라우드 | 300,000 |
| 🟢 하이브리드 | 5,000 |

→ **약 98% 절감**, 품질은 Gemini 수준 유지.

## 연결 방법 (LM Studio)
- LM Studio에서 모델 Load → 서버가 `http://127.0.0.1:1234`에 생성.
- 에이전트 도구 함수로 `POST /v1/chat/completions` 호출:
  ```python
  url = "http://127.0.0.1:1234/v1/chat/completions"
  ```
- 안티그래비티 SDK가 로컬 AI를 공식 지원 안 해도, **도구(tool)로 끼워** 하이브리드 구현.

## 비중 조정
- 돈 많으면 API 비중↑ / 컴퓨터 좋으면 로컬 비중↑ → '팔(비중)'을 상황에 맞게 조정.

## 관련 개념
[로컬 vs 클라우드](./local-vs-cloud-llm.md) · [Antigravity SDK](./antigravity-sdk.md) · [양자화](./quantization.md)
