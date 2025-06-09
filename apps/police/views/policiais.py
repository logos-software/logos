from django.db import transaction
from django.urls import reverse_lazy

from apps.police.forms import (PolicialContatoForm, PolicialDadosBancariosForm,
                               PolicialDadosFisicosForm,
                               PolicialDadosPessoaisForm,
                               PolicialEscolaridadeForm,
                               PolicialFamiliaresForm, PolicialFardamentoForm,
                               PolicialForm)
from apps.police.models import (DadosFamiliares, DadosFisicos, Escolaridade,
                                Fardamento, Policial)
from apps.utils.views import (BaseDeleteView, BaseDetailView, BaseListView,
                              BaseUpdateView, BaseWizardView)


class PolicialListView(BaseListView):
    model = Policial
    template_name = 'police/policiais/policial_list.html'
    context_object_name = 'policiais'
    ordering = ['nome']
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Policiais'
        return context


class PolicialUpdateView(BaseUpdateView):
    model = Policial
    form_class = PolicialForm
    template_name = 'police/policiais/includes/_policial_form.html'
    success_url = reverse_lazy('police:policial-list')
    success_message = 'Policial atualizado com sucesso!'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'title': f'Editar Policial: {self.object.nome}',
            'object': self.object,
        })
        return context


class PolicialDeleteView(BaseDeleteView):
    model = Policial
    success_url = reverse_lazy('police:policial-list')
    success_message = 'Policial excluído com sucesso!'


class PolicialWizardView(BaseWizardView):
    """View wizard para cadastro de policiais"""

    form_list = [
        ('dados_pessoais', PolicialDadosPessoaisForm),
        ('contato', PolicialContatoForm),
        ('dados_fisicos', PolicialDadosFisicosForm),
        ('fardamento', PolicialFardamentoForm),
        ('dados_bancarios', PolicialDadosBancariosForm),
        ('familiares', PolicialFamiliaresForm),
        ('escolaridade', PolicialEscolaridadeForm),
    ]

    templates = {
        'dados_pessoais': 'police/policiais/wizard/dados_pessoais.html',
        'contato': 'police/policiais/wizard/contato.html',
        'dados_fisicos': 'police/policiais/wizard/dados_fisicos.html',
        'fardamento': 'police/policiais/wizard/fardamento.html',
        'dados_bancarios': 'police/policiais/wizard/dados_bancarios.html',
        'familiares': 'police/policiais/wizard/familiares.html',
        'escolaridade': 'police/policiais/wizard/escolaridade.html',
    }

    step_titles = {
        'dados_pessoais': 'Dados Pessoais',
        'contato': 'Informações de Contato',
        'dados_fisicos': 'Dados Físicos',
        'fardamento': 'Fardamento',
        'dados_bancarios': 'Dados Bancários',
        'familiares': 'Familiares',
        'escolaridade': 'Escolaridade',
    }

    step_subtitles = {
        'dados_pessoais': 'Informações básicas do policial',
        'contato': 'Endereço e formas de contato',
        'dados_fisicos': 'Características físicas',
        'fardamento': 'Medidas para fardamento',
        'dados_bancarios': 'Informações bancárias',
        'familiares': 'Informações dos familiares',
        'escolaridade': 'Formação acadêmica',
    }

    step_icons = {
        'dados_pessoais': 'demo-pli-male',
        'contato': 'demo-pli-mail',
        'dados_fisicos': 'demo-pli-weight',
        'fardamento': 'demo-pli-shirt',
        'dados_bancarios': 'demo-pli-credit-card',
        'familiares': 'demo-pli-family',
        'escolaridade': 'demo-pli-graduation-cap',
    }

    success_url = reverse_lazy('police:policial-list')
    success_message = 'Policial cadastrado com sucesso!'

    def get_context_data(self, form, **kwargs):
        context = super().get_context_data(form, **kwargs)
        context.update({
            'title': self.step_titles.get(self.steps.current, ''),
            'subtitle': self.step_subtitles.get(self.steps.current, ''),
            'step_icon': self.step_icons.get(self.steps.current, ''),
            'prev_title': self.step_titles.get(self.get_prev_step(), ''),
            'next_title': self.step_titles.get(self.get_next_step(), ''),
        })
        return context

    def get_prev_step(self):
        """Retorna o nome da etapa anterior"""
        idx = list(self.form_list.keys()).index(self.steps.current)
        if idx > 0:
            return list(self.form_list.keys())[idx - 1]
        return None

    def get_next_step(self):
        """Retorna o nome da próxima etapa"""
        idx = list(self.form_list.keys()).index(self.steps.current)
        if idx < len(self.form_list) - 1:
            return list(self.form_list.keys())[idx + 1]
        return None

    def get_form(self, step=None, data=None, files=None):
        """Personaliza o formulário antes de renderizar"""
        form = super().get_form(step, data, files)

        current_step = step or self.steps.current

        if current_step == 'dados_pessoais' and data:
            data = data.copy()

            # Corrige o campo CPF que está vindo com nome errado
            if 'cpf' in data and f'{current_step}-cpf' not in data:
                data[f'{current_step}-cpf'] = data['cpf']
                del data['cpf']

            # Processa CPF
            cpf_key = f'{current_step}-cpf'
            if cpf_key in data:
                cpf = data[cpf_key]
                data[cpf_key] = ''.join(filter(str.isdigit, cpf))

        return form

    def process_forms(self, form_list, **kwargs):
        """Processa os formulários do wizard"""
        try:
            with transaction.atomic():
                form_dict = {
                    'dados_pessoais': form_list[0].cleaned_data,
                    'contato': form_list[1].cleaned_data,
                    'dados_fisicos': form_list[2].cleaned_data,
                    'fardamento': form_list[3].cleaned_data,
                    'dados_bancarios': form_list[4].cleaned_data,
                    'familiares': form_list[5].cleaned_data,
                    'escolaridade': form_list[6].cleaned_data,
                }

                # Remove máscaras dos documentos
                if 'cpf' in form_dict['dados_pessoais']:
                    form_dict['dados_pessoais']['cpf'] = ''.join(
                        filter(str.isdigit, form_dict['dados_pessoais']['cpf']))

                # Cria o policial com dados pessoais, contato e dados bancários
                policial_data = {
                    **form_dict['dados_pessoais'],
                    **form_dict['contato'],
                    **form_dict['dados_bancarios']
                }
                policial = Policial.objects.create(**policial_data)

                # Cria os dados relacionados
                DadosFisicos.objects.create(
                    policial=policial, **form_dict['dados_fisicos'])
                Fardamento.objects.create(
                    policial=policial, **form_dict['fardamento'])
                DadosFamiliares.objects.create(
                    policial=policial, **form_dict['familiares'])
                Escolaridade.objects.create(
                    policial=policial, **form_dict['escolaridade'])

                return policial

        except Exception as e:
            transaction.set_rollback(True)
            raise e


class PolicialDetailView(BaseDetailView):
    model = Policial
    template_name = 'police/policiais/includes/_policial_detail.html'
    context_object_name = 'policial'
    subtitle = 'Informações completas do policial'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = f'Detalhes do Policial: {self.object.nome}'
        return context
