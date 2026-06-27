from __future__ import annotations

import datetime
from decimal import Decimal

from sqlmodel import SQLModel


class PriceEntry(SQLModel):
    shop: str
    price_pln: Decimal
    currency: str
    date: datetime.date


class ComponentPriceResponse(SQLModel):
    name: str
    category: str
    latest_prices: list[PriceEntry]
