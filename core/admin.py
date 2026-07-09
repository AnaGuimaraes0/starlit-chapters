from django.contrib import admin
from .models import Autor, Genero, Livro, Trope

# Register your models here.

@admin.register(Autor)
class AutorAdmin(admin.ModelAdmin):
    list_display = ('nome',)
    search_fields = ('nome',)

@admin.register(Genero)
class GeneroAdmin(admin.ModelAdmin):
    list_display = ('nome',)
    search_fields = ('nome',)

@admin.register(Trope)
class TropeAdmin(admin.ModelAdmin):
    list_display = ('nome',)
    search_fields = ('nome',)

@admin.register(Livro)
class LivroAdmin(admin.ModelAdmin):
    # Exibe colunas organizadas no painel
    list_display = ('titulo', 'autor', 'serie', 'num_paginas', 'avaliacao', 'criado_at')
    # Adiciona filtros na lateral direita do painel
    list_filter = ('generos', 'tropes', 'avaliacao', 'autor')
    # Adiciona uma barra de pesquisa para buscar por título ou autor
    search_fields = ('titulo', 'autor__nome')
    # Facilita a seleção de muitos-para-muitos com uma caixa de busca dupla
    filter_horizontal = ('generos', 'tropes')