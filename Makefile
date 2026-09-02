.PHONY: up down logs test lint

up:
	docker compose up --build

down:
	docker compose down

logs:
	docker compose logs -f

test:
	docker compose run --rm backend pytest

lint:
	cd frontend && npm run lint && npm run typecheck

