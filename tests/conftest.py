from collections.abc import Generator

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from scraper.models import Base, Component, ComponentShopURL, Shop


@pytest.fixture()
def session() -> Generator[Session, None, None]:
    engine = create_engine("sqlite+pysqlite:///:memory:", future=True)
    Base.metadata.create_all(engine)
    session_factory = sessionmaker(bind=engine, expire_on_commit=False)
    with session_factory() as db_session:
        yield db_session
    engine.dispose()


@pytest.fixture()
def seeded_target(session: Session) -> ComponentShopURL:
    shop = Shop(name="x-kom", base_url="https://www.x-kom.pl")
    component = Component(name="Gigabyte Radeon RX 9060 XT Gaming OC 16GB GDDR6", category="GPU")
    session.add_all([shop, component])
    session.flush()
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
    return target
