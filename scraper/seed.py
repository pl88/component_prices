from sqlalchemy import select
from sqlalchemy.orm import Session

from scraper.models import Component, ComponentShopURL, Shop

MVP_SHOP_NAME = "x-kom"
MVP_SHOP_URL = "https://www.x-kom.pl"
MVP_COMPONENT_NAME = "Gigabyte Radeon RX 9060 XT Gaming OC 16GB GDDR6"
MVP_COMPONENT_CATEGORY = "GPU"
MVP_PRODUCT_URL = (
    "https://www.x-kom.pl/p/1339802-karta-graficzna-amd-gigabyte-radeon-rx-9060-xt-gaming-oc-16gb-"
    "gddr6.html"
)


def seed_mvp_data(session: Session) -> None:
    shop = session.scalar(select(Shop).where(Shop.name == MVP_SHOP_NAME))
    if shop is None:
        shop = Shop(name=MVP_SHOP_NAME, base_url=MVP_SHOP_URL)
        session.add(shop)
        session.flush()

    component = session.scalar(select(Component).where(Component.name == MVP_COMPONENT_NAME))
    if component is None:
        component = Component(name=MVP_COMPONENT_NAME, category=MVP_COMPONENT_CATEGORY)
        session.add(component)
        session.flush()

    mapping = session.scalar(
        select(ComponentShopURL).where(
            ComponentShopURL.component_id == component.id,
            ComponentShopURL.shop_id == shop.id,
        )
    )
    if mapping is None:
        session.add(
            ComponentShopURL(
                component_id=component.id,
                shop_id=shop.id,
                product_url=MVP_PRODUCT_URL,
                active=True,
            )
        )

    session.commit()
