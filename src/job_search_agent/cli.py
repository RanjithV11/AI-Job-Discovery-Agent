from __future__ import annotations

import argparse
import os

from dotenv import load_dotenv

from .adzuna import AdzunaClient
from .cleaning import deduplicate_jobs
from .matcher import GroqJobMatcher, filter_matches
from .models import CandidateProfile


def main() -> None:
    parser = argparse.ArgumentParser(description="Search Adzuna and rank jobs with a Groq LLM.")
    parser.add_argument("--keyword", default="AI Engineer")
    parser.add_argument("--location", default="Hyderabad")
    parser.add_argument("--experience", type=float, default=1)
    parser.add_argument("--skills", default="Java,Python,AI,ML,LLM,RAG,REST API")
    parser.add_argument("--limit", type=int, default=10)
    parser.add_argument("--min-score", type=int, default=0)
    args = parser.parse_args()
    load_dotenv()

    profile = CandidateProfile(args.experience, [s.strip() for s in args.skills.split(",") if s.strip()], args.keyword)
    jobs = AdzunaClient(os.environ["ADZUNA_APP_ID"], os.environ["ADZUNA_APP_KEY"]).search(args.keyword, args.location, results_per_page=args.limit)
    matches = GroqJobMatcher(os.environ["GROQ_API_KEY"], os.getenv("GROQ_MODEL", "openai/gpt-oss-120b")).match(profile, deduplicate_jobs(jobs))
    for match in filter_matches(matches, args.min_score):
        print(f"{match.score:3}/100 | {match.recommendation:14} | {match.title} — {match.company}")
        print(f"  Missing: {', '.join(match.missing_skills) or 'None identified'}")
        print(f"  Why: {match.reason}\n  Apply: {match.apply_url}\n")


if __name__ == "__main__":
    main()

