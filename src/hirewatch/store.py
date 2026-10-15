import json
from pathlib import Path


class Store:
    """Tracks seen job IDs in a JSON file."""

    def __init__(self, path: str | Path):
        self.path = Path(path)
        self._ids: set[str] = set()
        if self.path.exists():
            self._ids = set(json.loads(self.path.read_text()))

    def seen(self, job_id: str) -> bool:
        """Return True if job has been seen before

        Args:
            job_id (str): The job id to check
        """
        return job_id in self._ids

    def mark(self, job_id: str) -> None:
        """Mark job as seen

        Args:
            job_id (str): The job id to mark
        """
        self._ids.add(job_id)

    def save(self) -> None:
        """Save the store to disk"""
        self.path.write_text(json.dumps(sorted(self._ids), indent=2))
