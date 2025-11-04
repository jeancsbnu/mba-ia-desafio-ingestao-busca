SHELL := /bin/bash
.ONESHELL:
.SILENT:

PY ?= python3
VENV ?= venv
PIP := $(VENV)/bin/pip
PYTHON := $(VENV)/bin/python

.PHONY: psql up bash ingest chat prompt down

psql:
	docker exec -it postgres_rag psql -U postgres -d rag

up:
	docker-compose up -d	

down:
	docker-compose down

bash:
	docker exec -it postgres_rag bash

env:
	if [ ! -f .env ]; then
		if [ -f .env.example ]; then
			cp .env.example .env
			echo "Copiado .env.example -> .env"
		else
			echo ".env.example não encontrado"; exit 1
		fi
	else
		echo ".env já existe (nada a fazer)"
	fi

venv:
	$(PY) -m venv $(VENV)
	# garantir pip atualizado dentro da venv
	$(PYTHON) -m pip install --upgrade pip setuptools wheel

install: env venv
	$(PIP) install -r requirements.txt

ingest:
	$(PYTHON) src/ingest.py

chat:
	$(PYTHON) src/chat.py

clean:
	rm -rf $(VENV)

clean-db:
	docker exec -t postgres_rag psql -U postgres -d rag -c "TRUNCATE langchain_pg_embedding, langchain_pg_collection RESTART IDENTITY CASCADE;"
	echo "Limpeza do banco de dados concluida."


help:
	@echo "Comandos disponíveis:"
	@echo "  make venv     - Cria venv"
	@echo "  make install  - instala deps na venv"
	@echo "  make up       - Inicia os containers Docker"
	@echo "  make down     - Para os containers Docker"
	@echo "  make psql     - Acessa o banco de dados PostgreSQL"
	@echo "  make bash     - Acessa o container PostgreSQL via bash"
	@echo "  make ingest   - Executa o script de ingestão de dados"	
	@echo "  make chat     - Inicia o chat interativo com o modelo"
	@echo "  make clean    - Remove a venv"
	@echo "  make clean-db - Limpa os embeddings da coleção no banco de dados"