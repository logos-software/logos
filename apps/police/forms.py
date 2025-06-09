from django import forms
from .models import GrupoFuncao, Funcao


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
