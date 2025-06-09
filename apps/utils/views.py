import os

from django.conf import settings
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ImproperlyConfigured
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import redirect
from django.template.loader import render_to_string
from django.views import generic
from formtools.wizard.views import SessionWizardView


def is_ajax(request):
    """Verifica se a requisição é AJAX"""
    return request.headers.get('X-Requested-With') == 'XMLHttpRequest'


class BaseViewMixin(LoginRequiredMixin):
    """Mixin base para todas as views"""

    def is_ajax(self):
        """Verifica se a requisição atual é AJAX"""
        return is_ajax(self.request)

    def render_to_json_response(self, context, status=200):
        """Renderiza resposta JSON"""
        return JsonResponse(context, status=status)

    def render_template_to_json(self, template_name, context=None):
        """Renderiza template para JSON"""
        context = context or {}
        html = render_to_string(
            template_name,
            context=context,
            request=self.request
        )
        return self.render_to_json_response({'html': html})

    def json_success_response(self, message, **extra):
        """Retorna resposta de sucesso em JSON"""
        data = {
            'success': True,
            'message': message,
            **extra
        }
        return self.render_to_json_response(data)

    def json_error_response(self, errors, status=400):
        """Retorna resposta de erro em JSON"""
        return self.render_to_json_response(
            {'errors': errors},
            status=status
        )

    def add_message(self, message, level=messages.SUCCESS):
        """Adiciona mensagem ao sistema de mensagens"""
        messages.add_message(self.request, level, message)

    def get_ajax_context(self, form=None):
        """Contexto para respostas AJAX"""
        try:
            context = self.get_context_data() if hasattr(self, 'get_context_data') else {}
        except AttributeError:
            print("get_context_data não está implementado na view")
            context = {}

        if form:
            print("Adicionando formulário ao contexto")
            context['form'] = form

        # Verifica se é uma view de update
        if isinstance(self, generic.UpdateView):
            context['object'] = self.get_object()

        return context

    def get(self, request, *args, **kwargs):
        """Sobrescrevendo get para tratar AJAX"""
        if isinstance(self, (generic.UpdateView, generic.CreateView)):
            print("View é uma CreateView ou UpdateView, obtendo formulário")
            form = self.get_form()
            print('form', form)
        else:
            form = None
        print(f"Request: {request.method} - {request.path}")
        if self.is_ajax():
            print("Requisição AJAX detectada")
            context = self.get_ajax_context(form)
            return self.render_template_to_json(self.template_name, context)
        return super().get(request, *args, **kwargs)


class BaseListView(BaseViewMixin, generic.ListView):
    """View base para listagens"""
    paginate_by = 10
    ordering = ['id']


class BaseCreateView(BaseViewMixin, generic.CreateView):
    """View base para criação"""

    def form_valid(self, form):
        """Trata form válido"""
        response = super().form_valid(form)
        if self.is_ajax():
            return self.json_success_response('Registro criado com sucesso!')
        self.add_message('Registro criado com sucesso!')
        return response

    def form_invalid(self, form):
        """Trata form inválido"""
        if self.is_ajax():
            return self.json_error_response(form.errors)
        return super().form_invalid(form)


class BaseUpdateView(BaseViewMixin, generic.UpdateView):
    """View base para atualização"""

    def get(self, request, *args, **kwargs):
        """Sobrescrevendo get para tratar AJAX"""
        self.object = self.get_object()
        form = self.get_form()

        if self.is_ajax():
            context = self.get_ajax_context(form)
            return self.render_template_to_json(self.template_name, context)
        return super().get(request, *args, **kwargs)

    def get_ajax_context(self, form=None):
        """Contexto específico para AJAX em UpdateView"""
        context = super().get_ajax_context(form)
        context['object'] = self.object
        context['is_update'] = True
        return context

    def form_valid(self, form):
        """Trata form válido"""
        response = super().form_valid(form)
        if self.is_ajax():
            return self.json_success_response('Registro atualizado com sucesso!')
        self.add_message('Registro atualizado com sucesso!')
        return response

    def form_invalid(self, form):
        """Trata form inválido"""
        if self.is_ajax():
            return self.json_error_response(form.errors)
        return super().form_invalid(form)


class BaseDeleteView(BaseViewMixin, generic.DeleteView):
    """View base para exclusão"""

    def delete(self, request, *args, **kwargs):
        """Trata exclusão"""
        self.object = self.get_object()
        success_url = self.get_success_url()
        self.object.delete()

        if self.is_ajax():
            return self.json_success_response('Registro excluído com sucesso!')

        self.add_message('Registro excluído com sucesso!')
        return HttpResponseRedirect(success_url)


class BaseWizardView(LoginRequiredMixin, SessionWizardView):
    """Classe base para views tipo wizard"""

    file_storage = FileSystemStorage(
        location=os.path.join(settings.MEDIA_ROOT, 'temp_uploads')
    )
    success_message = None
    success_url = None

    def get_template_names(self):
        """Retorna o template da etapa atual"""
        if hasattr(self, 'templates'):
            return [self.templates[self.steps.current]]
        return super().get_template_names()

    def get_context_data(self, form, **kwargs):
        """Adiciona contexto comum para todas as etapas"""
        context = super().get_context_data(form, **kwargs)
        context.update({
            'title': self.get_step_title(),
            'subtitle': self.get_step_subtitle(),
            'step_title': self.get_step_title(),
            'step_subtitle': self.get_step_subtitle(),
        })
        return context

    def get_step_title(self):
        """Retorna o título da etapa atual"""
        if hasattr(self, 'step_titles'):
            return self.step_titles.get(self.steps.current, '')
        return ''

    def get_step_subtitle(self):
        """Retorna o subtítulo da etapa atual"""
        if hasattr(self, 'step_subtitles'):
            return self.step_subtitles.get(self.steps.current, '')
        return ''

    def done(self, form_list, **kwargs):
        """Método executado ao finalizar o wizard"""
        try:
            result = self.process_forms(form_list, **kwargs)
            if self.success_message:
                messages.success(self.request, self.success_message)
            return redirect(self.get_success_url())
        except Exception as e:
            messages.error(self.request, f'Erro ao salvar: {str(e)}')
            return redirect(self.request.path)

    def process_forms(self, form_list, **kwargs):
        """
        Método que deve ser sobrescrito para processar os formulários
        """
        raise NotImplementedError(
            "Você deve implementar process_forms em %s" % self.__class__.__name__
        )

    def get_success_url(self):
        """Retorna a URL de sucesso"""
        if self.success_url:
            return self.success_url
        raise ImproperlyConfigured(
            "No URL to redirect to. Provide a success_url."
        )


class BaseDetailView(BaseViewMixin, generic.DetailView):
    """View base para detalhes"""

    def get(self, request, *args, **kwargs):
        """Sobrescrevendo get para tratar AJAX"""
        self.object = self.get_object()
        context = self.get_context_data(object=self.object)

        if self.is_ajax():
            return self.render_template_to_json(self.template_name, context)
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        """Adiciona contexto padrão"""
        context = super().get_context_data(**kwargs)
        context.update({
            'title': self.get_title(),
            'subtitle': self.get_subtitle(),
            'object': self.object,
            'is_detail': True
        })
        return context

    def get_title(self):
        """Retorna o título da página"""
        model_name = self.model._meta.verbose_name.title()
        return f'Detalhes do {model_name}: {str(self.object)}'

    def get_subtitle(self):
        """Retorna o subtítulo da página"""
        return getattr(self, 'subtitle', '')
