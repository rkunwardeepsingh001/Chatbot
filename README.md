# Chatbot Project

A Django-based chatbot backend with a static frontend served from the `frontend/` directory.

## Features

- Django REST API powered by `djangorestframework`
- AI response generation using Google Gemini via `google-generativeai`
- Environment configuration from `.env`
- Dockerized backend and frontend services

## Project structure

- `chat/` — Django app logic, views, models, and AI service
- `chatbot_project/` — Django project settings, URLs, WSGI/ASGI
- `frontend/` — static frontend assets and simple HTTP server setup
- `Dockerfile` — backend image definition
- `docker-compose.yml` — service orchestration for backend and frontend
- `requirements.docker.txt` — backend runtime dependencies for Docker
- `.env` — local environment variables (not committed)

## Setup

1. Copy `.env` and set values:

```bash
cp .env .env.local
```

2. Edit `.env.local` and set your API key:

```text
DJANGO_SECRET_KEY=replace-me-with-a-secure-key
DJANGO_DEBUG=True
DJANGO_ALLOWED_HOSTS=localhost,127.0.0.1
DATABASE_URL=sqlite:///db.sqlite3
GOOGLE_API_KEY=YOUR_GOOGLE_API_KEY
API_BASE_URL=http://localhost:8000
```

3. If you are running without Docker, install Python dependencies:

```bash
pip install -r requirements.txt
python3 -m pip install -r requirements.docker.txt
```

## Docker

Use Docker Compose to build and run both services:

```bash
sudo docker compose up --build
```

Stop the services with:

```bash
sudo docker compose down
```

If Docker requires root access on your system, use:

```bash
sudo docker compose up --build
```

## Access

- Backend: `http://localhost:8000`
- Frontend: `http://localhost:5173`

## Notes

- The current backend is configured for development only.
- `google.generativeai` is currently used in `chat/ai_service.py`, but it is deprecated and should be updated to `google.genai` in a future upgrade.
- `.env` is excluded by `.gitignore` and should never be committed.

## Useful commands

```bash
# Run Django migrations
python3 manage.py migrate

# Run backend locally
python3 manage.py runserver

# Run frontend locally
cd frontend && npm run dev
```
