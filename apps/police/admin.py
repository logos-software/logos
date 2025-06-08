from django.contrib import admin

from .models import (CNH, RG, CertidaoNascimento, DadosFamiliares,
                     DadosFisicos, Escolaridade, Fardamento, Funcao,
                     GrupoFuncao, Policial, Reservista, TituloEleitor, HistoricoFuncao)


class DadosFisicosInline(admin.StackedInline):
    model = DadosFisicos
    can_delete = False
    extra = 0


class FardamentoInline(admin.StackedInline):
    model = Fardamento
    can_delete = False
    extra = 0


class DadosFamiliaresInline(admin.TabularInline):
    model = DadosFamiliares
    extra = 1


class EscolaridadeInline(admin.TabularInline):
    model = Escolaridade
    extra = 1


@admin.register(CNH)
class CNHAdmin(admin.ModelAdmin):
    list_display = ('numero', 'policial', 'categoria',
                    'data_validade', 'active')
    search_fields = ('numero', 'policial__nome')
    list_filter = ('categoria', 'data_validade', 'active')
    readonly_fields = ('created_at', 'updated_at')


@admin.register(RG)
class RGAdmin(admin.ModelAdmin):
    list_display = ('numero', 'policial', 'orgao_emissor', 'tipo', 'active')
    search_fields = ('numero', 'policial__nome')
    list_filter = ('tipo', 'active')
    readonly_fields = ('created_at', 'updated_at')


@admin.register(TituloEleitor)
class TituloEleitorAdmin(admin.ModelAdmin):
    list_display = ('numero', 'policial', 'zona', 'secao', 'active')
    search_fields = ('numero', 'policial__nome')
    readonly_fields = ('created_at', 'updated_at')


@admin.register(Reservista)
class ReservistaAdmin(admin.ModelAdmin):
    list_display = ('numero', 'policial', 'categoria', 'csm', 'active')
    search_fields = ('numero', 'policial__nome')
    list_filter = ('categoria', 'active')
    readonly_fields = ('created_at', 'updated_at')


@admin.register(CertidaoNascimento)
class CertidaoNascimentoAdmin(admin.ModelAdmin):
    list_display = ('numero', 'policial', 'cartorio', 'uf', 'active')
    search_fields = ('numero', 'policial__nome', 'cartorio')
    list_filter = ('uf', 'active')
    readonly_fields = ('created_at', 'updated_at')


@admin.register(GrupoFuncao)
class GrupoFuncaoAdmin(admin.ModelAdmin):
    list_display = ('nome', 'active')
    search_fields = ('nome',)
    readonly_fields = ('created_at', 'updated_at')


@admin.register(Funcao)
class FuncaoAdmin(admin.ModelAdmin):
    list_display = ('nome', 'grupo', 'active')
    search_fields = ('nome', 'grupo__nome')
    list_filter = ('grupo', 'active')
    readonly_fields = ('created_at', 'updated_at')

# Policial e Relacionamentos


@admin.register(Policial)
class PolicialAdmin(admin.ModelAdmin):
    list_display = ('nome', 'matricula', 'cpf', 'active')
    search_fields = ('nome', 'matricula', 'cpf')
    list_filter = ('active', 'sexo', 'estado_civil')
    readonly_fields = ('created_at', 'updated_at')
    inlines = [
        DadosFisicosInline,
        FardamentoInline,
        DadosFamiliaresInline,
        EscolaridadeInline
    ]

    fieldsets = (
        ('Dados Pessoais', {
            'fields': (
                ('nome', 'nome_guerra'),
                ('matricula', 'cpf'),
                ('data_nascimento', 'estado_civil', 'sexo'),
                'foto'
            )
        }),
        ('Contatos', {
            'fields': (
                ('email', 'email_pessoal'),
                ('telefone', 'celular')
            )
        }),
        ('Endereço', {
            'fields': (
                'cep',
                ('endereco', 'numero'),
                'complemento',
                ('bairro', 'cidade', 'uf')
            )
        }),
        ('Dados Bancários', {
            'classes': ('collapse',),
            'fields': (
                ('banco', 'agencia', 'conta'),
            )
        }),
        ('Auditoria', {
            'classes': ('collapse',),
            'fields': (('created_at', 'updated_at'), 'active')
        })
    )


@admin.register(HistoricoFuncao)
class HistoricoFuncaoAdmin(admin.ModelAdmin):
    list_display = ('policial', 'funcao', 'documento_numero', 'data_inicio', 'data_fim', 'esta_ativo')
    list_filter = ('funcao', 'data_inicio', 'active')
    search_fields = ('policial__nome', 'funcao__nome', 'matricula_sad', 'documento_numero')
    autocomplete_fields = ['policial', 'funcao']
    readonly_fields = ('created_at', 'updated_at')
    
    fieldsets = (
        ('Informações Básicas', {
            'fields': (('policial', 'funcao'), ('data_inicio', 'data_fim'))
        }),
        ('Documento', {
            'fields': ('documento_numero', 'documento_arquivo')
        }),
        ('Dados Complementares', {
            'fields': ('matricula_sad', 'observacao')
        }),
        ('Auditoria', {
            'classes': ('collapse',),
            'fields': (('created_at', 'updated_at'), 'active')
        })
    )
