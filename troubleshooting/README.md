# Troubleshooting Lab – README
# =============================================================================
# ⚠ WARNING: The manifests in this directory are INTENTIONALLY BROKEN.
# They are designed for educational troubleshooting exercises ONLY.
# Do NOT apply them to a production cluster.
# =============================================================================

## Exercise A – ImagePullBackOff (broken-image.yaml)

**File**: `broken-image.yaml`

### Symptoms
```
kubectl get pods -n taskboard -l app=taskboard-broken-image
NAME                                     READY   STATUS             RESTARTS
taskboard-broken-image-xxx               0/1     ImagePullBackOff   0
```

### Investigation
```powershell
# Step 1: Get pod name
kubectl get pods -n taskboard -l app=taskboard-broken-image

# Step 2: Describe the pod – look at Events section
kubectl describe pod <POD_NAME> -n taskboard

# Step 3: View cluster events sorted by time
kubectl get events -n taskboard --sort-by=.lastTimestamp

# Step 4: Read the error message
# You will see: Failed to pull image "...v99.99.99-does-not-exist": not found
```

### Root Cause
The Deployment references image tag `v99.99.99-does-not-exist` which does not exist in the registry.

### Fix
```powershell
# Option A: Patch the deployment
kubectl set image deployment/taskboard-broken-image `
  broken=ghcr.io/your-org/taskboard-backend:dev `
  -n taskboard

# Option B: Edit the YAML and reapply
# Change: image: ghcr.io/your-org/taskboard-backend:v99.99.99-does-not-exist
# To:     image: ghcr.io/your-org/taskboard-backend:dev
kubectl apply -f broken-image.yaml
```

### Verification
```powershell
kubectl get pods -n taskboard -l app=taskboard-broken-image
# Expected: STATUS = Running, READY = 1/1
```

---

## Exercise B – Service Selector Mismatch (broken-service.yaml)

**File**: `broken-service.yaml`

### Symptoms
```
# No traffic reaches backend through this service
kubectl get endpoints taskboard-broken-service -n taskboard
NAME                      ENDPOINTS   AGE
taskboard-broken-service  <none>      30s
```

### Investigation
```powershell
# Step 1: Check the service selector
kubectl get svc taskboard-broken-service -n taskboard -o yaml
# Look for: spec.selector – note the label key/value

# Step 2: Check what labels the backend pods actually have
kubectl get pods -n taskboard --show-labels
# Compare pod labels with the service selector

# Step 3: Confirm endpoints are empty
kubectl describe endpoints taskboard-broken-service -n taskboard

# Step 4: Test connectivity (should timeout or refuse)
kubectl run debug --image=curlimages/curl --restart=Never -n taskboard -- `
  curl -s http://taskboard-broken-service:8000/health
kubectl logs debug -n taskboard
kubectl delete pod debug -n taskboard
```

### Root Cause
The Service selector `app: taskboard-backend-WRONG` does not match any Pod labels.
Backend pods have label: `app.kubernetes.io/component: backend`.
When the selector matches no pods, the Service has no endpoints and traffic cannot be routed.

### Fix
```powershell
# Patch the service selector to the correct label
kubectl patch svc taskboard-broken-service -n taskboard `
  --type='merge' `
  -p='{"spec":{"selector":{"app.kubernetes.io/component":"backend"}}}'

# Or edit directly
kubectl edit svc taskboard-broken-service -n taskboard
# Change the selector section
```

### Verification
```powershell
kubectl get endpoints taskboard-broken-service -n taskboard
# Expected: ENDPOINTS shows <pod-ip>:8000

# Test connectivity
kubectl run debug --image=curlimages/curl --restart=Never -n taskboard -- `
  curl -s http://taskboard-broken-service:8000/health
kubectl logs debug -n taskboard
# Expected: {"status":"ok"}
```

---

## Additional Diagnostic Scenarios (Optional)

### C – Database Connection Failure
1. Set wrong `DATABASE_URL` in the secret
2. Observe: `/ready` returns 503, pods may CrashLoop
3. Fix: Correct the secret, restart pods
4. Commands: `kubectl edit secret taskboard-db-secret`, `kubectl rollout restart deployment/taskboard-backend`

### D – Failed Readiness Probe
1. Set `readinessProbe.path: /nonexistent`
2. Observe: Pods never become Ready, traffic not sent to them
3. Fix: Restore correct probe path
4. Understand: liveness vs readiness probe difference

### E – Missing Secret
1. Delete the database secret
2. Observe: Pods stuck in `CreateContainerConfigError`
3. Fix: Recreate the secret
4. Commands: `kubectl get events -n taskboard`

### F – OOMKilled
1. Set memory limit to `32Mi`
2. Observe: Pod repeatedly killed with OOMKilled status
3. Fix: Increase memory limits
4. Commands: `kubectl describe pod`, `kubectl top pod`

### G – CrashLoopBackOff
1. Set a wrong environment variable (bad DATABASE_URL format)
2. Observe: Pod starts, crashes, restarts, backs off
3. Fix: Correct the environment variable
4. Commands: `kubectl logs --previous`

### H – Ingress 404 / 502
1. Apply Ingress without installing the Ingress Controller
2. Observe: Browser returns 404 or times out
3. Fix: Install ingress-nginx, wait for LoadBalancer IP
4. Commands: `kubectl describe ingress`, `kubectl get svc -n ingress-nginx`
