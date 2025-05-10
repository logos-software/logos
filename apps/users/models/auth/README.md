# Sistema de Autenticação Modernizado LOGOSS

Este diretório contém a implementação modernizada do sistema de autenticação para o LOGOSS da Polícia Militar do Mato Grosso, utilizando práticas mais atuais e otimizadas do Django.

## Principais Melhorias

1. **Substituição de strings por IntegerChoices**
   - Uso de `models.IntegerChoices` em vez de strings para tipos, status e permissões
   - Melhor performance em banco de dados e menor uso de memória
   - Tipagem mais forte e menos sujeita a erros

2. **Modelo de usuário unificado**
   - Consolidação de `SenhaUsuario` e `SenhaServico` em um único modelo `User`
   - Facilita a administração e a autenticação
   - Reduz duplicação de código

3. **Gerenciamento de permissões flexível**
   - Substituição de colunas dinâmicas por um sistema relacional
   - Melhor escalabilidade para adicionar novas permissões

4. **Compatibilidade com legado**
   - Classes proxy para compatibilidade com código existente
   - Métodos auxiliares para converter entre formatos antigo e novo
   - Migração de dados automatizada

## Estrutura de Arquivos

- `choices.py` - Define `IntegerChoices` para tipos, status e permissões
- `constants.py` - Constantes e configurações globais 
- `managers.py` - Gerenciadores personalizados para o modelo User
- `permissions.py` - Classes para gerenciamento de permissões
- `user.py` - Modelos principais (User e UserAccess)

## Uso Básico

```python
# Criação de usuários
from apps.users.models import User
from apps.users.models.auth.choices import UserTypeChoices, UserStatusChoices

# Criar um usuário policial
usuario = User.objects.create_user(
    username='policial123',
    password='senha_segura',
    user_type=UserTypeChoices.POLICE,
    status=UserStatusChoices.ACTIVE
)

# Criar um usuário administrativo
admin = User.objects.create_user(
    username='admin123',
    password='senha_segura',
    user_type=UserTypeChoices.ADMIN,
    is_staff=True,
    is_superuser=True
)

# Verificar permissões
from apps.users.models.auth.permissions import EventPermission, UserPermission
from apps.users.models.auth.choices import PermissionChoices

evento = EventPermission.objects.get(codename='meu_evento')

# Conceder permissão
UserPermission.objects.create(
    user=usuario,
    event=evento,
    permission=PermissionChoices.YES
)

# Verificar permissão
tem_permissao = usuario.check_permission('meu_evento')
```

## Gerenciamento de Acesso

O sistema rastreia automaticamente:
- Tentativas de login (bem-sucedidas e falhas)
- Bloqueios temporários após tentativas falhas
- Logs de acesso detalhados para auditoria

## Compatibilidade com Sistema Legado

Para garantir compatibilidade com o código existente, foram implementados:

1. Modelos proxy:
   - `SenhaUsuario` - Para usuários do tipo policial
   - `SenhaServico` - Para usuários administrativos

2. Métodos de conversão:
   - Para converter entre strings legadas (S/N) e IntegerChoices
   - Para mapear tipos de usuário entre sistemas

### StaffUserAccess (Substituindo SenhaServAcesso)
Registra os acessos de usuários administrativos ao sistema.

## Como usar

```python
# Importando os modelos
from users.models.auth import User, StaffUser, UserAccess, StaffUserAccess

# Trabalhando com usuários regulares
user = User.objects.get(username='usuario123')
is_active = user.is_active

# Trabalhando com usuários administrativos
staff = StaffUser.objects.get(username='admin123')
has_permission = staff.has_perm(evento, AcaoModel)
```
