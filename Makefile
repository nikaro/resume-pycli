.PHONY: all
all:

.PHONY: setup
## setup: Install requirements
setup:
	poetry install --no-interaction

.PHONY: chglog
## chglog: Generate changelog
chglog:
	git chglog --sort semver $(shell [ -n "$(TAG)" ] && echo "--next-tag $(TAG)") --output CHANGELOG.md

.PHONY: lint
## lint: Run lint
lint:
	poetry run black --check --diff .
ifeq ($(CI), true)
	poetry run ruff check --format=github .
else
	poetry run ruff check .
endif
	poetry run mypy .

.PHONY: test
## test: Run tests
test:
	poetry run pytest

.PHONY: build
## build: Build package
build:
	poetry build
	cd dist/ ; sha512sum * > sha512sums.txt

.PHONY: publish
## publish: Publish on PyPI
publish:
	poetry publish

.PHONY: clean
## clean: Remove builds and cache
clean:
	rm -rf dist/
	rm -rf public/
	rm -rf src/resume_pycli/__pycache__/

.PHONY: help
## help: Prints this help message
help:
	@echo "Usage: \n"
	@sed -n 's/^##//p' ${MAKEFILE_LIST} | column -t -s ':' |  sed -e 's/^/ /'
