from __future__ import annotations

import logging
import requests

from ai_healthcheck.models import HealthResult

logger = logging.getLogger(__name__)


def _build_chat_url(endpoint: str) -> str:
    base = (endpoint or "").rstrip("/")
    if base.endswith("/v1"):
        return f"{base}/chat/completions"
    return f"{base}/v1/chat/completions"


def check_openai(
    endpoint: str,
    api_key: str,
    model: str,
    org_id: str | None = None,
    timeout: float = 10.0,
) -> HealthResult:
    """Health-check OpenAI chat completions.

    Behavior:
    - 200 -> ok=True
    - else (401/403 and other non-2xx, or network errors) -> ok=False with details
    
    Notes:
    - If `org_id` is provided, it will be sent via the `OpenAI-Organization` header.
    """
    if not endpoint or not api_key or not model:
        raise ValueError(
            "Missing required OpenAI parameters. Verify endpoint, api_key, and model."
        )

    url = _build_chat_url(endpoint)
    provider = "openai"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }
    if org_id:
        headers["OpenAI-Organization"] = org_id
    payload = {
        "model": model,
        "messages": [
            {"role": "system", "content": "health check"},
            {"role": "user", "content": "ping"},
        ],
        "max_tokens": 1,
        "temperature": 0,
    }

    try:
        resp = requests.post(url, headers=headers, json=payload, timeout=timeout)
    except Exception as e:  # network issues, DNS, etc.
        msg = (
            "Failed to reach OpenAI endpoint. Verify endpoint URL, networking, and DNS. "
            f"Details: {e}"
        )
        logger.warning(msg)
        return HealthResult(
            provider=provider,
            endpoint=endpoint,
            ok=False,
            status_code=None,
            message="Network/connection error. Check endpoint and connectivity.",
        )

    status = resp.status_code
    text_snippet = (resp.text or "")[:500]

    if status == 200:
        return HealthResult(
            provider=provider,
            endpoint=endpoint,
            ok=True,
            status_code=200,
            message="OpenAI reachable. Credentials and model appear valid.",
        )

    if status in (401, 403):
        message = (
            "OpenAI authentication/permission failed (401/403). "
            "Verify API key, endpoint, and model permissions."
        )
        logger.warning(message)
        return HealthResult(
            provider=provider,
            endpoint=endpoint,
            ok=False,
            status_code=status,
            message=message,
        )

    if status == 404:
        message = (
            "OpenAI returned HTTP 404 (Not Found). API key may be valid, but the endpoint/path "
            "or model name may be incorrect. Verify the endpoint format and model. Response snippet: "
            f"{text_snippet}"
        )
        logger.warning(message)
        return HealthResult(
            provider=provider,
            endpoint=endpoint,
            ok=False,
            status_code=404,
            message=message,
        )

    message = (
        f"OpenAI returned HTTP {status}. Verify endpoint and model. "
        f"Response snippet: {text_snippet}"
    )
    logger.warning(message)
    return HealthResult(
        provider=provider,
        endpoint=endpoint,
        ok=False,
        status_code=status,
        message=f"Non-2xx response. {message}",
    )
