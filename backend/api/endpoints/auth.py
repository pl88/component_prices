from __future__ import annotations

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select

from backend.api.schemas import AuthUserResponse, LoginRequest, LoginResponse, LogoutResponse
from backend.api.security import get_current_user
from backend.api.services.auth import create_access_token, verify_password
from backend.config import Settings, get_settings
from backend.db.models import User
from backend.db.session import get_session

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/login", response_model=LoginResponse)
def login(
    payload: LoginRequest,
    session: Annotated[Session, Depends(get_session)],
    settings: Annotated[Settings, Depends(get_settings)],
) -> LoginResponse:
    user = session.exec(
        select(User).where(
            User.email == payload.email,
            User.is_active.is_(True),
        )
    ).first()

    if user is None or not verify_password(payload.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    assert user.id is not None
    token = create_access_token(user_id=user.id, email=user.email, settings=settings)
    return LoginResponse(
        token=token,
        user=AuthUserResponse(
            id=str(user.id),
            email=user.email,
            name=user.name,
        ),
    )


@router.post("/logout", response_model=LogoutResponse)
def logout() -> LogoutResponse:
    return LogoutResponse(detail="Logged out")


@router.get("/me", response_model=AuthUserResponse)
def get_me(
    current_user: Annotated[User, Depends(get_current_user)],
) -> AuthUserResponse:
    assert current_user.id is not None
    return AuthUserResponse(
        id=str(current_user.id),
        email=current_user.email,
        name=current_user.name,
    )
