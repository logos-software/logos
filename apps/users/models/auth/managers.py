from django.contrib.auth.models import UserManager as DjangoUserManager
from django.db.models import Q
from django.utils import timezone

from apps.users.models.auth.constants import USER_STATUS_ACTIVE, USER_TYPE_ADMIN


class UserManager(DjangoUserManager):
    """
    Manager personalizado para o modelo de usuário unificado.
    """
    def create_user(self, username, email=None, password=None, **extra_fields):
        """
        Cria e salva um usuário com o username e senha fornecidos.
        """
        if not username:
            raise ValueError('O nome de usuário é obrigatório')
        
        # Configurações padrão
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('status', USER_STATUS_ACTIVE)
        
        if email:
            email = self.normalize_email(email)
        else:
            email = None
            
        user = self.model(username=username, email=email, **extra_fields)
        
        if password:
            user.set_password(password)
        
        user.save(using=self._db)
        return user
    
    def create_superuser(self, username, email=None, password=None, **extra_fields):
        """
        Cria um usuário com permissões de administrador.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('user_type', USER_TYPE_ADMIN)
        
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser deve ter is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser deve ter is_superuser=True.')
            
        return self.create_user(username, email, password, **extra_fields)
    
    def active(self):
        """
        Retorna apenas usuários ativos.
        """
        return self.get_queryset().filter(is_active=True)
    
    def staff(self):
        """
        Retorna apenas usuários da equipe administrativa.
        """
        return self.get_queryset().filter(is_staff=True)
    
    def police(self):
        """
        Retorna apenas usuários policiais (não administrativos).
        """
        return self.get_queryset().filter(is_staff=False)
    
    def with_failed_attempts(self):
        """
        Retorna usuários com tentativas de login falhas.
        """
        return self.get_queryset().filter(login_attempts__gt=0)
    
    def create_police_user(self, username, password=None, **extra_fields):
        """
        Cria um usuário do tipo policial.
        """
        from apps.users.models.auth.choices import UserTypeChoices
        
        extra_fields['user_type'] = UserTypeChoices.POLICE
        extra_fields['is_staff'] = False
        
        return self.create_user(username, None, password, **extra_fields)
        
    def create_staff_user(self, username, password=None, **extra_fields):
        """
        Cria um usuário do tipo administrativo.
        """
        from apps.users.models.auth.choices import UserTypeChoices
        
        extra_fields['user_type'] = UserTypeChoices.STAFF
        extra_fields['is_staff'] = True
        
        return self.create_user(username, None, password, **extra_fields)
        
    def create_admin_user(self, username, password=None, **extra_fields):
        """
        Cria um usuário do tipo administrador.
        """
        from apps.users.models.auth.choices import UserTypeChoices
        
        extra_fields['user_type'] = UserTypeChoices.ADMIN
        extra_fields['is_staff'] = True
        
        return self.create_user(username, None, password, **extra_fields)
        
    def get_by_type(self, user_type):
        """
        Retorna usuários por tipo.
        """
        return self.get_queryset().filter(user_type=user_type)
