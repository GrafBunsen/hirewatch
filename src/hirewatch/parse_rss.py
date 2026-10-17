from xml.etree import ElementTree as ET

from hirewatch.models import Job, Source

REQUIRED = {"title", "url"}


def parse_rss(content: str, source: Source) -> list[Job]:
    """Parse RSS Content

    Args:
        content (str): RSS Content
        source (Source): Source which provided the content

    Returns:
        list[Job]: List of Jobs
    """

    field_map = source.field_map
    namespaces = source.namespaces

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

        jobs.append(Job(source=source.title, **data))

    return jobs
