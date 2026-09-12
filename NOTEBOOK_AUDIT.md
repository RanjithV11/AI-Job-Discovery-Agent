# Prototype notebook audit

Audited source: `pythonforai (1).ipynb` (uploaded on 2026-09-12).

## Confirmed prototype functionality

| Area | Evidence in notebook | Status in this project |
| --- | --- | --- |
| Adzuna search | Calls the India endpoint with `what`, `where`, credentials, and maps response fields | Implemented in `AdzunaClient` |
| Normalization | Creates title, company, location, description, redirect URL fields | Implemented as `Job` |
| Deduplication | Has a title/company dedupe attempt | Corrected and tested |
| LLM matching | Groq JSON mode with score/missing skills/recommendation/reason prompt | Implemented in `GroqJobMatcher` |
| Ranking/filtering | Sorts score descending and hides `do_not_apply` in later cells | Implemented and tested |
| Apply link | Retains Adzuna `redirect_url` | Printed by CLI |

## Findings

- The notebook mixes introductory exercises, Gemini experiments, mock jobs, and the actual Adzuna/Groq flow. It has no reusable package boundary or test suite.
- Secrets are retrieved through `google.colab.userdata`, which is appropriate for Colab but not for a repository. This project uses a local `.env` file ignored by Git.
- The final `remove_duplicates` version has `return unique_jobs` inside its loop, so it stops after the first unique job. The project returns only after all jobs are processed.
- The Groq matcher is the strongest end-to-end version because it asks for JSON and includes a short reason. The project retains that path and rejects LLM match items that do not correspond to an actual returned job.
- There is no implemented resume upload, PDF/DOCX parsing, or ATS calculation in the notebook. It must not be presented as a finished feature.

