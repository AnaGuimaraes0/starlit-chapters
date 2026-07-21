from django.db.models import Case, When, Value, IntegerField, F
from django.shortcuts import get_object_or_404, render
from django.contrib.auth.decorators import login_required
from .models import Livro

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