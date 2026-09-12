# AI Job Search Agent

A small Python agent that searches real jobs through Adzuna, cleans the results, and uses Groq to rank each job against a candidate profile. Built as a clear, interview-friendly progression from a Colab prototype into a runnable application.

## What is implemented

- Real job search through the Adzuna API
- Normalized job records: title, company, location, description, and application link
- Deduplication by normalized title + company
- Groq LLM matching in JSON mode
- Match score, missing skills, recommendation, and reason for every matched job
- Score ranking, minimum-score filtering, and exclusion of `do_not_apply` by default
- Direct application links in terminal output
- Unit tests for deterministic cleaning/filtering logic

## What is deliberately not claimed as implemented

**ATS/resume compatibility is planned, not yet a production feature.** A future `resume_analyzer` module should safely extract resume text (PDF/DOCX), compare it with one selected job description, report keyword coverage, and give editing suggestions. It should be described as an *estimated resume-to-job compatibility score*, not the score of an employer's ATS. This is the right scope before Monday: the job-search and matching path is complete and demonstrable rather than a rushed, unreliable document parser.

## Architecture

```text
CLI → AdzunaClient → Job normalization → deduplicate_jobs
                                      ↓
CandidateProfile → GroqJobMatcher → validated JSON → rank/filter → apply links
```

## Setup

Requires Python 3.10+.

```bash
python -m venv .venv
# Windows PowerShell
.venv\Scripts\Activate.ps1
pip install -e ".[dev]"
Copy-Item .env.example .env
```

Put your own Adzuna and Groq keys in `.env`. `.env` is ignored by Git; never commit it.

## Run

```bash
job-agent --keyword "AI Engineer" --location Hyderabad --experience 1 --skills "Java,Python,AI,ML,LLM,RAG,REST API" --min-score 60
```

The first run makes real API calls and can incur normal provider usage/costs. Results and LLM scores can change because job listings and model output change.

## Test

```bash
pytest -q
```

## Interview walkthrough

1. Search Adzuna with a keyword and location.
2. Show the clean `Job` model and explain why API responses are normalized at the boundary.
3. Explain the original prototype's early-return deduplication bug and the tested fix.
4. Show Groq JSON mode and validation that prevents invented job entries from being displayed.
5. Distinguish job-fit scoring from ATS/resume compatibility; only the former is currently implemented.

## Possible next increment

Add a focused resume module with PDF/DOCX text extraction, deterministic keyword overlap, and LLM suggestions. Keep it separate from job-fit scoring and test it with fixture resumes.
