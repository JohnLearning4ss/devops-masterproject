#!/bin/bash
# Run this ONCE on a fresh Ubuntu server to manually set up prerequisites

set -e

echo "=== Installing Docker ==="
curl -fsSL https://get.docker.com | sh
sudo usermod -aG docker $USER

echo "=== Installing Docker Compose ==="
sudo apt-get install -y docker-compose-plugin

echo "=== Cloning project ==="
git clone https://github.com/YOUR_USERNAME/devops-masterproject.git /opt/devops-app

echo "=== Starting stack ==="
cd /opt/devops-app/docker
docker compose up -d --build

echo ""
echo "✅ Done! Access your app at: http://$(curl -s ifconfig.me)"
echo "   Grafana at:               http://$(curl -s ifconfig.me):3000"
