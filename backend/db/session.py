from collections.abc import Generator

from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from sqlmodel import Session

from backend.config import get_settings


def get_engine() -> Engine:
    settings = get_settings()
    return create_engine(settings.database_url, future=True, pool_pre_ping=True)


_engine: Engine | None = None


def _get_shared_engine() -> Engine:
    global _engine
    if _engine is None:
        _engine = get_engine()
    return _engine


def get_session() -> Generator[Session, None, None]:
    """FastAPI dependency that yields a database session."""
    with Session(_get_shared_engine()) as session:
        yield session
