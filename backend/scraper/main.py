from __future__ import annotations

import logging
import time

import httpx
from alembic import command
from alembic.config import Config as AlembicConfig
from sqlalchemy import create_engine, text
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import sessionmaker

from backend.config import Settings, get_settings
from backend.scraper.scraper import scrape_once
from backend.scraper.seed import seed_mvp_data, seed_test_user

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s [%(name)s] %(message)s",
)
logger = logging.getLogger(__name__)


def wait_for_db(settings: Settings) -> None:
    delay = settings.db_ready_base_delay_seconds
    for attempt in range(1, settings.db_ready_attempts + 1):
        try:
            engine = create_engine(settings.database_url, future=True)
            with engine.connect() as connection:
                connection.execute(text("SELECT 1"))
            engine.dispose()
            return
        except SQLAlchemyError:
            if attempt == settings.db_ready_attempts:
                raise
            logger.warning(
                "Database not ready (attempt %s/%s)", attempt, settings.db_ready_attempts
            )
            time.sleep(delay)
            delay *= 2


def run_migrations(settings: Settings) -> None:
    config = AlembicConfig("alembic.ini")
    config.set_main_option("sqlalchemy.url", settings.database_url)
    command.upgrade(config, "head")


def main() -> int:
    settings = get_settings()
    wait_for_db(settings)
    run_migrations(settings)

    engine = create_engine(settings.database_url, future=True, pool_pre_ping=True)
    session_factory = sessionmaker(bind=engine, expire_on_commit=False)

    with session_factory() as session:
        seed_mvp_data(session)
        seed_test_user(session)

    with session_factory() as session, httpx.Client() as client:
        summary = scrape_once(session=session, settings=settings, client=client)

    logger.info(
        "Scrape summary: total=%s inserted=%s skipped=%s failed=%s",
        summary.total,
        summary.inserted,
        summary.skipped,
        summary.failed,
    )
    engine.dispose()
    return 0 if summary.failed == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
