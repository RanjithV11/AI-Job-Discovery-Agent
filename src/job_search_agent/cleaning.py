from __future__ import annotations

import re

from .models import Job


def _key_part(value: str) -> str:
    return re.sub(r"\s+", " ", value.strip().casefold())


def deduplicate_jobs(jobs: list[Job]) -> list[Job]:
    """Keep the first job for each normalized title/company pair."""
    seen: set[tuple[str, str]] = set()
    unique: list[Job] = []
    for job in jobs:
        key = (_key_part(job.title), _key_part(job.company))
        if key not in seen:
            seen.add(key)
            unique.append(job)
    return unique

