from django.contrib import admin
# Importamos todos os modelos antigos e os três novos
from .models import Autor, Genero, Livro, Trope, AlertaGatilho, ReadingEntry
from usuarios.models import Profile

# =================================================================
# 1. MODELOS DE CATEGORIZAÇÃO (Mantidos como os seus originais)
# =================================================================
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

# Seguindo o seu padrão para o novo Alerta de Gatilho
@admin.register(AlertaGatilho)
class AlertaGatilhoAdmin(admin.ModelAdmin):
    list_display = ('nome',)
    search_fields = ('nome',)


# =================================================================
# 2. MODELO DE LIVRO (Atualizado com seus novos campos)
# =================================================================
@admin.register(Livro)
class LivroAdmin(admin.ModelAdmin):
    # Mantivemos as suas colunas e adicionamos o status_serie
    list_display = ('titulo', 'autor', 'serie', 'status_serie', 'num_paginas', 'criado_at')
    
    # Mantivemos seus filtros e adicionamos o status_serie
    list_filter = ('status_serie', 'generos', 'tropes', 'autor')
    
    # Sua barra de pesquisa maravilhosa continua igual
    search_fields = ('titulo', 'autor__nome')
    
    # Adicionamos os alertas_gatilho na caixa de busca dupla!
    filter_horizontal = ('generos', 'tropes', 'alertas_gatilho')


# =================================================================
# 3. MODELO DE DIÁRIO (Novo)
# =================================================================
@admin.register(ReadingEntry)
class ReadingEntryAdmin(admin.ModelAdmin):
    # Exibe quem leu, qual livro, o status, a nota e as datas
    list_display = ('user', 'livro', 'status', 'avaliacao', 'data_inicio', 'data_fim')
    list_filter = ('status', 'avaliacao')
    # Permite buscar pelo nome do usuário ou título do livro
    search_fields = ('user__username', 'livro__titulo')