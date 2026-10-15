from pydantic import BaseModel, HttpUrl


class Job(BaseModel):
    """A single job posting."""

    external_id: str | None = None
    title: str
    company: str | None = None
    location: str | None = None
    published: str | None = None
    description: str | None = None
    source: str
    url: HttpUrl

    @property
    def id(self) -> str:
        return self.external_id or f"{self.source}::{self.title}"
