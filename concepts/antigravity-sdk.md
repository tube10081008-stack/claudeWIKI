# Antigravity SDK (vs CLI/IDE/2.0)

**한 줄 정의:** 나만의 AI 에이전트를 코드로 처음부터 정밀하게 만드는 라이브러리. CLI가 '완성품 비서'라면 SDK는 '부품 상자'.

## 4단계 난이도
```
2.0(자동) < IDE < CLI(터미널) < SDK(코드)
어려울수록 → 에이전트를 더 상세하게 제어 가능
```
- **2.0:** "에이전트 만들어 줘" → 알아서 만들지만 내부를 못 봄.
- **SDK:** 권한·보안·루프·도구를 코드로 하나하나 제어.

## User vs Creator
| | CLI/IDE = 완성품 스마트폰 | SDK = 부품 상자 |
| --- | --- | --- |
| 대상 | 사용자(개발자 개인) | 생산자(새 서비스 제작자) |
| 한계/강점 | 내 터미널 안 도움용 | 배포·판매·홈페이지 탑재 가능 |

## SDK가 필요한 4가지 이유
1. 웹/모바일/챗봇에 **AI 탑재** (백엔드 `app.py`)
2. 사내 **DB·ERP 연동** (`tools=[fetch_db_data]`)
3. **초정밀 보안·승인 프로세스** (결제 한도 훅 등) → [가드레일](./agent-autonomy.md)
4. **백그라운드 자동화 SaaS** (24시간 자율 모니터링)

## 핵심 객체 (코드)
- `Agent`, `LocalAgentConfig` — 에이전트와 명세서(두뇌·보안·도구)
- `policy.deny/allow_all`, `hooks` — 정책/훅
- `tools=[...]` — 파이썬 함수를 도구로 부여

## 링크
- 저장소: https://github.com/google-antigravity/antigravity-sdk-python
- CLI: https://antigravity.google/product/antigravity-cli

## 관련 개념
[에이전트 자율성·가드레일](./agent-autonomy.md) · [하이브리드 비용 최적화](./hybrid-cost-optimization.md) · [오케스트레이션](./agent-orchestration.md)
