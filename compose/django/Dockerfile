# Dockerfile para ambiente de desenvolvimento
FROM python:3.10-slim

# Define variáveis de ambiente para Python
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/app

# Define o diretório de trabalho
WORKDIR /app

# Instala dependências do sistema
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    libaio1 \
    unzip \
    curl \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Oracle Instant Client (necessário para cx_Oracle)
WORKDIR /opt/oracle
RUN curl -LO https://download.oracle.com/otn_software/linux/instantclient/instantclient-basiclite-linuxx64.zip \
    && unzip instantclient-basiclite-linuxx64.zip \
    && rm instantclient-basiclite-linuxx64.zip \
    && echo /opt/oracle/instantclient* > /etc/ld.so.conf.d/oracle-instantclient.conf \
    && ldconfig

WORKDIR /app

# Copia requirements.txt e instala dependências Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copia os scripts de entrypoint e migrações
COPY compose/django/entrypoint.sh /usr/local/bin/
COPY compose/django/apply_migrations.sh /usr/local/bin/
RUN chmod +x /usr/local/bin/entrypoint.sh /usr/local/bin/apply_migrations.sh && \
    apt-get update && apt-get install -y --no-install-recommends postgresql-client && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# Copia o código do projeto
COPY . .

# Expõe a porta usada pela aplicação
EXPOSE 8000

# Define o entrypoint e comando de inicialização
ENTRYPOINT ["entrypoint.sh"]
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
