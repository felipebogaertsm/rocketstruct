.PHONY: install install-dev install-hooks test publish build verify-version check format-check lint typecheck format coverage clean

install:
	@uv sync

install-dev:
	@uv sync --group dev

install-hooks:
	@uv run pre-commit install

build:
	@uv build

verify-version:
	@PKG_VERSION=$$(uv run python -c "ns = {}; exec(open('rocketstruct/_version.py').read(), ns); print(ns['__version__'])"); \
	TAG_VERSION=$${GITHUB_REF_NAME#v}; \
	if [ "$$PKG_VERSION" != "$$TAG_VERSION" ]; then \
		echo "::error::Tag version ($$TAG_VERSION) does not match package version ($$PKG_VERSION)"; \
		exit 1; \
	fi; \
	echo "Version verified: $$PKG_VERSION"
test:
	@uv run pytest
publish:
	@$(MAKE) build
	@twine upload dist/*
check: format-check lint typecheck
format-check:
	@uv run ruff format --check
lint:
	@uv run ruff check .
typecheck:
	@uv run pyright rocketstruct
format:
	@uv run ruff format
	@uv run ruff check . --fix
coverage:
	@uv run pytest --cov=rocketstruct --cov-branch --cov-report=term-missing --cov-report=html --cov-report=xml tests/
clean:
	@rm -rf build dist htmlcov .coverage
	@find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	@find . -type d -name '*.egg-info' -exec rm -rf {} + 2>/dev/null || true
	@find . -type d -name .pytest_cache -exec rm -rf {} + 2>/dev/null || true
	@find . -type d -name .ruff_cache -exec rm -rf {} + 2>/dev/null || true