from django.conf import settings
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LogoutView
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse, reverse_lazy
from django.views.generic import TemplateView

from apps.users.exceptions import (IncorrectCredentialsException,
                                   UserAccountLockedException)
from apps.users.models import User
from apps.users.models.auth.permissions import EventPermission


class SignInView(TemplateView):
    template_name = "auth/signin.html"
    
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return HttpResponseRedirect(reverse("core:home"))
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            "title": "Login",
            "app_name": getattr(settings, "APP_NAME", "Sistema Logos")
        })
        return context

    def post(self, request, *args, **kwargs):
        username = request.POST.get("username")
        password = request.POST.get("password")

        try:
            try:
                user = User.objects.get(username=username)
            except User.DoesNotExist:
                raise IncorrectCredentialsException()

            if user.is_locked_out():
                raise UserAccountLockedException(username, user.lockout_until)

            user = authenticate(request, username=username, password=password)
            if user is None:
                user = User.objects.get(username=username)
                user.record_login_attempt(success=False, ip_address=request.META.get('REMOTE_ADDR'))
                raise IncorrectCredentialsException()

            login(request, user)
            
            user.record_login_attempt(
                success=True,
                ip_address=request.META.get('REMOTE_ADDR')
            )
            
            return HttpResponseRedirect(reverse("core:home"))

        except IncorrectCredentialsException:
            messages.error(request, "Usuário ou senha inválidos, favor tente novamente")
        except UserAccountLockedException as e:
            messages.error(request, str(e))
        
        return self.render_to_response(self.get_context_data())


class SignOutView(LogoutView):
    """View para fazer logout do usuário"""
    next_page = reverse_lazy('users:login')
    
    def dispatch(self, request, *args, **kwargs):
        response = super().dispatch(request, *args, **kwargs)
        messages.success(request, "Usuário desconectado com sucesso!")
        return response


class ProfileView(LoginRequiredMixin, TemplateView):
    """View do perfil do usuário"""
    template_name = "users/profile.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Meu Perfil"
        return context


class UserPermissionsView(LoginRequiredMixin, TemplateView):
    """View para gerenciar permissões de um usuário específico"""
    template_name = "users/permissions.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = get_object_or_404(User, id=self.kwargs.get('user_id'))
        context.update({
            'title': f'Permissões do Usuário {user.username}',
            'target_user': user,
            'events': EventPermission.objects.all()
        })
        return context
