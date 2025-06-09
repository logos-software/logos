from django.urls import path

from apps.police.views import (FuncaoCreateView, FuncaoDeleteView,
                               FuncaoListView, FuncaoUpdateView,
                               GrupoFuncaoCreateView, GrupoFuncaoDeleteView,
                               GrupoFuncaoListView, GrupoFuncaoUpdateView)
from apps.police.views.policiais import (PolicialDeleteView, PolicialListView,
                                         PolicialUpdateView,
                                         PolicialWizardView, PolicialDetailView)

app_name = 'police'

urlpatterns = [
    # URLs para Grupo de Função
    path('grupos-funcao/', GrupoFuncaoListView.as_view(), name='grupo-funcao-list'),
    path('grupos-funcao/novo/', GrupoFuncaoCreateView.as_view(), name='grupo-funcao-create'),
    path('grupos-funcao/<int:pk>/editar/', GrupoFuncaoUpdateView.as_view(), name='grupo-funcao-update'),
    path('grupos-funcao/<int:pk>/excluir/', GrupoFuncaoDeleteView.as_view(), name='grupo-funcao-delete'),

    # URLs para Função
    path('funcoes/', FuncaoListView.as_view(), name='funcao-list'),
    path('funcoes/nova/', FuncaoCreateView.as_view(), name='funcao-create'),
    path('funcoes/<int:pk>/editar/', FuncaoUpdateView.as_view(), name='funcao-update'),
    path('funcoes/<int:pk>/excluir/', FuncaoDeleteView.as_view(), name='funcao-delete'),

    # URLs para Policial
    path('policiais/', PolicialListView.as_view(), name='policial-list'),
    path('policiais/novo/', PolicialWizardView.as_view(), name='policial-create'),
    path('policiais/<int:pk>/', PolicialDetailView.as_view(), name='policial-detail'),  # Nova URL
    path('policiais/<int:pk>/editar/', PolicialUpdateView.as_view(), name='policial-update'),
    path('policiais/<int:pk>/excluir/', PolicialDeleteView.as_view(), name='policial-delete'),
]
