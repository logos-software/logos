from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.utils.models import UUIDBaseModel
from apps.users.models.auth.user import User
from apps.users.models.auth.permissions import EventPermission


class Module(UUIDBaseModel):
    """
    Módulos do sistema (Notas, Administrativo, etc).
    Usado para organizar e categorizar funcionalidades.
    """

    name = models.CharField(_('Nome'), max_length=100)
    code = models.CharField(_('Código'), max_length=50, unique=True)
    slug = models.SlugField(_('Identificador'), max_length=100, unique=True)
    description = models.TextField(_('Descrição'), blank=True)
    icon = models.CharField(_('Ícone'), max_length=50, blank=True)
    requires_authentication = models.BooleanField(_('Requer Autenticação'), default=True)
    permission_required = models.ForeignKey(
        EventPermission,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='modules',
        verbose_name=_('Permissão Necessária')
    )
    url_pattern = models.CharField(_('Padrão de URL'), max_length=200, blank=True)
    is_visible = models.BooleanField(_('Visível no Menu'), default=True)
    is_active = models.BooleanField(_('Ativo'), default=True)
    order = models.PositiveIntegerField(_('Ordem'), default=0)
    
    class Meta:
        verbose_name = _('Módulo')
        verbose_name_plural = _('Módulos')
        ordering = ['order', 'name']
        
    def __str__(self):
        return self.name

    def get_menu_title(self):
        """
        Retorna o título a ser exibido no menu.
        Para módulos de notas, inclui o status inicial.
        """
        if hasattr(self, 'note_module'):
            return f'{self.name}'
        return self.name

    def get_absolute_url(self):
        """
        Retorna a URL para acesso ao módulo, considerando a categoria.
        """
        if self.url_pattern:
            return self.url_pattern
            
        url = f'/'
        if hasattr(self, 'note_module'):
            url = f'{url}/{self.note_module.note_status.id}'
        return f'{url}/{self.slug}/'

    def user_has_permission(self, user):
        """
        Verifica se um usuário tem permissão para acessar este módulo.
        
        Args:
            user: Instância do modelo User
            
        Returns:
            bool: True se o usuário tem permissão, False caso contrário
        """
        # Se não requer autenticação, permite acesso
        if not self.requires_authentication:
            return True
            
        # Se requer autenticação, verifica se o usuário está logado
        if not user.is_authenticated:
            return False
            
        # Se não requer permissão específica, só precisa estar autenticado
        if not self.permission_required:
            return True
            
        # Verifica se o usuário tem a permissão específica
        return user.check_permission(self.permission_required.codename)

