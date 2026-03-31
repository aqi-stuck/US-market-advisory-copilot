# Pakistan Market Advisory RAG System Makefile

.PHONY: help setup install test run docker-build docker-up docker-down clean

help: ## Display this help message
	@echo "Pakistan Market Advisory RAG System"
	@echo ""
	@echo "Usage:"
	@echo "  make setup          Setup the development environment"
	@echo "  make install        Install dependencies"
	@echo "  make test           Run tests"
	@echo "  make run            Run the application"
	@echo "  make docker-up      Start services with Docker Compose"
	@echo "  make docker-down    Stop services with Docker Compose"
	@echo "  make docker-build   Build Docker images"
	@echo "  make clean          Clean up temporary files"
	@echo ""

setup: ## Setup the development environment
	cp .env.example .env
	poetry install

install: ## Install dependencies
	poetry install

test: ## Run tests
	poetry run pytest

run: ## Run the application
	poetry run uvicorn app.main:app --reload

docker-build: ## Build Docker images
	docker-compose build

docker-up: ## Start services with Docker Compose
	docker-compose up -d

docker-down: ## Stop services with Docker Compose
	docker-compose down

clean: ## Clean up temporary files
	rm -rf __pycache__
	rm -rf */__pycache__
	rm -rf */*/__pycache__
	find . -type f -name "*.pyc" -delete