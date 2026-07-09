from django.urls import path
from . import views

urlpatterns = [
    # Quando o endereço for vazio '', chama a função 'index' da views.py
    path('', views.index, name='index'),
    path('biblioteca/', views.biblioteca, name='biblioteca'),
    # Rotas para as páginas de recomendações
    path('recomendacoes/', views.recomendacoes_view, name='recomendacoes'),
    path('nao-recomendados/', views.nao_recomendados_view, name='nao_recomendados'),
    
    # Rota dinâmica para o Fichário de Leitura
    # O "<int:livro_id>" permite que a URL receba o ID do livro, assim sabemos qual fichário abrir.
    path('lendo-agora/', views.fichario_leitura_view, name='ficha-leitura'),
]