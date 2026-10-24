import logging
from pathlib import Path

from hirewatch.config import load_sources
from hirewatch.differ import new_jobs
from hirewatch.fetcher import fetch
from hirewatch.llm import LlmClient
from hirewatch.models import LlmConfig, SmtpConfig
from hirewatch.notify import notify
from hirewatch.parser import parse
from hirewatch.store import Store

log = logging.getLogger(__name__)


def run_once(config: SmtpConfig, store_path: Path | str, sources_dir: Path | str) -> None:
    """Run one watch cycle: crawl all sources, notify about new jobs, persist state.

    Each source is crawled in isolation so one failing source does not abort the
    others. Jobs are marked as seen only after the notification is sent, so a
    failed send never silently drops a job (worst case: a duplicate next run).

    Args:
        config: SMTP configuration for sending the notification.
    """
    store = Store(store_path)
    all_new = []

    sources = load_sources(sources_dir)

    if any(s.type == "ai" or s.criterion for s in sources):
        llmclient = LlmClient(LlmConfig())
    else:
        llmclient = None

    for source in sources:
        try:
            raw = fetch(source.url)
            if source.type == "ai":
                jobs = llmclient.extract(source, raw)
            else:
                jobs = parse(source, raw)
            if source.criterion:
                jobs = llmclient.filter_jobs(jobs, source.criterion)
            new = new_jobs(jobs, store)
            all_new.extend(new)
            log.info("source %s: %d parsed, %d new", source.title, len(jobs), len(new))
        except Exception as e:
            log.error("source %s failed: %s", source.title, e)
    try:
        notify(all_new, config)
    except Exception as e:
        # don't mark jobs seen, so the next run retries them
        log.error("notify failed, will retry next run: %s", e)
        return
    for job in all_new:
        store.mark(job.id)
    store.save()
