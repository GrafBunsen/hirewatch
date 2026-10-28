# Configuration

hirewatch is configured entirely through environment variables, read from a
`.env` file in the working directory. Copy [`.env.example`](../.env.example) to
`.env` and fill it in.

Under Docker, `.env` is mounted into the container read-only and read by the app
itself (not through compose's `env_file`), so values are taken verbatim — a `$`
or other special character in a password is passed through unchanged.

## Mail (required)

The digest is sent over SMTP using your own account.

| Variable | Default | Meaning |
|---|---|---|
| `SMTP_HOST` | — | SMTP server hostname. |
| `SMTP_PORT` | `587` | SMTP port (STARTTLS). |
| `SMTP_USER` | — | Login user for the SMTP account. |
| `SMTP_PASS` | — | Login password. |
| `MAIL_FROM` | — | Sender address (usually your SMTP account). |
| `MAIL_TO` | — | Recipient of the digest. |

All of these except `SMTP_PORT` are required; the app refuses to start without
them.

## Scheduling and state

| Variable | Default | Meaning |
|---|---|---|
| `HIREWATCH_LOOP` | `true` | `true`: run once, then keep running daily. `false`: run once and exit. |
| `HIREWATCH_SCHEDULE_AT` | `08:00` | Daily run time (24h `HH:MM`) when looping. |
| `HIREWATCH_STATE_PATH` | `state.json` | Where the "seen jobs" state is stored. |
| `HIREWATCH_SOURCES_DIR` | `sources` | Directory of source `*.yaml` files. |

Under Docker these last two point into the mounted `./data` volume
(`/data/state.json`, `/data/sources`); the compose file sets that for you.

Running more than one instance? `HIREWATCH_SOURCES_DIR`, `HIREWATCH_STATE_PATH`,
and `HIREWATCH_SCHEDULE_AT` are the per-instance knobs — see
[deployment.md](deployment.md#multiple-users).

## LLM

Only needed if a source uses `type: ai` or carries a `criterion`. Any
OpenAI-compatible endpoint works (e.g. a local [Ollama](https://ollama.com/)
server via its `/v1` API).

| Variable | Default | Meaning |
|---|---|---|
| `LLM_URL` | — | Base URL of the OpenAI-compatible API. |
| `LLM_MODEL` | — | Model name to use. |
| `LLM_API_KEY` | `""` | API key, if the endpoint needs one. |
| `LLM_PROMPT_OVERRIDE` | — | Replace the default extraction prompt (advanced). |

For `ai` sources the backend must allow a large enough context window to hold a
full page of HTML; a model or server configured with a small context will
truncate the page and miss jobs.
