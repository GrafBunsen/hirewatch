from hirewatch.models import Job, Source
from hirewatch.parse_css import parse_css
from hirewatch.parse_rss import parse_rss

PARSERS = {
    "rss": parse_rss,
    "css": parse_css,
    # "ai": parse_ai,
}


def parse(source: Source, content: str) -> list[Job]:
    """Parse content using correct parser from source

    Args:
        source (Source): Source of content
        content (str): Content to parse

    Returns:
        list[Job]: List of jobs parsed
    """
    parser = PARSERS.get(source.type)
    if parser is None:
        raise ValueError(f"no parser registered for source type: {source.type!r} yet")
    return parser(content, source)
