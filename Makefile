.PHONY: dev format lint check

dev:
	uvicorn app.main:app --reload

format:
	ruff format app tests
	ruff check --fix app tests

lint:
	ruff check app tests
	mypy app tests
	bandit -r app -x tests

check: format lint
