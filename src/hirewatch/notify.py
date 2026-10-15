import smtplib
from email.message import EmailMessage
from pathlib import Path

from jinja2 import Environment, FileSystemLoader, select_autoescape

from hirewatch.models import Job, SmtpConfig

_env = Environment(
    loader=FileSystemLoader(Path(__file__).parent / "templates"),
    autoescape=select_autoescape(["html"]),
)


def _render(jobs: list[Job]) -> tuple[str, str]:
    html = _env.get_template("email.html.j2").render(jobs=jobs)
    text = "\n\n".join(f"{j.title}\n{j.url}" for j in jobs)
    return text, html


def notify(jobs: list[Job], config: SmtpConfig) -> None:
    """
    Send email notification about new jobs.

    Args:
        jobs (list[Jobs]): list of jobs to notify about
        config (SmtpConfig): SMTP configuration
    """
    if not jobs:
        return
    text, html = _render(jobs)

    msg = EmailMessage()
    msg["Subject"] = f"hirewatch: {len(jobs)} new jobs"
    msg["From"] = config.mail_from
    msg["To"] = config.mail_to
    msg.set_content(text)
    msg.add_alternative(html, subtype="html")

    with smtplib.SMTP(config.smtp_host, config.smtp_port) as s:
        s.starttls()
        s.login(config.smtp_user, config.smtp_pass)
        s.send_message(msg)
