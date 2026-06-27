"""initial schema

Revision ID: 20260620_000001
Revises:
Create Date: 2026-06-20 16:30:00.000000
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "20260620_000001"
down_revision: str | None = None
branch_labels: Sequence[str] | None = None
depends_on: Sequence[str] | None = None


def upgrade() -> None:
    op.create_table(
        "shops",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column("base_url", sa.Text(), nullable=False),
        sa.Column(
            "created_at",
            sa.TIMESTAMP(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("name"),
    )
    op.create_table(
        "components",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column("category", sa.String(length=100), nullable=False),
        sa.Column(
            "created_at",
            sa.TIMESTAMP(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("name"),
    )
    op.create_table(
        "component_shop_urls",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("component_id", sa.Integer(), nullable=False),
        sa.Column("shop_id", sa.Integer(), nullable=False),
        sa.Column("product_url", sa.Text(), nullable=False),
        sa.Column("active", sa.Boolean(), server_default=sa.text("true"), nullable=False),
        sa.ForeignKeyConstraint(["component_id"], ["components.id"]),
        sa.ForeignKeyConstraint(["shop_id"], ["shops.id"]),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("component_id", "shop_id", name="uq_component_shop"),
    )
    op.create_table(
        "price_snapshots",
        sa.Column("id", sa.BigInteger(), autoincrement=True, nullable=False),
        sa.Column("component_shop_url_id", sa.Integer(), nullable=False),
        sa.Column("price_pln", sa.DECIMAL(precision=10, scale=2), nullable=False),
        sa.Column("currency", sa.CHAR(length=3), server_default=sa.text("'PLN'"), nullable=False),
        sa.Column("scraped_at", sa.TIMESTAMP(timezone=True), nullable=False),
        sa.Column("date", sa.DATE(), nullable=False),
        sa.ForeignKeyConstraint(["component_shop_url_id"], ["component_shop_urls.id"]),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("component_shop_url_id", "date", name="uq_component_shop_url_day"),
    )


def downgrade() -> None:
    op.drop_table("price_snapshots")
    op.drop_table("component_shop_urls")
    op.drop_table("components")
    op.drop_table("shops")
