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
