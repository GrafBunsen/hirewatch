from hirewatch.models import Job
from hirewatch.notify import _render


def test_render_includes_job_fields():
    jobs = [
        Job(
            title="Test Job",
            source="Test Source",
            company="Test Company",
            location="Test City",
            url="https://test.com/1",
        ),
    ]
    text, html = _render(jobs)
    assert "Test Job" in html
    assert "Test Company" in html
    assert "Test City" in html
    assert "Test Source" in html
    assert "Test Job" in text


def test_render_handles_missing_optional_fields():
    jobs = [Job(title="Test Job", source="Test Source", url="https://test.com/1")]
    text, html = _render(jobs)
    assert "Test Job" in html
    assert "Test Source" in html
