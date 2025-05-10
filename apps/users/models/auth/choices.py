from django.db import models
from django.utils.translation import gettext_lazy as _


class UserStatusChoices(models.IntegerChoices):
    """
    Choices para status do usuário utilizando IntegerChoices para melhor performance
    """
    ACTIVE = 1, _('Ativo')
    INACTIVE = 0, _('Inativo')
    SUSPENDED = 2, _('Suspenso')
    
    # Mapeamento para compatibilidade com o legado
    @classmethod
    def from_legacy(cls, value):
        legacy_map = {
            'S': cls.ACTIVE,
            'N': cls.INACTIVE
        }
        return legacy_map.get(value, cls.INACTIVE)
    
    @classmethod
    def to_legacy(cls, value):
        legacy_map = {
            cls.ACTIVE: 'S',
            cls.INACTIVE: 'N',
            cls.SUSPENDED: 'N'
        }
        return legacy_map.get(value, 'N')


class UserTypeChoices(models.IntegerChoices):
    """
    Choices para tipo de usuário utilizando IntegerChoices para melhor performance
    """
    POLICE = 1, _('Policial')
    STAFF = 2, _('Administrativo')
    ADMIN = 3, _('Administrador')
    
    # Mapeamento para compatibilidade com o legado
    @classmethod
    def from_legacy(cls, value):
        legacy_map = {
            'G': cls.ADMIN,  # Tipo Geral = Admin
            'R': cls.STAFF   # Tipo Restrito = Staff
        }
        return legacy_map.get(value, cls.POLICE)
    
    @classmethod
    def to_legacy(cls, value):
        legacy_map = {
            cls.ADMIN: 'G',
            cls.STAFF: 'R',
            cls.POLICE: 'R'  # Policiais são considerados restritos no sistema legado
        }
        return legacy_map.get(value, 'R')


class PermissionChoices(models.IntegerChoices):
    """
    Choices para permissões utilizando IntegerChoices para melhor performance
    """
    NO = 0, _('Não')
    YES = 1, _('Sim')
    
    # Mapeamento para compatibilidade com o legado
    @classmethod
    def from_legacy(cls, value):
        legacy_map = {
            'S': cls.YES,
            'N': cls.NO,
            True: cls.YES,
            False: cls.NO
        }
        return legacy_map.get(value, cls.NO)
    
    @classmethod
    def to_legacy(cls, value):
        legacy_map = {
            cls.YES: 'S',
            cls.NO: 'N'
        }
        return legacy_map.get(value, 'N')
    
    @classmethod
    def to_bool(cls, value):
        return value == cls.YES
    
    @classmethod
    def from_bool(cls, value):
        return cls.YES if value else cls.NO


class AccessChoices(models.IntegerChoices):
    """
    Choices para controle de acesso utilizando IntegerChoices para melhor performance
    """
    DENIED = 0, _('Negado')
    ALLOWED = 1, _('Permitido')
    
    # Mapeamento para compatibilidade com o legado
    @classmethod
    def from_legacy(cls, value):
        legacy_map = {
            'S': cls.ALLOWED,
            'N': cls.DENIED
        }
        return legacy_map.get(value, cls.DENIED)
    
    @classmethod
    def to_legacy(cls, value):
        legacy_map = {
            cls.ALLOWED: 'S',
            cls.DENIED: 'N'
        }
        return legacy_map.get(value, 'N')


# Funções auxiliares para mapeamentos legados
def legacy_to_boolean(value):
    """Converte valor legado (S/N) para booleano"""
    return value == 'S'

def boolean_to_legacy(value):
    """Converte booleano para valor legado (S/N)"""
    return 'S' if value else 'N'

# Mapeamento direto para APIs que precisam de valores específicos
PERMISSION_MAPPING = {
    'S': True,
    'N': False,
    True: 'S',
    False: 'N'
}

# Funções auxiliares para verificação de permissões

def check_permission_value(permission_value):
    """
    Verifica se um valor de permissão está concedido.
    
    Args:
        permission_value: valor da permissão (IntegerChoices.YES ou IntegerChoices.NO)
        
    Returns:
        bool: True se permissão concedida, False caso contrário
    """
    return permission_value == PermissionChoices.YES

def permission_to_boolean(permission_obj):
    """
    Converte um objeto UserPermission para booleano para fácil verificação.
    
    Args:
        permission_obj: objeto UserPermission ou None
        
    Returns:
        bool: True se permissão concedida ou usuário for superuser, False caso contrário
    """
    if permission_obj is None:
        return False
    return permission_obj.permission == PermissionChoices.YES
