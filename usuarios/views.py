from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages

# Importamos os formulários que criamos
from .forms import RegistroUsuarioForm, LoginUsuarioForm

# =================================================================
# VIEW DE CADASTRO
# =================================================================
def cadastro(request):
    # Trava: Se já estiver logado, não tem por que acessar o cadastro
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        form = RegistroUsuarioForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Loga o usuário recém-criado imediatamente
            login(request, user)
            messages.success(request, f"Bem-vinda ao Starlit Chapters, {user.username}!")
            return redirect('home')
    else:
        form = RegistroUsuarioForm()
        
    return render(request, 'usuarios/cadastro.html', {'form': form})


# =================================================================
# VIEW DE LOGIN (Método da Aula)
# =================================================================
def login_usuario(request):
    # Trava de segurança inicial para quem já está logado
    if request.user.is_authenticated:
        return redirect('home')
    
    if request.method == 'POST':
        # O formulário de login do Django exige o 'request' como primeiro argumento
        form = LoginUsuarioForm(request, data=request.POST)
        
        if form.is_valid():
            # Extração manual dos dados limpos
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            
            # Verificação no Banco de Dados
            usuario = authenticate(username=username, password=password)

            if usuario is not None:
                # Cria a sessão (cookie) do usuário
                login(request, usuario)

                # Redirecionamento inteligente: verifica se existe um parâmetro 'next' na URL
                redirect_to = request.GET.get('next', 'home')
                return redirect(redirect_to)
    else:
        form = LoginUsuarioForm()
    
    return render(request, 'usuarios/login.html', {'form': form})


# =================================================================
# VIEW DE LOGOUT (Método da Aula)
# =================================================================
def logout_usuario(request):
    logout(request)
    # Redireciona para a tela de login após sair
    return redirect('login')