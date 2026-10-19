import logging
from urllib.parse import urljoin

from openai import OpenAI
from pydantic import BaseModel
from selectolax.lexbor import LexborHTMLParser

from hirewatch.models import Job, LlmConfig, Source

log = logging.getLogger(__name__)


EXTRACT_PROMPT = (
    "Extract every job posting from the page content below. For each job return "
    "title, company, location and the url (taken from the <...> brackets after "
    "the link text). Ignore navigation, ads and anything that is not a job. "
    "Return only what the schema allows.\n\n"
)

FILTER_PROMPT = (
    "Below is a numbered list of job postings. For each one decide whether it "
    "matches this criterion: {criterion}\n"
    "Return every index with matches=true if it matches, else matches=false.\n\n"
)

_STRIP_TAGS = ("script", "style", "nav", "header", "footer", "noscript", "svg", "form")

_FILTER_DESC_CHARS = 300  # cap description per job in the filter list to avoid token explosion


def to_text(html: str) -> str:
    """Reduce an HTML page to LLM-friendly text

    Args:
        html: Raw HTML page content
    Returns:
        Text content of the page
    """
    tree = LexborHTMLParser(html)
    for sel in _STRIP_TAGS:
        for node in tree.css(sel):
            node.decompose()
    body = tree.css_first("body") or tree.root
    for a in body.css("a"):
        href = a.attributes.get("href") or ""
        text = a.text(strip=True)
        if href and text:
            a.replace_with(f"{text} <{href}>")
    lines = [ln.strip() for ln in body.text(separator="\n", strip=True).splitlines()]
    return "\n".join(ln for ln in lines if ln)


class LlmJob(BaseModel):
    title: str
    company: str | None = None
    location: str | None = None
    published: str | None = None
    description: str | None = None
    url: str


class LlmJobs(BaseModel):
    jobs: list[LlmJob]


class Verdict(BaseModel):
    index: int
    matches: bool


class Verdicts(BaseModel):
    verdicts: list[Verdict]


class LlmClient:
    config: LlmConfig

    def __init__(self, config: LlmConfig):
        api_key = config.api_key or "nokey"
        self.config = config
        self.client = OpenAI(base_url=str(config.url), api_key=api_key, timeout=180)

    def extract(self, source: Source, content: str) -> list[Job]:
        """
        Extract jobs from page content using an LLM

        Args:
            source: Source the content came from
            content: Raw HTML page content

        Returns:
            List of jobs found on the page

        """
        prompt = self.config.prompt_override or EXTRACT_PROMPT
        text = to_text(content)

        r = self.client.chat.completions.parse(
            model=self.config.model,
            messages=[{"role": "user", "content": prompt + text}],
            response_format=LlmJobs,
            reasoning_effort="none",
            temperature=0,
        )

        jobs = []
        for llmjob in r.choices[0].message.parsed.jobs:
            url = urljoin(str(source.url), llmjob.url)
            if not url.startswith(("http://", "https://")):  # drop mailto:/tel:/etc.
                log.warning("llm: dropped non-http url %s", llmjob.url)
                continue
            jobs.append(
                Job(
                    external_id=url,  # dedup by url: LLM titles drift, urls are stable
                    title=llmjob.title,
                    company=llmjob.company,
                    location=llmjob.location,
                    published=llmjob.published,
                    description=llmjob.description,
                    source=source.title,
                    url=url,
                )
            )
        return jobs

    def filter_jobs(self, jobs: list[Job], criterion: str) -> list[Job]:
        """Filter jobs using LLM classification

        Args:
            jobs: List of jobs to filter
            criterion: The filter text

        Returns:
            Filtered list of jobs

        """
        if not jobs:
            return []

        listing = "\n".join(
            f"[{i}] {j.title} | {j.company or '?'} | {j.location or '?'} | {(j.description or '?')[:_FILTER_DESC_CHARS]}"  # noqa: E501
            for i, j in enumerate(jobs)
        )

        r = self.client.chat.completions.parse(
            model=self.config.model,
            messages=[
                {"role": "user", "content": FILTER_PROMPT.format(criterion=criterion) + listing}
            ],
            response_format=Verdicts,
            temperature=0,
        )

        keep = {v.index for v in r.choices[0].message.parsed.verdicts if v.matches}
        result = [j for i, j in enumerate(jobs) if i in keep]
        log.info("filter: kept %d/%d (%s)", len(result), len(jobs), criterion)
        return result
