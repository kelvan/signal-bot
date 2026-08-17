FROM python:3.12-slim

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

WORKDIR /app

COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-install-project --no-dev

COPY signal_bot ./signal_bot
RUN uv sync --frozen --no-dev

CMD ["uv", "run", "python", "-m", "signal_bot.bot"]
