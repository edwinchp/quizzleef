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

Install requirements
```bash
pip install -r requirements.txt
```
```bash
pip install -r requirements-dev.txt
```
Run app
```bash
python manage.py runserver
```

## Docker Image
```bash
docker compose -f 'docker-compose.yml' up -d --build 'web' 
```