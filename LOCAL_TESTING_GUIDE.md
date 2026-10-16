# TaskBoard – Local Testing Guide
# =======================================================
# Step-by-step instructions to test every part of the
# project on your Windows machine BEFORE committing.
# =======================================================

## ✅ PROJECT COMPLETION STATUS

| Component | Status |
|-----------|--------|
| FastAPI backend (CRUD, health, metrics) | ✅ Complete |
| SQLAlchemy models + Alembic migrations | ✅ Complete |
| React frontend (dark SaaS UI) | ✅ Complete |
| 34 Pytest tests – ALL PASSING | ✅ Complete |
| Backend Dockerfile (Python 3.12-slim) | ✅ Complete |
| Frontend Dockerfile (Node → Nginx) | ✅ Complete |
| docker-compose.yml (full stack) | ✅ Complete |
| GitHub Actions CI/CD (3 stages) | ✅ Complete |
| Terraform (VPC + EKS in ap-south-1) | ✅ Complete |
| Helm chart (backend/frontend/postgres/HPA/Ingress) | ✅ Complete |
| Prometheus + Grafana monitoring config | ✅ Complete |
| Troubleshooting exercises (2 broken manifests) | ✅ Complete |
| Load testing script | ✅ Complete |
| README (30 sections) | ✅ Complete |

**YOUR PART: Only 2 things need YOUR action:**
1. Add real AWS credentials before running `terraform apply`
2. Replace placeholder passwords in Helm secret before deploying to Kubernetes

---

## STEP 1 – Run Tests (No Docker needed)

```powershell
cd C:\Users\harsh\OneDrive\Desktop\dev_project\session21-devops-capstone-final\backend
.\venv\Scripts\Activate.ps1
pytest -q
```
**EXPECTED:** `34 passed in 0.37s`

---

## STEP 2 – Run Docker Compose (Full Stack)

```powershell
cd C:\Users\harsh\OneDrive\Desktop\dev_project\session21-devops-capstone-final

# Start the stack
docker compose up --build -d

# Watch live logs
docker compose logs -f

# Check status (wait for all to be healthy)
docker compose ps
```

**EXPECTED STATUS:**
```
NAME                 STATUS
taskboard-db         Up (healthy)
taskboard-migrate    Exited (0)     <- must EXIT 0
taskboard-backend    Up (healthy)
taskboard-frontend   Up (healthy)
```

---

## STEP 3 – Test the Application in Browser

Open: **http://localhost:3000**
→ TaskBoard dashboard appears with dark SaaS UI

- Click "＋ Create Task" → fill in title, status, priority → Save
- Your task appears in the table
- Filter by status/priority chips
- Click a task row → edit it → Save
- Click 🗑️ to delete a task

---

## STEP 4 – Test the Backend API (Swagger UI)

Open: **http://localhost:8000/docs**
→ Interactive Swagger documentation

Test these endpoints:
- GET  /health           → `{"status":"ok"}`
- GET  /ready            → `{"status":"ready"}`
- GET  /metrics          → Prometheus text format
- POST /api/tasks        → Create a task
- GET  /api/tasks        → List all tasks
- GET  /api/tasks/stats  → KPI counts

---

## STEP 5 – Test via curl (PowerShell)

```powershell
# Health check
Invoke-RestMethod http://localhost:8000/health

# Create a task
Invoke-RestMethod http://localhost:8000/api/tasks `
  -Method POST `
  -ContentType "application/json" `
  -Body '{"title":"My first task","status":"TODO","priority":"HIGH"}'

# List tasks
Invoke-RestMethod http://localhost:8000/api/tasks

# Stats
Invoke-RestMethod http://localhost:8000/api/tasks/stats
```

---

## STEP 6 – Verify Database Directly

```powershell
# Open PostgreSQL CLI inside the container
docker compose exec db psql -U taskboard -d taskboard

# Inside psql:
\dt
SELECT id, title, status, priority FROM tasks;
\q
```

---

## STEP 7 – Run Load Test

While docker-compose is running:

```powershell
cd C:\Users\harsh\OneDrive\Desktop\dev_project\session21-devops-capstone-final
python scripts\load-test.py --url http://localhost:8000 --rps 10 --duration 30
```
**EXPECTED:** Requests: ~300, Errors: 0, Avg: <50ms

---

## STEP 8 – Test Data Persistence

```powershell
# 1. Create tasks in the UI at http://localhost:3000
# 2. Stop stack (KEEP database volume)
docker compose down

# 3. Restart
docker compose up -d

# 4. Open http://localhost:3000 -> tasks still there!
```

---

## STEP 9 – CI/CD Pipeline (GitHub)

To test the GitHub Actions pipeline:

```powershell
# From project root:
git init
git add .
git commit -m "Initial TaskBoard capstone"

# Create repo at https://github.com/new
# Then push:
git remote add origin https://github.com/YOUR_USERNAME/taskboard.git
git push -u origin main
```

Go to GitHub → Actions → watch the pipeline run:
- Stage 1 (Tests) runs automatically on every push
- Stage 2 (Build+Scan) runs only on pushes to `main`
- Stage 3 (Deploy) needs AWS secrets configured

---

## STEP 10 – Stop the Stack

```powershell
# Stop, keep database data
docker compose down

# Stop AND delete all data (fresh start)
docker compose down -v
```

---

## WHAT YOU DON'T NEED TO DO

- ❌ Install PostgreSQL locally (Docker Compose handles it)
- ❌ Create tables manually (Alembic migration runs automatically)
- ❌ Set any DATABASE_URL (docker-compose.yml configures it)
- ❌ Configure Nginx manually (it's in the frontend container)
- ❌ Install MongoDB (this project uses PostgreSQL)

---

## KNOWN WARNINGS (Not Errors)

These are completely normal:
- `asyncio.iscoroutinefunction is deprecated` – from FastAPI/Starlette library, not our code
- `LF will be replaced by CRLF` – normal on Windows, .gitattributes handles it
- `2 vulnerabilities (npm)` – in eslint devDependencies, not in production bundle
