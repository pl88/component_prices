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
    test_user: Any,
) -> None:
    del test_user
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
            login_response: Response = cast(
                Response,
                client_any.post(
                    "/auth/login",
                    json={"email": "test", "password": "test"},
                ),
            )
            assert login_response.status_code == 200
            token = cast(dict[str, Any], login_response.json())["token"]
            response: Response = cast(
                Response,
                client_any.get(
                    "/api/v1/components/Gigabyte Radeon RX 9060 XT Gaming OC 16GB GDDR6",
                    headers={"Authorization": f"Bearer {token}"},
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


def test_get_component_by_name_returns_404(session: Session, test_user: Any) -> None:
    del test_user
    app.dependency_overrides[get_session] = lambda: session
    try:
        with TestClient(app) as client:
            client_any: Any = client
            login_response: Response = cast(
                Response,
                client_any.post(
                    "/auth/login",
                    json={"email": "test", "password": "test"},
                ),
            )
            assert login_response.status_code == 200
            token = cast(dict[str, Any], login_response.json())["token"]
            response: Response = cast(
                Response,
                client_any.get(
                    "/api/v1/components/not-found",
                    headers={"Authorization": f"Bearer {token}"},
                ),
            )
    finally:
        app.dependency_overrides.clear()

    assert response.status_code == 404


def test_components_endpoint_requires_auth(session: Session) -> None:
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

    assert response.status_code == 401


def test_login_success(session: Session, test_user: Any) -> None:
    del test_user
    app.dependency_overrides[get_session] = lambda: session
    try:
        with TestClient(app) as client:
            client_any: Any = client
            response: Response = cast(
                Response,
                client_any.post(
                    "/auth/login",
                    json={"email": "test", "password": "test"},
                ),
            )
    finally:
        app.dependency_overrides.clear()

    assert response.status_code == 200
    payload = cast(dict[str, Any], response.json())
    assert "token" in payload
    assert payload["user"] == {
        "id": "1",
        "email": "test",
        "name": "Test User",
    }


def test_login_invalid_credentials(session: Session, test_user: Any) -> None:
    del test_user
    app.dependency_overrides[get_session] = lambda: session
    try:
        with TestClient(app) as client:
            client_any: Any = client
            response: Response = cast(
                Response,
                client_any.post(
                    "/auth/login",
                    json={"email": "test", "password": "wrong"},
                ),
            )
    finally:
        app.dependency_overrides.clear()

    assert response.status_code == 401
