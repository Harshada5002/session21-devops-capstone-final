# ── Backend Dockerfile ────────────────────────────────────────────────────────
# Multi-layer build for a lean, secure production image.
# Python 3.12-slim (Debian-based) for broad library compatibility.
# Runs as a non-root user to follow least-privilege principles.
# ─────────────────────────────────────────────────────────────────────────────

FROM python:3.12-slim AS base
# NOTE: Tested on Python 3.12 (pinned for Docker reproducibility).
# Local development on Python 3.14 also works with the same requirements.txt.

# Prevent Python from writing .pyc files; use unbuffered stdout/stderr
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# System dependencies needed by psycopg (PostgreSQL client library)
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
       libpq-dev \
       gcc \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# ── Install Python dependencies ───────────────────────────────────────────────
# Copy requirements first to leverage Docker layer caching.
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# ── Copy application source ───────────────────────────────────────────────────
# Explicitly copy only what the application needs.
# .dockerignore prevents .env, __pycache__, .git, etc. from being included.
COPY app/ ./app/
COPY alembic/ ./alembic/
COPY alembic.ini ./

# ── Security: non-root runtime user ──────────────────────────────────────────
RUN addgroup --system appgroup \
    && adduser --system --ingroup appgroup --no-create-home appuser
USER appuser

# ── Runtime configuration ─────────────────────────────────────────────────────
EXPOSE 8000

# Uvicorn: single worker is correct for a container in Kubernetes.
# The cluster scheduler controls horizontal scale, not multiple in-process workers.
# --forwarded-allow-ips='*' trusts X-Forwarded-* headers from Nginx/Ingress.
CMD ["uvicorn", "app.main:app", \
     "--host", "0.0.0.0", \
     "--port", "8000", \
     "--workers", "1", \
     "--forwarded-allow-ips=*", \
     "--proxy-headers"]
