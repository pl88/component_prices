.PHONY: run backend-up backend-down down test lint format check

run:
	docker compose up -d db
	docker compose run --build --rm scraper

backend-up:
	docker compose up -d db backend

backend-down:
	docker compose stop backend

down:
	docker compose down

test:
	pytest

lint:
	ruff check backend tests
	pyright

format:
	ruff format backend tests
	ruff check --fix backend tests

check: format lint test
