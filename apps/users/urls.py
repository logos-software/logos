"""
URLs para o aplicativo users.
"""
from django.contrib.auth import views as auth_views
from django.urls import path, include

from . import views

app_name = 'users'

urlpatterns = [
    # URLs para autenticação
    path('login/', views.SignInView.as_view(), name='login'),
    path('logout/', views.SignOutView.as_view(), name='logout'),
    path('perfil/', views.ProfileView.as_view(), name='profile'),

    # URLs para gerenciamento de permissões
    path('usuario/<int:user_id>/permissoes/',
         views.UserPermissionsView.as_view(), name='user_permissions'),

    # Redefinição de senha
    path('senha/resetar/',
         auth_views.PasswordResetView.as_view(),
         name='password_reset'
         ),
    path(
        'senha/resetar/confirmacao/<uidb64>/<token>/',
        auth_views.PasswordResetConfirmView.as_view(),
        name='password_reset_confirm'
    ),
    path(
        'senha/alterada/',
        auth_views.PasswordResetCompleteView.as_view(),
        name='password_reset_complete'
    ),
    path(
        'senha/resetar/enviado/',
        auth_views.PasswordResetDoneView.as_view(),
        name='password_reset_done'
    ),
    # API URLs serão implementadas posteriormente
    # path('api/', include(router.urls)),
]
