from django.db.models import Case, When, Value, IntegerField, F, Q
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from .models import Livro, Autor, ReadingEntry
from .forms import LivroForm, ReadingEntryForm

# =================================================================
# PÁGINA INICIAL (DASHBOARD)
# =================================================================
# Se a pessoa não estiver logada, ela é chutada de volta para a URL 'login'
@login_required(login_url='login')
def home(request):
    # Por enquanto, vamos apenas renderizar o HTML.
    # No futuro, vamos puxar os livros do banco de dados aqui!
    return render(request, 'core/home.html')


def biblioteca(request):
    recomendados = Livro.objects.filter(diarios__avaliacao__gte=4).distinct().order_by('-criado_at')[:4]
    nao_recomendados = Livro.objects.filter(diarios__avaliacao__lte=3).distinct().order_by('-criado_at')[:4]

    contexto = {
        'livros_recomendados': recomendados,
        'livros_nao_recomendados': nao_recomendados,
    }

    return render(request, 'core/biblioteca.html', contexto)


def recomendacoes_view(request):
    livros_base = Livro.objects.filter(diarios__avaliacao__gte=4).distinct()

    livros_recomendados = livros_base.annotate(
        is_standalone=Case(
            When(serie__exact='', then=Value(1)),
            When(serie__isnull=True, then=Value(1)),
            default=Value(0),
            output_field=IntegerField(),
        )
    ).order_by(
        'is_standalone',
        'serie',
        F('volume').asc(nulls_last=True),
        'titulo',
    )

    context = {
        'livros': livros_recomendados,
        'titulo_pagina': 'Livros Recomendados',
    }
    return render(request, 'core/recomendacoes.html', context)


def nao_recomendados_view(request):
    livros_base = Livro.objects.filter(diarios__avaliacao__lte=3).distinct()

    livros_nao_recomendados = livros_base.annotate(
        is_standalone=Case(
            When(serie__exact='', then=Value(1)),
            When(serie__isnull=True, then=Value(1)),
            default=Value(0),
            output_field=IntegerField(),
        )
    ).order_by(
        'is_standalone',
        'serie',
        F('volume').asc(nulls_last=True),
        'titulo',
    )

    context = {
        'livros': livros_nao_recomendados,
        'titulo_pagina': 'Livros Não Recomendados',
    }
    return render(request, 'core/nao_recomendados.html', context)


def fichario_leitura_view(request, livro_id=None):
    if livro_id is not None:
        livro = get_object_or_404(Livro, id=livro_id)
    else:
        livro = Livro.objects.first()

    context = {
        'livro': livro,
    }
    return render(request, 'core/ficha-leitura.html', context)


# =================================================================
# BUSCAR LIVRO (para escrever resenha ou continuar cadastro)
# =================================================================
@login_required(login_url='login')
def buscar_livro_view(request):
    q = request.GET.get('q', '').strip()

    # A usuária só pode ver livros já aprovados pela moderação OU
    # livros que ela mesma cadastrou (mesmo que ainda não aprovados),
    # senão ela cadastraria um livro e não conseguiria nem resenhar o próprio livro.
    livros = Livro.objects.filter(
        Q(aprovado=True) | Q(criado_por=request.user)
    ).distinct()

    if q:
        livros = livros.filter(
            Q(titulo__icontains=q) | Q(autor__nome__icontains=q)
        ).distinct()

    context = {
        'livros': livros.order_by('titulo') if q else livros.none(),
        'q': q,
        'buscou': bool(q),
    }
    return render(request, 'core/buscar_livro.html', context)


# =================================================================
# CADASTRAR LIVRO (feito pela usuária, entra como pendente de aprovação)
# =================================================================
@login_required(login_url='login')
def cadastrar_livro_view(request):
    if request.method == 'POST':
        form = LivroForm(request.POST, request.FILES)
        if form.is_valid():
            livro = form.save(commit=False)

            # Reaproveita o autor se ele já existir, ou cria um novo
            nome_autor = form.cleaned_data['autor_nome'].strip()
            autor, _ = Autor.objects.get_or_create(
                nome__iexact=nome_autor,
                defaults={'nome': nome_autor}
            )
            livro.autor = autor

            livro.criado_por = request.user
            livro.aprovado = False
            livro.save()
            form.save_m2m()  # salva gêneros, tropes e alertas de gatilho

            messages.success(
                request,
                f'"{livro.titulo}" foi cadastrado! Ele ficará pendente de aprovação, '
                'mas você já pode escrever sua resenha.'
            )
            return redirect('escrever_resenha', livro_id=livro.id)
    else:
        form = LivroForm()

    return render(request, 'core/cadastrar_livro.html', {'form': form})


# =================================================================
# ESCREVER RESENHA (cria/atualiza o ReadingEntry e marca como "lido")
# =================================================================
@login_required(login_url='login')
def escrever_resenha_view(request, livro_id):
    livro = get_object_or_404(Livro, id=livro_id)

    # Impede acesso a livros de outra usuária que ainda não foram aprovados
    if not livro.aprovado and livro.criado_por != request.user:
        messages.error(request, "Esse livro ainda não foi aprovado pela moderação.")
        return redirect('buscar_livro')

    entrada, _ = ReadingEntry.objects.get_or_create(user=request.user, livro=livro)

    if request.method == 'POST':
        form = ReadingEntryForm(request.POST, instance=entrada)
        if form.is_valid():
            entrada = form.save(commit=False)
            entrada.status = 'lido'
            if not entrada.data_fim:
                entrada.data_fim = timezone.now().date()
            entrada.save()
            messages.success(request, f'Resenha de "{livro.titulo}" salva com sucesso!')
            return redirect('perfil_usuario', username=request.user.username)
    else:
        form = ReadingEntryForm(instance=entrada)

    return render(request, 'core/escrever_resenha.html', {'form': form, 'livro': livro})