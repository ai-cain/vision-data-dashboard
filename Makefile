DC = docker compose

.PHONY: dev down logs build backend-shell frontend-shell db-shell migrate seed seed-reset docs-install docs-serve docs-build

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
