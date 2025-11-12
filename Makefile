.RECIPEPREFIX := >
.DEFAULT_GOAL := help
COMPOSE := docker compose
API_HOST ?= 0.0.0.0
API_PORT ?= 8000

.PHONY: help
help:

	@echo "Targets:"
	@echo " up - build & start all services"
	@echo " down - stop and remove services"
	@echo " restart - restart api & worker"
	@echo " logs - follow api/worker logs"
	@echo " ps - list compose services"
	@echo " migrate - alembic revision --autogenerate"
	@echo " upgrade - alembic upgrade head"
	@echo " downgrade - alembic downgrade -1"
	@echo " api - run uvicorn locally (no docker)"
	@echo " worker - run dramatiq worker locally"
	@echo " fmt - ruff import/order + lint fix"
	@echo " test - pytest"

.PHONY: up
up:

	$(COMPOSE) up -d --build

.PHONY: down
down:

	$(COMPOSE) down

.PHONY: restart
restart:

	$(COMPOSE) restart api worker

.PHONY: logs
logs:

	$(COMPOSE) logs -f --tail=200 api worker

.PHONY: ps
ps:

	$(COMPOSE) ps

.PHONY: migrate
migrate:

	alembic revision --autogenerate -m "auto"

.PHONY: upgrade
upgrade:

	alembic upgrade head

.PHONY: downgrade
downgrade:

	alembic downgrade -1

.PHONY: api
api:

	uvicorn app.main:create_app --factory --host $(API_HOST) --port $(API_PORT) --reload

.PHONY: worker
worker:

	python -m app.workers.worker

.PHONY: fmt
fmt:

	ruff check --select I --fix .
	ruff check --fix .

.PHONY: test
test:

	pytest -q

.PHONY: dev

env-local:
	@set -a; . ops/env/.env.local; set +a; env | grep -E '^(APP_ENV|PG_DSN|REDIS_URL|OS_URL|API_|JWT_|CORS_|OTEL_)'

migrate:
	@set -a; . ops/env/.env.local; set +a; alembic revision --autogenerate -m "$(m)"

upgrade:
	@set -a; . ops/env/.env.local; set +a; alembic upgrade head

seed-admin:
	@set -a; . ops/env/.env.local; set +a; python -m app.apps.users.seed_admin

seed-viewer:
	@set -a; . ops/env/.env.local; set +a; python -m app.apps.users.seed_viewer

dev:
	@ops/dev.sh