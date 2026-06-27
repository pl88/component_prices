from datetime import UTC, date, datetime
from decimal import Decimal

from sqlmodel import Session

from backend.db.models import ComponentShopURL, PriceSnapshot
from backend.db.repositories.component import ComponentRepository


def test_repository_returns_component_and_latest_price(
    session: Session,
    seeded_target: ComponentShopURL,
) -> None:
    assert seeded_target.id is not None
    target_id = seeded_target.id

    session.add(
        PriceSnapshot(
            component_shop_url_id=target_id,
            price_pln=Decimal("1999.00"),
            currency="PLN",
            scraped_at=datetime(2026, 6, 26, 8, 0, tzinfo=UTC),
            date=date(2026, 6, 26),
        )
    )
    session.add(
        PriceSnapshot(
            component_shop_url_id=target_id,
            price_pln=Decimal("2099.00"),
            currency="PLN",
            scraped_at=datetime(2026, 6, 27, 8, 0, tzinfo=UTC),
            date=date(2026, 6, 27),
        )
    )
    session.commit()

    repo = ComponentRepository(session)
    component = repo.get_by_name("Gigabyte Radeon RX 9060 XT Gaming OC 16GB GDDR6")

    assert component is not None
    assert component.id is not None
    rows = repo.get_latest_prices(component.id)
    assert len(rows) == 1
    assert rows[0].shop == "x-kom"
    assert rows[0].price_pln == Decimal("2099.00")
