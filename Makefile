.PHONY: run down test lint format check

run:
	docker compose up -d db
	docker compose run --build --rm scraper

down:
	docker compose down

test:
	pytest

lint:
	ruff check scraper tests
	pyright

format:
	ruff format scraper tests
	ruff check --fix scraper tests

check: format lint test
