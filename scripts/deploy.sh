#!/bin/bash
# Quick redeploy script — run on server or call via SSH
set -e

APP_DIR="/opt/devops-app/docker"

echo "=== Pulling latest images ==="
cd $APP_DIR
docker compose pull

echo "=== Restarting containers ==="
docker compose up -d --remove-orphans

echo "=== Cleaning old images ==="
docker image prune -f

echo "=== Container status ==="
docker compose ps

echo "✅ Deploy complete at $(date)"
