from __future__ import annotations

import json
from typing import Any

from groq import Groq

from .models import CandidateProfile, Job, JobMatch

ALLOWED_RECOMMENDATIONS = {"strongly_apply", "apply", "caution", "do_not_apply"}


class GroqJobMatcher:
    """Uses Groq JSON mode to explain and score candidate-to-job fit."""

    def __init__(self, api_key: str, model: str = "openai/gpt-oss-120b"):
        if not api_key:
            raise ValueError("GROQ_API_KEY is required.")
        self.client = Groq(api_key=api_key)
        self.model = model

    def match(self, profile: CandidateProfile, jobs: list[Job]) -> list[JobMatch]:
        if not jobs:
            return []
        content = self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": self._prompt(profile, jobs)}],
            response_format={"type": "json_object"},
            temperature=0.2,
        ).choices[0].message.content
        payload = json.loads(self._strip_fence(content or "{}"))
        return self._validated_matches(payload, jobs)

    @staticmethod
    def _prompt(profile: CandidateProfile, jobs: list[Job]) -> str:
        return f"""You are an AI job matching assistant. Evaluate only the supplied candidate and jobs.

Candidate profile:\n{json.dumps(profile.as_dict())}
Jobs:\n{json.dumps([job.as_dict() for job in jobs])}

For every job return one result. Score 0-100, list genuine missing skills, give one of
strongly_apply, apply, caution, do_not_apply, and a concise reason. Do not claim the
candidate has skills not shown. Return ONLY a JSON object:
{{"matches":[{{"title":"...","company":"...","score":0,"missing_skills":[],"recommendation":"apply","reason":"..."}}]}}"""

    @staticmethod
    def _strip_fence(value: str) -> str:
        value = value.strip()
        if value.startswith("```") and value.endswith("```"):
            return value.split("\n", 1)[1].rsplit("```", 1)[0].strip()
        return value

    @staticmethod
    def _validated_matches(payload: dict[str, Any], jobs: list[Job]) -> list[JobMatch]:
        jobs_by_key = {(job.title.casefold(), job.company.casefold()): job for job in jobs}
        matches: list[JobMatch] = []
        for item in payload.get("matches", []):
            key = (str(item.get("title", "")).casefold(), str(item.get("company", "")).casefold())
            job = jobs_by_key.get(key)
            if not job:
                continue  # Reject invented job results.
            recommendation = item.get("recommendation", "caution")
            if recommendation not in ALLOWED_RECOMMENDATIONS:
                recommendation = "caution"
            matches.append(JobMatch(
                title=job.title, company=job.company,
                score=max(0, min(100, int(item.get("score", 0)))),
                missing_skills=[str(skill) for skill in item.get("missing_skills", [])],
                recommendation=recommendation, reason=str(item.get("reason", "")),
                location=job.location, apply_url=job.apply_url,
            ))
        return sorted(matches, key=lambda match: match.score, reverse=True)


def filter_matches(matches: list[JobMatch], minimum_score: int = 0, include_do_not_apply: bool = False) -> list[JobMatch]:
    return [match for match in matches if match.score >= minimum_score and (include_do_not_apply or match.recommendation != "do_not_apply")]

