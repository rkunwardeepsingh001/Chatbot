# Chatbot Frontend

This is a standalone React frontend for the Django chatbot API.

## Setup

1. Run the local frontend server:

```bash
cd frontend
npm run dev
```

2. Open the browser at:

```bash
http://localhost:5173
```

3. Start your Django backend at:

```bash
cd /home/developer/project/chatbot_project
python manage.py runserver
```

## Notes

- The app calls `/api/chat/` on the backend.
- The frontend is served as static files, so it does not require Vite or Node 16+.
- If `python3` is not available, run:

```bash
cd frontend
python -m http.server 5173
```
