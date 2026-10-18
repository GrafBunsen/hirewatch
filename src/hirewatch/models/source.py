from pydantic import BaseModel, HttpUrl, field_validator, model_validator

REQUIRED_FIELDS = {"title", "url"}


class Source(BaseModel):
    """A Source for Jobpostings. Loaded from config yaml."""

    title: str
    url: HttpUrl
    type: str
    field_map: dict[str, str] | None = None  # rss/css only
    namespaces: dict[str, str] | None = None  # rss only
    item_selector: str | None = None  # css only
    criterion: str | None = None

    @field_validator("type")
    @classmethod
    def _check_type(cls, v: str) -> str:
        if v not in {"rss", "css", "ai"}:
            raise ValueError(f"Unknown source type: {v}")
        return v

    @model_validator(mode="after")
    def _require_type_fields(self) -> Source:
        if self.type in {"rss", "css"}:
            if self.field_map is None:
                raise ValueError(f"{self.type} source requires field_map")
            missing = REQUIRED_FIELDS - self.field_map.keys()
            if missing:
                raise ValueError(f"field_map missing required keys: {sorted(missing)}")
        if self.type == "css" and self.item_selector is None:
            raise ValueError("css source requires item_selector")
        return self
