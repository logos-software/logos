#!/bin/bash
# Script para aplicar migrações em todos os bancos de dados configurados

echo "=== Aplicando migrações em todos os bancos de dados ==="

# Aplicar migrações no banco default (PostgreSQL)
echo "-> Aplicando migrações no banco default (PostgreSQL)..."
python manage.py migrate --database=default

# Aplicar migrações no banco oracle
echo "-> Aplicando migrações no banco oracle..."
python manage.py migrate --database=oracle

echo "=== Migrações concluídas com sucesso! ==="