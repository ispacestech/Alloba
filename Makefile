.PHONY: install test lint build-index run docker-build help

help:
	@echo "Alloba — development targets"
	@echo "  make install        pip install -e \".[dev]\""
	@echo "  make test           run pytest"
	@echo "  make lint           run ruff check"
	@echo "  make build-index    build the FAISS knowledge index from kb/docs"
	@echo "  make run            start the gateway on 127.0.0.1:8582"
	@echo "  make docker-build   build the Alloba image"

install:
	pip install -e ".[dev]"

test:
	python -m pytest -q

lint:
	python -m ruff check src tests ingest.py scripts

build-index:
	python ingest.py

run:
	python -m alloba

docker-build:
	docker build -t alloba/gateway:latest .
