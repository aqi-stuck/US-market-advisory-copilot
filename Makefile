
.PHONY: help setup install test run docker-build docker-up docker-down clean

help: 
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

setup:
	cp .env.example .env
	poetry install

install: 
	poetry install

test: 
	poetry run pytest

run: #
	poetry run uvicorn app.main:app --reload

docker-build: 
	docker-compose build

docker-up:
	docker-compose up -d

docker-down: 
	docker-compose down

clean:
	rm -rf __pycache__
	rm -rf */__pycache__
	rm -rf */*/__pycache__
	find . -type f -name "*.pyc" -delete