# 🌿Quizzleef Question Manager

A simple Django-based Question Manager application created as part of my Python/Django learning journey. Questions that eventually will be used in different platforms that I haven't decided on yet. Easily managining those questions in a csv file did not sound so that cool enough so I decided to spend several hours learning and building this system instead. It's funny, I guess.

## Features
- Basic question management (CRUD operations)
- Categorize questions
- Search/filter functionality
- Simple Django admin interface
- (Future) Docker integration
- (Future) Take the questions in exam mode
- (Future) AI Integration analizing score and as a study buddy

## Installation
Define environment variables
```bash
cp .env_example .env
```

Replace .env with your information

Set environment variables (not recommended for Production)
```bash
export $(grep -v '^#' .env | xargs)
```


Create a virtual environment (only needed once):
Windows
```bash
python -m venv venv
.\venv\Scripts\activate
```
MacOS/Linux
```bash
python -m venv venv
source venv/bin/activate
```

Install requirements
```bash
pip install -r requirements.txt
```
```bash
pip install -r requirements-dev.txt
```

Run Migrations
```bash
python manage.py migrate
```

Create admin superuser
```bash
python manage.py createsuperuser
```

Run app
```bash
python manage.py runserver
```

## Docker (recommended)

With Docker, a PostgreSQL database and Django application will be automatically started. Migrations will be run and, optionally, a superuser will be created if you define the environment variables.

1) Copy example environment variables and edit them
```bash
cp .env_example .env
```

2) (Optional) Define superuser in `.env`
```dotenv
DJANGO_SUPERUSER_USERNAME=admin
DJANGO_SUPERUSER_EMAIL=admin@example.com
DJANGO_SUPERUSER_PASSWORD=admin
```

3) Start containers
```bash
docker compose up -d --build
```

4) View logs
```bash
docker compose logs -f web
```

5) Stop containers
```bash
docker compose down
```

6) Remove Postgres data (destructive)
```bash
docker compose down -v
```

Notes:
- Change the database, user and password in `.env` according to your preferences.
- The `pgdata` volume persists the database data between restarts.