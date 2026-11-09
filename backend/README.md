# Chat.com backend

FastAPI service skeleton. Python 3.11+ is recommended.

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
uvicorn app.main:app --reload --host 0.0.0.0 --port 8059
```

- Health: `GET /health`
- API system info: `GET /api/v1/system`
- Interactive API docs: `/docs`

Run checks with `pytest`. SQLite is only the local development default; configure PostgreSQL before deployment. Authentication and messaging endpoints are not implemented yet.
