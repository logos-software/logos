from django import template
from django.utils.safestring import mark_safe
from django.utils.translation import gettext as _

from apps.core.models import Module
from apps.notes.models import NoteTypeGroup, NoteType

register = template.Library()


@register.simple_tag(takes_context=True)
def render_nav_menu(context):
    """
    Renderiza o menu de navegação baseado nos módulos cadastrados.
    Verifica permissões e organiza por categorias.
    """
    user = context['request'].user

    def build_menu_item(module, title=None, note_type=None, indent=False):
        """Constrói um item do menu"""
        if not module.user_has_permission(user):
            return ''

        if not module.is_active or not module.is_visible:
            return ''

        # Link e ícone
        url = module.get_absolute_url()
        if note_type:
            url = f"{url}?type={note_type.id}"

        icon = f'<i class="{module.icon if module.icon else "pli-file"} fs-5 me-2"></i>'
        
        # Usa o título fornecido ou pega do módulo
        menu_title = title or module.get_menu_title()

        # Classes adicionais se o item estiver indentado
        indent_class = 'ps-4' if indent else ''

        # Construção do HTML do item
        return (
            '<li class="nav-item">'
            f'<a href="{url}" class="nav-link {indent_class}">'
            f'{icon}<span class="nav-label ms-1">{menu_title}</span></a>'
            '</li>'
        )

    # Prefetch dos módulos de notas
    notes_modules = Module.objects.filter(
        is_active=True,
        is_visible=True,
        note_module__isnull=False
    ).select_related(
        'note_module'
    ).order_by('order', 'name')

    # Prefetch dos grupos de tipos de notas e seus tipos
    note_type_groups = NoteTypeGroup.objects.filter(
        is_active=True,
        module__module__in=notes_modules
    ).prefetch_related(
        'note_types',
        'module__module'
    ).order_by('name')

    # Módulos administrativos
    admin_modules = Module.objects.filter(
        is_active=True,
        is_visible=True,
        code__startswith='ADM_'
    ).exclude(
        note_module__isnull=False
    ).order_by('order', 'name')

    # Módulos do sistema
    system_modules = Module.objects.filter(
        is_active=True,
        is_visible=True,
        code__startswith='SYS_'
    ).exclude(
        note_module__isnull=False
    ).order_by('order', 'name')

    menu_sections = []

    # Seção de Notas
    if notes_modules:
        notes_section = []

        # Primeiro, vamos adicionar todos os grupos de tipos
        for i, group in enumerate(note_type_groups):
            if not group.is_active:
                continue

            # Pegar o módulo associado ao grupo
            module = group.module.module

            # Criar um ID único para o collapse
            collapse_id = f'group-collapse-{group.id}'
            
            # Adicionar o cabeçalho do grupo com botão de collapse
            group_html = [
                '<li class="nav-item sub-category">',
                f'<div class="d-flex align-items-center justify-content-between px-3 py-2">',
                f'<h6 class="nav-label mb-0 fw-bold">{group.name}</h6>',
                f'<button class="btn btn-link p-0 text-decoration-none" type="button" ',
                f'data-bs-toggle="collapse" data-bs-target="#{collapse_id}" ',
                f'aria-expanded="true" aria-controls="{collapse_id}">',
                '<i class="fas fa-chevron-down"></i>',
                '</button>',
                '</div>',
                '</li>'
            ]
            notes_section.extend(group_html)

            # Container colapsável para os tipos de notas
            collapse_html = [
                f'<div class="collapse show" id="{collapse_id}">',
                '<div class="py-1">'
            ]
            notes_section.extend(collapse_html)

            # Adicionar os tipos de notas do grupo
            for note_type in group.note_types.filter(is_active=True):
                notes_section.append(build_menu_item(
                    module, 
                    title=note_type.name, 
                    note_type=note_type,
                    indent=True
                ))

            # Fechar o container colapsável
            notes_section.extend(['</div>', '</div>'])

        if notes_section:  # Se houver algum item com permissão
            menu_sections.append((
                _('Notas'),
                'pli-note',
                notes_section
            ))

    # Seção Administrativa
    if admin_modules:
        items = [build_menu_item(module) for module in admin_modules]
        if any(items):
            menu_sections.append((
                _('Administrativo'),
                'pli-gear',
                items
            ))

    # Seção Sistema
    if system_modules:
        items = [build_menu_item(module) for module in system_modules]
        if any(items):
            menu_sections.append((
                _('Sistema'),
                'pli-computer',
                items
            ))

    # Construção do menu completo
    final_html = []
    for title, icon, items in menu_sections:
        if items:
            section_html = [
                '<div class="mainnav__category py-3">',
                f'<h6 class="mainnav__caption mt-0 px-3 fw-bold">'
                f'<i class="{icon} me-2"></i>{title}</h6>',
                '<ul class="mainnav__menu nav flex-column">',
            ]
            
            # Se items for uma lista de strings HTML, adiciona diretamente
            if isinstance(items, list) and items and isinstance(items[0], str):
                section_html.extend(items)
            else:
                # Se não, trata como antes, removendo itens vazios
                section_html.extend([item for item in items if item])
            
            section_html.extend([
                '</ul>',
                '</div>'
            ])
            
            final_html.extend(section_html)

    return mark_safe('\n'.join(final_html))
