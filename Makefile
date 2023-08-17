.PHONY: fmt check tests

fmt:
	poetry run black .
	poetry run ruff --fix .

check:
	poetry run black . --check
	poetry run ruff .
	poetry run mypy src/

tests:
	poetry run pytest -vvv -s tests
