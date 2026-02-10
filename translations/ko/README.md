# ai-healthcheck

[![Python package](https://img.shields.io/pypi/v/ai-healthcheck?color=4BA3FF)](https://pypi.org/project/ai-healthcheck/)
[![License: MIT](https://img.shields.io/github/license/skytin1004/ai-healthcheck?color=4BA3FF)](https://github.com/skytin1004/ai-healthcheck/blob/main/LICENSE)
[![Downloads](https://static.pepy.tech/badge/ai-healthcheck)](https://pepy.tech/project/ai-healthcheck)
[![Downloads](https://static.pepy.tech/badge/ai-healthcheck/month)](https://pepy.tech/project/ai-healthcheck)

[![GitHub contributors](https://img.shields.io/github/contributors/skytin1004/ai-healthcheck.svg)](https://GitHub.com/skytin1004/ai-healthcheck/graphs/contributors/)
[![GitHub issues](https://img.shields.io/github/issues/skytin1004/ai-healthcheck.svg)](https://GitHub.com/skytin1004/ai-healthcheck/issues/)
[![GitHub pull-requests](https://img.shields.io/github/issues-pr/skytin1004/ai-healthcheck.svg)](https://GitHub.com/skytin1004/ai-healthcheck/pulls/)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](http://makeapullrequest.com)

## Languages
[Chinese](../zh/README.md) | [French](../fr/README.md) | [Japanese](../ja/README.md) | [Korean](./README.md) | [Spanish](../es/README.md)

OpenAI용 경량 헬스 체크 — 무거운 SDK 불필요.

- 작은 페이로드와 짧은 타임아웃으로 최소한의 데이터 플레인 호출
- 명확하고 예측 가능한 동작 (항상 `HealthResult` 반환)
- 작은 설치 크기 (`requests`만 사용)
- 애플리케이션 시작 프로브 및 CI/CD 스모크 테스트에 적합

## Installation

```bash
pip install ai-healthcheck
```

## Quickstart

환경 변수 사용 예제를 포함한 자격 증명을 설정한 후, 체크를 호출하세요.

```python
import os
from ai_healthcheck import check_openai

res = check_openai(
    endpoint=os.environ["OPENAI_ENDPOINT"],  # 예: https://api.openai.com
    api_key=os.environ["OPENAI_API_KEY"],
    model="gpt-5-mini",
    # 선택 사항: 계정에 조직이 있는 경우 조직 범위 지정
    # org_id=os.environ.get("OPENAI_ORG_ID"),
)
print(res)
```

### Sample output

```python
# 헬스결과(provider='openai',
#              엔드포인트='https://api.openai.com',
#              정상=True,
#              상태_코드=200,
#              메시지='OpenAI에 연결 가능. 자격 증명과 모델이 유효한 것으로 보임.')
```

## Usage

```python
from ai_healthcheck import check_openai

res = check_openai(
    endpoint="https://api.openai.com",
    api_key="***",
    model="gpt-5-mini",
    # 선택적 조직 헤더
    # org_id="org_12345",
    timeout=10.0,
)
print(res.ok, res.status_code, res.message)
```

동작:
- 200 -> ok=True
- 그 외 (401/403 및 기타 비 2xx, 또는 네트워크 오류) -> ok=False 및 상세 정보 포함

## Notes

- `requests`만 사용; SDK 의존성 없음.
- 커스텀 User-Agent 헤더를 설정하지 않음 (요청 최소화 유지).

## Troubleshooting

- 404: API 키는 유효할 수 있으나 엔드포인트/경로나 모델 이름이 잘못된 것일 가능성 있음. 엔드포인트(e.g., `/v1`을 한 번만 포함)와 모델을 확인하세요.
- 401/403: 인증/권한 오류. API 키 및 계정 접근 권한을 확인하세요.

## CI/CD and startup probes

이 체크를 파이프라인이나 앱 시작 시 사용하여 명확한 안내와 함께 빠르게 실패할 수 있습니다.

```python
def app_startup_probe():
    from ai_healthcheck import check_openai
    res = check_openai(endpoint=..., api_key=..., model=...)
    if not res.ok:
        raise RuntimeError(f"OpenAI health check failed: {res.message}")
```

## Contributing

기여를 환영합니다! GitHub에서 이슈 및 풀 리퀘스트를 제출해 주세요.