import pytest
from pydantic import ValidationError

from hirewatch.models import Source


def test_field_map_key_validation():
    with pytest.raises(ValidationError, match="field_map missing required keys"):
        Source(
            title="Test Source", url="https://test.com", field_map={"title": "title"}, type="rss"
        )


def test_css_requires_item_selector():
    with pytest.raises(ValidationError, match="css source requires item_selector"):
        Source(
            title="Test Source",
            url="https://test.com",
            type="css",
            field_map={"title": "h3", "url": "@href"},
        )


def test_ai_source_needs_no_field_map():
    src = Source(title="Test", url="https://test.com", type="ai", criterion="only Berlin")
    assert src.field_map is None


def test_rss_requires_field_map():
    with pytest.raises(ValidationError, match="requires field_map"):
        Source(title="Test", url="https://test.com", type="rss")
