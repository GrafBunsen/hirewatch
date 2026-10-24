# ---- Stage 1: build ----
FROM ghcr.io/astral-sh/uv:python3.14-bookworm-slim AS build

WORKDIR /app

COPY pyproject.toml uv.lock ./
RUN uv sync --locked --no-install-project --no-dev

COPY . .
RUN uv sync --locked --no-dev

# ---- Stage 2: runtime ----
FROM python:3.14-slim-bookworm

RUN useradd --create-home app
USER app
WORKDIR /app

COPY --from=build --chown=app:app /app /app

ENV PATH="/app/.venv/bin:$PATH"

ENTRYPOINT ["hirewatch"]
