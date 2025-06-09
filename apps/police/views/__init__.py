from .funcoes import (FuncaoCreateView, FuncaoDeleteView, FuncaoListView,
                      FuncaoUpdateView, GrupoFuncaoCreateView,
                      GrupoFuncaoDeleteView, GrupoFuncaoListView,
                      GrupoFuncaoUpdateView)

__all__ = [
    # Grupo de Função
    'GrupoFuncaoListView',
    'GrupoFuncaoCreateView',
    'GrupoFuncaoUpdateView',
    'GrupoFuncaoDeleteView',

    # Função
    'FuncaoListView',
    'FuncaoCreateView',
    'FuncaoUpdateView',
    'FuncaoDeleteView',
]
