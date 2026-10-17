from urllib.parse import urljoin

from selectolax.lexbor import LexborHTMLParser

from hirewatch.models import Job, Source

REQUIRED = {"title", "url"}


def parse_css(content: str, source: Source) -> list[Job]:
    """Parse HTML content using CSS selectors

    Args:
        content (str): HTML content
        source (Source): Source which provided the content

    Returns:
        list[Job]: List of Jobs
    """

    field_map = source.field_map
    base = str(source.url)

    tree = LexborHTMLParser(content)
    jobs = []

    for card in tree.css(source.item_selector):
        data = {}
        for job_field, locator in field_map.items():
            # "sel" -> element text, "sel@attr" -> attribute, "@attr" -> the card itself
            sel, _, attr = locator.partition("@")
            node = card if sel == "" else card.css_first(sel)
            if node is None:
                continue
            value = node.attributes.get(attr) if attr else node.text(strip=True)
            if value:
                data[job_field] = value

        # skip job if missing required arguments, no logging for now
        if not REQUIRED <= data.keys():
            continue

        # resolve relative hrefs against the listing url
        data["url"] = urljoin(base, data["url"])

        jobs.append(Job(source=source.title, **data))

    return jobs
