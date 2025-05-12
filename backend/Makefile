# Build configuration
# -------------------

APP_NAME := `sed -n 's/^ *name.*=.*"\([^"]*\)".*/\1/p' pyproject.toml`
APP_VERSION := `sed -n 's/^ *version.*=.*"\([^"]*\)".*/\1/p' pyproject.toml`
GIT_REVISION = `git rev-parse HEAD`


# ------------------------------
# Help target
# ------------------------------
.PHONY: help
help: header targets

.PHONY: header
header:
	@echo "\033[34mEnvironment\033[0m"
	@echo "\033[34m---------------------------------------------------------------\033[0m"
	@printf "\033[33m%-23s\033[0m" "APP_NAME"
	@printf "\033[35m%s\033[0m" $(APP_NAME)
	@echo ""
	@printf "\033[33m%-23s\033[0m" "APP_VERSION"
	@printf "\033[35m%s\033[0m" $(APP_VERSION)
	@echo ""
	@printf "\033[33m%-23s\033[0m" "GIT_REVISION"
	@printf "\033[35m%s\033[0m" $(GIT_REVISION)
	@echo "\n"

.PHONY: targets
targets:
	@echo "\033[34mDevelopment Targets\033[0m"
	@echo "\033[34m---------------------------------------------------------------\033[0m"
	@perl -nle'print $& if m{^[a-zA-Z_-]+:.*?## .*$$}' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-22s\033[0m %s\n", $$1, $$2}'


# ------------------------------
# Development targets
# ------------------------------

.PHONY: install
install: ## Install dependencies
	poetry install

.PHONY: run
run: start

.PHONY: start
start:
	poetry run uvicorn main:app --host 0.0.0.0 --port 8000 --reload --loop uvloop --timeout-keep-alive 5 --reload-include "*.py" --reload-include ".env" --log-level debug

.PHONY: run-prod
run-prod:
	poetry run uvicorn main:app --host 0.0.0.0 --port 800 --workers 4 --timeout-keep-alive 5 --log-level debug

# ------------------------------
# Prisma targets
# ------------------------------
.PHONY: generate
generate: 

	poetry run prisma generate 

.PHONY: migrate-prod
migrate-prod: 

	poetry run prisma migrate deploy 
	
.PHONY: migrate-dev
migrate-dev: 

	@read -p "Enter migration message: " message; \
	poetry run prisma migrate dev --name "$$message" 

.PHONY: reset
reset: ## Reset db

	poetry run prisma migrate reset 

.PHONY: reset-database
reset-database: ## Rollback all migrations

	poetry run prisma migrate reset --force 

.PHONY: push
push: ## Push the schema

	poetry run prisma db push

# ------------------------------
# Check, lint, and format targets
# ------------------------------
.PHONY: check
check: check-format lint

.PHONY: check-format
check-format: ## Dry-run code formatter
	poetry run black ./ --check
	poetry run isort ./ --profile black --check

.PHONY: lint
lint: ## Run linter
	poetry run pylint ./app ./core ./worker

.PHONY: format
format: ## Run code formatter
	poetry run black ./
	poetry run isort ./ --profile black

.PHONY: lint-format
lint-format: ## Run lint and format
	make format
	make lint

.PHONY: check-lockfile
check-lockfile: ## Compares lock file with pyproject.toml
	poetry lock --no-update

# ------------------------------
# Test targets
# ------------------------------
.PHONY: test
test: ## Run the test suite

	poetry run pytest -vv -s --cache-clear ./

# ------------------------------
# Celery worker target
# ------------------------------
.PHONY: worker
worker: ## Run the Celery worker
	poetry run celery -A worker worker -l info --uid nobody --loglevel=info

.PHONY: worker-docker
worker-docker: ## Run the Celery worker on docker
	poetry run celery -A app.worker worker --loglevel=info

.PHONY: flower
flower: ## Run the Flower worker monitoring tool
	poetry run celery -A worker flower --port=5555 --loglevel=info