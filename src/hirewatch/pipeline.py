import logging

from hirewatch.config import load_sources
from hirewatch.differ import new_jobs
from hirewatch.models import SmtpConfig
from hirewatch.notify import notify
from hirewatch.rss import collect
from hirewatch.store import Store

log = logging.getLogger(__name__)


def run_once(config: SmtpConfig) -> None:
    """Run one watch cycle: crawl all sources, notify about new jobs, persist state.

    Each source is crawled in isolation so one failing source does not abort the
    others. Jobs are marked as seen only after the notification is sent, so a
    failed send never silently drops a job (worst case: a duplicate next run).

    Args:
        config: SMTP configuration for sending the notification.
    """
    store = Store("state.json")
    all_new = []
    for source in load_sources():
        try:
            jobs = collect(source)
            new = new_jobs(jobs, store)
            all_new.extend(new)
            log.info("source %s: %d parsed, %d new", source.title, len(jobs), len(new))
        except Exception as e:
            log.error("source %s failed: %s", source.title, e)
    notify(all_new, config)
    for job in all_new:
        store.mark(job.id)
    store.save()
