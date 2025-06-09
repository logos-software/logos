from django.urls import path

from apps.police.views import (FuncaoCreateView, FuncaoDeleteView,
                               FuncaoListView, FuncaoUpdateView,
                               GrupoFuncaoCreateView, GrupoFuncaoDeleteView,
                               GrupoFuncaoListView, GrupoFuncaoUpdateView)

app_name = 'police'

urlpatterns = [
    # URLs para Grupo de Função
    path(
        'grupos-funcao/',
        GrupoFuncaoListView.as_view(),
        name='grupo-funcao-list'
    ),
    path(
        'grupos-funcao/novo/',
        GrupoFuncaoCreateView.as_view(),
        name='grupo-funcao-create'
    ),
    path(
        'grupos-funcao/<int:pk>/editar/',
        GrupoFuncaoUpdateView.as_view(),
        name='grupo-funcao-update'
    ),
    path(
        'grupos-funcao/<int:pk>/excluir/',
        GrupoFuncaoDeleteView.as_view(),
        name='grupo-funcao-delete'
    ),

    # URLs para Função
    path(
        'funcoes/',
        FuncaoListView.as_view(),
        name='funcao-list'
    ),
    path(
        'funcoes/nova/',
        FuncaoCreateView.as_view(),
        name='funcao-create'
    ),
    path(
        'funcoes/<int:pk>/editar/',
        FuncaoUpdateView.as_view(),
        name='funcao-update'
    ),
    path(
        'funcoes/<int:pk>/excluir/',
        FuncaoDeleteView.as_view(),
        name='funcao-delete'
    ),
]
