from datetime import UTC, datetime

import httpx
from sqlalchemy import select
from sqlalchemy.orm import Session

from scraper.config import Settings
from scraper.models import ComponentShopURL, PriceSnapshot
from scraper.scraper import scrape_once


def test_end_to_end_scrape_flow(session: Session, seeded_target: ComponentShopURL) -> None:
    assert seeded_target.active is True
    transport = httpx.MockTransport(
        lambda request: httpx.Response(
            200,
            request=request,
            text="<html><body><div data-name='ProductPrice'>2 349,00 zł</div></body></html>",
        )
    )
    with httpx.Client(transport=transport) as client:
        summary = scrape_once(
            session=session,
            settings=Settings(),
            client=client,
            scraped_at=datetime(2026, 1, 2, 9, 0, tzinfo=UTC),
        )

    snapshots = session.scalars(select(PriceSnapshot)).all()
    assert summary.total == 1
    assert summary.inserted == 1
    assert len(snapshots) == 1
