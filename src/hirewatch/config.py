from pathlib import Path

import yaml

from hirewatch.models.source import Source


def load_source(path: str | Path) -> Source:
    with open(path) as f:
        data = yaml.safe_load(f)
    return Source(**data)
