# ==============================
# AnswerMe AI — Frontend Dockerfile
# ==============================
# Multi-stage build for React + Vite SPA.
#
# Stage 1 (builder): Install deps, build static files with Vite
# Stage 2 (production): Serve static files with Nginx (no Node.js in prod!)
#
# Why Nginx for serving?
#   - Vite is a BUILD tool, not a production server
#   - Nginx serves static files 10-50x faster than Node.js
#   - Handles gzip, caching headers, and SPA routing (try_files)
#   - Final image is ~25MB (alpine nginx) vs ~300MB (node)
#
# Usage:
#   docker build -t answerme-frontend .
#   docker run -p 5173:80 answerme-frontend

# ──────────────────────────────
# Stage 1: Builder
# ──────────────────────────────
FROM node:22-alpine AS builder

WORKDIR /build

# Copy dependency files first (Docker layer caching)
COPY package.json package-lock.json* ./

# Install dependencies
# --frozen-lockfile: fail if lock file is out of sync (CI safety)
RUN npm ci --frozen-lockfile 2>/dev/null || npm install

# Copy source code
COPY . .

# Build the production bundle
# Vite outputs to dist/ by default
RUN npm run build

# ──────────────────────────────
# Stage 2: Production (Nginx)
# ──────────────────────────────
FROM nginx:alpine AS production

# Copy custom Nginx config for SPA routing
# This handles client-side routing: all routes → index.html
COPY nginx.conf /etc/nginx/conf.d/default.conf

# Copy built static files from builder
COPY --from=builder /build/dist /usr/share/nginx/html

# Expose port 80
EXPOSE 80

# Nginx runs as PID 1
CMD ["nginx", "-g", "daemon off;"]
