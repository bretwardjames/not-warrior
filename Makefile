.PHONY: help install install-dev test lint format type-check clean build docs run

# Default target
help:
	@echo "Available targets:"
	@echo "  install      - Install package and dependencies"
	@echo "  install-dev  - Install package with development dependencies"
	@echo "  test         - Run tests"
	@echo "  test-cov     - Run tests with coverage"
	@echo "  lint         - Run linting checks"
	@echo "  format       - Format code with black and isort"
	@echo "  type-check   - Run type checking with mypy"
	@echo "  clean        - Clean build artifacts"
	@echo "  build        - Build package"
	@echo "  docs         - Generate documentation"
	@echo "  run          - Run the application"
	@echo "  check-all    - Run all checks (lint, type-check, test)"

# Installation targets
install:
	pip install -e .

install-dev:
	pip install -e .[dev,test]
	pre-commit install

# Testing targets
test:
	pytest tests/ -v

test-cov:
	pytest tests/ -v --cov=not_warrior --cov-report=html --cov-report=term

test-integration:
	pytest tests/integration/ -v -m integration

test-unit:
	pytest tests/unit/ -v -m unit

# Code quality targets
lint:
	flake8 not_warrior/ tests/
	pylint not_warrior/

format:
	black not_warrior/ tests/
	isort not_warrior/ tests/

format-check:
	black --check not_warrior/ tests/
	isort --check-only not_warrior/ tests/

type-check:
	mypy not_warrior/

# Security check
security-check:
	bandit -r not_warrior/

# All checks
check-all: format-check lint type-check test

# Build targets
clean:
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info/
	rm -rf htmlcov/
	rm -rf .coverage
	rm -rf .pytest_cache/
	rm -rf .mypy_cache/
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete

build: clean
	python -m build

wheel: clean
	python setup.py bdist_wheel

sdist: clean
	python setup.py sdist

# Documentation targets
docs:
	@echo "Documentation generation not yet implemented"

# Development targets
run:
	python -m not_warrior.main

run-dev:
	NOT_WARRIOR_DEV=1 python -m not_warrior.main

# Database/sync targets
setup-auth:
	python -m not_warrior.main auth setup

test-auth:
	python -m not_warrior.main auth validate

init-config:
	python -m not_warrior.main config init

show-config:
	python -m not_warrior.main config show

test-sync:
	python -m not_warrior.main sync run --dry-run

install-hook:
	python -m not_warrior.main sync install-hook

remove-hook:
	python -m not_warrior.main sync remove-hook

# Release targets
release-test: build
	python -m twine upload --repository testpypi dist/*

release: build
	python -m twine upload dist/*

# Git hooks
pre-commit:
	pre-commit run --all-files

update-deps:
	pip-compile requirements.in
	pip-compile requirements-dev.in

# Docker targets (if needed)
docker-build:
	docker build -t not-warrior .

docker-run:
	docker run -it --rm not-warrior

# Performance testing
perf-test:
	@echo "Performance testing not yet implemented"

# Backup and restore
backup-config:
	python -c "from not_warrior.utils.config_manager import ConfigManager; ConfigManager().backup_config()"

# Environment setup
setup-env:
	python -m venv venv
	@echo "Virtual environment created. Activate with 'source venv/bin/activate'"

activate:
	@echo "Run 'source venv/bin/activate' to activate the virtual environment"

# Quick development workflow
dev-setup: setup-env install-dev
	@echo "Development environment setup complete!"

quick-test: format lint type-check test
	@echo "Quick test suite completed!"

# CI/CD helpers
ci-install:
	pip install -e .[dev,test]

ci-test: format-check lint type-check test-cov
	@echo "CI test suite completed!"

# Debugging
debug:
	python -c "import not_warrior; print('Package location:', not_warrior.__file__)"

version:
	python -c "from not_warrior import __version__; print(__version__)"

# Cleanup for fresh start
fresh-start: clean
	rm -rf venv/
	rm -rf .git/hooks/pre-commit
	@echo "Cleaned up for fresh start"

# Help with common tasks
first-run: install-dev init-config
	@echo "First-time setup complete. Try 'make setup-auth' next."

# Monitoring
check-deps:
	pip list --outdated

check-security:
	pip-audit

# Performance profiling
profile:
	python -m cProfile -o profile.stats -m not_warrior.main --help
	python -c "import pstats; p = pstats.Stats('profile.stats'); p.sort_stats('cumulative').print_stats(20)"

# Memory usage
memory-profile:
	memory_profiler python -m not_warrior.main --help