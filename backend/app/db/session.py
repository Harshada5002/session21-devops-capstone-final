"""
Database Session Management
-----------------------------
Creates the SQLAlchemy async-compatible engine and session factory.
All database credentials are read from the DATABASE_URL environment
variable – never from source code.

Connection pool settings are tuned for a production Kubernetes workload
where multiple replicas connect to the same PostgreSQL instance.
"""

from __future__ import annotations

import logging

from sqlalchemy import create_engine, text
from sqlalchemy.orm import DeclarativeBase, sessionmaker

from app.core.config import settings

logger = logging.getLogger(__name__)


# ── Engine ────────────────────────────────────────────────────────────────────
engine = create_engine(
    settings.DATABASE_URL,
    pool_pre_ping=True,          # validates connections before use
    pool_size=5,                 # connections kept open per replica
    max_overflow=10,             # extra connections under burst load
    pool_timeout=30,             # seconds to wait for a connection
    pool_recycle=1800,           # recycle connections every 30 min
    echo=settings.DEBUG,         # log SQL only in debug mode
)

# ── Session factory ───────────────────────────────────────────────────────────
SessionLocal = sessionmaker(
    bind=engine,
    autocommit=False,
    autoflush=False,
    expire_on_commit=False,
)


# ── Declarative base ──────────────────────────────────────────────────────────
class Base(DeclarativeBase):
    pass


# ── Dependency ────────────────────────────────────────────────────────────────
def get_db():
    """
    FastAPI dependency that yields a database session and ensures
    it is closed after the request – even if an exception is raised.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# ── Connectivity check ────────────────────────────────────────────────────────
def check_db_connection() -> bool:
    """
    Lightweight connectivity probe used by the /ready endpoint.
    Returns True when the database is reachable, False otherwise.
    Never raises – failure is reported as a boolean.
    """
    try:
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        return True
    except Exception as exc:
        logger.warning("Database connectivity check failed: %s", exc)
        return False
