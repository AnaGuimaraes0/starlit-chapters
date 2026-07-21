from django.urls import path
from . import views

urlpatterns = [
    # Quando o endereço for vazio '', chama a função 'home' da views.py
    path('', views.home, name='home'),
    path('biblioteca/', views.biblioteca, name='biblioteca'),
    # Rotas para as páginas de recomendações
    path('recomendacoes/', views.recomendacoes_view, name='recomendacoes'),
    path('nao-recomendados/', views.nao_recomendados_view, name='nao_recomendados'),
    
    # Rota principal para o Fichário de Leitura, com ou sem id do livro
    path('lendo-agora/', views.fichario_leitura_view, name='ficha-leitura-sem-id'),
    path('lendo-agora/<int:livro_id>/', views.fichario_leitura_view, name='ficha-leitura'),
]