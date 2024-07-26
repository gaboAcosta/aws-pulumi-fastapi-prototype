# Sample Makefile for running a FastAPI app and managing development tasks

# Define the Python interpreter to use
PYTHON = python
UVICORN = uvicorn
APP_FILE = api:app

# Install dependencies
install:
	pip install -r requirements.txt

# Run the FastAPI app using uvicorn
run:
	$(UVICORN) $(APP_FILE) --reload

# Autogenerate alembic migrations
autogen:
	alembic revision --autogenerate

# Run database migrations
migrate:
	alembic upgrade head

# Rollback database migrations
rollback:
	alembic downgrade -1

# Generate requirements.txt file with current dependencies
freeze:
	pip freeze > requirements.txt

# Run pytest for testing
test:
	pytest

# Run pytest for testing and watch for changes
test-watch:
	ptw

# Clean up compiled Python files
clean:
	find . -type f -name '*.pyc' -delete
	find . -type d -name __pycache__ -delete

db-up:
	docker-compose up -d

db-stop:
	docker-compose stop

db-down:
	docker-compose down

# Help - Display available commands
help:
	@echo "Please use 'make <target>' where <target> is one of"
	@echo "  install     to install dependencies"
	@echo "  run         to run the FastAPI app using uvicorn"
	@echo "  migrate     to run database migrations"
	@echo "  rollback    to rollback database migrations"
	@echo "  freeze      to generate requirements.txt file with current dependencies"
	@echo "  test        to run pytest for testing"
	@echo "  test-watch  to run pytest for testing and watch for changes"
	@echo "  clean       to clean up compiled Python files"
	@echo "  help        to display this help message"

# Default target
.DEFAULT_GOAL := help