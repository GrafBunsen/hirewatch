from hirewatch.models import Job
from hirewatch.store import Store


def new_jobs(jobs: list[Job], store: Store) -> list[Job]:
    """Return jobs that have not been seen before.

    Args:
        jobs: A list of jobs to check.
        store: The store to check against.

    Returns:
        A list of jobs that have not been seen before.
    """
    return [job for job in jobs if not store.seen(job.id)]
