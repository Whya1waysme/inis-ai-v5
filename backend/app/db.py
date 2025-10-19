from __future__ import annotations

import os
from contextlib import contextmanager

from sqlmodel import SQLModel, create_engine, Session

from .config import settings


def _ensure_sqlite_dir(database_url: str) -> None:
    if database_url.startswith("sqlite"):
        # sqlite:///./data/data.db -> ./data/data.db
        path = database_url.split("///")[-1]
        dirpath = os.path.dirname(path)
        if dirpath and not os.path.exists(dirpath):
            os.makedirs(dirpath, exist_ok=True)


def get_engine():
    url = settings.database_url
    _ensure_sqlite_dir(url)
    connect_args = {"check_same_thread": False} if url.startswith("sqlite") else {}
    engine = create_engine(url, echo=False, connect_args=connect_args)
    return engine


engine = get_engine()


def init_db() -> None:
    # Import models to register tables
    from . import models  # noqa: F401

    SQLModel.metadata.create_all(engine)


@contextmanager
def session_scope():
    session = Session(engine)
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()


def get_session():
    with Session(engine) as session:
        yield session
