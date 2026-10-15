import logging
import time

import schedule

from hirewatch.models import AppConfig, SmtpConfig
from hirewatch.pipeline import run_once

log = logging.getLogger(__name__)


def main() -> None:
    """Entry point: run one watch cycle, then (unless HIREWATCH_LOOP=false) keep
    running it daily at the configured time."""

    logging.basicConfig(
        level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s: %(message)s"
    )
    app = AppConfig()
    smtp = SmtpConfig()

    run_once(smtp, app.state_path)

    if not app.loop:
        return

    log.info("scheduling daily run at %s", app.schedule_at)
    schedule.every().day.at(app.schedule_at).do(run_once, smtp, app.state_path)
    while True:
        schedule.run_pending()
        time.sleep(60)
