from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from .models import Module


@admin.register(Module)
class ModuleAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'slug', 'is_visible', 'is_active', 'order')
    list_filter = ('is_active', 'is_visible', 'requires_authentication')
    search_fields = ('name', 'code', 'slug', 'description')
    prepopulated_fields = {'slug': ('name',)}
    ordering = ('order', 'name')
