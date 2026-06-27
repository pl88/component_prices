from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session

from backend.api.queries.component_query import ComponentQuery
from backend.api.schemas import ComponentPriceResponse
from backend.api.security import get_current_user
from backend.db.models import User
from backend.db.repositories.component import ComponentRepository
from backend.db.session import get_session

router = APIRouter(prefix="/api/v1", tags=["components"])


@router.get("/components/{name}", response_model=ComponentPriceResponse)
def get_component_by_name(
    name: str,
    session: Annotated[Session, Depends(get_session)],
    current_user: Annotated[User, Depends(get_current_user)],
) -> ComponentPriceResponse:
    del current_user
    query = ComponentQuery(ComponentRepository(session))
    result = query.get_component_latest_prices(name)
    if result is None:
        raise HTTPException(status_code=404, detail=f"Component '{name}' not found")
    return result
