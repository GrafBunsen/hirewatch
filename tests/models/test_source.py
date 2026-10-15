import pytest
from pydantic import ValidationError

from hirewatch.models.source import Source


def test_field_map_key_validation():
    with pytest.raises(ValidationError, match="field_map missing required keys"):
        Source(title="test", url="http://test.com", field_map={"title": "title"})
