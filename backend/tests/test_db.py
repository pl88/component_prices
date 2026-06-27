from datetime import UTC, datetime
from decimal import Decimal

import httpx
from sqlalchemy import select
from sqlalchemy.orm import Session

from backend.config import Settings
from backend.db.models import ComponentShopURL, PriceSnapshot
from backend.scraper.scraper import scrape_once


def test_daily_snapshot_insert_is_idempotent(
    session: Session,
    seeded_target: ComponentShopURL,
) -> None:
    class DummyClient:
        @staticmethod
        def get(
            url: str,
            *,
            headers: dict[str, str],
            timeout: float,
        ) -> httpx.Response:
            del headers, timeout
            return httpx.Response(
                200,
                request=httpx.Request("GET", url),
                text='<span data-name="ProductPrice">2 199,99 zł</span>',
            )

    settings = Settings()
    now = datetime(2026, 1, 1, 9, 0, tzinfo=UTC)

    assert seeded_target.active is True
    first = scrape_once(session=session, settings=settings, client=DummyClient(), scraped_at=now)
    second = scrape_once(session=session, settings=settings, client=DummyClient(), scraped_at=now)

    rows = session.scalars(select(PriceSnapshot)).all()
    assert first.inserted == 1
    assert second.skipped == 1
    assert len(rows) == 1
    assert rows[0].price_pln == Decimal("2199.99")
