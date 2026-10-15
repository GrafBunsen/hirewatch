from hirewatch.models import Job
from hirewatch.store import Store


def new_jobs(jobs: list[Job], store: Store) -> list[Job]:
    return [job for job in jobs if not store.seen(job.id)]
