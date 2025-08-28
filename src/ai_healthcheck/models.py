from __future__ import annotations

from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True)
class HealthResult:
    """Result of a health check.

    Attributes:
        provider: Provider identifier, e.g., "azure_openai" or "azure_ai_vision".
        endpoint: The endpoint URL that was checked.
        ok: True if the check succeeded (HTTP 200/success path).
        status_code: HTTP status code when available.
        message: Concise message with next-step guidance.
    """

    provider: str
    endpoint: str
    ok: bool
    status_code: Optional[int]
    message: str
