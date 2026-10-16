# ── Frontend Dockerfile ───────────────────────────────────────────────────────
# Stage 1: Node.js build environment – compiles the React app
# Stage 2: Nginx runtime      – serves the static files only
# The final image does NOT contain Node.js, npm, or source files.
# ─────────────────────────────────────────────────────────────────────────────

# ── Stage 1: Build ────────────────────────────────────────────────────────────
FROM node:20-alpine AS builder

WORKDIR /app

# Install dependencies first (better caching – only re-runs if lockfile changes)
COPY package.json package-lock.json* ./
RUN npm ci --silent

# Copy source and build
COPY . .
RUN npm run build

# ── Stage 2: Nginx runtime ────────────────────────────────────────────────────
FROM nginx:1.27-alpine AS runtime

# Remove the default Nginx configuration
RUN rm /etc/nginx/conf.d/default.conf

# Copy our custom Nginx configuration
COPY nginx.conf /etc/nginx/conf.d/taskboard.conf

# Copy the compiled React application from the build stage
COPY --from=builder /app/dist /usr/share/nginx/html

# Nginx runs as root by default on port 80.
# For tighter security in Kubernetes, configure the Pod securityContext
# to run as non-root and map port 8080 – see the Helm chart values.
EXPOSE 80

# nginx in the foreground (docker stop sends SIGTERM which nginx handles gracefully)
CMD ["nginx", "-g", "daemon off;"]
