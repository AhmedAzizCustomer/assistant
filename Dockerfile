# Multi-stage build for the AI Personal Assistant

# Stage 1: Build frontend
FROM node:18-alpine as frontend-build
WORKDIR /app/frontend
COPY frontend/package*.json ./
RUN npm install
COPY frontend/ ./
RUN npm run build

# Stage 2: Setup Python backend
FROM python:3.11-slim

WORKDIR /app

# Install system dependencies (including build tools for cryptography)
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    make \
    libffi-dev \
    libssl-dev \
    cargo \
    rustc \
    && rm -rf /var/lib/apt/lists/*

# Copy backend requirements and install
COPY backend/requirements.txt ./backend/requirements.txt
RUN pip install --no-cache-dir -r backend/requirements.txt

# Copy backend code
COPY backend/ ./backend/

# Copy built frontend
COPY --from=frontend-build /app/frontend/build ./frontend/build

# Copy startup script
COPY run.py ./run.py

# Create data directory for SQLite
RUN mkdir -p /app/data

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV DATABASE_URL=sqlite:////app/data/assistant.db
ENV PYTHONPATH=/app

# Expose port
EXPOSE 8000

# Run the application
CMD ["python", "run.py"]
