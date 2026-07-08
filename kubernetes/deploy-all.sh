#!/bin/bash
# Run this script to deploy everything to Kubernetes in one go

echo "=== Step 1: Creating namespace ==="
kubectl apply -f namespace.yml

echo "=== Step 2: Deploying Redis ==="
kubectl apply -f redis/

echo "=== Step 3: Deploying Flask App ==="
kubectl apply -f app/

echo "=== Step 4: Deploying Nginx ==="
kubectl apply -f nginx/

echo "=== Step 5: Deploying Monitoring (Prometheus + Grafana) ==="
kubectl apply -f monitoring/

echo "=== Step 6: Deploying Node Exporter ==="
kubectl apply -f node-exporter/

echo ""
echo "=== Waiting for pods to be ready... ==="
kubectl wait --namespace devops-app --for=condition=ready pod --all --timeout=120s

echo ""
echo "=== All pods status ==="
kubectl get pods -n devops-app

echo ""
echo "=== Access URLs ==="
echo "App:        http://$(minikube ip):30080"
echo "Prometheus: http://$(minikube ip):30090"
echo "Grafana:    http://$(minikube ip):30030  (admin / admin123)"
