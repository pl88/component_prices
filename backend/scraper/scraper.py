from __future__ import annotations

import logging
import re
from dataclasses import dataclass
from datetime import UTC, datetime
from decimal import Decimal, InvalidOperation
from typing import Protocol, cast

import httpx
from bs4 import BeautifulSoup
from sqlalchemy import Select, select
from sqlalchemy.dialects.postgresql import insert as pg_insert
from sqlalchemy.dialects.sqlite import insert as sqlite_insert
from sqlalchemy.engine import Dialect
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from sqlalchemy.sql.dml import Insert

from backend.config import Settings
from backend.db.models import ComponentShopURL, PriceSnapshot

logger = logging.getLogger(__name__)
PRICE_PATTERN = re.compile(r"([0-9][0-9 \u00a0]*[,.][0-9]{2})\s*z[łl]", re.IGNORECASE)
CATEGORY_MIN_PRICE: dict[str, Decimal] = {
    "CPU": Decimal("500"),
    "GPU": Decimal("1000"),
}
PRICE_SELECTORS = (
    "[data-name='ProductPrice']",
    "[data-price]",
    ".sc-2rx2l6-2",
    ".price",
)


@dataclass(slots=True)
class ScrapeSummary:
    total: int
    inserted: int
    skipped: int
    failed: int


class HttpClient(Protocol):
    def get(
        self,
        url: str,
        *,
        headers: dict[str, str],
        timeout: float,
    ) -> httpx.Response: ...


def parse_price_pln(html: str, min_price: Decimal | None = None) -> Decimal:
    soup = BeautifulSoup(html, "lxml")

    for selector in PRICE_SELECTORS:
        for element in soup.select(selector):
            text = element.get_text(" ", strip=True)
            parsed = _extract_price(text, min_price)
            if parsed is not None:
                return parsed

    text = soup.get_text(" ", strip=True)
    parsed = _extract_price(text, min_price)
    if parsed is None:
        msg = "Unable to locate a valid price in HTML content."
        raise ValueError(msg)
    return parsed


def _extract_price(text: str, min_price: Decimal | None = None) -> Decimal | None:
    for match in PRICE_PATTERN.finditer(text):
        normalized = match.group(1).replace(" ", "").replace("\u00a0", "").replace(",", ".")
        try:
            value = Decimal(normalized).quantize(Decimal("0.01"))
        except InvalidOperation:
            continue
        if min_price is None or value >= min_price:
            return value
    return None


def _target_query() -> Select[tuple[ComponentShopURL]]:
    return select(ComponentShopURL).where(ComponentShopURL.active.is_(True))


def _insert_stmt(
    *,
    dialect: Dialect,
    component_shop_url_id: int,
    price_pln: Decimal,
    scraped_at: datetime,
) -> Insert:
    payload = {
        "component_shop_url_id": component_shop_url_id,
        "price_pln": price_pln,
        "currency": "PLN",
        "scraped_at": scraped_at,
        "date": scraped_at.date(),
    }
    index_elements = ["component_shop_url_id", "date"]

    if dialect.name == "postgresql":
        return (
            pg_insert(PriceSnapshot)
            .values(**payload)
            .on_conflict_do_nothing(index_elements=index_elements)
        )

    if dialect.name == "sqlite":
        return (
            sqlite_insert(PriceSnapshot)
            .values(**payload)
            .on_conflict_do_nothing(index_elements=index_elements)
        )

    msg = f"Unsupported SQL dialect for idempotent insert: {dialect.name}"
    raise RuntimeError(msg)


def scrape_once(
    *,
    session: Session,
    settings: Settings,
    client: HttpClient,
    scraped_at: datetime | None = None,
) -> ScrapeSummary:
    scrape_time = scraped_at or datetime.now(tz=UTC)
    targets = session.scalars(_target_query()).all()
    inserted = 0
    skipped = 0
    failed = 0
    headers = {"User-Agent": settings.user_agent}

    for target in targets:
        try:
            response = client.get(
                target.product_url,
                headers=headers,
                timeout=settings.http_timeout_seconds,
            )
            response.raise_for_status()
            category = target.component.category.upper()
            min_price = CATEGORY_MIN_PRICE.get(category)
            price = parse_price_pln(response.text, min_price)
            stmt = _insert_stmt(
                dialect=session.get_bind().dialect,
                component_shop_url_id=cast(int, target.id),
                price_pln=price,
                scraped_at=scrape_time,
            )
            result = session.execute(stmt)
            session.commit()
            if result.rowcount == 1:
                inserted += 1
                logger.info("Inserted price %.2f PLN for %s", price, target.product_url)
            else:
                skipped += 1
                logger.info("Skipped (already exists today) %s", target.product_url)
        except SQLAlchemyError:
            session.rollback()
            failed += 1
            logger.exception("DB error for %s", target.product_url)
        except Exception:
            failed += 1
            logger.exception("Failed to scrape %s", target.product_url)

    return ScrapeSummary(
        total=len(targets),
        inserted=inserted,
        skipped=skipped,
        failed=failed,
    )
