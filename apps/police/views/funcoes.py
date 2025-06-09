from django.contrib import messages
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, ListView, UpdateView

from apps.police.forms import FuncaoForm, GrupoFuncaoForm
from apps.police.models import Funcao, GrupoFuncao
from apps.utils.views import (BaseCreateView, BaseDeleteView, BaseListView,
                              BaseUpdateView)


class GrupoFuncaoListView(BaseListView):
    model = GrupoFuncao
    template_name = 'police/funcoes/grupo_list.html'
    context_object_name = 'grupos'
    ordering = ['nome']


class GrupoFuncaoCreateView(BaseCreateView):
    model = GrupoFuncao
    form_class = GrupoFuncaoForm
    template_name = 'police/funcoes/includes/_grupo_form.html'
    success_url = reverse_lazy('police:grupo-funcao-list')
    success_message = 'Grupo de função criado com sucesso!'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Novo Grupo de Função'
        return context


class GrupoFuncaoUpdateView(BaseUpdateView):
    model = GrupoFuncao
    form_class = GrupoFuncaoForm
    template_name = 'police/funcoes/includes/_grupo_form.html'
    success_url = reverse_lazy('police:grupo-funcao-list')
    success_message = 'Grupo de função atualizado com sucesso!'

    def get_form_kwargs(self):
        """Garante que os dados do objeto são passados para o form"""
        kwargs = super().get_form_kwargs()
        if hasattr(self, 'object'):
            kwargs.update({'instance': self.object})
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'title': f'Editar Grupo: {self.object.nome}',
            'object': self.object,
        })
        return context


class GrupoFuncaoDeleteView(BaseDeleteView):
    model = GrupoFuncao
    success_url = reverse_lazy('police:grupo-funcao-list')

# Views para Função


class FuncaoListView(ListView):
    model = Funcao
    template_name = 'police/funcoes/funcao_list.html'
    context_object_name = 'funcoes'
    ordering = ['nome']
    paginate_by = 10


class FuncaoCreateView(CreateView):
    model = Funcao
    form_class = FuncaoForm
    template_name = 'police/funcoes/funcao_form.html'
    success_url = reverse_lazy('police:funcao-list')

    def form_valid(self, form):
        messages.success(self.request, 'Função criada com sucesso!')
        return super().form_valid(form)

    def form_invalid(self, form):
        if self.request.is_ajax():
            return JsonResponse(form.errors, status=400)
        return super().form_invalid(form)


class FuncaoUpdateView(UpdateView):
    model = Funcao
    form_class = FuncaoForm
    template_name = 'police/funcoes/funcao_form.html'
    success_url = reverse_lazy('police:funcao-list')

    def form_valid(self, form):
        messages.success(self.request, 'Função atualizada com sucesso!')
        return super().form_valid(form)


class FuncaoDeleteView(DeleteView):
    model = Funcao
    template_name = 'police/funcoes/funcao_confirm_delete.html'
    success_url = reverse_lazy('police:funcao-list')

    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Função excluída com sucesso!')
        return super().delete(request, *args, **kwargs)
