# Vision Data Dashboard

Vision Data Dashboard is a full-stack reference app for monitoring computer vision pipelines, edge telemetry, and industrial inspection results in real time.

## What This Repo Includes

- Flask API for telemetry, events, inspections, auth, and Swagger docs
- React dashboard for overview, devices, events, and inspections
- WebSocket live stream for recent event updates
- PostgreSQL schema managed with SQLAlchemy and Alembic
- MkDocs documentation with Mermaid diagrams
- Docker Compose setup for local development

## Stack

- Backend: Flask 3, SQLAlchemy 2.0, Alembic, PostgreSQL
- Frontend: React 18, TypeScript, Vite, Tailwind CSS, React Query, Recharts
- Docs: MkDocs
- Tooling: Docker Compose, Makefile, backend/frontend test suites

## Quick Start

### 1. Create the environment file

```bash
cp .env.example .env
```

PowerShell alternative:

```powershell
Copy-Item .env.example .env
```

### 2. Start the full stack

```bash
make dev
```

### 3. Open the services

- Frontend: `http://localhost:5173`
- Backend API: `http://localhost:5000/api/v1`
- Swagger UI: `http://localhost:5000/api/v1/docs`
- WebSocket stream: `ws://localhost:5000/ws/events`
- PostgreSQL: `localhost:5432`

Useful helpers:

```bash
make logs
make down
```

## Local Development Without Docker

### Backend

```powershell
cd backend
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements-dev.txt
flask db upgrade
flask seed
flask run
```

### Frontend

```powershell
cd frontend
npm install
npm run dev
```

## Auth and Realtime

Write endpoints support two modes:

- local development mode with `AUTH_REQUIRED=false`
- hardened mode with `AUTH_REQUIRED=true`

When hardened mode is enabled:

- `POST /api/v1/auth/token` issues a JWT from a configured API key
- `GET /api/v1/auth/me` resolves the current authenticated context
- write routes accept `Authorization: Bearer <token>` or `X-API-Key: <key>`

Realtime event updates are exposed through:

- `WS /ws/events`

The dashboard consumes that stream for recent event updates, with React Query polling as a fallback.

## Database Workflow

The PostgreSQL schema is defined in Python, not through a raw SQL bootstrap script.

Source of truth:

- `backend/app/models/`
- `backend/migrations/versions/`

Database lifecycle commands:

```bash
flask db-create
flask db-reset --yes-i-know
flask db-delete --yes-i-know
```

Makefile shortcuts:

```bash
make db-create
make db-reset
make db-delete
make seed
make seed-reset
```

## Testing and Docs

```bash
make test-backend
make test-frontend
make test
make docs-build
make docs-serve
```

CI is defined in `.github/workflows/ci.yml`.

## Documentation

Detailed docs live in `docs/` and are served through MkDocs.

```bash
make docs-install
make docs-serve
```

Or directly:

```bash
python -m pip install -r docs/requirements.txt
python -m mkdocs serve
```

Docs index:

- [Documentation home](docs/index.md)
- [Getting started](docs/getting-started.md)
- [Architecture](docs/architecture.md)
- [Database and migrations](docs/database.md)
- [Backend](docs/backend.md)
- [Frontend](docs/frontend.md)
- [API reference](docs/api.md)
- [Development workflow](docs/development-workflow.md)
