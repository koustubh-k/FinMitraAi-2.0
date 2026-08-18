.PHONY: up down logs test lint

up:
	docker compose up --build -d

down:
	docker compose down

logs:
	docker compose logs -f

test:
	cd apps/api && python -m pytest

lint:
	cd apps/api && ruff check .
	cd apps/web && npm run lint
