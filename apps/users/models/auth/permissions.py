from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.utils.models import BaseModel
from apps.users.models.auth.choices import PermissionChoices



class Permission(BaseModel):
    """
    Modelo para gerenciar permissões de usuários no sistema.
    Esse modelo substitui a lógica anterior de campos dinâmicos.
    """
    name = models.CharField(_('Nome'), max_length=100)
    codename = models.CharField(_('Código'), max_length=100, unique=True)
    description = models.TextField(_('Descrição'), blank=True, null=True)
    
    class Meta:
        verbose_name = _('Permissão')
        verbose_name_plural = _('Permissões')
        db_table = 'PERMISSAO'
        ordering = ['name']
        
    def __str__(self):
        return self.name


class EventPermission(BaseModel):
    """
    Modelo para relacionar eventos do sistema com permissões.
    """
    name = models.CharField(_('Nome do evento'), max_length=100)
    short_name = models.CharField(_('Nome abreviado'), max_length=50)
    codename = models.CharField(_('Código'), max_length=100, unique=True)
    description = models.TextField(_('Descrição'), blank=True, null=True)
    
    class Meta:
        verbose_name = _('Evento do sistema')
        verbose_name_plural = _('Eventos do sistema')
        db_table = 'EVENTO_SISTEMA'
        ordering = ['name']
        
    def __str__(self):
        return self.name
        
    def get_normalized_name(self):
        """
        Retorna o nome normalizado do evento para uso em permissões.
        """
        from unidecode import unidecode
        return unidecode(self.short_name.lower().replace(" ", "_"))


class UserPermission(BaseModel):
    """
    Modelo para relacionar usuários com suas permissões.
    Substitui a lógica de colunas dinâmicas usada anteriormente.
    """
    user = models.ForeignKey(
        'users.User',
        on_delete=models.CASCADE,
        related_name='event_permissions',
        verbose_name=_('Usuário')
    )
    event = models.ForeignKey(
        EventPermission,
        on_delete=models.CASCADE, 
        related_name='user_permissions',
        verbose_name=_('Evento')
    )
    permission = models.IntegerField(
        _('Permissão'), 
        choices=PermissionChoices.choices,
        default=PermissionChoices.NO
    )
    
    # Campos para compatibilidade legada
    legacy_value = models.CharField(_('Valor legado'), max_length=1, blank=True, null=True)
    
    class Meta:
        verbose_name = _('Permissão do usuário')
        verbose_name_plural = _('Permissões dos usuários')
        db_table = 'USUARIO_PERMISSAO'
        unique_together = ['user', 'event']
        
    def __str__(self):
        return f"{self.user} - {self.event}"
        
    def save(self, *args, **kwargs):
        self.legacy_value = PermissionChoices.to_legacy(self.permission)
        super().save(*args, **kwargs)
        
    @property
    def is_allowed(self):
        """Verifica se a permissão foi concedida"""
        return self.permission == PermissionChoices.YES
