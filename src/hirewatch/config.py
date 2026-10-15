import logging
from pathlib import Path

import yaml

from hirewatch.models import Source

log = logging.getLogger(__name__)


def load_source(path: str | Path) -> Source:
    """Load YAML of a single source.

    Args:
        path: Path to the source config file

    Returns:
        Source: The source configuration
    """
    with open(path) as f:
        data = yaml.safe_load(f)
    return Source(**data)


def load_sources(directory: str | Path = "sources") -> list[Source]:
    """Load all source configs from a directory.

    Args:
        directory: Directory containing source config files

    Returns:
        list[Source]: List of source configurations
    """
    sources = []
    for path in sorted(Path(directory).glob("*.yaml")):
        try:
            sources.append(load_source(path))
        except Exception as e:
            log.error("skipping broken source config %s: %s", path, e)
    return sources
