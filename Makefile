.PHONY: fmt check tests

fmt:
	poetry run ruff format .
	poetry run ruff check --fix .

check:
	poetry run ruff format --check .
	poetry run ruff check .
	poetry run mypy src/

tests:
	poetry run pytest -vvv -s tests
