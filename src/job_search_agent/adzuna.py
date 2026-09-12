from __future__ import annotations

from typing import Any

import requests

from .models import Job

BASE_URL = "https://api.adzuna.com/v1/api/jobs/{country}/search/{page}"


class AdzunaClient:
    """Small wrapper around Adzuna's public job-search endpoint."""

    def __init__(self, app_id: str, app_key: str, *, country: str = "in", session: requests.Session | None = None):
        if not app_id or not app_key:
            raise ValueError("ADZUNA_APP_ID and ADZUNA_APP_KEY are required.")
        self.app_id = app_id
        self.app_key = app_key
        self.country = country
        self.session = session or requests.Session()

    def search(self, keyword: str, location: str, *, results_per_page: int = 10, page: int = 1) -> list[Job]:
        response = self.session.get(
            BASE_URL.format(country=self.country, page=page),
            params={
                "app_id": self.app_id,
                "app_key": self.app_key,
                "what": keyword,
                "where": location,
                "results_per_page": results_per_page,
            },
            timeout=20,
        )
        response.raise_for_status()
        return [self._to_job(item) for item in response.json().get("results", [])]

    @staticmethod
    def _to_job(item: dict[str, Any]) -> Job:
        return Job(
            title=(item.get("title") or "Unknown title").strip(),
            company=(item.get("company") or {}).get("display_name") or "Unknown company",
            location=(item.get("location") or {}).get("display_name") or "Unknown location",
            description=(item.get("description") or "").strip(),
            apply_url=item.get("redirect_url") or "",
        )

