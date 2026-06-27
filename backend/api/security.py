from __future__ import annotations

from typing import Annotated

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlmodel import Session, select

from backend.api.services.auth import decode_access_token
from backend.config import Settings, get_settings
from backend.db.models import User
from backend.db.session import get_session

bearer_scheme = HTTPBearer(auto_error=False)


def _unauthorized_error() -> HTTPException:
    return HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Not authenticated",
        headers={"WWW-Authenticate": "Bearer"},
    )


def get_current_user(
    credentials: Annotated[HTTPAuthorizationCredentials | None, Depends(bearer_scheme)],
    session: Annotated[Session, Depends(get_session)],
    settings: Annotated[Settings, Depends(get_settings)],
) -> User:
    if credentials is None:
        raise _unauthorized_error()

    payload = decode_access_token(credentials.credentials, settings)
    if payload is None:
        raise _unauthorized_error()

    subject = payload.get("sub")
    if not isinstance(subject, str):
        raise _unauthorized_error()

    try:
        user_id = int(subject)
    except ValueError:
        raise _unauthorized_error() from None

    user = session.exec(
        select(User).where(
            User.id == user_id,
            User.is_active.is_(True),
        )
    ).first()
    if user is None:
        raise _unauthorized_error()

    return user
