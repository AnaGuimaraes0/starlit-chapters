from django.urls import path
from .views import cadastro, login_usuario, logout_usuario, perfil_usuario, configuracoes

urlpatterns = [
    # As rotas apontam diretamente para as suas funções customizadas
    path('cadastro/', cadastro, name='cadastro'),
    path('login/', login_usuario, name='login'),
    path('logout/', logout_usuario, name='logout'),
    path('configuracoes/', configuracoes, name='configuracoes'),
    path('usuario/<str:username>/', perfil_usuario, name='perfil_usuario'),
]