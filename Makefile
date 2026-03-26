DC = docker compose

.PHONY: dev down logs build backend-shell frontend-shell db-shell db-create db-reset db-delete migrate seed seed-reset docs-install docs-serve docs-build test-backend test-frontend test ci-local

dev:
	$(DC) up --build

down:
	$(DC) down -v

logs:
	$(DC) logs -f

build:
	$(DC) build

backend-shell:
	$(DC) exec backend sh

frontend-shell:
	$(DC) exec frontend sh

db-shell:
	$(DC) exec db psql -U $$POSTGRES_USER -d $$POSTGRES_DB

db-create:
	$(DC) exec backend flask db-create

db-reset:
	$(DC) exec backend flask db-reset --yes-i-know

db-delete:
	$(DC) exec backend flask db-delete --yes-i-know

migrate:
	$(DC) exec backend flask db upgrade

seed:
	$(DC) exec backend flask seed

seed-reset:
	$(DC) exec backend flask seed --truncate

docs-install:
	python -m pip install -r docs/requirements.txt

docs-serve:
	python -m mkdocs serve

docs-build:
	python -m mkdocs build --strict

test-backend:
	backend/.venv/Scripts/python -m pytest backend/tests

test-frontend:
	cd frontend && npm run test

test:
	$(MAKE) test-backend
	$(MAKE) test-frontend

ci-local:
	$(MAKE) test
	$(MAKE) docs-build
