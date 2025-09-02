# ai-healthcheck

[![Python package](https://img.shields.io/pypi/v/ai-healthcheck?color=4BA3FF)](https://pypi.org/project/ai-healthcheck/)
[![License: MIT](https://img.shields.io/github/license/skytin1004/ai-healthcheck?color=4BA3FF)](https://github.com/skytin1004/ai-healthcheck/blob/main/LICENSE)
[![Downloads](https://static.pepy.tech/badge/ai-healthcheck)](https://pepy.tech/project/ai-healthcheck)
[![Downloads](https://static.pepy.tech/badge/ai-healthcheck/month)](https://pepy.tech/project/ai-healthcheck)

[![GitHub contributors](https://img.shields.io/github/contributors/skytin1004/ai-healthcheck.svg)](https://GitHub.com/skytin1004/ai-healthcheck/graphs/contributors/)
[![GitHub issues](https://img.shields.io/github/issues/skytin1004/ai-healthcheck.svg)](https://GitHub.com/skytin1004/ai-healthcheck/issues/)
[![GitHub pull-requests](https://img.shields.io/github/issues-pr/skytin1004/ai-healthcheck.svg)](https://GitHub.com/skytin1004/ai-healthcheck/pulls/)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](http://makeapullrequest.com)

Lightweight health checks for OpenAI — no heavy SDKs required.

- Minimal data-plane calls with tiny payloads and short timeouts
- Clear, predictable behavior (always returns `HealthResult`)
- Small install footprint (uses `requests` only)
- Perfect for application startup probes and CI/CD smoke tests

## Installation

```bash
pip install ai-healthcheck
```

## Quickstart

Set your credentials (example using environment variables), then call the check.

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

### Sample output

```python
# HealthResult(provider='openai',
#              endpoint='https://api.openai.com',
#              ok=True,
#              status_code=200,
#              message='OpenAI reachable. Credentials and model appear valid.')
```

## Usage

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

Behavior:
- 200 -> ok=True
- else (401/403 and other non-2xx, or network errors) -> ok=False with details

## Notes

- Uses `requests` only; no SDK dependency.
- No custom User-Agent header is set (keep requests minimal).

## Troubleshooting

- 404: API key may be valid, but the endpoint/path or model name is likely incorrect. Verify the endpoint (e.g., include `/v1` only once) and the model.
- 401/403: Authentication/permission errors. Check API key and account access.

## CI/CD and startup probes

Use these checks in your pipelines or app startup to fail fast with clear guidance.

```python
def app_startup_probe():
    from ai_healthcheck import check_openai
    res = check_openai(endpoint=..., api_key=..., model=...)
    if not res.ok:
        raise RuntimeError(f"OpenAI health check failed: {res.message}")
```

## Contributing

Contributions are welcome! Please open issues and pull requests on GitHub.
