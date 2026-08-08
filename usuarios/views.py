from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import RegistroUsuarioForm, LoginUsuarioForm,  UserUpdateForm, PerfilUpdateForm
from core.models import ReadingEntry

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
            login(request, user)
            messages.success(request, f"Bem-vinda ao Starlit Chapters, {user.username}!")
            return redirect('perfil_usuario', username=user.username)
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

                next_url = request.GET.get('next')
                if next_url:
                    return redirect(next_url)
                
                # 2. Se fez login direto, vai para o seu Perfil!
                return redirect('perfil_usuario', username=usuario.username)
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

# =================================================================
# VIEW DE PERFIL DE USUÁRIO
# =================================================================
def perfil_usuario(request, username):
    # Busca a usuária pelo username na URL; se não existir, retorna erro 404
    usuario_perfil = get_object_or_404(User, username=username)

    diarios_lidos = ReadingEntry.objects.filter(user=usuario_perfil, status='lido')

    # Livro que a usuária está lendo agora (entrada mais recente com status "lendo")
    entrada_lendo = ReadingEntry.objects.filter(
        user=usuario_perfil, status='lendo'
    ).order_by('-atualizado_em').first()

    contexto = {
        # --- DADOS DE USUÁRIO E PERFIL ---
        'usuario_perfil': usuario_perfil,
        'perfil': usuario_perfil.perfil,
        
        # --- CONTADORES ---
        'livros_lidos_count': diarios_lidos.count(),
        'resenhas_count': diarios_lidos.exclude(resenha__isnull=True).exclude(resenha__exact='').count(),
        'listas_count': None,   # app de Listas ainda não existe
        'clubes_count': None,   # app de Clubes ainda não existe
        
        # --- LEITURA ATUAL (None aciona o "Estado Vazio" visual) ---
        'leitura_atual': entrada_lendo.livro if entrada_lendo else None,
        
        # --- ESTATÍSTICAS DETALHADAS ---
        'tempo_leitura_horas': None,
        'paginas_lidas_count': None,
        'media_paginas': None,
        'genero_favorito': None,
        'genero_favorito_count': None,
        
        # --- LISTAS (Inicializadas como listas vazias "[]") ---
        'atividades': [],
        'conquistas': [],
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