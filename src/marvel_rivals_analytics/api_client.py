"""HTTP client for MarvelRivalsAPI.com."""

from __future__ import annotations

from dataclasses import dataclass
from urllib.parse import urljoin

import requests


class ApiClientError(RuntimeError):
    """Raised when API requests fail."""


@dataclass(frozen=True)
class RequestResult:
    """Container for response details."""

    url: str
    params: dict[str, str] | None
    status_code: int
    response_text: str
    json_data: dict | None


class ApiClient:
    """Simple API client that enforces x-api-key auth on every request."""

    def __init__(self, base_url: str, api_key: str) -> None:
        if not base_url:
            raise ValueError("MR_API_BASE_URL is required")
        if not api_key:
            raise ValueError("MR_API_KEY is required")

        self.base_url = base_url.rstrip("/") + "/"
        self.api_key = api_key

    def build_url(self, path: str) -> str:
        """Build a URL from a relative endpoint path."""
        clean_path = path.lstrip("/")
        return urljoin(self.base_url, clean_path)

    def request(self, path: str, params: dict[str, str] | None = None) -> RequestResult:
        """Execute an API request and return details for persistence/inspection."""
        url = self.build_url(path)
        response = requests.get(
            url,
            params=params,
            headers={"x-api-key": self.api_key},
            timeout=30,
        )
        text = response.text

        json_data: dict | None = None
        if response.status_code == 200:
            try:
                json_data = response.json()
            except ValueError as exc:
                raise ApiClientError(f"Expected JSON response from {url}") from exc

        return RequestResult(
            url=response.url,
            params=params,
            status_code=response.status_code,
            response_text=text,
            json_data=json_data,
        )

    def request_json(self, path: str, params: dict[str, str] | None = None) -> dict:
        """Request endpoint JSON and raise on non-200 responses."""
        result = self.request(path, params=params)
        if result.status_code != 200:
            snippet = result.response_text[:500]
            raise ApiClientError(
                f"API request failed ({result.status_code}) for {result.url}: {snippet}"
            )
        if result.json_data is None:
            raise ApiClientError(f"API returned empty JSON payload for {result.url}")
        return result.json_data
