"""
Exceções personalizadas para o app de usuários.
"""

class IncorrectCredentialsException(Exception):
    """Exceção para credenciais inválidas."""
    def __init__(self, message=None):
        self.message = message or "Usuário ou senha inválidos."
        super().__init__(self.message)


class UserAccountLockedException(Exception):
    """Exceção para conta de usuário bloqueada."""
    def __init__(self, username, lockout_until=None, message=None):
        self.username = username
        self.lockout_until = lockout_until
        self.message = message or f"A conta do usuário {username} está temporariamente bloqueada."
        super().__init__(self.message)


class PasswordExpiredException(Exception):
    """Exceção para senha expirada."""
    def __init__(self, username, message=None):
        self.username = username
        self.message = message or f"A senha do usuário {username} expirou e precisa ser alterada."
        super().__init__(self.message)


class InsufficientPermissionsException(Exception):
    """Exceção para permissões insuficientes."""
    def __init__(self, username, permission_needed, message=None):
        self.username = username
        self.permission_needed = permission_needed
        self.message = message or f"Usuário {username} não tem a permissão necessária: {permission_needed}"
        super().__init__(self.message)
