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


class LoginRequest(SQLModel):
    email: str
    password: str


class AuthUserResponse(SQLModel):
    id: str
    email: str
    name: str


class LoginResponse(SQLModel):
    token: str
    user: AuthUserResponse


class LogoutResponse(SQLModel):
    detail: str
