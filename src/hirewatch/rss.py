from xml.etree import ElementTree as ET

import httpx
from pydantic import HttpUrl

from hirewatch.models import Job, Source

REQUIRED = {"title", "url"}


def fetch(url: HttpUrl) -> str:
    """Fetch RSS Feed
    Args:
        url (HttpUrl): RSS Feed URL

    Returns:
        str: RSS Content
    """

    headers = {"User-Agent": "hirewatch/0.1 (+https://github.com/GrafBunsen/hirewatch)"}
    response = httpx.get(str(url), headers=headers, timeout=15, follow_redirects=True)
    response.raise_for_status()
    return response.text


def parse(
    content: str, source: str, field_map: dict[str, str], namespaces: dict[str, str]
) -> list[Job]:
    """Parse RSS Content

    Args:
        content (str): RSS Content
        source (str): Job Source
        field_map (dict[str, str]): Fieldmap to map RSS fields to Job fields
        namespaces (dict [str, str]): XML Namespaces

    Returns:
        list[Job]: List of Jobs
    """

    root = ET.fromstring(content)
    jobs = []

    for item in root.findall(".//item"):
        data = {}
        for job_field, rss_name in field_map.items():
            el = item.find(rss_name, namespaces)
            if el is not None:
                data[job_field] = el.text

        # skip job if missing required arguments, no logging for now
        if not REQUIRED <= data.keys():
            continue

        jobs.append(Job(source=source, **data))

    return jobs


def collect(source: Source) -> list[Job]:
    return parse(fetch(source.url), source.title, source.field_map, source.namespaces)
