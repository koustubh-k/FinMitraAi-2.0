.PHONY: setup up down test lint clean

setup:
	cp -n .env.example .env || true
	pre-commit install

up:
	docker compose up -d

down:
	docker compose down

test-backend:
	cd apps/api && pytest -v tests/

lint:
	cd apps/api && ruff check . && ruff format --check .
	cd apps/web && npm run lint

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type d -name ".pytest_cache" -exec rm -rf {} +
	find . -type d -name ".ruff_cache" -exec rm -rf {} +
