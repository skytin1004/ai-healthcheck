# ai-healthcheck

[![Python 패키지](https://img.shields.io/pypi/v/ai-healthcheck?color=4BA3FF)](https://pypi.org/project/ai-healthcheck/)
[![라이선스: MIT](https://img.shields.io/github/license/skytin1004/ai-healthcheck?color=4BA3FF)](https://github.com/skytin1004/ai-healthcheck/blob/main/LICENSE)
[![다운로드 수](https://static.pepy.tech/badge/ai-healthcheck)](https://pepy.tech/project/ai-healthcheck)
[![다운로드 수](https://static.pepy.tech/badge/ai-healthcheck/month)](https://pepy.tech/project/ai-healthcheck)

[![GitHub 기여자](https://img.shields.io/github/contributors/skytin1004/ai-healthcheck.svg)](https://GitHub.com/skytin1004/ai-healthcheck/graphs/contributors/)
[![GitHub 이슈](https://img.shields.io/github/issues/skytin1004/ai-healthcheck.svg)](https://GitHub.com/skytin1004/ai-healthcheck/issues/)
[![GitHub 풀 리퀘스트](https://img.shields.io/github/issues-pr/skytin1004/ai-healthcheck.svg)](https://GitHub.com/skytin1004/ai-healthcheck/pulls/)
[![PRs 환영](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](http://makeapullrequest.com)

### 🌐 다국어 지원

#### [Localizeflow](https://localizeflow.com/)에서 지원

[한국어](./README.md)

OpenAI용 경량 헬스 체크 — 무거운 SDK가 필요 없습니다.

- 최소한의 데이터 플레인 호출(작은 페이로드와 짧은 타임아웃)
- 명확하고 예측 가능한 동작(항상 `HealthResult` 반환)
- 작은 설치 크기(`requests`만 사용)
- 애플리케이션 시작 프로브 및 CI/CD 스모크 테스트에 적합

## 설치

```bash
pip install ai-healthcheck
```

## 빠른 시작

자격 증명(예: 환경 변수 사용)을 설정한 뒤 체크를 호출하세요.

```python
import os
from ai_healthcheck import check_openai

res = check_openai(
    endpoint=os.environ["OPENAI_ENDPOINT"],  # 예: https://api.openai.com
    api_key=os.environ["OPENAI_API_KEY"],
    model="gpt-5-mini",
    # 선택 사항: 계정이 조직을 사용하는 경우 조직으로 범위를 지정
    # org_id=os.environ.get("OPENAI_ORG_ID"),
)
print(res)
```

### 샘플 출력

```python
# HealthResult(제공자='openai',
#              엔드포인트='https://api.openai.com',
#              정상=True,
#              상태_코드=200,
#              메시지='OpenAI에 연결 가능. 자격 증명과 모델이 유효한 것으로 보입니다.')
```

## 사용법

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
- 그 외(401/403 및 기타 non-2xx, 또는 네트워크 오류) -> ok=False(세부 정보 포함)

## 참고

- `requests`만 사용; SDK 의존성이 없음.
- 사용자 정의 User-Agent 헤더를 설정하지 않음(요청을 최소화).

## 문제 해결

- 404: API 키는 유효할 수 있으나, 엔드포인트/경로 또는 모델 이름이 잘못되었을 가능성이 있습니다. 엔드포인트(예: `/v1`를 한 번만 포함)와 모델을 확인하세요.
- 401/403: 인증/권한 오류. API 키 및 계정 접근 권한을 확인하세요.

## CI/CD 및 시작 프로브

이러한 체크를 파이프라인이나 앱 시작 시 사용하여 명확한 안내와 함께 빠르게 실패 처리하세요.

```python
def app_startup_probe():
    from ai_healthcheck import check_openai
    res = check_openai(endpoint=..., api_key=..., model=...)
    if not res.ok:
        raise RuntimeError(f"OpenAI health check failed: {res.message}")
```

## 기여

기여는 환영입니다! GitHub에 이슈와 풀 리퀘스트를 열어주세요.