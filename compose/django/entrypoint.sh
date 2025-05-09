#!/bin/sh

echo "Aguardando serviços..."
sleep 5

# Verificar se o banco de dados PostgreSQL está disponível
echo "Verificando PostgreSQL..."
while ! pg_isready -h $DB_HOST -p $DB_PORT -U postgres > /dev/null 2>&1; do
    echo "Aguardando PostgreSQL..."
    sleep 1
done

echo "Verificando conexão com PostgreSQL como usuário django..."
# Verificar se conseguimos conectar como usuário django
if ! PGPASSWORD=$DB_PASSWORD psql -h $DB_HOST -p $DB_PORT -U $DB_USER -d $DB_NAME -c "SELECT 1" > /dev/null 2>&1; then
    echo "Erro ao conectar como usuário django. Verifique as permissões."
    echo "Tentando conectar como usuário postgres para corrigir permissões..."
    
    # Conceder permissões ao usuário django
    PGPASSWORD=postgres psql -h $DB_HOST -p $DB_PORT -U postgres -d $DB_NAME -c "
        GRANT ALL ON SCHEMA public TO $DB_USER;
        ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON TABLES TO $DB_USER;
        ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON SEQUENCES TO $DB_USER;
        ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON FUNCTIONS TO $DB_USER;
        ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON TYPES TO $DB_USER;
    "
fi

# Aplicar migrações do Django em todos os bancos
echo "Aplicando migrações do Django em todos os bancos..."
sh /usr/local/bin/apply_migrations.sh

# Coletar arquivos estáticos
echo "Coletando arquivos estáticos..."
python manage.py collectstatic --noinput

echo "Inicializando servidor Django..."
exec "$@"
