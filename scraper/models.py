from datetime import UTC, date, datetime
from decimal import Decimal

from sqlalchemy import (
    BIGINT,
    BOOLEAN,
    CHAR,
    DATE,
    DECIMAL,
    TIMESTAMP,
    ForeignKey,
    Integer,
    String,
    Text,
    UniqueConstraint,
    func,
)
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


def utc_now() -> datetime:
    return datetime.now(UTC)


class Base(DeclarativeBase):
    pass


class Shop(Base):
    __tablename__ = "shops"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)
    base_url: Mapped[str] = mapped_column(Text, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True), nullable=False, server_default=func.now()
    )

    component_urls: Mapped[list[ComponentShopURL]] = relationship(back_populates="shop")


class Component(Base):
    __tablename__ = "components"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)
    category: Mapped[str] = mapped_column(String(100), nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True), nullable=False, server_default=func.now()
    )

    shop_urls: Mapped[list[ComponentShopURL]] = relationship(back_populates="component")


class ComponentShopURL(Base):
    __tablename__ = "component_shop_urls"
    __table_args__ = (UniqueConstraint("component_id", "shop_id", name="uq_component_shop"),)

    id: Mapped[int] = mapped_column(primary_key=True)
    component_id: Mapped[int] = mapped_column(ForeignKey("components.id"), nullable=False)
    shop_id: Mapped[int] = mapped_column(ForeignKey("shops.id"), nullable=False)
    product_url: Mapped[str] = mapped_column(Text, nullable=False)
    active: Mapped[bool] = mapped_column(
        BOOLEAN, nullable=False, default=True, server_default="true"
    )

    component: Mapped[Component] = relationship(back_populates="shop_urls")
    shop: Mapped[Shop] = relationship(back_populates="component_urls")
    snapshots: Mapped[list[PriceSnapshot]] = relationship(back_populates="component_shop_url")


class PriceSnapshot(Base):
    __tablename__ = "price_snapshots"
    __table_args__ = (
        UniqueConstraint("component_shop_url_id", "date", name="uq_component_shop_url_day"),
    )

    id: Mapped[int] = mapped_column(
        BIGINT().with_variant(Integer, "sqlite"),
        primary_key=True,
        autoincrement=True,
    )
    component_shop_url_id: Mapped[int] = mapped_column(
        ForeignKey("component_shop_urls.id"), nullable=False
    )
    price_pln: Mapped[Decimal] = mapped_column(DECIMAL(10, 2), nullable=False)
    currency: Mapped[str] = mapped_column(
        CHAR(3), nullable=False, default="PLN", server_default="PLN"
    )
    scraped_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True), nullable=False, default=utc_now
    )
    date: Mapped[date] = mapped_column(DATE, nullable=False)

    component_shop_url: Mapped[ComponentShopURL] = relationship(back_populates="snapshots")
