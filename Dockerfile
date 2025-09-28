FROM python:3.11-slim

# Prevents Python from writing .pyc files and enables unbuffered logs
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

# System deps (psql client for healthchecks and wait, and bash)
RUN apt-get update && apt-get install -y --no-install-recommends \
    postgresql-client \
    bash \
  && rm -rf /var/lib/apt/lists/*

# Install Python dependencies first for better caching
COPY requirements.txt /app/requirements.txt
RUN pip install --upgrade pip && \
    pip install -r requirements.txt

# Copy project files
COPY . /app
EXPOSE 8000
