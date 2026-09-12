from job_search_agent.cleaning import deduplicate_jobs
from job_search_agent.matcher import filter_matches
from job_search_agent.models import Job, JobMatch


def test_deduplicate_keeps_each_distinct_job():
    jobs = [
        Job(" AI Engineer ", "Acme", "Hyderabad", "", "one"),
        Job("ai  engineer", " acme ", "Hyderabad", "", "two"),
        Job("ML Engineer", "Acme", "Hyderabad", "", "three"),
    ]
    assert [job.apply_url for job in deduplicate_jobs(jobs)] == ["one", "three"]


def test_filter_hides_do_not_apply_and_low_scores():
    matches = [
        JobMatch("A", "A", 90, recommendation="apply"),
        JobMatch("B", "B", 95, recommendation="do_not_apply"),
        JobMatch("C", "C", 40, recommendation="apply"),
    ]
    assert [match.title for match in filter_matches(matches, minimum_score=70)] == ["A"]

