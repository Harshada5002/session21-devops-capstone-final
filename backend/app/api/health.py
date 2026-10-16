"""
Health and Readiness Endpoints
-------------------------------
/health   – lightweight liveness probe (no DB call).
/ready    – readiness probe that verifies database connectivity.

Kubernetes uses /health for liveness and /ready for readiness.
Separating them avoids restart loops when the DB is temporarily
unavailable during a rolling update.
"""

from __future__ import annotations

from fastapi import APIRouter, status
from fastapi.responses import JSONResponse

from app.db.session import check_db_connection

router = APIRouter()


@router.get(
    "/health",
    summary="Liveness probe",
    response_description="Returns 200 when the process is alive.",
)
async def health():
    return {"status": "ok"}


@router.get(
    "/ready",
    summary="Readiness probe",
    response_description="Returns 200 when the app can serve traffic, 503 otherwise.",
)
async def ready():
    if check_db_connection():
        return {"status": "ready", "database": "connected"}
    return JSONResponse(
        status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
        content={"status": "not ready", "database": "unavailable"},
    )
