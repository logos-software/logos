from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from .models import (
    NoteModule, NoteTypeGroup, NoteType, NoteStatus,
    Note, NoteEvent, NoteApproval, NoteRevision
)


@admin.register(NoteModule)
class NoteModuleAdmin(admin.ModelAdmin):
    list_display = ('module', 'note_status', 'require_approval', 'allow_drafts')
    list_filter = ('require_approval', 'allow_drafts')
    search_fields = ('module__name',)
    raw_id_fields = ('module', 'note_status')


@admin.register(NoteTypeGroup)
class NoteTypeGroupAdmin(admin.ModelAdmin):
    list_display = ('name', 'module', 'description', 'is_active')
    list_filter = ('is_active', 'module')
    search_fields = ('name', 'description')
    raw_id_fields = ('module',)


@admin.register(NoteType)
class NoteTypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'group', 'description', 'is_active')
    search_fields = ('name', 'description')
    list_filter = ('is_active', 'group')
    raw_id_fields = ('group',)


@admin.register(NoteStatus)
class NoteStatusAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'order', 'is_active')
    search_fields = ('name', 'description')
    list_filter = ('is_active',)
    ordering = ('order',)


@admin.register(Note)
class NoteAdmin(admin.ModelAdmin):
    list_display = ('title', 'note_type', 'status', 'created_by', 'created_at', 'version')
    search_fields = ('title', 'content', 'created_by__username')
    list_filter = ('note_type', 'status', 'is_draft', 'is_active')
    date_hierarchy = 'created_at'
    readonly_fields = ('created_by', 'updated_by', 'created_at', 'updated_at')

    def save_model(self, request, obj, form, change):
        if not change:  # Se é uma nova nota
            obj.created_by = request.user
        obj.updated_by = request.user
        super().save_model(request, obj, form, change)


@admin.register(NoteEvent)
class NoteEventAdmin(admin.ModelAdmin):
    list_display = ('note', 'event_type', 'user', 'created_at')
    search_fields = ('note__title', 'description', 'user__username')
    list_filter = ('event_type', 'created_at')
    date_hierarchy = 'created_at'
    readonly_fields = ('created_at', 'updated_at')


@admin.register(NoteApproval)
class NoteApprovalAdmin(admin.ModelAdmin):
    list_display = ('note', 'user', 'is_approved', 'created_at')
    search_fields = ('note__title', 'user__username', 'comments')
    list_filter = ('is_approved', 'created_at')
    date_hierarchy = 'created_at'
    readonly_fields = ('created_at', 'updated_at')


@admin.register(NoteRevision)
class NoteRevisionAdmin(admin.ModelAdmin):
    list_display = ('note', 'version', 'user', 'created_at')
    search_fields = ('note__title', 'title', 'user__username', 'comments')
    list_filter = ('version', 'created_at')
    date_hierarchy = 'created_at'
    readonly_fields = ('created_at', 'updated_at')
