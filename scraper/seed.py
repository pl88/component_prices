from sqlalchemy import select
from sqlalchemy.orm import Session

from scraper.models import Component, ComponentShopURL, Shop

MVP_SHOP_NAME = "x-kom"
MVP_SHOP_URL = "https://www.x-kom.pl"
MVP_COMPONENTS = (
    (
        "Gigabyte Radeon RX 9060 XT Gaming OC 16GB GDDR6",
        "GPU",
        "https://www.x-kom.pl/p/1339802-karta-graficzna-amd-gigabyte-radeon-rx-9060-xt-gaming-oc-"
        "16gb-gddr6.html",
    ),
    (
        "AMD Ryzen 9 5950X",
        "CPU",
        "https://www.x-kom.pl/p/597434-procesor-amd-ryzen-9-amd-ryzen-9-5950x.html",
    ),
)


def seed_mvp_data(session: Session) -> None:
    shop = session.scalar(select(Shop).where(Shop.name == MVP_SHOP_NAME))
    if shop is None:
        shop = Shop(name=MVP_SHOP_NAME, base_url=MVP_SHOP_URL)
        session.add(shop)
        session.flush()

    for component_name, component_category, product_url in MVP_COMPONENTS:
        component = session.scalar(select(Component).where(Component.name == component_name))
        if component is None:
            component = Component(name=component_name, category=component_category)
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
                    product_url=product_url,
                    active=True,
                )
            )

    session.commit()
