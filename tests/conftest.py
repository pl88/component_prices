from collections.abc import Generator
from datetime import UTC, datetime

import pytest
from sqlalchemy import create_engine
from sqlalchemy.pool import StaticPool
from sqlmodel import Session, SQLModel

from backend.api.services.auth import hash_password
from backend.db.models import Component, ComponentShopURL, Shop, User


@pytest.fixture()
def session() -> Generator[Session]:
    engine = create_engine(
        "sqlite+pysqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
        future=True,
    )
    SQLModel.metadata.create_all(engine)
    with Session(engine) as db_session:
        yield db_session
    engine.dispose()


@pytest.fixture()
def seeded_target(session: Session) -> ComponentShopURL:
    now = datetime.now(UTC)
    shop = Shop(name="x-kom", base_url="https://www.x-kom.pl", created_at=now)
    component = Component(
        name="Gigabyte Radeon RX 9060 XT Gaming OC 16GB GDDR6",
        category="GPU",
        created_at=now,
    )
    session.add(shop)
    session.add(component)
    session.commit()
    session.refresh(shop)
    session.refresh(component)
    assert shop.id is not None
    assert component.id is not None

    target = ComponentShopURL(
        component_id=component.id,
        shop_id=shop.id,
        product_url=(
            "https://www.x-kom.pl/p/1339802-karta-graficzna-amd-gigabyte-radeon-rx-9060-xt-"
            "gaming-oc-16gb-gddr6.html"
        ),
        active=True,
    )
    session.add(target)
    session.commit()
    session.refresh(target)
    return target


@pytest.fixture()
def test_user(session: Session) -> User:
    now = datetime.now(UTC)
    user = User(
        email="test",
        name="Test User",
        password_hash=hash_password("test"),
        is_active=True,
        created_at=now,
    )
    session.add(user)
    session.commit()
    session.refresh(user)
    return user
