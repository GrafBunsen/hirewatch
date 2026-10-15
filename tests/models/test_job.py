import pytest
from pydantic import ValidationError

from hirewatch.models import Job


def test_url_is_valid():
    with pytest.raises(ValidationError):
        Job(title="Test Job", source="Test Source", url="not a url")


def test_id_uses_external_id_when_present():
    job = Job(
        title="Test Job", source="Test Source", url="https://test.com", external_id="guid-123"
    )
    assert job.id == "guid-123"


def test_id_falls_back_to_source_and_title():
    job = Job(title="Test Job", source="Test Source", url="https://test.com")
    assert job.id == "Test Source::Test Job"
