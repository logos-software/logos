from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from apps.users.models.auth.managers import UserManager
from apps.users.models.auth.choices import (
    UserTypeChoices, UserStatusChoices,
)

from apps.utils.models import UUIDBaseModel

from apps.users.models.auth.constants import (
    USER_STATUS_ACTIVE, USER_TYPE_POLICE
)


class User(AbstractUser, UUIDBaseModel):
    """
    Modelo unificado de usuário do sistema.
    Substitui os modelos SenhaUsuario e SenhaServico.
    Usa o AbstractUser do Django para aproveitar recursos como permissões.
    """
    # Campos do usuário
    username = models.CharField(_('Nome de usuário'), max_length=150, unique=True)
    email = models.EmailField(_('Email'), blank=True, null=True)
    first_name = models.CharField(_('Nome'), max_length=150, blank=True)
    last_name = models.CharField(_('Sobrenome'), max_length=150, blank=True)

    # Campos específicos do sistema
    registration_number = models.CharField(_('Matrícula'), max_length=30, blank=True, null=True)

    # Tipo e status do usuário
    user_type = models.IntegerField(
        _('Tipo de usuário'),
        choices=UserTypeChoices.choices,
        default=USER_TYPE_POLICE
    )
    status = models.IntegerField(
        _('Status'),
        choices=UserStatusChoices.choices,
        default=USER_STATUS_ACTIVE
    )

    # Campos de segurança
    login_attempts = models.PositiveIntegerField(
        _('Tentativas de login'), default=0)
    lockout_until = models.DateTimeField(
        _('Bloqueado até'), null=True, blank=True)
    password_changed_at = models.DateTimeField(
        _('Senha alterada em'), default=timezone.now)

    # Campos de rastreabilidade
    created_by = models.ForeignKey(
        'self',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='created_users',
        verbose_name=_('Criado por')
    )
    last_login_ip = models.GenericIPAddressField(
        _('IP do último login'), null=True, blank=True)

    objects = UserManager()

    class Meta:
        verbose_name = _('Usuário')
        verbose_name_plural = _('Usuários')
        db_table = 'USUARIOS'
        ordering = ['username']

    def __str__(self):
        if self.first_name or self.last_name:
            return f"{self.first_name} {self.last_name} ({self.username})"
        return self.username

    @property
    def full_name(self):
        """
        Retorna o nome completo do usuário ou username se não existir.
        """
        if self.first_name and self.last_name:
            return f"{self.first_name} {self.last_name}"
        return self.username    
    
    # Vamos substituir por um método que verifica o status
    def check_if_active(self):
        """
        Determina se o usuário está ativo baseado no status e bloqueio.
        """
        return self.status == USER_STATUS_ACTIVE and not self.is_locked_out()
        
    def save(self, *args, **kwargs):
        self.is_active = (self.status == USER_STATUS_ACTIVE)
        super().save(*args, **kwargs)

    def is_locked_out(self):
        """
        Verifica se o usuário está bloqueado por tentativas excessivas de login.
        """
        if not self.lockout_until:
            return False
        return timezone.now() < self.lockout_until

    def password_expired(self):
        """
        Verifica se a senha do usuário expirou.
        """
        from apps.users.models.auth.constants import PASSWORD_EXPIRY_DAYS
        if not self.password_changed_at:
            return True
        return (timezone.now() - self.password_changed_at).days > PASSWORD_EXPIRY_DAYS

    def record_login_attempt(self, success, ip_address=None):
        """
        Registra uma tentativa de login e bloqueia o usuário após muitas tentativas.
        """
        from apps.users.models.auth.constants import MAX_LOGIN_ATTEMPTS, LOGIN_LOCKOUT_MINUTES

        if success:
            self.login_attempts = 0
            self.lockout_until = None
            if ip_address:
                self.last_login_ip = ip_address
        else:
            self.login_attempts += 1

            if self.login_attempts >= MAX_LOGIN_ATTEMPTS:
                self.lockout_until = timezone.now() + timezone.timedelta(minutes=LOGIN_LOCKOUT_MINUTES)

        self.save(update_fields=['login_attempts',
                  'lockout_until', 'last_login_ip'])

        # Registra o acesso
        if success:
            UserAccess.objects.create(
                user=self,
                ip_address=ip_address,
                success=success
            )    
    
    def has_event_permission(self, event_codename):
        """
        Verifica se o usuário tem permissão para o evento especificado.

        Args:
            event_codename: Código do evento

        Returns:
            bool: True se tem permissão, False caso contrário
        """
        # Superusuários têm todas as permissões
        if self.is_superuser:
            return True

        # Verifica nas permissões do usuário usando IntegerChoices
        from apps.users.models.auth.choices import PermissionChoices
        
        return self.user_permissions.filter(
            event__codename=event_codename,
            permission=PermissionChoices.YES
        ).exists()

    def check_permission(self, event_codename):
        """
        Verifica se o usuário tem permissão para um evento específico.
        Este método é uma interface mais limpa que has_event_permission.
        
        Args:
            event_codename: Código do evento
            
        Returns:
            bool: True se o usuário tem permissão
        """
        # Atalho para usuários superusuários
        if self.is_superuser:
            return True
            
        # Para usuários normais, verificamos nas permissões
        from apps.users.models.auth.permissions import UserPermission, EventPermission
        from apps.users.models.auth.choices import PermissionChoices
        
        try:
            # Tentamos obter o evento pelo codename
            event = EventPermission.objects.get(codename=event_codename)
            
            # Verificamos a permissão do usuário
            perm = UserPermission.objects.get(user=self, event=event)
            return perm.permission == PermissionChoices.YES
        except (EventPermission.DoesNotExist, UserPermission.DoesNotExist):
            # Se o evento ou permissão não existir, negamos acesso
            return False

    def activate(self):
        """
        Ativa o usuário.
        """
        self.status = UserStatusChoices.ACTIVE
        self.is_active = True
        self.save(update_fields=['status', 'is_active'])
        
    def deactivate(self):
        """
        Desativa o usuário.
        """
        self.status = UserStatusChoices.INACTIVE
        self.is_active = False
        self.save(update_fields=['status', 'is_active'])
        
    def suspend(self):
        """
        Suspende o usuário.
        """
        self.status = UserStatusChoices.SUSPENDED
        self.is_active = False
        self.save(update_fields=['status', 'is_active'])

    def convert_to_legacy_format(self):
        """
        Converte os valores do modelo para formato legado.
        Útil para interagir com código legado.
        """
        return {
            'username': self.username,
            'status': UserStatusChoices.to_legacy(self.status),
            'user_type': UserTypeChoices.to_legacy(self.user_type),
            'cod_pm': self.cod_pm,
            'cod_senha_serv': self.cod_senha_serv,
        }
        
    @classmethod
    def from_legacy_data(cls, data):
        """
        Cria uma instância de User a partir de dados legados.
        
        Args:
            data: Dicionário com dados do formato legado
            
        Returns:
            User: Nova instância de User
        """
        user = cls(
            username=data.get('username'),
            status=UserStatusChoices.from_legacy(data.get('status')),
            user_type=UserTypeChoices.from_legacy(data.get('tipo')),
            cod_pm=data.get('cod_pm'),
            cod_senha_serv=data.get('cod_senha_serv'),
        )
        
        # Define is_active baseado no status
        user.is_active = (user.status == UserStatusChoices.ACTIVE)
        
        # Define se é staff baseado no tipo de usuário
        user.is_staff = user.user_type in [UserTypeChoices.STAFF, UserTypeChoices.ADMIN]
        
        return user


class UserAccess(models.Model):
    """
    Modelo unificado para registrar acessos de usuários.
    Substitui os modelos UsuarioAcesso e SenhaServAcesso.
    """
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='access_logs',
        verbose_name=_('Usuário')
    )
    date_time = models.DateTimeField(_('Data/hora'), auto_now_add=True)
    ip_address = models.GenericIPAddressField(_('Endereço IP'), null=True, blank=True)
    user_agent = models.CharField(_('User Agent'), max_length=255, blank=True, null=True)
    session_id = models.CharField(_('ID da sessão'), max_length=100, blank=True, null=True)
    success = models.BooleanField(_('Sucesso'), default=True)
    details = models.TextField(_('Detalhes'), blank=True, null=True)

    class Meta:
        verbose_name = _('Log de acesso')
        verbose_name_plural = _('Logs de acesso')
        db_table = 'USUARIO_ACESSO_LOG'
        ordering = ['-date_time']

    def __str__(self):
        return f"Acesso de {self.user} em {self.date_time.strftime('%d/%m/%Y %H:%M')}"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
