from django.urls import path
from .views import cadastro, login_usuario, logout_usuario

urlpatterns = [
    # As rotas apontam diretamente para as suas funções customizadas
    path('cadastro/', cadastro, name='cadastro'),
    path('login/', login_usuario, name='login'),
    path('logout/', logout_usuario, name='logout'),
]