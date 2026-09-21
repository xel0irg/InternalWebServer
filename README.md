# InternalWebServer

Internal web server built with Python + Flask, with a plain HTML/CSS/JavaScript front end.

## Quick start (Windows PowerShell)

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python app.py
```

Then open http://127.0.0.1:8080

## Endpoints

| Route         | Purpose                          |
|---------------|----------------------------------|
| `/`           | Home page                        |
| `/health`     | Health check (JSON)              |
| `/api/info`   | Server info (JSON), used by the page |

## Configuration

Copy `.env.example` to `.env` and adjust. Settings:

- `HOST`: bind address (default `127.0.0.1`, local only)
- `PORT`: port (default `8080`)
- `FLASK_DEBUG`: `1` for auto-reload and debugger (never in production)

## Tests

```powershell
python -m pytest
```

## Workflow

Work happens on feature branches (e.g. `feature/local-web-server`), never directly on `main`.
