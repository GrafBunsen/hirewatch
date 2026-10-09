from datetime import date

import pytest
from pydantic import ValidationError

from hirewatch.models.job import Job


def test_first_seen_today():
    job = Job(title="Test", source="Test", url="http://test.com")

    assert job.first_seen == date.today()


def test_url_is_valid():
    with pytest.raises(ValidationError):
        Job(title="Test", source="Test", url="not a url")
