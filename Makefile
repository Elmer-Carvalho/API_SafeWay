# Makefile para facilitar o uso do projeto

.PHONY: help build up down logs shell clean

help: ## Mostrar esta ajuda
	@echo "Comandos disponíveis:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

build: ## Construir as imagens Docker
	docker-compose build

up: ## Iniciar todos os serviços
	docker-compose up -d

down: ## Parar todos os serviços
	docker-compose down

logs: ## Ver logs dos serviços
	docker-compose logs -f

shell: ## Acessar shell do container da aplicação
	docker-compose exec app bash

db-shell: ## Acessar shell do banco de dados
	docker-compose exec db psql -U safeway_user -d safeway_db

clean: ## Limpar containers e volumes
	docker-compose down -v
	docker system prune -f

restart: ## Reiniciar todos os serviços
	docker-compose restart

status: ## Ver status dos serviços
	docker-compose ps
