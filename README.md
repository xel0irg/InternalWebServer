# InternalWebServer

An internal resource hub: a searchable page of the team's links and tools, built with
Python + Flask and a plain HTML/CSS/JavaScript front end.

Content comes from a single file, [`data/links.json`](data/links.json), so updating the
page means editing JSON and refreshing the browser. No database, no restart.

The site is served at **http://hub.internal.rg**

## One-time setup: the hostname

`hub.internal.rg` is not a public domain, so each machine that uses it needs a line in
its Windows hosts file pointing the name at itself. That file is system-owned, so this
is the one step that needs Administrator rights.

1. Right-click the Start button and choose **Terminal (Admin)** (or **Windows PowerShell
   (Admin)**), then approve the User Account Control prompt.
2. In that window run:

   ```powershell
   cd C:\Users\nonon\Desktop\internal-web
   powershell -ExecutionPolicy Bypass -File .\scripts\add-hosts-entry.ps1
   ```

The script backs up the hosts file, adds `127.0.0.1  hub.internal.rg`, flushes the DNS
cache and confirms the name resolves. Running it twice is harmless.

Check it yourself with `ping hub.internal.rg`, which should answer from `127.0.0.1`.
To undo it, edit `C:\Windows\System32\drivers\etc\hosts` in an elevated Notepad and
delete the line.

## Quick start (Windows PowerShell)

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
copy .env.example .env
python app.py
```

Then open http://hub.internal.rg

`Activate.ps1` must be run in each new terminal, before `python app.py`. It is what makes
`python` mean the project's `.venv` copy, which has Flask installed. If activation is
blocked by the execution policy, either run
`Set-ExecutionPolicy -Scope CurrentUser RemoteSigned` and **open a new terminal**, or skip
activation entirely and run the virtual environment's Python directly:

```powershell
.\.venv\Scripts\python.exe app.py
```

## Editing the page content

Each entry in `data/links.json` looks like this:

```json
{
  "name": "Development",
  "links": [
    {
      "title": "Source control",
      "url": "https://github.com/xel0irg/InternalWebServer",
      "description": "This project's repository.",
      "tags": ["git", "code", "repo"]
    }
  ]
}
```

`title` and `url` are required; `description` and `tags` are optional. Tags are
searchable, so they are worth filling in. If the file has a mistake in it, the page
shows what is wrong instead of crashing.

## Endpoints

| Route         | Purpose                              |
|---------------|--------------------------------------|
| `/`           | The resource hub page                |
| `/api/links`  | The catalogue as JSON                |
| `/health`     | Health check (JSON)                  |
| `/api/info`   | Server info (JSON)                   |

## Configuration

Copy `.env.example` to `.env` and adjust:

- `HOST`: bind address (default `127.0.0.1`, reachable only from this machine)
- `PORT`: port (default `80`, so the URL needs no `:port` suffix)
- `FLASK_DEBUG`: `1` for auto-reload and the debugger (never in production)

If something else already uses port 80, set `PORT=8080` and browse to
http://hub.internal.rg:8080

To let others on the network reach the server, set `HOST=0.0.0.0`, turn `FLASK_DEBUG`
off, and serve it behind a production server such as Waitress rather than Flask's
built-in development server.

## Tests

```powershell
python -m pytest
```

## Project layout

```
app.py              Flask routes and entry point
links.py            Loads and validates data/links.json
data/links.json     The link catalogue (edit this)
templates/          index.html (the hub), error.html (config problems)
static/css, static/js   Styling and the client-side search
tests/              pytest suite
```

## Workflow

Work happens on feature branches (e.g. `feature/local-web-server`), never directly on `main`.
