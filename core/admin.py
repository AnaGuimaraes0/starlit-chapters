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

@admin.register(AlertaGatilho)
class AlertaGatilhoAdmin(admin.ModelAdmin):
    list_display = ('nome',)
    search_fields = ('nome',)


# =================================================================
# 2. MODELO DE LIVRO (Atualizado para Moderação Avançada)
# =================================================================
@admin.register(Livro)
class LivroAdmin(admin.ModelAdmin):
    # 1. Adicionamos 'aprovado' e 'criado_por' para você ver quem enviou e se está liberado
    list_display = ('titulo', 'autor', 'serie', 'status_serie', 'aprovado', 'criado_por', 'criado_at')
    
    # 2. TRUQUE DE PRODUTIVIDADE: Permite marcar a caixinha de 'aprovado' direto na lista, sem precisar abrir o cadastro do livro!
    list_editable = ('aprovado',)
    
    # 3. Adicionamos 'aprovado' nos filtros para você achar rapidamente os livros pendentes
    list_filter = ('aprovado', 'status_serie', 'generos', 'tropes', 'autor')
    
    # A sua barra de pesquisa e filtros horizontais continuam intactos
    search_fields = ('titulo', 'autor__nome')
    filter_horizontal = ('generos', 'tropes', 'alertas_gatilho')


# =================================================================
# 3. MODELO DE DIÁRIO 
# =================================================================
@admin.register(ReadingEntry)
class ReadingEntryAdmin(admin.ModelAdmin):
    list_display = ('user', 'livro', 'status', 'avaliacao', 'data_inicio', 'data_fim')
    list_filter = ('status', 'avaliacao')
    search_fields = ('user__username', 'livro__titulo')