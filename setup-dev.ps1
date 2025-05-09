# Script de inicialização para ambiente de desenvolvimento (Windows PowerShell)

Write-Host "Iniciando configuração do ambiente de desenvolvimento..." -ForegroundColor Green

Write-Host "Verificando se o Docker está rodando..." -ForegroundColor Cyan
try {
    docker info | Out-Null
} catch {
    Write-Host "Docker não está rodando! Por favor, inicie o Docker e tente novamente." -ForegroundColor Red
    exit 1
}

Write-Host "Construindo containers..." -ForegroundColor Cyan
docker-compose build

Write-Host "Iniciando containers..." -ForegroundColor Cyan
docker-compose up -d

Write-Host "Esperando o banco de dados estar pronto..." -ForegroundColor Cyan
Start-Sleep -Seconds 10

Write-Host "Aplicando migrações..." -ForegroundColor Cyan
docker-compose exec web python manage.py migrate

Write-Host "Coletando arquivos estáticos..." -ForegroundColor Cyan
docker-compose exec web python manage.py collectstatic --no-input

Write-Host "Ambiente de desenvolvimento configurado com sucesso!" -ForegroundColor Green
Write-Host "Acesse a aplicação em: http://localhost:8000" -ForegroundColor Yellow
Write-Host ""
Write-Host "Para criar um superusuário, execute:" -ForegroundColor Cyan
Write-Host "docker-compose exec web python manage.py createsuperuser" -ForegroundColor Yellow
