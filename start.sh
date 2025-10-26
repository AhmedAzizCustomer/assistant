#!/bin/sh
set -e

# Use Railway's PORT or default to 8000
PORT=${PORT:-8000}

echo "🚀 Starting AI Personal Assistant on port $PORT..."

# Run uvicorn
exec uvicorn backend.src.main:app --host 0.0.0.0 --port "$PORT"
