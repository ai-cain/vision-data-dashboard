# vision-data-dashboard

Real-time dashboard for computer vision pipeline metrics, edge telemetry, and industrial inspection results.

The project is built as a full-stack reference implementation:

- Backend: Flask 3, SQLAlchemy 2.0, Alembic, PostgreSQL 16
- Frontend: React 18, TypeScript, Vite, Tailwind CSS, React Query, Recharts
- Dev environment: Docker Compose
- Documentation: MkDocs + Mermaid

## Current Status

The repository already includes:

- PostgreSQL-oriented backend configuration
- SQLAlchemy models and Alembic migration in Python
- REST API for devices, events, inspections, and dashboard stats
- Seed data generator in Python
- React dashboard with overview, devices, events, and inspections pages
- MkDocs documentation in `docs/`

## Quick Start

### 1. Environment

```bash
cp .env.example .env
```

### 2. Run with Docker

```bash
make dev
```

Services:

- Frontend: `http://localhost:5173`
- Backend API: `http://localhost:5000/api/v1`
- Swagger UI: `http://localhost:5000/api/v1/docs`
- PostgreSQL: `localhost:5432`

## Local Development Without Docker

### Backend

```bash
cd backend
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
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

## Documentation

Detailed project docs live in `docs/` and can be served locally with MkDocs.

```bash
make docs-install
make docs-serve
```

Or directly:

```bash
python -m pip install -r docs/requirements.txt
python -m mkdocs serve
```

## Database Definition

The schema is not defined through an `init.sql` script.

It is defined in Python in two places:

- SQLAlchemy models in `backend/app/models/`
- Alembic migration files in `backend/migrations/versions/`

PostgreSQL schema changes are applied with:

```bash
flask db upgrade
```

## Useful Commands

```bash
make dev
make down
make migrate
make seed
make seed-reset
make docs-build
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
