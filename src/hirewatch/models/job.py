from datetime import date

from pydantic import BaseModel, Field, HttpUrl


class Job(BaseModel):
    """A single job posting."""

    external_id: str | None = None
    title: str
    company: str | None = None
    location: str | None = None
    published: str | None = None
    first_seen: date = Field(default_factory=date.today)
    description: str | None = None
    source: str
    url: HttpUrl
