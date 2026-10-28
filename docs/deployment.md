# Deployment

## Docker (recommended)

The bundled [`docker-compose.yml`](../docker-compose.yml) runs a single instance:

```bash
cp .env.example .env            # edit SMTP, recipient, LLM
mkdir -p data/sources
cp docs/examples/*.yaml data/sources/   # then edit for your sites
docker compose up --build
```

Everything the instance owns lives in `./data`:

- `data/sources/*.yaml` — your source configs (you create and edit these).
- `data/state.json` — which jobs have been seen (written by the app).

That single folder is your entire state: back it up and you have backed up
everything. `.env` is mounted read-only and holds your secrets; it is never
baked into the image.

The container runs the daily loop and restarts on failure (up to five times, so
a permanent misconfiguration stops instead of looping forever). Check it with:

```bash
docker compose ps        # is it up?
docker compose logs -f   # what is it doing / any errors
```

### Published image

Tagging a release (`vX.Y.Z`) publishes a multi-arch image to
`ghcr.io/grafbunsen/hirewatch`. To run that instead of building locally, replace
`build: .` in the compose file with:

```yaml
    image: ghcr.io/grafbunsen/hirewatch:latest
```

## Running one-shot (cron / systemd)

If you would rather schedule runs yourself, set `HIREWATCH_LOOP=false`. The app
then runs a single cycle and exits, which fits a host cron job or a
`systemd` timer. Without Docker:

```bash
HIREWATCH_LOOP=false uv run hirewatch
```

## Multiple users

hirewatch is single-user by design, but running it for a few people from one
host needs no code changes — just a second compose service using the same image
with its own data folder, recipient, and schedule.

Give each person their own `./data/<user>` directory (with their own `sources/`)
and their own `MAIL_TO`. The server-side settings (SMTP account, `MAIL_FROM`,
LLM) are shared.

```yaml
services:
  watch-alice:
    build: .
    environment:
      HIREWATCH_SOURCES_DIR: /data/sources
      HIREWATCH_STATE_PATH: /data/state.json
      HIREWATCH_SCHEDULE_AT: "08:00"
      MAIL_TO: alice@example.com
    volumes:
      - ./data/alice:/data
      - ./.env:/app/.env:ro       # shared SMTP + LLM settings
    restart: on-failure:5

  watch-bob:
    build: .
    environment:
      HIREWATCH_SOURCES_DIR: /data/sources
      HIREWATCH_STATE_PATH: /data/state.json
      HIREWATCH_SCHEDULE_AT: "08:30"   # stagger so runs don't overlap
      MAIL_TO: bob@example.com
    volumes:
      - ./data/bob:/data
      - ./.env:/app/.env:ro
    restart: on-failure:5
```

Note how the in-container paths (`/data/sources`, `/data/state.json`) are
identical for everyone — only the host side of the volume mount differs
(`./data/alice` vs `./data/bob`), which is what keeps each person's sources and
seen-state separate. `MAIL_TO` here overrides the one from `.env`.

Each instance is its own long-running process (a few tens of MB of RAM, almost
no CPU while idle), so a handful of users on one small host is no problem.
