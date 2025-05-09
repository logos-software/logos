#!/bin/bash
set -e

echo "Iniciando configuração do ambiente de desenvolvimento..."

echo "Verificando se o Docker está rodando..."
if ! docker info > /dev/null 2>&1; then
    echo "Docker não está rodando! Por favor, inicie o Docker e tente novamente."
    exit 1
fi

echo "Construindo containers..."
docker-compose build

echo "Iniciando containers..."
docker-compose up -d

echo "Esperando o banco de dados estar pronto..."
sleep 10

echo "Aplicando migrações..."
docker-compose exec web python manage.py migrate

echo "Coletando arquivos estáticos..."
docker-compose exec web python manage.py collectstatic --no-input

echo "Ambiente de desenvolvimento configurado com sucesso!"
echo "Acesse a aplicação em: http://localhost:8000"
echo ""
echo "Para criar um superusuário, execute:"
echo "docker-compose exec web python manage.py createsuperuser"
