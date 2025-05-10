from django.contrib.auth.backends import ModelBackend
from ipware import get_client_ip

from apps.users.models.auth.user import User, UserAccess


class CustomAuthBackend(ModelBackend):
    """
    Backend de autenticação personalizado que:
    1. Suporta login por username ou matrícula
    2. Gerencia tentativas de login e bloqueio de conta
    3. Usa ipware para detecção confiável de IP
    """
    
    def user_can_authenticate(self, user):
        """
        Sobrescreve o método da classe pai para verificar também o bloqueio.
        """
        return super().user_can_authenticate(user) and not user.is_locked_out()
    
    def authenticate(self, request, username=None, password=None, **kwargs):
        if username is None:
            username = kwargs.get('username')
            
        if username is None or password is None:
            return None
            
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            try:
                user = User.objects.get(registration_number=username)
            except User.DoesNotExist:
                if request:
                    ip = self.get_client_ip(request)
                    self.log_failed_attempt(username, ip)
                return None
        
        if user.is_locked_out():
            return None
        
        if user.check_password(password) and self.user_can_authenticate(user):
            if request:
                ip = self.get_client_ip(request)
                user.record_login_attempt(success=True, ip_address=ip)
            return user
        else:
            if request:
                ip = self.get_client_ip(request)
                user.record_login_attempt(success=False, ip_address=ip)
            return None
    
    def get_client_ip(self, request):
        """
        Obtém o IP do cliente usando ipware, que lida melhor com proxies e diferentes
        configurações de servidor.
        
        Returns:
            str|None: O endereço IP do cliente ou None se não for possível determinar
        """
        client_ip, is_routable = get_client_ip(request)
        if client_ip is None:
            return None
            
        return client_ip
    
    def log_failed_attempt(self, username, ip):
        """
        Registra uma tentativa de login falha sem usuário identificado.
        
        Args:
            username: O identificador tentado (username ou matrícula)
            ip: O endereço IP do cliente (pode ser None)
        """
        UserAccess.objects.create(
            user=None,
            ip_address=ip,
            success=False,
            details=f"Tentativa de login com identificador inválido: {username}"
        )
