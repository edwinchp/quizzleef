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

# Start script baked into CMD (no entrypoint)
CMD bash -lc ' \
  if [ -n "${DB_HOST:-}" ]; then \
    echo "Waiting for Postgres at ${DB_HOST}:${DB_PORT:-5432}..."; \
    until pg_isready -h "${DB_HOST}" -p "${DB_PORT:-5432}" -U "${DB_USER:-postgres}" >/dev/null 2>&1; do \
      sleep 1; \
    done; \
  fi; \
  python manage.py migrate --noinput; \
  if [ -n "${DJANGO_SUPERUSER_USERNAME:-}" ] && [ -n "${DJANGO_SUPERUSER_EMAIL:-}" ] && [ -n "${DJANGO_SUPERUSER_PASSWORD:-}" ]; then \
    echo "Ensuring Django superuser exists: ${DJANGO_SUPERUSER_USERNAME}"; \
    python manage.py createsuperuser --noinput --username "${DJANGO_SUPERUSER_USERNAME}" --email "${DJANGO_SUPERUSER_EMAIL}" || true; \
  fi; \
  python manage.py runserver 0.0.0.0:8000 \
'
