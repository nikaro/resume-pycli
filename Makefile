.PHONY: all
all:

.PHONY: install
## install: Install requirements
install:
	poetry install

.PHONY: build
## build: Build package
build:
	poetry build

.PHONY: test
## test: Run tests
test:
	poetry run pytest

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
	@echo -e "Usage: \n"
	@sed -n 's/^##//p' ${MAKEFILE_LIST} | column -t -s ':' |  sed -e 's/^/ /'
