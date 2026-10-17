import httpx
from pydantic import HttpUrl


def fetch(url: HttpUrl) -> str:
    """Fetch static HTML site
    Args:
        url (HttpUrl): RSS Feed URL

    Returns:
        str: RSS Content
    """

    headers = {"User-Agent": "hirewatch/0.1 (+https://github.com/GrafBunsen/hirewatch)"}
    response = httpx.get(str(url), headers=headers, timeout=15, follow_redirects=True)
    response.raise_for_status()
    return response.text
