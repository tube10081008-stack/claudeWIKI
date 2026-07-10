# Week 2 · Day 5 (5강) — 로컬 에이전트 → 클라우드 에이전트 완벽 연결

> **단계:** Step 2 (Agent) 진입 — 로컬 AI와 자동화 에이전트를 연결하는 다리
> **주제:** Antigravity CLI / SDK를 사용해 **내 에이전트를 처음부터 직접 만들고**, 로컬 AI로 비용을 절감한다
> **참고:** https://antigravity.google/product/antigravity-cli · https://github.com/google-antigravity/antigravity-sdk-python

---

## 0. 큰 그림: 구글이 안티그래비티를 4개로 쪼갰다

안티그래비티(에이전트를 만드는 도구)가 너무 커지자 **세분화**됨. 난이도 순:

```
난이도 낮음 ────────────────────────────► 난이도 높음
 2.0(자동)  <  IDE  <  CLI(터미널)  <  SDK(코드)
 알아서 뚝딱      에디터    검은 창        파이썬으로 정밀 제어
```

- 어려울수록 **상세하게(디테일하게) 나만의 에이전트를 제어**할 수 있다.
- 2.0은 "에이전트 만들어 줘" → 알아서 만들지만 **내부를 볼 수 없다**.
- **SDK는 코드로 하나하나 제어** → 보안·권한·루프·도구를 정밀 설계.

> 📌 구글은 큰 회사라 서비스를 '빵' 런칭하면 전 세계가 동시에 쓴다. 흐름을 아는 사람은 잘 쓰고,
> 큰 구조를 못 보면 "왜 이렇게 불편하게 바꿨어"라며 불평한다. → **우리는 흐름을 보는 쪽이 된다.**

---

## 1. CLI vs SDK — 'User'와 'Creator'의 차이

| | **Antigravity CLI/IDE** = 완성품 스마트폰 | **Antigravity SDK** = 부품 상자 |
| --- | --- | --- |
| 대상 | 개발자 개인 (사용자) | 새 AI 서비스를 만드는 사람 (생산자) |
| 역할 | 구글이 미리 만든 **완성형 코딩 비서** | 나만의 AI 에이전트 제품을 만드는 **원재료(라이브러리)** |
| 한계 | 내 터미널 안에서 나를 돕는 용도 | 배포·판매·홈페이지 탑재 가능 |

> 한 줄: **CLI = 내가 쓰는 비서 / SDK = 남이 쓸 새 비서 서비스를 만드는 재료.**

### 💡 SDK가 꼭 필요한 4가지 이유
1. **나만의 웹/모바일 서비스에 AI 탑재** — 홈페이지·앱·카톡 챗봇에 에이전트 내장 (백엔드 `app.py`에서 구동).
2. **사내 시스템·DB(ERP) 연동** — 내가 짠 파이썬 함수를 도구로 쥐여줌 (`tools=[fetch_db_data]`).
3. **초정밀 보안 제어·승인 프로세스** — "100만 원 이상 결제 시 사장 텔레그램 승인 대기" 같은 훅(Hook)을 코드로 설계.
4. **백그라운드 자동화 SaaS** — 터미널을 켜두지 않아도 클라우드에서 24시간 모니터링·보고하는 자율 시스템.

---

## 2. 실습 준비: 가상환경(venv) + API 키

### 가상환경 — 설치물이 서로 꼬이지 않게 격리
```bash
# macOS
python3 -m venv venv
source venv/bin/activate            # 성공 시 왼쪽에 (venv) 표시
pip install --upgrade pip
pip install google-antigravity uvicorn sse-starlette starlette
```
```powershell
# Windows (PowerShell)
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install google-antigravity uvicorn sse-starlette starlette
```

### API 키 세팅 (터미널 세션 유지)
```bash
# macOS
export GEMINI_API_KEY="발급받은_키"
# Windows
set GEMINI_API_KEY=발급받은_키
```
> 키는 **AI Studio → Get API key → Copy**. (안티그래비티 CLI 초기화: `agy` 입력 → 테마 선택 →
> ⚠️ 데이터 수집 동의 화면의 `[x]`는 *동의함* 표시 — 원치 않으면 엔터로 해제 후 `[Done]`.)

---

## 3. Hello World — 첫 에이전트

```python
import os, asyncio
from google.antigravity import Agent, LocalAgentConfig

async def main() -> None:
    config = LocalAgentConfig()                 # 1) 작업 명세서(두뇌·보안 규칙)
    async with Agent(config) as my_agent:        # 2) 안전한 작업공간으로 소환(끝나면 자동 정리)
        prompt = "작동되는지 테스트! 잘되면 오케이!라고 해주세요"
        response = await my_agent.chat(prompt)   # 3) 질문 전달하고 대기
        print(await response.text())             # 4) 답변 합쳐서 출력
if __name__ == "__main__":
    asyncio.run(main())                          # 5) 비동기 엔진 시작
```
실행: `python3 hello.py` → "오케이, 잘 작동하고 있습니다" 응답 확인.

> 이제 에이전트는 단순 대화가 아니라 **내 파일에 접근하고, API로 유튜브 업로드** 등 행동을 한다.
> 그래서 **권한(permission)·도구(tools)·보안(security)을 직접 설정**해야 한다.

---

## 4. 안전 가드 — Policy/Hook으로 위험 명령 차단

> 시나리오: 터미널 실행 권한은 주되, `rm`(삭제) 같은 위험 명령은 파이썬 검증 함수가 **자동 차단**.

```python
from google.antigravity import Agent, LocalAgentConfig, types
from google.antigravity.hooks import policy

def check_command_danger(args) -> bool:          # True = 위험 → 차단
    cmd = args.get("command_line", "").strip()
    forbidden = ["rm", "delete", "shutdown", "cat /etc/passwd", "mv"]
    for w in forbidden:
        if w in cmd.split() or cmd.startswith(w):
            return True
    return False

config = LocalAgentConfig(
    system_instructions="You can run terminal commands, but obey safety rules...",
    policies=[
        policy.deny("run_command", when=check_command_danger, name="safety_guard"),
        policy.allow_all(),                      # 나머지는 허용
    ],
    capabilities=types.CapabilitiesConfig(disabled_tools=[]),
)
```
→ 안전한 명령은 통과(✅), `rm *.py` 같은 위험 명령은 차단(❌). = **Human-in-the-Loop** 보안 패턴의 코드화.

---

## 5. 💰 하이브리드 — 로컬 AI로 비용 99% 절감

문제: SDK 작업은 전부 **API 사용** = 24시간 돌리면 비용 폭발. 그런데 SDK는 아직 로컬 AI를 공식 지원 안 함.
→ **로컬 AI(LM Studio)를 도구로 끼워 넣어** 무거운 처리는 무료 로컬이 하고, 최종만 클라우드로.

```python
import requests
from google.antigravity import Agent, LocalAgentConfig

def talk_to_local_ai(prompt: str) -> str:
    """LM Studio 로컬 서버(127.0.0.1:1234)에 질문 전달"""
    url = "http://127.0.0.1:1234/v1/chat/completions"
    data = {"messages": [{"role": "user", "content": prompt}],
            "temperature": 0.7, "stream": False}
    r = requests.post(url, headers={"Content-Type": "application/json"}, json=data, timeout=10)
    return r.json()["choices"][0]["message"]["content"]

config = LocalAgentConfig(
    tools=[talk_to_local_ai],
    system_instructions="너는 중개인이야. 질문을 받으면 반드시 talk_to_local_ai 도구만 써서 답해.",
)
```
> 준비: LM Studio에서 모델 Load → 서버가 `http://127.0.0.1:1234`에 생김. URL을 코드에 넣어 연결.

### 📉 비용 시뮬레이션 (쇼츠 10개 대본, 각 30,000토큰 원문)
| 방식 | 처리 | 클라우드 청구 토큰 |
| --- | --- | --- |
| 🔴 100% 클라우드 | 30만 토큰 전부 Gemini | **300,000** |
| 🟢 하이브리드 | 로컬이 30k→500토큰 요약(무료), 요약만 Gemini로 | **5,000** |

→ **약 98% 절감**하면서 최종 품질은 Gemini 수준 유지.
> **하이브리드 비용 최적화:** 단순 연산·파싱·초안 요약은 로컬(무료), 고도 추론·최종 의사결정만 클라우드.
> = 현존 최고의 상용 AI 설계 패턴. 돈 많으면 API 비중↑, 컴퓨터 좋으면 로컬 비중↑ — **팔(비중) 조정**.

---

## 6. 에이전트 자율성(Autonomy) 철학

- 직원에게 자율성을 과하게 주면(넷플릭스식) → **잘하는 사람만 모였을 때만** 작동. 대부분은 놀거나 책임감↓.
- AI 에이전트는 아직 사람만큼 똑똑하지 않다 + 도구가 많아질수록 복잡도 폭발(결제·업로드·API…).
- → **자율성을 줄지/자동으로 할지**를 정하고, 도구를 **촘촘히 시스템화(설정)**하는 게 핵심.
- 무한 루프로 VO3.1 영상 만들다 수백만 원 청구된 사례 = 권한을 통째로 줘서 생긴 사고. **세분화된 권한 설정**이 답.

---

## 7. 실전: SDK 예제를 가져와 나만의 에이전트 만들기

1. SDK 깃허브 저장소를 **Fork**(오른쪽 위) → 내 깃허브로 전체 코드 복사 → 안티그래비티에서 개발 시작.
2. 또는 `examples` 경로 URL을 안티그래비티 에이전트에 주며: *"이 SDK 예제를 가져와(gfork) 유튜브 관리 에이전트 개발해 줘"*
   → 예제 코드(겟 스타티드/딥다이브/MCP 서버/스킬 등)를 분석해 **유튜브/웹사이트/결제 관리 에이전트**를 생성.
3. 여기에 **4강에서 학습시킨 로컬 AI**를 두뇌로 끼우고 **RAG로 실시간 지식**을 연결 → 똑똑하고 저렴한 나만의 에이전트.

> 핵심은 "만드는 것"보다 **무엇을 자동화할지**. 어떤 서비스/채널을 만들고 관리·업로드할지가 더 중요.

---

## 🔮 다음 주(6강) 예고
4강에서 학습시킨 **로컬 AI → Hugging Face 업로드 → LM Studio로 이동 → 오늘 만든 SDK 에이전트에 연결**.
(+ 파인튜닝을 더 잘하는 방법)

## 🌐 곁들임: Project Genie 3
이미지/지도를 넣으면 **3D 가상 환경(물리 적용)**을 생성 — 로봇·자율주행 학습용 월드. (try Genie → Explore now)

---

## 📎 참고 링크
- Antigravity CLI: https://antigravity.google/product/antigravity-cli
- SDK 저장소: https://github.com/google-antigravity/antigravity-sdk-python
- SDK 예제: https://github.com/google-antigravity/antigravity-sdk-python/tree/main/examples
- LM Studio 로컬 서버: http://127.0.0.1:1234

## 🔑 핵심 한 줄 정리

> **CLI는 내가 쓰는 비서, SDK는 남이 쓸 비서를 만드는 재료.** SDK로 권한·보안을 코드로 정밀 제어하고,
> 로컬 AI를 하이브리드로 끼워 비용을 ~98% 줄이며, 내 1인 기업의 에이전트를 처음부터 직접 만든다.

→ 개념: [Antigravity SDK](../../concepts/antigravity-sdk.md) · [에이전트 자율성·가드레일](../../concepts/agent-autonomy.md) · [하이브리드 비용 최적화](../../concepts/hybrid-cost-optimization.md)
