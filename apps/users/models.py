# Este arquivo importa os modelos do pacote auth
from apps.users.models.auth import User, UserAccess, Permission, EventPermission, UserPermission
from apps.users.models.auth.choices import UserTypeChoices

# Classes de compatibilidade para código legado
class SenhaUsuario(User):
    """Classe de compatibilidade para código legado. Use User."""
    class Meta:
        proxy = True
        
    def save(self, *args, **kwargs):
        # Garantir que seja salvo como usuário tipo policial
        self.user_type = UserTypeChoices.POLICE
        super().save(*args, **kwargs)
        
    @property
    def vigente(self):
        """Compatibilidade com código legado"""
        from apps.users.models.auth.choices import UserStatusChoices, legacy_to_boolean
        return legacy_to_boolean(UserStatusChoices.to_legacy(self.status))
        
    @vigente.setter
    def vigente(self, value):
        """Compatibilidade com código legado"""
        from apps.users.models.auth.choices import UserStatusChoices
        if value == 'S':
            self.status = UserStatusChoices.ACTIVE
        else:
            self.status = UserStatusChoices.INACTIVE


class SenhaServico(User):
    """Classe de compatibilidade para código legado. Use User.""" 
    class Meta:
        proxy = True
        
    def save(self, *args, **kwargs):
        # Garantir que seja salvo como usuário tipo administrativo
        self.user_type = UserTypeChoices.STAFF
        self.is_staff = True
        super().save(*args, **kwargs)
    
    @property
    def is_general_type(self):
        return self.user_type == UserTypeChoices.ADMIN
        
    @property
    def valida(self):
        """Compatibilidade com código legado"""
        from apps.users.models.auth.choices import UserStatusChoices, legacy_to_boolean
        return UserStatusChoices.to_legacy(self.status)
        
    @valida.setter
    def valida(self, value):
        """Compatibilidade com código legado"""
        from apps.users.models.auth.choices import UserStatusChoices
        self.status = UserStatusChoices.from_legacy(value)
        
    @property
    def tipo(self):
        """Compatibilidade com código legado"""
        from apps.users.models.auth.choices import UserTypeChoices
        return UserTypeChoices.to_legacy(self.user_type)
        
    @tipo.setter
    def tipo(self, value):
        """Compatibilidade com código legado"""
        from apps.users.models.auth.choices import UserTypeChoices
        self.user_type = UserTypeChoices.from_legacy(value)

class UsuarioAcesso(UserAccess):
    """Classe de compatibilidade para código legado. Use UserAccess."""
    class Meta:
        proxy = True

class SenhaServAcesso(UserAccess):
    """Classe de compatibilidade para código legado. Use UserAccess."""
    class Meta:
        proxy = True