.PHONY: all
all:

.PHONY: setup
## setup: Install requirements
setup:
	poetry install --no-interaction

.PHONY: chglog
## chglog: Generate changelog
chglog:
	git chglog --sort semver -o CHANGELOG.md

.PHONY: lint
## lint: Run lint
lint:
	poetry run black --check --diff .
	poetry run ruff check .

.PHONY: test
## test: Run tests
test:
	poetry run pytest

.PHONY: build
## build: Build package
build:
	poetry build

.PHONY: publish
## publish: Publish on PyPI
publish:
	poetry publish

.PHONY: clean
## clean: Remove builds and cache
clean:
	rm -rf dist/
	rm -rf src/resume_pycli/__pycache__/

.PHONY: help
## help: Prints this help message
help:
	@echo "Usage: \n"
	@sed -n 's/^##//p' ${MAKEFILE_LIST} | column -t -s ':' |  sed -e 's/^/ /'
