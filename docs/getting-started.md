# Getting Started

## Prerequisites

- Python 3.11+
- Node 20+
- Docker Desktop or Docker Engine
- PostgreSQL 16 if running without Docker

## Environment file

Create the root `.env` file from the project example:

```bash
cp .env.example .env
```

Main variables:

| Variable | Purpose |
| --- | --- |
| `POSTGRES_DB` | PostgreSQL database name |
| `POSTGRES_USER` | PostgreSQL user |
| `POSTGRES_PASSWORD` | PostgreSQL password |
| `DATABASE_URL` | SQLAlchemy connection string |
| `AUTH_REQUIRED` | Enables hardened write auth |
| `AUTH_ALLOW_LOCAL_BYPASS` | Keeps local write bypass when auth is off |
| `ADMIN_API_KEYS` | Comma-separated API keys for token issuance or direct write access |
| `JWT_ACCESS_TOKEN_EXPIRES_MINUTES` | JWT access token lifetime |
| `VITE_API_BASE_URL` | Frontend API base URL |
| `VITE_WS_EVENTS_URL` | Frontend WebSocket URL for live events |

## Run with Docker

```bash
make dev
```

Services:

- Frontend: `http://localhost:5173`
- Backend: `http://localhost:5000`
- Swagger: `http://localhost:5000/api/v1/docs`
- WebSocket: `ws://localhost:5000/ws/events`
- PostgreSQL: `localhost:5432`

## Run without Docker

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

## Verify the project locally

```bash
make test
make docs-build
```

## Serve the docs

Install doc dependencies:

```bash
python -m pip install -r docs/requirements.txt
```

Start the docs server:

```bash
python -m mkdocs serve
```

Build the docs strictly:

```bash
python -m mkdocs build --strict
```

## Recommended project workflow

```mermaid
flowchart TD
    A[Create .env] --> B[Install dependencies]
    B --> C[Run flask db upgrade]
    C --> D[Seed local data]
    D --> E[Run frontend and backend]
    E --> F[Run tests and docs build]
```
