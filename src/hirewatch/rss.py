from xml.etree import ElementTree as ET

import httpx
from pydantic import HttpUrl

from hirewatch.models.job import Job


def fetch(url: HttpUrl) -> str:
    """Fetch RSS Feed
    Args:
        url (HttpUrl): RSS Feed URL

    Returns:
        str: RSS Content
    """

    headers = {"User-Agent": "hirewatch/0.1 (+https://github.com/GrafBunsen/hirewatch)"}
    return httpx.get(str(url), headers=headers, timeout=15, follow_redirects=True).text


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
        guid = item.find(field_map["external_id"]).text
        title = item.find(field_map["title"]).text
        company = item.find(field_map["company"], namespaces).text
        location = item.find(field_map["location"], namespaces).text
        published = item.find(field_map["published"]).text
        description = item.find(field_map["description"]).text
        url = item.find(field_map["url"]).text

        job = Job(
            external_id=guid,
            title=title,
            company=company,
            location=location,
            published=published,
            description=description,
            source=source,
            url=url,
        )

        jobs.append(job)

    return jobs
