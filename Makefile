.PHONY: help build dev init test lint docs
include .env

TIMESTAMP=$(shell /bin/date -u +"%Y%m%d%H%M%s")

.DEFAULT: help
help:
	@echo "make build"
	@echo "       build a wheel to the dist directory"
	@echo "make clean"
	@echo "       remove python cache files and build artifacts"
	@echo "make db-bak"
	@echo "       backup vault db with timestamp"
	@echo "make run"
	@echo "       run airflow using containers"
	@echo "make init"
	@echo "       install all project dependencies"
	@echo "make install"
	@echo "       install nugflow as a python module"
	@echo "make test"
	@echo "       run tests"
	@echo "make lint"
	@echo "       run pylint and mypy"
	@echo "make docs"
	@echo "       build sphinx and schemaspy documentation"

build: clean
	docker build -f docker/Dockerfile -t "${ECR_REPOSITORY_URL}" .

clean:
	@rm -rf ./dist
	@rm -rf ./build
	@rm -rf ./vault.egg-info
	@find . -name '*.pyc' -delete

db-bak:
	sudo cp /var/lib/docker/volumes/docker_vault_data_volume/_data/vault.db "bak/vault_bak_$(TIMESTAMP).db"
	cp "bak/vault_bak_$(TIMESTAMP).db" vault.db

db-migrate: db-bak
	alembic upgrade head
	sudo cp vault.db /var/lib/docker/volumes/docker_vault_data_volume/_data/vault.db 

run: clean
	docker-compose -f docker/docker-compose.yml down
	docker-compose -f docker/docker-compose.yml up --build

init:
	pip install -r requirements.dev.txt --no-cache-dir && pip install -r requirements.txt --no-cache-dir

install:
	python -m setup install

test: lint
	python -m pytest

lint:
	mypy nugflow
	mypy tests
	mypy dags

docs:
	sphinx-apidoc -f -M -o docs/source/docstring/ nugflow
	cd docs; make html
	cd docs/resources; java -jar schemaspy-6.0.0.jar
