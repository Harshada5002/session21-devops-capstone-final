# TaskBoard — Full-Stack DevOps Capstone Project

> A production-oriented SaaS task management application demonstrating the **complete software delivery lifecycle**: development → testing → containerization → security scanning → CI/CD → cloud infrastructure → Kubernetes deployment → monitoring → troubleshooting.

---

## Table of Contents

1. [Project Overview](#1-project-overview)
2. [Architecture Diagram](#2-architecture-diagram)
3. [Features](#3-features)
4. [Technology Stack](#4-technology-stack)
5. [Repository Structure](#5-repository-structure)
6. [Prerequisites](#6-prerequisites)
7. [Local Docker Compose Setup](#7-local-docker-compose-setup)
8. [Backend Development Setup](#8-backend-development-setup)
9. [Frontend Development Setup](#9-frontend-development-setup)
10. [Environment Variables](#10-environment-variables)
11. [Database Migrations](#11-database-migrations)
12. [Testing](#12-testing)
13. [Git & GitHub Workflow](#13-git--github-workflow)
14. [Docker Build Instructions](#14-docker-build-instructions)
15. [CI/CD Pipeline](#15-cicd-pipeline)
16. [Trivy Security Scanning](#16-trivy-security-scanning)
17. [GHCR Image Publishing](#17-ghcr-image-publishing)
18. [Terraform AWS Infrastructure](#18-terraform-aws-infrastructure)
19. [AWS EKS Configuration](#19-aws-eks-configuration)
20. [Kubernetes Deployment](#20-kubernetes-deployment)
21. [Helm Operations](#21-helm-operations)
22. [Ingress Configuration](#22-ingress-configuration)
23. [HPA & Load Testing](#23-hpa--load-testing)
24. [Prometheus & Grafana](#24-prometheus--grafana)
25. [Troubleshooting Exercises](#25-troubleshooting-exercises)
26. [Security Considerations](#26-security-considerations)
27. [AWS Cost Management & Cleanup](#27-aws-cost-management--cleanup)
28. [Final Demonstration Checklist](#28-final-demonstration-checklist)
29. [Known Limitations](#29-known-limitations)
30. [Future Improvements](#30-future-improvements)

---

## 1. Project Overview

**TaskBoard** is a SaaS-style project and task management dashboard built as a DevOps capstone to demonstrate every phase of the software delivery lifecycle.

The application allows teams to create, update, delete, search, and filter tasks. It is backed by a PostgreSQL database accessed through a FastAPI REST API and displayed through a polished React dashboard.

The infrastructure is provisioned on AWS using Terraform, the application is containerized with Docker, the images are scanned for vulnerabilities using Trivy, and the deployment is automated through GitHub Actions CI/CD into an Amazon EKS Kubernetes cluster.

---

## 2. Architecture Diagram

```mermaid
graph TB
    subgraph "Developer Laptop (Windows + Docker Desktop)"
        DEV[VS Code / PowerShell]
        DC[Docker Compose]
        DEV -->|docker compose up| DC
    end

    subgraph "Local Stack"
        FE[Frontend :3000\nReact + Nginx]
        BE[Backend :8000\nFastAPI + Uvicorn]
        DB[(PostgreSQL :5432)]
        FE -->|/api proxy| BE
        BE -->|SQLAlchemy| DB
    end

    subgraph "GitHub"
        GH[GitHub Repository]
        GA[GitHub Actions CI/CD]
        GHCR[GHCR Container Registry]
        GH --> GA
        GA -->|Trivy scan + push| GHCR
    end

    subgraph "AWS ap-south-1"
        subgraph "VPC 10.0.0.0/16"
            subgraph "Public Subnets"
                IGW[Internet Gateway]
                NAT[NAT Gateway]
                ALB[AWS Load Balancer]
            end
            subgraph "Private Subnets"
                subgraph "EKS Cluster"
                    ING[Ingress Controller]
                    FEP[Frontend Pods]
                    BEP[Backend Pods x2]
                    PG[(PostgreSQL StatefulSet)]
                    HPA[HPA]
                    PROM[Prometheus]
                    GRAF[Grafana]
                end
            end
        end
    end

    DC --> GH
    GHCR -->|helm upgrade| BEP
    GHCR -->|helm upgrade| FEP
    ALB --> ING
    ING -->|/| FEP
    ING -->|/api| BEP
    BEP --> PG
    HPA --> BEP
    PROM -->|scrape /metrics| BEP
    GRAF --> PROM
```

---

## 3. Features

- ✅ **Full CRUD** — create, read, update, delete tasks
- ✅ **Search & filter** — by status, priority, assignee, full-text
- ✅ **Pagination** — configurable page size
- ✅ **Dashboard KPIs** — total, done, in-progress, overdue counts
- ✅ **Visual pipeline** — TODO → IN_PROGRESS → DONE flow
- ✅ **Activity feed** — recent task events
- ✅ **Responsive design** — desktop, tablet, mobile
- ✅ **Dark mode SaaS UI** — premium glassmorphism design
- ✅ **REST API docs** — Swagger UI at `/docs`
- ✅ **Prometheus metrics** — at `/metrics`
- ✅ **Health probes** — `/health` and `/ready` for Kubernetes
- ✅ **Database migrations** — Alembic with versioned scripts
- ✅ **Automated tests** — Pytest suite with 30+ assertions
- ✅ **Container security** — Trivy scanning, non-root users
- ✅ **CI/CD pipeline** — GitHub Actions with 3 stages
- ✅ **Kubernetes autoscaling** — HPA on CPU utilization
- ✅ **Monitoring** — Prometheus + Grafana dashboards

---

## 4. Technology Stack

| Layer | Technology | Version |
|-------|-----------|---------|
| Frontend | React | 18.3 |
| Build tool | Vite | 5.4 |
| Frontend server | Nginx | 1.27-alpine |
| Backend | FastAPI | 0.115 |
| ASGI server | Uvicorn | 0.32 |
| ORM | SQLAlchemy | 2.0 |
| Migrations | Alembic | 1.14 |
| Validation | Pydantic | 2.10 |
| Database | PostgreSQL | 16 |
| DB driver | psycopg | 3.2 |
| Metrics | prometheus-fastapi-instrumentator | 7.0 |
| Testing | Pytest + HTTPX | 8.3 / 0.28 |
| Container runtime | Docker | 27+ |
| Orchestration | Kubernetes | 1.31 |
| Package manager | Helm | 3.16 |
| IaC | Terraform | 1.9+ |
| Cloud | AWS EKS | ap-south-1 |
| CI/CD | GitHub Actions | — |
| Scanning | Trivy | latest |
| Registry | GHCR | — |
| Monitoring | Prometheus + Grafana | kube-prometheus-stack |

---

## 5. Repository Structure

```
session21-devops-capstone-final/
├── frontend/               React + Vite application
│   ├── src/
│   │   ├── components/     Reusable UI components
│   │   ├── pages/          Dashboard page
│   │   ├── services/       API client (api.js)
│   │   ├── hooks/          useTasks custom hook
│   │   ├── App.jsx         Root component + layout
│   │   └── main.jsx        React entry point
│   ├── Dockerfile          Multi-stage Node → Nginx
│   ├── nginx.conf          SPA + /api proxy config
│   ├── vite.config.js      Dev proxy + build settings
│   └── package.json
├── backend/                FastAPI application
│   ├── app/
│   │   ├── main.py         App factory + middleware
│   │   ├── api/            HTTP routers (health, tasks)
│   │   ├── core/           Configuration (pydantic-settings)
│   │   ├── db/             Session + engine + connectivity probe
│   │   ├── models/         SQLAlchemy ORM models
│   │   ├── schemas/        Pydantic request/response schemas
│   │   └── services/       Business logic (task_service.py)
│   ├── tests/              Pytest test suite
│   ├── alembic/            Database migration scripts
│   ├── alembic.ini         Alembic configuration
│   ├── requirements.txt    Pinned Python dependencies
│   ├── Dockerfile          Python 3.12-slim, non-root user
│   └── .dockerignore
├── docker-compose.yml      Local development stack
├── .env.example            Safe environment variable template
├── .gitignore
├── terraform/              AWS infrastructure (VPC + EKS)
├── helm/taskboard/         Kubernetes Helm chart
├── k8s/                    Raw Kubernetes manifests
├── monitoring/             Prometheus + Grafana configuration
├── troubleshooting/        Intentionally broken manifests
├── scripts/load-test.py    Load testing script
├── .github/workflows/      GitHub Actions CI/CD pipeline
└── README.md               This file
```

---

## 6. Prerequisites

### Windows (Primary Environment)

| Tool | Version | Install |
|------|---------|---------|
| Docker Desktop | 27+ | https://www.docker.com/products/docker-desktop/ |
| WSL 2 + Ubuntu | 22.04+ | `wsl --install` in PowerShell (Admin) |
| Python | 3.12 | https://www.python.org/downloads/ |
| Node.js | 20 LTS | https://nodejs.org/ |
| Git | Latest | https://git-scm.com/ |
| VS Code | Latest | https://code.visualstudio.com/ |
| AWS CLI | 2.x | https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html |
| kubectl | 1.31 | `winget install Kubernetes.kubectl` |
| Helm | 3.16 | `winget install Helm.Helm` |
| Terraform | 1.9+ | `winget install Hashicorp.Terraform` |

### Verify Docker Desktop

```powershell
# Ensure Linux containers mode is active
docker version
docker compose version
docker run hello-world
```

> In Docker Desktop: Settings → General → ensure "Use the WSL 2 based engine" is checked.

---

## 7. Local Docker Compose Setup

### Quick Start

```powershell
# 1. Clone the repository
git clone https://github.com/YOUR_ORG/taskboard.git
cd taskboard\session21-devops-capstone-final

# 2. Create your local environment file
Copy-Item .env.example .env
# Edit .env with a secure password if desired

# 3. Build and start the complete stack
docker compose up --build
```

The stack starts in this order:
1. **PostgreSQL** (health check: pg_isready)
2. **Migration job** (runs `alembic upgrade head`, then exits)
3. **Backend** (starts after migrations succeed)
4. **Frontend** (starts after backend is healthy)

### Access Points

| Service | URL |
|---------|-----|
| TaskBoard UI | http://localhost:3000 |
| API documentation | http://localhost:8000/docs |
| Backend health | http://localhost:8000/health |
| Backend metrics | http://localhost:8000/metrics |

### Useful Commands

```powershell
# View logs from all services
docker compose logs -f

# View logs from a specific service
docker compose logs -f backend

# Check container status and health
docker compose ps

# Stop the stack (keeps database volume)
docker compose down

# Rebuild images after code changes
docker compose up --build

# Remove containers (keeps database volume)
docker compose down

# ⚠ WARNING: This deletes ALL task data permanently
docker compose down -v

# Open a shell in the backend container
docker compose exec backend /bin/sh

# Check database connectivity
docker compose exec db psql -U taskboard -c "SELECT COUNT(*) FROM tasks;"
```

### Verify Database Persistence

```powershell
# 1. Create a task via the UI at http://localhost:3000
# 2. Stop the stack (without -v)
docker compose down

# 3. Restart the stack
docker compose up

# 4. Open http://localhost:3000 – your task should still be there
```

---

## 8. Backend Development Setup

```powershell
cd session21-devops-capstone-final\backend

# Create and activate virtual environment
python -m venv venv
.\venv\Scripts\Activate.ps1

# Install dependencies
pip install -r requirements.txt

# Configure environment
Copy-Item ..\.env.example .env
# Edit .env: set DATABASE_URL to point to a running PostgreSQL instance

# Run migrations
alembic upgrade head

# Start the development server (auto-reload)
uvicorn app.main:app --reload --port 8000

# Open API docs
Start-Process "http://localhost:8000/docs"
```

---

## 9. Frontend Development Setup

```powershell
cd session21-devops-capstone-final\frontend

# Install dependencies
npm install

# Start Vite development server (proxies /api to localhost:8000)
npm run dev

# Open browser
Start-Process "http://localhost:3000"
```

> The Vite dev proxy in `vite.config.js` forwards `/api` requests to `http://localhost:8000`, so the backend must be running separately.

---

## 10. Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `DATABASE_URL` | SQLAlchemy connection string | `postgresql+psycopg://taskboard:taskboard@localhost:5432/taskboard` |
| `ENVIRONMENT` | `development` or `production` | `development` |
| `DEBUG` | Enable SQL logging | `false` |
| `CORS_ORIGINS` | Comma-separated allowed origins | `http://localhost:3000` |
| `POSTGRES_USER` | PostgreSQL username (Compose/K8s) | `taskboard` |
| `POSTGRES_PASSWORD` | PostgreSQL password | *(required)* |
| `POSTGRES_DB` | PostgreSQL database name | `taskboard` |
| `VITE_API_BASE_URL` | Frontend API base URL | *(empty = same origin)* |

---

## 11. Database Migrations

### Apply pending migrations

```powershell
# Using virtual environment
.\venv\Scripts\Activate.ps1
alembic upgrade head

# Using Docker Compose
docker compose exec backend alembic upgrade head
```

### Check current migration state

```powershell
alembic current
alembic history --verbose
```

### Generate a new migration after model changes

```powershell
# 1. Modify app/models/task.py
# 2. Generate migration (autogenerate detects schema diff)
alembic revision --autogenerate -m "add_tags_column"

# 3. Review the generated file in alembic/versions/
# 4. Apply it
alembic upgrade head
```

### Rollback one migration

```powershell
alembic downgrade -1
```

> **Production rule**: Never run migrations automatically at application startup when multiple replicas are running. Always use the dedicated migration Job (Docker Compose `migrate` service or Kubernetes pre-install Hook).

---

## 12. Testing

### Run the full test suite

```powershell
cd session21-devops-capstone-final\backend
.\venv\Scripts\Activate.ps1
pytest -q
```

### Run with coverage report

```powershell
pytest --cov=app --cov-report=html
# Open htmlcov/index.html in a browser
```

### Test categories

| Marker | Description | DB required |
|--------|-------------|-------------|
| `integration` | Full HTTP stack with SQLite | No (in-memory) |
| `unit` | Isolated function tests | No |

> All tests use an **in-memory SQLite database** via SQLAlchemy – no PostgreSQL instance required. This means tests run in CI without any external services.

### Limitations

- Tests do not cover concurrent database access patterns
- Integration tests use SQLite, which does not support all PostgreSQL-specific features (e.g., `ILIKE` in PostgreSQL vs SQLite case-insensitivity)
- No end-to-end browser tests (Playwright/Selenium) are included

---

## 13. Git & GitHub Workflow

### Initial setup

```powershell
cd session21-devops-capstone-final
git init
git add .
git commit -m "Initial TaskBoard application"
git branch -M main
```

### Create GitHub repository

1. Go to https://github.com/new
2. Create a new **private** repository named `taskboard`
3. Do NOT initialize with README (we already have one)

```powershell
git remote add origin https://github.com/YOUR_ORG/taskboard.git
git push -u origin main
```

### Branch strategy

```powershell
# Feature development
git checkout -b feature/add-task-tags
# ... make changes ...
git add .
git commit -m "feat: add task tags"
git push origin feature/add-task-tags
# Create Pull Request on GitHub
```

---

## 14. Docker Build Instructions

### Build images individually

```powershell
# Backend
docker build -t taskboard-backend:local .\backend\

# Frontend
docker build -t taskboard-frontend:local .\frontend\
```

### Build and tag for GHCR

```powershell
$SHA = git rev-parse --short HEAD
docker build -t ghcr.io/YOUR_ORG/taskboard-backend:$SHA .\backend\
docker build -t ghcr.io/YOUR_ORG/taskboard-frontend:$SHA .\frontend\
```

---

## 15. CI/CD Pipeline

The pipeline at `.github/workflows/ci-cd.yml` has three stages:

```
Push to main
    │
    ▼
┌─────────────────────┐
│  Stage 1: Test      │
│  • Pytest (SQLite)  │
│  • npm build        │
└──────────┬──────────┘
           │ (both pass)
           ▼
┌──────────────────────────┐
│  Stage 2: Build+Scan     │
│  • docker build backend  │
│  • Trivy scan backend    │
│  • push to GHCR          │
│  • docker build frontend │
│  • Trivy scan frontend   │
│  • push to GHCR          │
└──────────┬───────────────┘
           │ (scan passes)
           ▼
┌──────────────────────────┐
│  Stage 3: Deploy         │
│  • AWS OIDC auth         │
│  • kubectl verify        │
│  • helm upgrade --atomic │
│  • health check          │
└──────────────────────────┘
```

### Required GitHub Secrets/Variables

| Name | Type | Description |
|------|------|-------------|
| `AWS_ACCOUNT_ID` | Secret | Your 12-digit AWS account ID |
| `AWS_REGION` | Variable | `ap-south-1` |
| `EKS_CLUSTER_NAME` | Variable | `taskboard-cluster` |

> The pipeline uses **GitHub OIDC** to authenticate to AWS — no long-lived access keys are stored in GitHub Secrets.

---

## 16. Trivy Security Scanning

Trivy scans container images for vulnerabilities in OS packages and application dependencies.

### Scan types explained

| Type | What it checks |
|------|---------------|
| **Container image** | OS packages, language dependencies in the final image |
| **Dependency (SCA)** | `requirements.txt`, `package.json` known CVEs |
| **Secret scanning** | Hardcoded credentials in source code |
| **SAST** | Static code analysis for code vulnerabilities |
| **IaC scanning** | Terraform misconfiguration |
| **Runtime** | Live container behaviour (requires Falco/Sysdig) |

### Scan locally

```powershell
# Install Trivy (winget or scoop)
winget install AquaSecurity.Trivy

# Scan the backend image
trivy image --severity HIGH,CRITICAL taskboard-backend:local

# Scan ignoring unfixed vulnerabilities
trivy image --ignore-unfixed --severity HIGH,CRITICAL taskboard-backend:local
```

### Handling vulnerabilities

1. **Update the dependency** (preferred) — bump the version in `requirements.txt` or `package.json`
2. **Document exceptions** — if no fix exists, add to `.trivyignore` with justification and expiry date
3. **Never disable scans** just to make the pipeline green

> A clean Trivy scan does not mean the application is secure. It only means no known CVEs are present in the scanned packages at that point in time.

---

## 17. GHCR Image Publishing

Images are published to GitHub Container Registry automatically by the CI/CD pipeline.

### Manual publish (PowerShell)

```powershell
# Login to GHCR
echo $env:GITHUB_TOKEN | docker login ghcr.io -u YOUR_USERNAME --password-stdin

# Tag and push
$SHA = git rev-parse --short HEAD
docker push ghcr.io/YOUR_ORG/taskboard-backend:$SHA
docker push ghcr.io/YOUR_ORG/taskboard-frontend:$SHA
```

### Image naming convention

| Image | Tag | Purpose |
|-------|-----|---------|
| `taskboard-backend` | `<commit-sha>` | Immutable, traceable deployment tag |
| `taskboard-backend` | `dev` | Latest main branch build |
| `taskboard-frontend` | `<commit-sha>` | Immutable deployment tag |

> Never use `latest` as the deployment identity in Kubernetes — it makes rollbacks ambiguous.

---

## 18. Terraform AWS Infrastructure

> ⚠ **Cost warning**: Running this infrastructure costs approximately $5–10/day in ap-south-1 (EKS control plane + 2× t3.medium + NAT Gateway). **Destroy when not in use.**

### Prerequisites

```powershell
# Configure AWS credentials
aws configure
# Enter: Access Key ID, Secret Access Key, region (ap-south-1), output (json)

# Verify
aws sts get-caller-identity
```

### Deploy infrastructure

```powershell
cd session21-devops-capstone-final\terraform

# Initialize (downloads providers)
terraform init

# Validate configuration
terraform validate

# Preview changes
terraform plan

# ⚠ Apply only after reviewing the plan output
terraform apply
```

### Get cluster credentials

```powershell
# After terraform apply completes, run the output command:
terraform output kubeconfig_command
# Copy and run the output, e.g.:
aws eks update-kubeconfig --region ap-south-1 --name taskboard-cluster

# Verify
kubectl get nodes
```

### Destroy infrastructure

```powershell
# ⚠ DESTRUCTIVE: This permanently deletes all AWS resources and any stored data
terraform destroy
```

---

## 19. AWS EKS Configuration

### Install cluster add-ons

```powershell
# Metrics Server (required for HPA)
kubectl apply -f https://github.com/kubernetes-sigs/metrics-server/releases/latest/download/components.yaml

# Verify Metrics Server
kubectl top nodes

# Ingress Controller (nginx)
helm repo add ingress-nginx https://kubernetes.github.io/ingress-nginx
helm repo update
helm upgrade --install ingress-nginx ingress-nginx/ingress-nginx `
  --namespace ingress-nginx --create-namespace `
  --set controller.replicaCount=2

# Wait for LoadBalancer IP
kubectl get svc -n ingress-nginx ingress-nginx-controller --watch
```

---

## 20. Kubernetes Deployment

### Create the database secret FIRST

```powershell
kubectl create namespace taskboard

kubectl create secret generic taskboard-db-secret `
  --namespace taskboard `
  --from-literal=DATABASE_URL="postgresql+psycopg://taskboard:SECURE_PASSWORD@taskboard-postgresql:5432/taskboard" `
  --from-literal=POSTGRES_USER="taskboard" `
  --from-literal=POSTGRES_PASSWORD="SECURE_PASSWORD" `
  --from-literal=POSTGRES_DB="taskboard"
```

### Deploy with Helm

```powershell
helm upgrade --install taskboard .\helm\taskboard `
  --namespace taskboard `
  --create-namespace `
  --values .\helm\taskboard\values.yaml `
  --set backend.image.tag="YOUR_COMMIT_SHA" `
  --set frontend.image.tag="YOUR_COMMIT_SHA"
```

### Verify deployment

```powershell
# Check pods
kubectl get pods -n taskboard

# Check services
kubectl get svc -n taskboard

# Check HPA
kubectl get hpa -n taskboard

# Check ingress
kubectl get ingress -n taskboard

# View backend logs
kubectl logs -l app.kubernetes.io/component=backend -n taskboard -f
```

---

## 21. Helm Operations

```powershell
# Install
helm upgrade --install taskboard .\helm\taskboard --namespace taskboard --create-namespace

# Check release status
helm status taskboard -n taskboard

# List releases
helm list -n taskboard

# Preview rendered templates (dry run)
helm template taskboard .\helm\taskboard --values .\helm\taskboard\values.yaml

# Upgrade with new image tag
helm upgrade taskboard .\helm\taskboard --namespace taskboard `
  --set backend.image.tag="abc1234" --set frontend.image.tag="abc1234"

# Roll back to previous revision
helm rollback taskboard -n taskboard

# Uninstall (removes all k8s resources except PVCs with helm.sh/resource-policy: keep)
helm uninstall taskboard -n taskboard
```

---

## 22. Ingress Configuration

The Ingress resource routes traffic:

```
Internet → LoadBalancer → ingress-nginx → /api → backend:8000
                                        → /    → frontend:80
```

### Local testing (port-forward)

```powershell
# Test backend directly
kubectl port-forward svc/taskboard-backend 8000:8000 -n taskboard

# Test frontend directly
kubectl port-forward svc/taskboard-frontend 8080:80 -n taskboard

# Open http://localhost:8080
```

### Get the Ingress LoadBalancer URL

```powershell
kubectl get ingress -n taskboard
# Note the ADDRESS field – this is your LoadBalancer DNS name
```

---

## 23. HPA & Load Testing

### Check HPA status

```powershell
kubectl get hpa -n taskboard
kubectl describe hpa taskboard-backend -n taskboard
```

### Run load test against Kubernetes

```powershell
# Port-forward the backend first
kubectl port-forward svc/taskboard-backend 8000:8000 -n taskboard

# In another terminal, run the load test
python scripts\load-test.py --url http://localhost:8000 --rps 20 --duration 120

# Watch HPA scale up in real time
kubectl get hpa -n taskboard --watch
```

> **Important**: HPA only scales when CPU utilization exceeds the target threshold **and** the Metrics Server is running. A simple `/health` request generates minimal CPU — use the load test which POSTs new tasks and runs search queries.

---

## 24. Prometheus & Grafana

### Install monitoring stack

```powershell
helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
helm repo update

helm upgrade --install prometheus prometheus-community/kube-prometheus-stack `
  --namespace monitoring `
  --create-namespace `
  --values .\monitoring\prometheus-values.yaml
```

### Access Grafana

```powershell
kubectl port-forward svc/prometheus-grafana 3001:80 -n monitoring
# Open http://localhost:3001
# Default credentials: admin / admin  ← CHANGE IN PRODUCTION
```

### Import TaskBoard dashboard

1. Open Grafana → Dashboards → Import
2. Upload `monitoring/dashboards/taskboard-dashboard.json`

### Access Prometheus

```powershell
kubectl port-forward svc/prometheus-kube-prometheus-prometheus 9090:9090 -n monitoring
# Open http://localhost:9090
```

### Useful PromQL queries

```promql
# Request rate per second
rate(http_requests_total{namespace="taskboard"}[1m])

# 95th percentile response time
histogram_quantile(0.95, rate(http_request_duration_seconds_bucket{namespace="taskboard"}[5m]))

# Error rate percentage
rate(http_requests_total{namespace="taskboard",status_code=~"5.."}[1m])
/ rate(http_requests_total{namespace="taskboard"}[1m]) * 100

# Current backend replicas
count(kube_pod_info{namespace="taskboard",pod=~"taskboard-backend.*"})
```

---

## 25. Troubleshooting Exercises

### Exercise A: Broken Image (ImagePullBackOff)

```powershell
kubectl apply -f troubleshooting\broken-image.yaml
kubectl get pods -n taskboard -l app=taskboard-broken-image
# Expected: ImagePullBackOff

kubectl describe pod -l app=taskboard-broken-image -n taskboard
# Look for: Failed to pull image
```

**Fix**: Update the image tag to a valid one.

### Exercise B: Broken Service Selector

```powershell
kubectl apply -f troubleshooting\broken-service.yaml
kubectl get endpoints taskboard-broken-service -n taskboard
# Expected: <none>
```

**Fix**: Correct the Service selector to match Pod labels.

### Additional Diagnostic Scenarios

| Scenario | Symptoms | Key Commands |
|----------|----------|--------------|
| DB connection failure | `/ready` returns 503, CrashLoopBackOff | `kubectl logs`, `kubectl describe pod` |
| Missing Secret | Pod stuck in `CreateContainerConfigError` | `kubectl get events` |
| Wrong env variable | Application behaviour errors | `kubectl exec` + inspect env |
| OOMKilled | Pod restarts frequently | `kubectl describe pod`, `kubectl top pod` |
| HPA not scaling | Replicas stuck at minimum | `kubectl describe hpa`, verify Metrics Server |
| Ingress 404 | Application not reachable | `kubectl describe ingress`, check `ingressClassName` |

---

## 26. Security Considerations

| Control | Implementation |
|---------|---------------|
| Non-root containers | `runAsUser: 1000`, `runAsNonRoot: true` |
| Read-only filesystem | `readOnlyRootFilesystem: false` (Nginx needs writes; backend can be enabled) |
| Drop capabilities | `capabilities: drop: [ALL]` |
| No privilege escalation | `allowPrivilegeEscalation: false` |
| Secrets management | Kubernetes Secrets, never in Git |
| Dependency pinning | All versions pinned in requirements.txt / package.json |
| Container scanning | Trivy on every CI run |
| OIDC authentication | No long-lived AWS keys in GitHub Actions |
| Least privilege | IAM roles with minimal permissions |
| Network isolation | Private subnets for EKS nodes |
| CORS | Restricted to known origins |

---

## 27. AWS Cost Management & Cleanup

### Estimated hourly costs (ap-south-1)

| Resource | Cost/hour |
|----------|-----------|
| EKS control plane | ~$0.10 |
| 2× t3.medium nodes | ~$0.10 |
| NAT Gateway | ~$0.045 |
| Load Balancer | ~$0.025 |
| **Total** | **~$0.27/hour (~$6.5/day)** |

### Cleanup procedure

```powershell
# 1. Uninstall Helm releases
helm uninstall taskboard -n taskboard
helm uninstall prometheus -n monitoring

# 2. Delete namespaces
kubectl delete namespace taskboard monitoring

# 3. Destroy Terraform infrastructure
cd terraform
terraform destroy
# Type 'yes' when prompted

# 4. Verify no resources remain
aws ec2 describe-instances --filters Name=tag:Project,Values=TaskBoard
aws eks list-clusters
```

> ⚠ **Always run `terraform destroy` when done.** Idle EKS clusters accumulate charges even with no workloads.

---

## 28. Final Demonstration Checklist

- [ ] Open http://localhost:3000 — dashboard loads
- [ ] Create a task via the UI
- [ ] Verify via API: `curl http://localhost:8000/api/tasks`
- [ ] Check DB: `docker compose exec db psql -U taskboard -c "SELECT * FROM tasks;"`
- [ ] Update and delete the task
- [ ] Run: `pytest -q` — all tests pass
- [ ] Show GitHub Actions pipeline running
- [ ] Show Trivy scan results
- [ ] Show published GHCR images
- [ ] Show `terraform plan` output
- [ ] Show EKS nodes: `kubectl get nodes`
- [ ] Show Helm release: `helm list -n taskboard`
- [ ] Show pods/services: `kubectl get all -n taskboard`
- [ ] Open application through Ingress URL
- [ ] Show HPA: `kubectl get hpa -n taskboard`
- [ ] Run load test: `python scripts\load-test.py`
- [ ] Show HPA scaling: `kubectl get hpa --watch`
- [ ] Show Prometheus targets
- [ ] Show Grafana dashboard
- [ ] Apply `troubleshooting\broken-image.yaml` — show ImagePullBackOff
- [ ] Fix the broken image — pods recover
- [ ] Run `terraform destroy` — infrastructure cleaned up

---

## 29. Known Limitations

- In-cluster PostgreSQL is not production-grade (no HA, no automated backups)
- Grafana admin password is exposed in Helm values for the demo (must be changed for real use)
- Activity feed is simulated (not a real event log table)
- Load test creates real tasks in the database (clean up manually)
- SQLite used in tests does not support all PostgreSQL features
- Terraform state is local by default (configure S3 backend for team use)

---

## 30. Future Improvements

- Replace in-cluster PostgreSQL with Amazon RDS Multi-AZ
- Add External Secrets Operator for AWS Secrets Manager integration
- Implement JWT authentication with user management
- Add Playwright end-to-end browser tests
- Configure PodDisruptionBudgets for zero-downtime node upgrades
- Add Vertical Pod Autoscaler (VPA)
- Implement OpenTelemetry distributed tracing
- Add Alertmanager rules for error rate and latency SLOs
- Add task attachments using S3 pre-signed URLs
- Configure Karpenter for more efficient node autoscaling
- Add real-time updates via WebSockets
