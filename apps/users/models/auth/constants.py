from django.conf import settings
from django.utils.translation import gettext_lazy as _

from apps.users.models.auth.choices import (
    UserStatusChoices, UserTypeChoices, 
    PermissionChoices, AccessChoices,
    PERMISSION_MAPPING
)

# Constantes relacionadas ao tipo de usuário
USER_TYPE_POLICE = UserTypeChoices.POLICE
USER_TYPE_STAFF = UserTypeChoices.STAFF
USER_TYPE_ADMIN = UserTypeChoices.ADMIN

# Status do usuário
USER_STATUS_ACTIVE = UserStatusChoices.ACTIVE
USER_STATUS_INACTIVE = UserStatusChoices.INACTIVE
USER_STATUS_SUSPENDED = UserStatusChoices.SUSPENDED

# Configurações de segurança
PASSWORD_EXPIRY_DAYS = getattr(settings, 'PASSWORD_EXPIRY_DAYS', 90)
MAX_LOGIN_ATTEMPTS = getattr(settings, 'MAX_LOGIN_ATTEMPTS', 5)
LOGIN_LOCKOUT_MINUTES = getattr(settings, 'LOGIN_LOCKOUT_MINUTES', 30)

# Constantes para permissões
PERMISSION_YES = PermissionChoices.YES
PERMISSION_NO = PermissionChoices.NO

# Constantes para acesso
ACCESS_ALLOWED = AccessChoices.ALLOWED
ACCESS_DENIED = AccessChoices.DENIED
