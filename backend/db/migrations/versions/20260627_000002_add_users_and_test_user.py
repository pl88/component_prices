"""add users table and test user

Revision ID: 20260627_000002
Revises: 20260620_000001
Create Date: 2026-06-27 12:00:00.000000
"""

import base64
import hashlib
import secrets
from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "20260627_000002"
down_revision: str | None = "20260620_000001"
branch_labels: Sequence[str] | None = None
depends_on: Sequence[str] | None = None


def _hash_password(password: str) -> str:
    iterations = 600_000
    salt = secrets.token_bytes(16)
    digest = hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt, iterations)
    return (
        f"pbkdf2_sha256${iterations}$"
        f"{base64.b64encode(salt).decode('ascii')}$"
        f"{base64.b64encode(digest).decode('ascii')}"
    )


def upgrade() -> None:
    op.create_table(
        "users",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("email", sa.String(length=255), nullable=False),
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column("password_hash", sa.Text(), nullable=False),
        sa.Column("is_active", sa.Boolean(), server_default=sa.text("true"), nullable=False),
        sa.Column(
            "created_at",
            sa.TIMESTAMP(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("email"),
    )
    op.create_index("ix_users_email", "users", ["email"], unique=True)

    password_hash = _hash_password("test")
    op.execute(
        sa.text(
            """
            INSERT INTO users (email, name, password_hash, is_active)
            VALUES (:email, :name, :password_hash, :is_active)
            ON CONFLICT (email) DO NOTHING
            """
        ).bindparams(
            email="test",
            name="Test User",
            password_hash=password_hash,
            is_active=True,
        )
    )


def downgrade() -> None:
    op.drop_index("ix_users_email", table_name="users")
    op.drop_table("users")
