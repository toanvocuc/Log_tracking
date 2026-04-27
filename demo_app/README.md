# Demo App

A small FastAPI application used to generate realistic logs for the log-investigator project.

## Endpoints

- `/health` - health check
- `/slow` - simulates a slow response
- `/error` - simulates an error response

## Run

```bash
uvicorn demo_app.app.main:app --host 0.0.0.0 --port 8000
