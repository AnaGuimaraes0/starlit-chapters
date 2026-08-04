from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import RegistroUsuarioForm, LoginUsuarioForm,  UserUpdateForm, PerfilUpdateForm

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

def perfil_usuario(request, username):
    # Busca a usuária pelo username na URL; se não existir, retorna erro 404
    usuario_perfil = get_object_or_404(User, username=username)
    
    contexto = {
        'usuario_perfil': usuario_perfil,
        'perfil': usuario_perfil.perfil,
    }
    return render(request, 'usuarios/perfil.html', contexto)


# =================================================================
# 2. CONFIGURAÇÕES / PERFIL (Privado)
# =================================================================
@login_required(login_url='login')
def configuracoes(request):
    if request.method == 'POST':
        # Instanciamos os dois formulários com os dados enviados no POST
        u_form = UserUpdateForm(request.POST, instance=request.user)
        # request.FILES é OBRIGATÓRIO quando enviamos arquivos (como imagens de avatar)
        p_form = PerfilUpdateForm(request.POST, request.FILES, instance=request.user.perfil)

        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, "Seu perfil foi atualizado com sucesso!")
            return redirect('configuracoes')
    else:
        # Carrega os formulários preenchidos com os dados atuais do usuário
        u_form = UserUpdateForm(instance=request.user)
        p_form = PerfilUpdateForm(instance=request.user.perfil)

    contexto = {
        'u_form': u_form,
        'p_form': p_form,
    }
    return render(request, 'usuarios/configuracoes.html', contexto)