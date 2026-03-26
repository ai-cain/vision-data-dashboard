# Development Workflow

## Daily commands

### Environment

```bash
cp .env.example .env
```

### Start full stack

```bash
make dev
```

### Stop full stack

```bash
make down
```

### Create PostgreSQL database

```bash
make db-create
```

### Reset PostgreSQL database

```bash
make db-reset
```

### Delete PostgreSQL database

```bash
make db-delete
```

### Run migrations

```bash
make migrate
```

### Seed data

```bash
make seed
```

### Reset and reseed

```bash
make seed-reset
```

### Run tests

```bash
make test-backend
make test-frontend
make test
```

### Serve docs

```bash
make docs-install
make docs-serve
```

### Run the local CI bundle

```bash
make ci-local
```

## Suggested change flow

```mermaid
flowchart TD
    A[Change model service or page] --> B[Update schema route hook or UI]
    B --> C[Run backend tests]
    C --> D[Run frontend tests]
    D --> E[Run frontend build]
    E --> F[Build MkDocs]
    F --> G[Commit by phase]
```

## What to change when

### Schema change

Touch:

- `backend/app/models/`
- `backend/migrations/versions/`

### API change

Touch:

- `backend/app/routes/`
- `backend/app/services/`
- `backend/app/schemas/`

### Realtime change

Touch:

- `backend/app/routes/stream.py`
- `backend/app/services/live_stream_service.py`
- `frontend/src/hooks/useDashboardLiveStream.ts`
- `frontend/src/lib/live-stream.ts`

### Frontend data change

Touch:

- `frontend/src/types/models.ts`
- `frontend/src/lib/api.ts`
- `frontend/src/hooks/`
- `frontend/src/pages/`

### Documentation change

Touch:

- `README.md`
- `mkdocs.yml`
- `docs/`

## Validation checklist

Run these before pushing:

- `cd backend && .venv\Scripts\pytest`
- `cd frontend && npm run test`
- `cd frontend && npm run build`
- `python -m mkdocs build --strict`

CI then re-checks the same areas from `.github/workflows/ci.yml`.
