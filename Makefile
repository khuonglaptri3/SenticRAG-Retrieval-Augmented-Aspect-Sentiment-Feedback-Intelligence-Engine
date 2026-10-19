.PHONY: help install lint typecheck test test-unit test-integration build-api build-train run-api clean

POETRY ?= poetry

help:
	@echo "SenticRAG Development Commands:"
	@echo "  make install           Install dependencies in editable mode"
	@echo "  make lint              Run ruff linter"
	@echo "  make typecheck         Run mypy static type analysis"
	@echo "  make test              Run unit and integration test suite"
	@echo "  make test-unit         Run unit tests only"
	@echo "  make test-integration  Run integration tests only"
	@echo "  make build-api         Build production API Docker image"
	@echo "  make build-train       Build training Docker image"
	@echo "  make run-api           Run local API server"
	@echo "  make clean             Clean build and cache artifacts"

install:
	$(POETRY) install --extras dev

lint:
	$(POETRY) run ruff check .

typecheck:
	$(POETRY) run mypy packages apps pipelines

test:
	$(POETRY) run pytest tests/unit tests/integration -v

test-unit:
	$(POETRY) run pytest tests/unit -v

test-integration:
	$(POETRY) run pytest tests/integration -v

build-api:
	docker build -f infra/docker/Dockerfile.api -t senticrag-api:latest .

build-train:
	docker build -f infra/docker/Dockerfile.train -t senticrag-train:latest .

run-api:
	$(POETRY) run uvicorn apps.api.app.main:app --host 0.0.0.0 --port 8000 --reload

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type d -name "*.egg-info" -exec rm -rf {} +
	find . -type d -name ".pytest_cache" -exec rm -rf {} +
	find . -type d -name ".mypy_cache" -exec rm -rf {} +
	find . -type d -name ".ruff_cache" -exec rm -rf {} +
	rm -rf build dist .coverage
