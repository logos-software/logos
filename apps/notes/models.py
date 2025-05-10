from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.utils.models import UUIDBaseModel
from apps.users.models.auth.user import User


class NoteModule(UUIDBaseModel):
    """
    Modelo para configurações específicas de módulos de notas.
    Possui uma relação um-para-um com o modelo Module.
    """
    module = models.OneToOneField(
        "core.Module",
        on_delete=models.CASCADE,
        related_name='note_module',
        verbose_name=_('Módulo')
    )
    note_status = models.ForeignKey(
        'NoteStatus',
        on_delete=models.PROTECT,
        related_name='note_modules',
        verbose_name=_('Status Inicial'),
        help_text=_('Status inicial para notas criadas neste módulo')
    )
    require_approval = models.BooleanField(
        _('Requer Aprovação'),
        default=True,
        help_text=_('Se notas deste módulo requerem aprovação')
    )
    allow_drafts = models.BooleanField(
        _('Permite Rascunhos'),
        default=True,
        help_text=_('Se notas podem ser salvas como rascunho')
    )

    class Meta:
        verbose_name = _('Módulo de Notas')
        verbose_name_plural = _('Módulos de Notas')
        ordering = ['module__order', 'module__name']

    def __str__(self):
        return f"Configurações de Nota - {self.module.name}"

    def can_create_revision(self, note):
        """
        Verifica se uma nova revisão pode ser criada para a nota.
        """
        return note.version < self.max_version

    def validate_note(self, note):
        """
        Valida se uma nota está de acordo com as regras do módulo.
        """
        if not self.allow_drafts and note.is_draft:
            raise ValueError(_('Este módulo não permite rascunhos'))

        if self.require_approval and note.status != self.note_status:
            raise ValueError(_('Status inicial inválido'))


class NoteTypeGroup(UUIDBaseModel):
    """
    Modelo para grupos de tipos de notas (Afastamento, etc).
    """
    module = models.ForeignKey(NoteModule, on_delete=models.CASCADE, related_name='type_groups', verbose_name=_('Módulo'))
    
    name = models.CharField(_('Nome'), max_length=100)
    description = models.TextField(_('Descrição'), blank=True)
    is_active = models.BooleanField(_('Ativo'), default=True)

    class Meta:
        verbose_name = _('Grupo de Tipos de Nota')
        verbose_name_plural = _('Grupos de Tipos de Nota')
        ordering = ['name']

    def __str__(self):
        return self.name


class NoteType(UUIDBaseModel):
    """
    Modelo para os tipos de notas (Ferias, etc).
    """
    group = models.ForeignKey(
        NoteTypeGroup,
        on_delete=models.PROTECT,
        related_name='note_types',
        null=True,
        blank=True,
        verbose_name=_('Grupo de Tipos')
    )
    
    name = models.CharField(_('Nome'), max_length=100)
    description = models.TextField(_('Descrição'), blank=True)
    is_active = models.BooleanField(_('Ativo'), default=True)

    class Meta:
        verbose_name = _('Tipo de Nota')
        verbose_name_plural = _('Tipos de Nota')
        ordering = ['name']

    def __str__(self):
        return self.name


class NoteStatus(UUIDBaseModel):
    """
    Modelo para os status possíveis de uma nota no fluxo de trabalho.
    """
    name = models.CharField(_('Nome'), max_length=100)
    description = models.TextField(_('Descrição'), blank=True)
    is_active = models.BooleanField(_('Ativo'), default=True)
    order = models.PositiveIntegerField(_('Ordem'), default=0)

    class Meta:
        verbose_name = _('Status de Nota')
        verbose_name_plural = _('Status de Nota')
        ordering = ['order', 'name']

    def __str__(self):
        return self.name


class Note(UUIDBaseModel):
    """
    Modelo principal para notas.
    """
    title = models.CharField(_('Título'), max_length=200)
    content = models.TextField(_('Conteúdo'))
    note_type = models.ForeignKey(
        NoteType,
        on_delete=models.PROTECT,
        related_name='notes',
        verbose_name=_('Tipo de Nota')
    )
    status = models.ForeignKey(
        NoteStatus,
        on_delete=models.PROTECT,
        related_name='notes',
        verbose_name=_('Status')
    )

    # Campos de controle
    is_draft = models.BooleanField(_('Rascunho'), default=True)
    is_active = models.BooleanField(_('Ativa'), default=True)
    version = models.PositiveIntegerField(_('Versão'), default=1)

    # Relações com usuários
    created_by = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name='notes_created',
        verbose_name=_('Criado por')
    )
    updated_by = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name='notes_updated',
        verbose_name=_('Atualizado por'),
        null=True,
        blank=True
    )

    class Meta:
        verbose_name = _('Nota')
        verbose_name_plural = _('Notas')
        ordering = ['-created_at']

    def __str__(self):
        return self.title


class NoteEvent(UUIDBaseModel):
    """
    Modelo para eventos relacionados a notas (criação, atualização, etc).
    """
    note = models.ForeignKey(
        Note,
        on_delete=models.CASCADE,
        related_name='events',
        verbose_name=_('Nota')
    )
    event_type = models.CharField(_('Tipo de Evento'), max_length=50)
    description = models.TextField(_('Descrição'))
    user = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name='note_events',
        verbose_name=_('Usuário')
    )

    class Meta:
        verbose_name = _('Evento de Nota')
        verbose_name_plural = _('Eventos de Nota')
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.event_type} - {self.note.title}"


class NoteApproval(UUIDBaseModel):
    """
    Modelo para registrar aprovações de notas.
    """
    note = models.ForeignKey(
        Note,
        on_delete=models.CASCADE,
        related_name='approvals',
        verbose_name=_('Nota')
    )
    user = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name='note_approvals',
        verbose_name=_('Usuário')
    )
    is_approved = models.BooleanField(_('Aprovado'), default=False)
    comments = models.TextField(_('Comentários'), blank=True)

    class Meta:
        verbose_name = _('Aprovação de Nota')
        verbose_name_plural = _('Aprovações de Nota')
        ordering = ['-created_at']

    def __str__(self):
        status = _('aprovada') if self.is_approved else _('rejeitada')
        return f"Nota {status} por {self.user.get_full_name()}"


class NoteRevision(UUIDBaseModel):
    """
    Modelo para controle de versões de notas.
    """
    note = models.ForeignKey(
        Note,
        on_delete=models.CASCADE,
        related_name='revisions',
        verbose_name=_('Nota')
    )
    title = models.CharField(_('Título'), max_length=200)
    content = models.TextField(_('Conteúdo'))
    version = models.PositiveIntegerField(_('Número da Versão'))
    user = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name='note_revisions',
        verbose_name=_('Usuário')
    )
    comments = models.TextField(_('Comentários da Revisão'), blank=True)

    class Meta:
        verbose_name = _('Revisão de Nota')
        verbose_name_plural = _('Revisões de Nota')
        ordering = ['-version']
        unique_together = [('note', 'version')]

    def __str__(self):
        return f"{self.note.title} - Versão {self.version}"
