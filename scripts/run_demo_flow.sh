#!/usr/bin/env bash

set -e

PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

echo "Project root: $PROJECT_ROOT"
echo "Starting demo flow..."

cd "$PROJECT_ROOT/demo_app"

echo
echo "[1/5] Stopping old containers if any..."
docker compose down || true

echo
echo "[2/5] Starting demo app with Docker Compose..."
docker compose up --build -d

echo
echo "[3/5] Waiting for app to become ready..."
sleep 5

cd "$PROJECT_ROOT"

echo
echo "[4/5] Generating demo traffic..."
./scripts/generate_traffic.sh

echo
echo "[5/5] Running log quality gate..."
./scripts/run_log_quality_gate.sh demo_app/logs/app.log config/rule.json reports/demo_app_report.txt

echo
echo "Demo flow completed."
echo "----------------------------------------"
echo "Generated log file: demo_app/logs/app.log"
echo "Generated report:   reports/demo_app_report.txt"
echo "----------------------------------------"

echo
echo "Report preview:"
cat reports/demo_app_report.txt
