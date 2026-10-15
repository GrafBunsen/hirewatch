import json
from pathlib import Path


class Store:
    """Tracks jobs in a JSON File"""

    def __init__(self, path: str | Path):
        self.path = Path(path)
        self._ids: set[str] = set()
        if self.path.exists():
            self._ids = set(json.loads(self.path.read_text()))

    def seen(self, job_id: str) -> bool:
        return job_id in self._ids

    def mark(self, job_id: str) -> None:
        self._ids.add(job_id)

    def save(self) -> None:
        self.path.write_text(json.dumps(sorted(self._ids), indent=2))
