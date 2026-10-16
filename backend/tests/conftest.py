"""
Pytest configuration and fixtures
----------------------------------
Uses an in-process SQLite database (via SQLAlchemy) for unit and
integration tests so no external PostgreSQL instance is required
during CI or local test runs.

Test isolation:
- Each test function gets a fresh database with the schema applied.
- The TestClient is recreated per test via the `client` fixture.
- No test data leaks between tests.

Test categories:
- Unit tests: functions that test a single service function with
  a mocked/isolated session (marked with @pytest.mark.unit).
- Integration tests: tests that use the full HTTP stack via TestClient
  and a real (SQLite) database (marked with @pytest.mark.integration).
  These tests are still fast because SQLite runs in-process.
"""

from __future__ import annotations

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.db.session import Base, get_db
from app.main import app

# ── In-memory SQLite engine for tests ────────────────────────────────────────
TEST_DATABASE_URL = "sqlite://"  # in-memory, auto-deleted after process ends

test_engine = create_engine(
    TEST_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(
    bind=test_engine, autocommit=False, autoflush=False, expire_on_commit=False
)


@pytest.fixture(scope="function")
def db_session():
    """
    Create all tables before each test and drop them after.
    Guarantees complete isolation between tests.
    """
    Base.metadata.create_all(bind=test_engine)
    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.close()
        Base.metadata.drop_all(bind=test_engine)


@pytest.fixture(scope="function")
def client(db_session):
    """
    Return a TestClient whose DB dependency is replaced by the
    isolated test session created above.
    """

    def override_get_db():
        try:
            yield db_session
        finally:
            pass  # session lifecycle managed by db_session fixture

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as c:
        yield c
    app.dependency_overrides.clear()
