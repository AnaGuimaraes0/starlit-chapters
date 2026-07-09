from django.shortcuts import get_object_or_404, render

from .models import Livro


def index(request):
    return render(request, 'core/index.html')


def biblioteca(request):
    recomendados = Livro.objects.filter(avaliacao__gte=4).order_by('-criado_at')[:4]
    nao_recomendados = Livro.objects.filter(avaliacao__lte=3).order_by('-criado_at')[:4]

    contexto = {
        'livros_recomendados': recomendados,
        'livros_nao_recomendados': nao_recomendados,
    }

    return render(request, 'core/biblioteca.html', contexto)


def recomendacoes_view(request):
    livros_recomendados = Livro.objects.filter(avaliacao__gte=4).order_by('-criado_at')

    context = {
        'livros': livros_recomendados,
        'titulo_pagina': 'Livros Recomendados',
    }
    return render(request, 'core/recomendacoes.html', context)


def nao_recomendados_view(request):
    livros_nao_recomendados = Livro.objects.filter(avaliacao__lte=3).order_by('-criado_at')

    context = {
        'livros': livros_nao_recomendados,
        'titulo_pagina': 'Livros Não Recomendados',
    }
    return render(request, 'core/nao_recomendados.html', context)


def fichario_leitura_view(request, livro_id):
    livro = get_object_or_404(Livro, id=livro_id)

    context = {
        'livro': livro,
    }
    return render(request, 'core/ficha-leitura.html', context)