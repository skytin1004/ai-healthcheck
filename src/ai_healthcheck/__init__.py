"""ai_healthcheck

Lightweight health checks for OpenAI.
"""
from ai_healthcheck.models import HealthResult
from ai_healthcheck.openai import check_openai

__all__ = [
    "HealthResult",
    "check_openai",
]
