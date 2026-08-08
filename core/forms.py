from django import forms
from .models import Livro, Genero, Trope, AlertaGatilho, ReadingEntry


# =================================================================
# FORMULÁRIO DE CADASTRO DE LIVRO (feito pela usuária, sem admin)
# =================================================================
class LivroForm(forms.ModelForm):
    # Em vez de escolher um Autor já cadastrado numa lista, a usuária
    # digita o nome. Se o autor já existir no banco, reaproveitamos;
    # se não existir, criamos um novo (get_or_create na view).
    autor_nome = forms.CharField(
        label="Autor",
        max_length=150,
        help_text="Se o autor já estiver cadastrado, vamos usar o existente."
    )

    class Meta:
        model = Livro
        fields = [
            'titulo', 'serie', 'volume', 'sinopse', 'num_paginas', 'isbn',
            'status_serie', 'capa', 'generos', 'tropes', 'alertas_gatilho',
        ]
        widgets = {
            'generos': forms.CheckboxSelectMultiple(),
            'tropes': forms.CheckboxSelectMultiple(),
            'alertas_gatilho': forms.CheckboxSelectMultiple(),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Campos de texto/arquivo/select simples ganham a classe padrão do site
        for name, field in self.fields.items():
            if name in ('generos', 'tropes', 'alertas_gatilho'):
                field.widget.attrs['class'] = 'settings-checkbox-group'
            elif name == 'capa':
                field.widget.attrs['class'] = 'settings-file'
            elif name == 'sinopse':
                field.widget.attrs['class'] = 'settings-textarea'
            else:
                field.widget.attrs['class'] = 'settings-input'


# =================================================================
# FORMULÁRIO DE RESENHA (marcar como lido + avaliar + comentar)
# =================================================================
class ReadingEntryForm(forms.ModelForm):
    class Meta:
        model = ReadingEntry
        fields = ['avaliacao', 'resenha', 'data_inicio', 'data_fim']
        widgets = {
            'data_inicio': forms.DateInput(attrs={'type': 'date'}),
            'data_fim': forms.DateInput(attrs={'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            if name == 'resenha':
                field.widget.attrs['class'] = 'settings-textarea'
            else:
                field.widget.attrs['class'] = 'settings-input'
