# Makefile para comandos comuns do projeto

.PHONY: up down build ps logs shell migrate collectstatic makemigrations createsuperuser test help

help:
	@echo "Comandos disponíveis:"
	@echo "  up            : Iniciar containers"
	@echo "  down          : Parar e remover containers"
	@echo "  build         : Construir containers"
	@echo "  ps            : Verificar status dos containers"
	@echo "  logs          : Ver logs dos containers (use logs web para logs específicos)"
	@echo "  shell         : Abrir shell no container Django"
	@echo "  migrate       : Aplicar migrações"
	@echo "  makemigrations: Criar migrações"
	@echo "  collectstatic : Coletar arquivos estáticos"
	@echo "  createsuperuser: Criar superusuário"
	@echo "  test          : Executar testes"

up:
	docker-compose up -d

down:
	docker-compose down

build:
	docker-compose build

ps:
	docker-compose ps

logs:
	docker-compose logs -f $(service)

shell:
	docker-compose exec web python manage.py shell

migrate:
	docker-compose exec web python manage.py migrate

makemigrations:
	docker-compose exec web python manage.py makemigrations

collectstatic:
	docker-compose exec web python manage.py collectstatic --no-input

createsuperuser:
	docker-compose exec web python manage.py createsuperuser

test:
	docker-compose exec web python manage.py test
