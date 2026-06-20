FROM python:3.14-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

RUN pip install --no-cache-dir uv

COPY pyproject.toml uv.lock README.md alembic.ini /app/
COPY scraper /app/scraper
COPY migrations /app/migrations

RUN uv sync --frozen --extra dev

CMD ["uv", "run", "python", "-m", "scraper.main"]
