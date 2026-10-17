from pydantic import BaseModel, HttpUrl, field_validator

REQUIRED_FIELDS = {"title", "url"}


class Source(BaseModel):
    """A Source for Jobpostings. Loaded from config yaml."""

    title: str
    url: HttpUrl
    type: str
    field_map: dict[str, str]
    namespaces: dict[str, str] | None = None

    @field_validator("field_map")
    @classmethod
    def _require_keys(cls, v: dict[str, str]) -> dict[str, str]:
        missing = REQUIRED_FIELDS - v.keys()
        if missing:
            raise ValueError(f"field_map missing required keys: {sorted(missing)}")
        return v

    @field_validator("type")
    @classmethod
    def _check_type(cls, v: str) -> str:
        if v not in {"rss", "css", "ai"}:
            raise ValueError(f"Unknown source type: {v}")
        return v
