<!--
CO_OP_TRANSLATOR_METADATA:
{
  "original_hash": "4165a35b2cff9daf32f2382837902c11",
  "translation_date": "2025-11-17T04:31:27+00:00",
  "source_file": "README.md",
  "language_code": "ko"
}
-->
# ai-healthcheck

[![Python package](https://img.shields.io/pypi/v/ai-healthcheck?color=4BA3FF)](https://pypi.org/project/ai-healthcheck/)
[![License: MIT](https://img.shields.io/github/license/skytin1004/ai-healthcheck?color=4BA3FF)](https://github.com/skytin1004/ai-healthcheck/blob/main/LICENSE)
[![Downloads](https://static.pepy.tech/badge/ai-healthcheck)](https://pepy.tech/project/ai-healthcheck)
[![Downloads](https://static.pepy.tech/badge/ai-healthcheck/month)](https://pepy.tech/project/ai-healthcheck)

[![GitHub contributors](https://img.shields.io/github/contributors/skytin1004/ai-healthcheck.svg)](https://GitHub.com/skytin1004/ai-healthcheck/graphs/contributors/)
[![GitHub issues](https://img.shields.io/github/issues/skytin1004/ai-healthcheck.svg)](https://GitHub.com/skytin1004/ai-healthcheck/issues/)
[![GitHub pull-requests](https://img.shields.io/github/issues-pr/skytin1004/ai-healthcheck.svg)](https://GitHub.com/skytin1004/ai-healthcheck/pulls/)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](http://makeapullrequest.com)

### 🌐 다국어 지원
[Korean](./README.md)

OpenAI를 위한 가벼운 헬스 체크 — 무거운 SDK가 필요 없습니다.

- 최소한의 데이터 전송과 짧은 타임아웃으로 빠른 호출
- 명확하고 예측 가능한 동작 (항상 `HealthResult` 반환)
- 설치 용량이 작음 (`requests`만 사용)
- 애플리케이션 시작 프로브와 CI/CD 스모크 테스트에 최적

## 설치

```bash
pip install ai-healthcheck
```

## 빠른 시작

환경 변수 예시를 사용해 자격 증명을 설정한 후, 체크를 호출하세요.

```python
import os
from ai_healthcheck import check_openai

res = check_openai(
    endpoint=os.environ["OPENAI_ENDPOINT"],  # e.g., https://api.openai.com
    api_key=os.environ["OPENAI_API_KEY"],
    model="gpt-4o-mini",
    # Optional: scope to an organization if your account uses one
    # org_id=os.environ.get("OPENAI_ORG_ID"),
)
print(res)
```

### 샘플 출력

```python
# HealthResult(provider='openai',
#              endpoint='https://api.openai.com',
#              ok=True,
#              status_code=200,
#              message='OpenAI reachable. Credentials and model appear valid.')
```

## 사용법

```python
from ai_healthcheck import check_openai

res = check_openai(
    endpoint="https://api.openai.com",
    api_key="***",
    model="gpt-4o-mini",
    # Optional organization header
    # org_id="org_12345",
    timeout=10.0,
)
print(res.ok, res.status_code, res.message)
```

동작 방식:
- 200 -> ok=True
- 그 외 (401/403 및 기타 2xx가 아닌 상태, 네트워크 오류 포함) -> ok=False와 상세 정보 반환

## 참고 사항

- `requests`만 사용하며 SDK 의존성이 없습니다.
- 사용자 지정 User-Agent 헤더를 설정하지 않아 요청을 최소화합니다.

## 문제 해결

- 404: API 키는 유효할 수 있으나 엔드포인트/경로나 모델 이름이 잘못되었을 가능성이 큽니다. 엔드포인트(예: `/v1`이 한 번만 포함되었는지)와 모델을 확인하세요.
- 401/403: 인증 또는 권한 오류입니다. API 키와 계정 접근 권한을 점검하세요.

## CI/CD 및 시작 프로브

파이프라인이나 앱 시작 시 이 체크를 사용해 빠르게 실패를 감지하고 명확한 안내를 받을 수 있습니다.

```python
def app_startup_probe():
    from ai_healthcheck import check_openai
    res = check_openai(endpoint=..., api_key=..., model=...)
    if not res.ok:
        raise RuntimeError(f"OpenAI health check failed: {res.message}")
```

## 기여하기

기여를 환영합니다! GitHub에서 이슈와 풀 리퀘스트를 열어 주세요.