# Makefile for VEPmcp

.PHONY: help install test test-unit test-integration test-all lint type clean build

# Default target
help:
	@echo "Available targets:"
	@echo "  install          Install package in development mode"
	@echo "  test             Run unit tests only (fast)"
	@echo "  test-unit        Run unit tests only"
	@echo "  test-integration Run integration tests (requires internet)"
	@echo "  test-all         Run all tests"
	@echo "  lint             Run linting checks"
	@echo "  type             Run type checking"
	@echo "  clean            Clean build artifacts"
	@echo "  build            Build package"

# Install package in development mode
install:
	pip install -e .[dev]

# Run unit tests only (default)
test:
	python run_tests.py --mode unit

# Run unit tests
test-unit:
	python run_tests.py --mode unit --verbose

# Run integration tests
test-integration:
	python run_tests.py --mode integration --verbose

# Run all tests
test-all:
	python run_tests.py --mode all --verbose

# Run linting
lint:
	python run_tests.py --mode lint

# Run type checking
type:
	python run_tests.py --mode type

# Clean build artifacts
clean:
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info/
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete

# Build package
build: clean
	python -m build
