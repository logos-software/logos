# Logoss

Aplicação Django com configuração Docker para desenvolvimento e produção.

## Requisitos

- Docker
- Docker Compose

## Configuração do Ambiente de Desenvolvimento

1. Clone o repositório:

```bash
git clone <seu-repositorio>
cd logoss
```

2. Use o script de inicialização automatizada (escolha um dos dois):

   - No Linux/macOS:
   ```bash
   chmod +x setup-dev.sh
   ./setup-dev.sh
   ```
   
   - No Windows (PowerShell):
   ```powershell
   .\setup-dev.ps1
   ```

   Ou execute manualmente os comandos:

   ```bash
   # Inicie os containers
   docker-compose up -d
   
   # Aguarde o banco de dados iniciar e aplique as migrações
   docker-compose exec web python manage.py migrate
   
   # Colete os arquivos estáticos
   docker-compose exec web python manage.py collectstatic --no-input
   ```

3. Crie um superusuário (opcional):

```bash
docker-compose exec web python manage.py createsuperuser
```

4. Você também pode usar o Makefile para comandos comuns:

```bash
# Ver todos os comandos disponíveis
make help

# Iniciar containers
make up

# Aplicar migrações
make migrate
```

5. Acesse a aplicação em [http://localhost:8000](http://localhost:8000)

## Configuração do Ambiente de Produção

1. Crie um arquivo `.env` baseado no `.env.example`:

```bash
cp .env.example .env
```

2. Edite o arquivo `.env` com suas configurações de produção.

3. Construa e inicie os containers de produção:

```bash
docker-compose -f docker-compose.prod.yml up -d --build
```

4. Execute as migrações:

```bash
docker-compose -f docker-compose.prod.yml exec web python manage.py migrate
```

5. Colete os arquivos estáticos:

```bash
docker-compose -f docker-compose.prod.yml exec web python manage.py collectstatic --no-input
```

6. Crie um superusuário (opcional):

```bash
docker-compose -f docker-compose.prod.yml exec web python manage.py createsuperuser
```

7. Acesse a aplicação em [http://seu-dominio.com](http://seu-dominio.com)

## Componentes

- **Django**: Framework web para desenvolvimento rápido
- **PostgreSQL**: Banco de dados relacional principal
- **Oracle**: Banco de dados secundário
- **Redis**: Cache e filas de mensagens
- **Nginx**: Servidor web e proxy reverso (apenas em produção)

## Estrutura do Projeto

```
logoss/
├── apps/                # Aplicações Django
│   ├── core/            # Funcionalidades principais
│   ├── notes/           # Gerenciamento de Notas
│   ├── users/           # Autenticação e usuários
│   └── utils/           # Utilitários e funções auxiliares
├── compose/             # Arquivos de configuração Docker
│   ├── django/          # Dockerfiles para Django
│   ├── nginx/           # Configuração do Nginx
│   ├── oracle/          # Scripts de inicialização do Oracle
│   └── postgres/        # Scripts de inicialização do PostgreSQL
├── config/              # Configuração do projeto Django
│   ├── settings/        # Configurações específicas de ambiente
│   └── ...
├── docker-compose.yml       # Configuração para desenvolvimento
├── docker-compose.prod.yml  # Configuração para produção
└── ...
```
