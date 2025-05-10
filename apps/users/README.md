# Módulo de Usuários do Sistema LOGOSS

Este módulo gerencia usuários, autenticação e permissões para o sistema LOGOSS da Polícia Militar do Mato Grosso. Foi refatorado para usar Django IntegerChoices para melhor performance e manutenibilidade.

## Estrutura

- `backends.py`: Backend de autenticação personalizado
- `migrations_utils.py`: Utilidades para migração de dados dos modelos legados
- `models/`: Pasta com modelos organizados
  - `auth/`: Modelos de autenticação modernizados
    - `choices.py`: Enumeradores para tipos, status e permissões usando IntegerChoices
    - `constants.py`: Constantes relacionadas a autenticação
    - `managers.py`: Managers para modelos de usuário
    - `permissions.py`: Sistema moderno de permissões
    - `user.py`: Modelo unificado de usuário (User)
    - `README.md`: Documentação específica do subsistema de autenticação

## Modelos Principais

### User

Modelo unificado que substitui os antigos `SenhaUsuario` e `SenhaServico`. Usa o `AbstractUser` do Django e adiciona:

- Campo `user_type` (IntegerChoices) para diferenciar policiais, administrativos e administradores
- Campo `status` (IntegerChoices) para controle de estado (ativo, inativo, suspenso)
- Sistema de segurança com controle de tentativas de login e bloqueio automático
- Rastreamento de acessos através do modelo UserAccess
- Métodos de compatibilidade com código legado

### UserAccess

Modelo unificado para registro de acessos de usuários, substituindo os antigos `UsuarioAcesso` e `SenhaServAcesso`. Registra:

- Data/hora de acesso
- Endereço IP
- User-Agent do navegador
- Sucesso ou falha no login
- Informações adicionais para auditoria

### Permission & EventPermission

Sistema de permissões por eventos do sistema:

- `Permission`: Define permissões básicas
- `EventPermission`: Define eventos do sistema que podem ter permissões
- `UserPermission`: Associa usuários a eventos com suas respectivas permissões

## Compatibilidade com Legacy

Para garantir compatibilidade com código existente, são fornecidos:

### Classes Proxy

```python
# Uso como antes
from apps.users.models import SenhaUsuario, SenhaServico

# Internamente, estas são classes proxy para o novo modelo User
usuario = SenhaUsuario.objects.create(username="pm123", password="senha")
admin = SenhaServico.objects.create(username="admin123", password="senha")
```

### Métodos de Conversão

```python
from apps.users.models.auth.choices import UserStatusChoices, UserTypeChoices

# Converter de/para formatos legados
status_legado = UserStatusChoices.to_legacy(UserStatusChoices.ACTIVE)  # Retorna 'S'
status_novo = UserStatusChoices.from_legacy('S')  # Retorna UserStatusChoices.ACTIVE
```

## Migração de Dados

O arquivo `migrations_utils.py` contém funções para migrar dados dos modelos legados:

- `migrate_legacy_users()`: Migra usuários policiais e administrativos
- `migrate_legacy_permissions()`: Migra permissões
- `migrate_legacy_access_logs()`: Migra logs de acesso

Principais atributos:
- `username`: Nome de usuário
- `email`: Email (opcional)
- `user_type`: Tipo de usuário (Policial, Staff, Admin)
- `status`: Status do usuário (Ativo, Inativo, Suspenso)
- `policial`: Relacionamento com o modelo Policial
- `policial_funcao`: Relacionamento com o modelo PolicialFuncao

### UserAccess

Modelo unificado que substitui os antigos `UsuarioAcesso` e `SenhaServAcesso`. Registra todos os acessos ao sistema.

## Compatibilidade com Código Legado

Para manter compatibilidade com o código existente, são fornecidas classes proxy:
- `SenhaUsuario`: Classe proxy para `User` com tipo "POLICE"
- `SenhaServico`: Classe proxy para `User` com tipo "STAFF"
- `UsuarioAcesso` e `SenhaServAcesso`: Classes proxy para `UserAccess`

## Segurança

- Bloqueia usuários após múltiplas tentativas de login
- Armazena histórico de acessos com informações como IP
- Sistema de permissões baseado em eventos

## Instruções para Migração

Para migrar os dados dos modelos antigos para os novos:

1. Execute as migrações iniciais: `python manage.py makemigrations users`
2. Crie uma migração de dados: `python manage.py makemigrations users --empty --name=migrate_users`
3. Edite a migração criada para usar as funções em `migrations_utils.py`
4. Execute as migrações: `python manage.py migrate users`

## Exemplo de uso do modelo User

```python
from django.contrib.auth import get_user_model

User = get_user_model()

# Criar um usuário policial
user = User.objects.create_user(
    username='pm12345',
    password='senha_segura',
    first_name='João',
    last_name='Silva',
    user_type='POLICE',
    registration_number='12345'
)

# Verificar permissões
has_permission = user.has_event_permission('visualizar_ocorrencias')
```
