# hirewatch

Watch job listings on the sites you care about and get an email when new jobs
appear. Point it at RSS feeds or plain HTML pages, optionally let a local LLM
extract jobs from messy pages and filter them by a plain-language rule, and run
it once a day in Docker. Named after *Firewatch*.

- **Sources you define** — RSS feeds, static HTML (CSS selectors), or LLM
  extraction for pages with no usable structure.
- **Only new jobs** — hirewatch remembers what it has seen and mails you the
  difference, not the whole list.
- **Optional LLM filter** — keep only the jobs matching a sentence you write
  ("only permanent roles in Berlin, no internships"). Works on any source type.
- **One email per run** — a single digest, sent via your own SMTP account.

## Quick start (Docker)

```bash
# 1. configuration
cp .env.example .env            # then edit: SMTP credentials, recipient, LLM (optional)

# 2. your sources
mkdir -p data/sources
cp docs/examples/*.yaml data/sources/   # start from the examples, then edit

# 3. run
docker compose up --build
```

On the first run every matching job counts as new, so expect a full digest. From
then on you only get new ones. By default the container keeps running and checks
once a day at 08:00; see [docs/deployment.md](docs/deployment.md) to change the
schedule or run it as a one-shot.

State (which jobs have been seen) and your source configs live in `./data`, so
they survive restarts and are easy to back up — one folder is your whole state.

## Running without Docker

hirewatch is a normal Python package managed with [uv](https://docs.astral.sh/uv/):

```bash
uv sync
cp .env.example .env            # edit it
mkdir -p sources                # drop your *.yaml source configs here
uv run hirewatch
```

Set `HIREWATCH_LOOP=false` for a single run (then exit), e.g. to drive it from
cron or a systemd timer instead of the built-in daily loop.

## Configuration

All configuration is environment variables, read from `.env`. Start from
[.env.example](.env.example). Full reference:
[docs/configuration.md](docs/configuration.md).

The essentials:

| Variable | Purpose |
|---|---|
| `SMTP_HOST`, `SMTP_USER`, `SMTP_PASS` | your outgoing mail account |
| `MAIL_FROM`, `MAIL_TO` | sender and recipient of the digest |
| `LLM_URL`, `LLM_MODEL` | OpenAI-compatible LLM endpoint (only if you use `ai` sources or a `criterion`) |

## Defining sources

Each source is one YAML file in your sources directory. There are three types —
`rss`, `css`, and `ai` — and any of them can carry an optional natural-language
`criterion` to filter the results. Full guide with examples for each type:
[docs/sources.md](docs/sources.md).

## Multiple users on one host

Want to run it for a few friends from the same install? Each person gets their
own sources, state, and recipient via a second compose service — no code changes.
See [docs/deployment.md](docs/deployment.md#multiple-users).

## Development

```bash
uv sync
uv run pytest
uv run ruff check .
```

CI runs lint, format check, and tests on every push. Tagging a release
(`vX.Y.Z`) builds and publishes a multi-arch image to GHCR.

## A note on authorship

The code in this repository is written by hand. The documentation (this README
and the files under `docs/`) was written with AI assistance.
