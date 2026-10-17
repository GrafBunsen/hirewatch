import pytest

from hirewatch.models import Source
from hirewatch.parser import parse


def _source(type_: str) -> Source:
    return Source(
        title="Test Source",
        url="https://test.com",
        type=type_,
        field_map={"title": "title", "url": "link"},
    )


def test_dispatch_unregistered_type():
    with pytest.raises(ValueError, match="no parser registered"):
        parse(_source("ai"), "")


def test_dispatch_routes_to_rss():
    content = (
        '<?xml version="1.0"?><rss><channel>'
        "<item><title>Test Job</title><link>https://test.com/1</link></item>"
        "</channel></rss>"
    )
    jobs = parse(_source("rss"), content)
    assert len(jobs) == 1
    assert jobs[0].title == "Test Job"
