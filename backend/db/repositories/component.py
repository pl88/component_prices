from __future__ import annotations

import datetime
from decimal import Decimal
from typing import NamedTuple

import sqlalchemy as sa
from sqlalchemy import func
from sqlmodel import Session, select

from backend.db.models import Component, ComponentShopURL, PriceSnapshot, Shop


class LatestPriceRow(NamedTuple):
    shop: str
    price_pln: Decimal
    currency: str
    date: datetime.date


class ComponentRepository:
    def __init__(self, session: Session) -> None:
        self._session = session

    def get_by_name(self, name: str) -> Component | None:
        return self._session.exec(select(Component).where(Component.name == name)).first()

    def get_latest_prices(self, component_id: int) -> list[LatestPriceRow]:
        """Return the most recent price snapshot per shop for the given component."""
        latest_per_url = (
            select(
                PriceSnapshot.component_shop_url_id,
                func.max(PriceSnapshot.date).label("max_date"),
            )
            .join(ComponentShopURL, PriceSnapshot.component_shop_url_id == ComponentShopURL.id)
            .where(ComponentShopURL.component_id == component_id)
            .group_by(PriceSnapshot.component_shop_url_id)
            .subquery()
        )

        stmt = (
            select(
                Shop.name.label("shop"),
                PriceSnapshot.price_pln,
                PriceSnapshot.currency,
                PriceSnapshot.date,
            )
            .join(ComponentShopURL, PriceSnapshot.component_shop_url_id == ComponentShopURL.id)
            .join(Shop, ComponentShopURL.shop_id == Shop.id)
            .join(
                latest_per_url,
                sa.and_(
                    PriceSnapshot.component_shop_url_id == latest_per_url.c.component_shop_url_id,
                    PriceSnapshot.date == latest_per_url.c.max_date,
                ),
            )
            .where(ComponentShopURL.component_id == component_id)
            .order_by(Shop.name)
        )

        rows = self._session.execute(stmt).all()
        return [
            LatestPriceRow(
                shop=r.shop,
                price_pln=r.price_pln,
                currency=r.currency,
                date=r.date,
            )
            for r in rows
        ]
