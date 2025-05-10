from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin
from django.utils.translation import gettext_lazy as _

from apps.users.models import User, UserAccess, Permission, EventPermission, UserPermission


@admin.register(User)
class UserAdmin(DjangoUserAdmin):
    """Admin para o modelo User"""
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('Informações Pessoais'), {'fields': ('first_name', 'last_name', 'email', 'registration_number')}),
        (_('Permissões'), {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'user_type', 'status', 
                       'groups'),
        }),
        (_('Datas Importantes'), {'fields': ('last_login', 'date_joined')}),
        (_('Segurança'), {'fields': ('login_attempts', 'lockout_until', 'password_changed_at', 'last_login_ip')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2', 'user_type', 'status'),
        }),
    )

    list_display = ('username', 'first_name', 'last_name', 'is_active', 'user_type', 'status')
    list_filter = ('is_active', 'user_type', 'status', 'is_staff', 'is_superuser')
    search_fields = ('username', 'first_name', 'last_name', 'email', 'registration_number')
    ordering = ('username',)
    filter_horizontal = ('groups', 'user_permissions')
    
    actions = ['activate_users', 'deactivate_users', 'suspend_users']
    
    def activate_users(self, request, queryset):
        """Ativa usuários selecionados"""
        for user in queryset:
            user.activate()
        self.message_user(request, f"{queryset.count()} usuários foram ativados com sucesso.")
    activate_users.short_description = "Ativar usuários selecionados"
    
    def deactivate_users(self, request, queryset):
        """Desativa usuários selecionados"""
        for user in queryset:
            user.deactivate()
        self.message_user(request, f"{queryset.count()} usuários foram desativados com sucesso.")
    deactivate_users.short_description = "Desativar usuários selecionados"
    
    def suspend_users(self, request, queryset):
        """Suspende usuários selecionados"""
        for user in queryset:
            user.suspend()
        self.message_user(request, f"{queryset.count()} usuários foram suspensos com sucesso.")
    suspend_users.short_description = "Suspender usuários selecionados"


@admin.register(UserAccess)
class UserAccessAdmin(admin.ModelAdmin):
    """Admin para o modelo UserAccess"""
    list_display = ('user', 'date_time', 'ip_address', 'success')
    list_filter = ('success', 'date_time')
    search_fields = ('user__username', 'ip_address', 'user_agent')
    date_hierarchy = 'date_time'
    readonly_fields = ('date_time', 'user', 'ip_address', 'user_agent', 'session_id', 'success', 'details')


@admin.register(Permission)
class PermissionAdmin(admin.ModelAdmin):
    """Admin para o modelo Permission"""
    list_display = ('name', 'codename')
    search_fields = ('name', 'codename')


@admin.register(EventPermission)
class EventPermissionAdmin(admin.ModelAdmin):
    """Admin para o modelo EventPermission"""
    list_display = ('name', 'codename', 'short_name')
    search_fields = ('name', 'codename', 'short_name')


@admin.register(UserPermission)
class UserPermissionAdmin(admin.ModelAdmin):
    """Admin para o modelo UserPermission"""
    list_display = ('user', 'event', 'permission_display', 'updated_at')
    list_filter = ('permission', 'event')
    search_fields = ('user__username', 'event__name', 'event__codename')
    date_hierarchy = 'updated_at'
    
    def permission_display(self, obj):
        """Mostra o valor da permissão de forma mais amigável"""
        from apps.users.models.auth.choices import PermissionChoices
        return _('Sim') if obj.permission == PermissionChoices.YES else _('Não')
    permission_display.short_description = _('Permissão')
