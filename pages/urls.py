from django.urls import path
from . import views

urlpatterns = [
    # O caminho vazio aqui indica a raiz da vitrine
    path('', views.landing_page, name='landing_page'),
    path('recursos/', views.recursos, name='recursos'),
    path('avaliacoes/', views.avaliacoes, name='avaliacoes'),
    path('clubes/', views.clubes, name='clubes'),
    path('sobre/', views.sobre, name='sobre'),
]