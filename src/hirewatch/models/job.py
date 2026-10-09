from datetime import date

from pydantic import BaseModel, Field, HttpUrl


class Job(BaseModel):
    """A single job posting.

    Dedup via title + source.
    """

    title: str
    source: str
    first_seen: date = Field(default_factory=date.today)
    url: HttpUrl
    published: str | None = None
    company: str | None = None
    location: str | None = None
    description: str | None = None
