#!/usr/bin/env bash

set -e

INPUT_LOG="${1:-demo_app/logs/app.log}"
CONFIG_FILE="${2:-config/rule.json}"
OUTPUT_REPORT="${3:-reports/demo_app_report.txt}"

echo "Running log quality gate..."
echo "Input log: $INPUT_LOG"
echo "Config: $CONFIG_FILE"
echo "Output report: $OUTPUT_REPORT"

PYTHONPATH=src python3 -m log_investigator.main \
  --input "$INPUT_LOG" \
  --config "$CONFIG_FILE" \
  --output "$OUTPUT_REPORT"

echo
echo "Log quality gate completed."
echo "Report preview:"
echo "----------------------------------------"
cat "$OUTPUT_REPORT"
echo "----------------------------------------"
