#!/usr/bin/env bash

set -e

BASE_URL="${1:-http://127.0.0.1:8080}"

echo "Generating traffic against: $BASE_URL"

echo "Calling /health 3 times..."
for i in 1 2 3; do
  curl -s "$BASE_URL/health" > /dev/null
done

echo "Calling /slow 2 times..."
for i in 1 2; do
  curl -s "$BASE_URL/slow" > /dev/null
done

echo "Calling /error 2 times..."
for i in 1 2; do
  curl -s "$BASE_URL/error" > /dev/null || true
done

echo "Traffic generation completed."
