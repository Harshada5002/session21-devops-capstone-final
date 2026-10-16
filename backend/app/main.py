"""
TaskBoard FastAPI Application Entry Point
-----------------------------------------
Initialises the application, registers routers, sets up CORS,
mounts the Prometheus metrics endpoint, and provides startup/
shutdown lifecycle hooks.
"""

from __future__ import annotations

import logging
import time
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from prometheus_fastapi_instrumentator import Instrumentator

from app.api import tasks, health
from app.core.config import settings
from app.db.session import engine, Base

# ── Logging ──────────────────────────────────────────────────────────────────
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
)
logger = logging.getLogger(__name__)


# ── Lifespan (startup / shutdown) ────────────────────────────────────────────
@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("TaskBoard backend starting – version %s", settings.APP_VERSION)
    # Tables are created by Alembic migrations, not here.
    # We only log that the app is ready.
    logger.info("Application ready.  Environment: %s", settings.ENVIRONMENT)
    yield
    logger.info("TaskBoard backend shutting down.")


# ── Application factory ───────────────────────────────────────────────────────
app = FastAPI(
    title="TaskBoard API",
    description=(
        "Production-ready REST API for the TaskBoard project management dashboard. "
        "Demonstrates FastAPI, SQLAlchemy 2, Alembic, PostgreSQL, Prometheus, "
        "Docker, Kubernetes, and GitHub Actions CI/CD."
    ),
    version=settings.APP_VERSION,
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
    lifespan=lifespan,
)

# ── CORS ──────────────────────────────────────────────────────────────────────
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── Request timing middleware ─────────────────────────────────────────────────
@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start = time.perf_counter()
    response = await call_next(request)
    response.headers["X-Process-Time"] = f"{time.perf_counter() - start:.4f}s"
    return response

# ── Prometheus instrumentation ────────────────────────────────────────────────
Instrumentator(
    should_group_status_codes=False,
    should_ignore_untemplated=True,
    should_respect_env_var=False,
    should_instrument_requests_inprogress=True,
    excluded_handlers=["/metrics", "/health", "/ready"],
).instrument(app).expose(app, endpoint="/metrics", include_in_schema=False)

# ── Routers ───────────────────────────────────────────────────────────────────
app.include_router(health.router, tags=["Health"])
app.include_router(tasks.router, prefix="/api", tags=["Tasks"])


# ── Root endpoint ─────────────────────────────────────────────────────────────
@app.get("/", summary="Application info")
async def root():
    return {
        "application": "TaskBoard",
        "version": settings.APP_VERSION,
        "environment": settings.ENVIRONMENT,
        "docs": "/docs",
        "health": "/health",
        "metrics": "/metrics",
    }


# ── Global exception handler ──────────────────────────────────────────────────
@app.exception_handler(Exception)
async def unhandled_exception_handler(request: Request, exc: Exception):
    logger.exception("Unhandled exception on %s %s", request.method, request.url.path)
    return JSONResponse(
        status_code=500,
        content={"detail": "An internal server error occurred."},
    )
