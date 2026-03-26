# vision-data-dashboard

Real-time dashboard for computer vision pipeline metrics, edge telemetry, and industrial inspection results.

This repository is a full-stack reference implementation built around:

- Flask 3 + SQLAlchemy 2.0 + Alembic + PostgreSQL
- React 18 + TypeScript + Vite + Tailwind CSS + React Query + Recharts
- MkDocs + Mermaid documentation
- Docker Compose for local development

## Implementation Status

- [x] Backend application factory
- [x] SQLAlchemy models for devices, events, and inspections
- [x] Alembic initial migration in Python
- [x] Seed flow in Python
- [x] Dashboard pages for overview, devices, events, and inspections
- [x] MkDocs documentation
- [x] Auth hardening beyond local optional mode
- [x] WebSocket live stream
- [x] Automated backend/frontend test suites
- [x] CI skeleton

## Quick Start

### 1. Create the environment file

```bash
cp .env.example .env
```

### 2. Run the full stack

```bash
make dev
```

Services:

- Frontend: `http://localhost:5173`
- Backend API: `http://localhost:5000/api/v1`
- Swagger UI: `http://localhost:5000/api/v1/docs`
- WebSocket stream: `ws://localhost:5000/ws/events`
- PostgreSQL: `localhost:5432`

## Local Development Without Docker

### Backend

```bash
cd backend
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements-dev.txt
flask db upgrade
flask seed
flask run
```

### Frontend

```bash
cd frontend
npm install
npm run dev
```

## Realtime and Auth

Write endpoints can run in two modes:

- local bypass mode with `AUTH_REQUIRED=false`
- hardened mode with `AUTH_REQUIRED=true`

When hardened mode is enabled:

- `POST /api/v1/auth/token` issues a JWT from a configured API key
- `GET /api/v1/auth/me` resolves the current authenticated context
- write routes accept `Authorization: Bearer <token>` or `X-API-Key: <key>`

Realtime event updates are exposed through:

- `WS /ws/events`

The dashboard overview consumes that stream and updates recent events immediately while React Query polling remains as a fallback.

## Database Definition

The PostgreSQL schema is defined in Python, not through `init.sql`.

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
```

## Quality Checks

```bash
make test-backend
make test-frontend
make test
make docs-build
```

CI is defined in:

- `.github/workflows/ci.yml`

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

## Docs Index

- [Documentation home](docs/index.md)
- [Getting started](docs/getting-started.md)
- [Architecture](docs/architecture.md)
- [Database and migrations](docs/database.md)
- [Backend](docs/backend.md)
- [Frontend](docs/frontend.md)
- [API reference](docs/api.md)
- [Development workflow](docs/development-workflow.md)
