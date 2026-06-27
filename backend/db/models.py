import datetime
from decimal import Decimal

import sqlalchemy as sa
from sqlmodel import Field, Relationship, SQLModel


class Shop(SQLModel, table=True):
    __tablename__ = "shops"

    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(sa_column=sa.Column(sa.String(255), nullable=False, unique=True))
    base_url: str = Field(sa_column=sa.Column(sa.Text, nullable=False))
    created_at: datetime.datetime = Field(
        sa_column=sa.Column(
            sa.TIMESTAMP(timezone=True),
            nullable=False,
            server_default=sa.func.now(),
        )
    )

    component_urls: list[ComponentShopURL] = Relationship(back_populates="shop")


class Component(SQLModel, table=True):
    __tablename__ = "components"

    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(sa_column=sa.Column(sa.String(255), nullable=False, unique=True))
    category: str = Field(sa_column=sa.Column(sa.String(100), nullable=False))
    created_at: datetime.datetime = Field(
        sa_column=sa.Column(
            sa.TIMESTAMP(timezone=True),
            nullable=False,
            server_default=sa.func.now(),
        )
    )

    shop_urls: list[ComponentShopURL] = Relationship(back_populates="component")


class ComponentShopURL(SQLModel, table=True):
    __tablename__ = "component_shop_urls"
    __table_args__ = (sa.UniqueConstraint("component_id", "shop_id", name="uq_component_shop"),)

    id: int | None = Field(default=None, primary_key=True)
    component_id: int = Field(foreign_key="components.id", nullable=False)
    shop_id: int = Field(foreign_key="shops.id", nullable=False)
    product_url: str = Field(sa_column=sa.Column(sa.Text, nullable=False))
    active: bool = Field(
        sa_column=sa.Column(sa.Boolean, nullable=False, default=True, server_default=sa.true())
    )

    component: Component | None = Relationship(back_populates="shop_urls")
    shop: Shop | None = Relationship(back_populates="component_urls")
    snapshots: list[PriceSnapshot] = Relationship(back_populates="component_shop_url")


class PriceSnapshot(SQLModel, table=True):
    __tablename__ = "price_snapshots"
    __table_args__ = (
        sa.UniqueConstraint("component_shop_url_id", "date", name="uq_component_shop_url_day"),
    )

    id: int | None = Field(
        default=None,
        sa_column=sa.Column(
            sa.BIGINT().with_variant(sa.Integer, "sqlite"),
            primary_key=True,
            autoincrement=True,
        ),
    )
    component_shop_url_id: int = Field(foreign_key="component_shop_urls.id", nullable=False)
    price_pln: Decimal = Field(sa_column=sa.Column(sa.DECIMAL(10, 2), nullable=False))
    currency: str = Field(
        sa_column=sa.Column(
            sa.CHAR(3), nullable=False, default="PLN", server_default=sa.text("'PLN'")
        )
    )
    scraped_at: datetime.datetime = Field(
        sa_column=sa.Column(sa.TIMESTAMP(timezone=True), nullable=False)
    )
    date: datetime.date = Field(sa_column=sa.Column(sa.DATE, nullable=False))

    component_shop_url: ComponentShopURL | None = Relationship(back_populates="snapshots")


class User(SQLModel, table=True):
    __tablename__ = "users"

    id: int | None = Field(default=None, primary_key=True)
    email: str = Field(sa_column=sa.Column(sa.String(255), nullable=False, unique=True, index=True))
    name: str = Field(sa_column=sa.Column(sa.String(255), nullable=False))
    password_hash: str = Field(sa_column=sa.Column(sa.Text, nullable=False))
    is_active: bool = Field(
        sa_column=sa.Column(sa.Boolean, nullable=False, default=True, server_default=sa.true())
    )
    created_at: datetime.datetime = Field(
        sa_column=sa.Column(
            sa.TIMESTAMP(timezone=True),
            nullable=False,
            server_default=sa.func.now(),
        )
    )
