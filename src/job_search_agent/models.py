from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass(frozen=True)
class CandidateProfile:
    experience: float
    skills: list[str]
    target_role: str

    def as_dict(self) -> dict[str, Any]:
        return {"experience": self.experience, "skills": self.skills, "target_role": self.target_role}


@dataclass(frozen=True)
class Job:
    title: str
    company: str
    location: str
    description: str
    apply_url: str
    source: str = "Adzuna"

    def as_dict(self) -> dict[str, str]:
        return {
            "title": self.title,
            "company": self.company,
            "location": self.location,
            "description": self.description,
            "apply_url": self.apply_url,
            "source": self.source,
        }


@dataclass(frozen=True)
class JobMatch:
    title: str
    company: str
    score: int
    missing_skills: list[str] = field(default_factory=list)
    recommendation: str = "caution"
    reason: str = ""
    location: str = ""
    apply_url: str = ""

