from .funcoes import (FuncaoCreateView, FuncaoDeleteView, FuncaoListView,
                      FuncaoUpdateView, GrupoFuncaoCreateView,
                      GrupoFuncaoDeleteView, GrupoFuncaoListView,
                      GrupoFuncaoUpdateView)
from .policiais import (PolicialDeleteView, PolicialListView,
                        PolicialUpdateView, PolicialWizardView)

__all__ = [
    'FuncaoCreateView', 'FuncaoDeleteView', 'FuncaoListView', 'FuncaoUpdateView',
    'GrupoFuncaoCreateView', 'GrupoFuncaoDeleteView', 'GrupoFuncaoListView',
    'GrupoFuncaoUpdateView', 'PolicialWizardView',
    'PolicialListView', 'PolicialUpdateView',
    'PolicialDeleteView'
]
