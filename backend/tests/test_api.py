from datetime import UTC, date, datetime
from decimal import Decimal
from typing import Any, cast

from fastapi.testclient import TestClient
from httpx import Response
from sqlmodel import Session

from backend.api.app import app
from backend.db.models import ComponentShopURL, PriceSnapshot
from backend.db.session import get_session


def test_get_component_by_name_returns_latest_price(
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
            scraped_at=datetime(2026, 6, 26, 9, 0, tzinfo=UTC),
            date=date(2026, 6, 26),
        )
    )
    session.add(
        PriceSnapshot(
            component_shop_url_id=target_id,
            price_pln=Decimal("2099.00"),
            currency="PLN",
            scraped_at=datetime(2026, 6, 27, 9, 0, tzinfo=UTC),
            date=date(2026, 6, 27),
        )
    )
    session.commit()

    app.dependency_overrides[get_session] = lambda: session
    try:
        with TestClient(app) as client:
            client_any: Any = client
            response: Response = cast(
                Response,
                client_any.get(
                    "/api/v1/components/Gigabyte Radeon RX 9060 XT Gaming OC 16GB GDDR6"
                ),
            )
    finally:
        app.dependency_overrides.clear()

    assert response.status_code == 200
    payload = cast(dict[str, Any], response.json())
    assert payload["name"] == "Gigabyte Radeon RX 9060 XT Gaming OC 16GB GDDR6"
    assert payload["category"] == "GPU"
    assert payload["latest_prices"] == [
        {
            "shop": "x-kom",
            "price_pln": "2099.00",
            "currency": "PLN",
            "date": "2026-06-27",
        }
    ]


def test_get_component_by_name_returns_404(session: Session) -> None:
    app.dependency_overrides[get_session] = lambda: session
    try:
        with TestClient(app) as client:
            client_any: Any = client
            response: Response = cast(Response, client_any.get("/api/v1/components/not-found"))
    finally:
        app.dependency_overrides.clear()

    assert response.status_code == 404
