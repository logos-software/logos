from django import forms

from apps.police.models import (DadosFamiliares, DadosFisicos, Escolaridade,
                                Fardamento, Funcao, GrupoFuncao, Policial)


class GrupoFuncaoForm(forms.ModelForm):
    class Meta:
        model = GrupoFuncao
        fields = ['nome']
        widgets = {
            'nome': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nome do grupo'
            })
        }


class FuncaoForm(forms.ModelForm):
    class Meta:
        model = Funcao
        fields = ['nome', 'grupo', 'tipo']
        widgets = {
            'nome': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nome da função'
            }),
            'grupo': forms.Select(attrs={
                'class': 'form-control select2'
            }),
            'tipo': forms.Select(attrs={
                'class': 'form-control'
            })
        }


class PolicialForm(forms.ModelForm):
    class Meta:
        model = Policial
        fields = [
            'matricula', 'nome', 'nome_guerra', 'cpf', 'rg',
            'data_nascimento', 'data_inclusao', 'sexo', 'tipo_sanguineo',
            'estado_civil', 'email', 'email_pessoal', 'telefone', 'celular',
            'cep', 'endereco', 'numero', 'complemento', 'bairro',
            'cidade', 'uf', 'banco', 'agencia', 'conta', 'foto'
        ]
        widgets = {
            'matricula': forms.TextInput(attrs={'class': 'form-control'}),
            'nome': forms.TextInput(attrs={'class': 'form-control'}),
            'nome_guerra': forms.TextInput(attrs={'class': 'form-control'}),
            'cpf': forms.TextInput(attrs={'class': 'form-control cpf-mask'}),
            'rg': forms.TextInput(attrs={'class': 'form-control'}),
            'data_nascimento': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'data_inclusao': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'sexo': forms.Select(attrs={'class': 'form-control'}),
            'tipo_sanguineo': forms.Select(attrs={'class': 'form-control'}),
            'estado_civil': forms.Select(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'email_pessoal': forms.EmailInput(attrs={'class': 'form-control'}),
            'telefone': forms.TextInput(attrs={'class': 'form-control phone-mask'}),
            'celular': forms.TextInput(attrs={'class': 'form-control phone-mask'}),
            'cep': forms.TextInput(attrs={'class': 'form-control cep-mask'}),
            'endereco': forms.TextInput(attrs={'class': 'form-control'}),
            'numero': forms.TextInput(attrs={'class': 'form-control'}),
            'complemento': forms.TextInput(attrs={'class': 'form-control'}),
            'bairro': forms.TextInput(attrs={'class': 'form-control'}),
            'cidade': forms.TextInput(attrs={'class': 'form-control'}),
            'uf': forms.Select(attrs={'class': 'form-control'}),
            'banco': forms.TextInput(attrs={'class': 'form-control'}),
            'agencia': forms.TextInput(attrs={'class': 'form-control'}),
            'conta': forms.TextInput(attrs={'class': 'form-control'}),
            'foto': forms.FileInput(attrs={'class': 'form-control'})
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Tornar campos opcionais em não required
        optional_fields = ['email_pessoal', 'telefone', 'complemento',
                           'banco', 'agencia', 'conta', 'foto']
        for field in optional_fields:
            self.fields[field].required = False


class PolicialDadosPessoaisForm(forms.ModelForm):
    def clean_cpf(self):
        """Limpa o CPF antes da validação"""
        cpf = self.cleaned_data.get('cpf')
        if cpf:
            # Remove todos os caracteres não numéricos
            cpf = ''.join(filter(str.isdigit, cpf))
        return cpf

    class Meta:
        model = Policial
        fields = [
            'matricula', 'nome', 'nome_guerra', 'cpf', 'rg',
            'data_nascimento', 'data_inclusao', 'sexo', 'estado_civil'
        ]
        widgets = {
            'matricula': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Digite a matrícula'
            }),
            'nome': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nome completo'
            }),
            'nome_guerra': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nome de guerra'
            }),
            'cpf': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '___.___.___-__',
                'autocomplete': 'off',
                'maxlength': '14'
            }),
            'rg': forms.TextInput(attrs={
                'class': 'form-control rg-mask',
                'placeholder': '__.___.___-_',
                'autocomplete': 'off',
                'maxlength': '12',
                'data-mask': '00.000.000-0'
            }),
            'data_nascimento': forms.DateInput(attrs={
                'class': 'form-control flatpickr-date',
                'placeholder': 'Selecione a data',
                'autocomplete': 'off'
            }),
            'data_inclusao': forms.DateInput(attrs={
                'class': 'form-control flatpickr-date',
                'placeholder': 'Selecione a data',
                'autocomplete': 'off'
            }),
            'sexo': forms.Select(attrs={
                'class': 'form-select'
            }),
            'estado_civil': forms.Select(attrs={
                'class': 'form-select'
            })
        }


class PolicialContatoForm(forms.ModelForm):
    class Meta:
        model = Policial
        fields = [
            'email', 'email_pessoal', 'telefone', 'celular',
            'cep', 'endereco', 'numero', 'complemento',
            'bairro', 'cidade', 'uf'
        ]
        widgets = {
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'email@corporativo.com'
            }),
            'email_pessoal': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'email@pessoal.com'
            }),
            'telefone': forms.TextInput(attrs={
                'class': 'form-control phone-mask',
                'placeholder': '(00) 0000-0000',
                'maxlength': '15'
            }),
            'celular': forms.TextInput(attrs={
                'class': 'form-control phone-mask',
                'placeholder': '(00) 00000-0000',
                'maxlength': '16'
            }),
            'cep': forms.TextInput(attrs={
                'class': 'form-control cep-mask',
                'placeholder': '00000-000',
                'maxlength': '9'
            }),
            'endereco': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Rua, Avenida, etc'
            }),
            'numero': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nº'
            }),
            'complemento': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Apto, Bloco, etc'
            }),
            'bairro': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Bairro'
            }),
            'cidade': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Cidade'
            }),
            'uf': forms.Select(attrs={
                'class': 'form-select'
            })
        }


class PolicialDadosFisicosForm(forms.ModelForm):
    class Meta:
        model = DadosFisicos
        exclude = ['policial', 'created_at', 'updated_at', 'active']
        widgets = {
            'altura': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Em metros (ex: 1.75)',
                'step': '0.01',
                'min': '1.00',
                'max': '2.50'
            }),
            'peso': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Em kg (ex: 75.5)',
                'step': '0.1',
                'min': '40',
                'max': '200'
            }),
            'tipo_sanguineo': forms.Select(attrs={
                'class': 'form-select'
            }),
            'cor_pele': forms.Select(attrs={
                'class': 'form-select',
                'placeholder': 'Selecione a cor da pele'
            }),
            'cor_olhos': forms.Select(attrs={
                'class': 'form-select',
                'placeholder': 'Selecione a cor dos olhos'
            }),
            'cor_cabelos': forms.Select(attrs={
                'class': 'form-select',
                'placeholder': 'Selecione a cor do cabelo'
            }),
            'tipo_cabelos': forms.Select(attrs={
                'class': 'form-select',
                'placeholder': 'Selecione o tipo do cabelo'
            })
        }

    def clean_altura(self):
        altura = self.cleaned_data.get('altura')
        if altura and (altura < 1.00 or altura > 2.50):
            raise forms.ValidationError('A altura deve estar entre 1,00m e 2,50m')
        return altura

    def clean_peso(self):
        peso = self.cleaned_data.get('peso')
        if peso and (peso < 40 or peso > 200):
            raise forms.ValidationError('O peso deve estar entre 40kg e 200kg')
        return peso


class PolicialFardamentoForm(forms.ModelForm):
    class Meta:
        model = Fardamento
        exclude = ['policial', 'created_at', 'updated_at', 'active']
        widgets = {
            'manequim': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ex: P, M, G, GG',
                'maxlength': '5'
            }),
            'calcado': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ex: 40',
                'maxlength': '2'
            })
        }

    def clean_manequim(self):
        manequim = self.cleaned_data.get('manequim')
        if manequim:
            return manequim.upper()
        return manequim


class PolicialDadosBancariosForm(forms.ModelForm):
    class Meta:
        model = Policial
        fields = ['banco', 'agencia', 'conta']
        widgets = {
            'banco': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Código do banco',
                'maxlength': '3'
            }),
            'agencia': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Número da agência',
                'maxlength': '10'
            }),
            'conta': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Número da conta',
                'maxlength': '20'
            })
        }


class PolicialFamiliaresForm(forms.ModelForm):
    class Meta:
        model = DadosFamiliares
        exclude = ['policial', 'created_at', 'updated_at', 'active']
        widgets = {
            'nome': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nome completo'
            }),
            'grau_parentesco': forms.Select(attrs={
                'class': 'form-select'
            }),
            'data_nascimento': forms.DateInput(attrs={
                'class': 'form-control flatpickr-date',
                'placeholder': 'Selecione a data'
            }),
            'cpf': forms.TextInput(attrs={
                'class': 'form-control cpf-mask',
                'placeholder': '___.___.___-__'
            }),
            'rg': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Número do RG'
            }),
            'dependente': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
            'contato': forms.TextInput(attrs={
                'class': 'form-control phone-mask',
                'placeholder': '(00) 00000-0000'
            }),
            'observacao': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Observações adicionais'
            })
        }


class PolicialEscolaridadeForm(forms.ModelForm):
    class Meta:
        model = Escolaridade
        exclude = ['policial', 'created_at', 'updated_at', 'active']
        widgets = {
            'nivel': forms.Select(attrs={
                'class': 'form-select'
            }),
            'curso': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nome do curso'
            }),
            'instituicao': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nome da instituição'
            }),
            'ano_conclusao': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ano de conclusão',
                'min': '1950',
                'max': '2050'
            }),
            'data_colacao': forms.DateInput(attrs={
                'class': 'form-control flatpickr-date',
                'placeholder': 'Data da colação'
            }),
            'registro': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Número do registro/diploma'
            }),
            'arquivo_diploma': forms.FileInput(attrs={
                'class': 'form-control'
            }),
            'observacao': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Observações adicionais'
            })
        }
