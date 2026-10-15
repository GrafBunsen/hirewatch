from hirewatch.differ import new_jobs
from hirewatch.models.job import Job
from hirewatch.store import Store


def test_new_job_empty_store(tmp_path):
    job = Job(title="Test Job", source="Test Source", url="https://test.com")
    store = Store(tmp_path / "state.json")

    assert new_jobs([job], store) == [job]


def test_new_job_existing_store(tmp_path):
    job1 = Job(title="Test Job", source="Test Source", url="https://test.com")
    job2 = Job(title="Test Job 2", source="Test Source 2", url="https://test.com/2")
    store = Store(tmp_path / "state.json")

    store.mark(job1.id)

    assert new_jobs([job1, job2], store) == [job2]
