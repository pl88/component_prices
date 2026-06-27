from backend.api.schemas import ComponentPriceResponse, PriceEntry
from backend.db.repositories.component import ComponentRepository


class ComponentQuery:
    """Read-side query handler (CQRS query side)."""

    def __init__(self, repository: ComponentRepository) -> None:
        self._repository = repository

    def get_component_latest_prices(self, name: str) -> ComponentPriceResponse | None:
        component = self._repository.get_by_name(name)
        if component is None:
            return None

        price_rows = self._repository.get_latest_prices(component.id)  # type: ignore[arg-type]
        return ComponentPriceResponse(
            name=component.name,
            category=component.category,
            latest_prices=[
                PriceEntry(
                    shop=row.shop,
                    price_pln=row.price_pln,
                    currency=row.currency,
                    date=row.date,
                )
                for row in price_rows
            ],
        )
