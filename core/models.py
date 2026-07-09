from django.db import models

# Create your models here.

class Autor(models.Model):
    nome = models.CharField(max_length=150, verbose_name="Nome do Autor")
    biografia = models.TextField(blank=True, null=True, verbose_name="Biografia")

    def __str__(self):
        return self.nome

    class Meta:
        verbose_name = "Autor"
        verbose_name_plural = "Autores"


class Genero(models.Model):
    nome = models.CharField(max_length=100, unique=True, verbose_name="Gênero")

    def __str__(self):
        return self.nome

    class Meta:
        verbose_name = "Gênero"
        verbose_name_plural = "Gêneros"

class Trope(models.Model):
    nome = models.CharField(max_length=100, unique=True, verbose_name="Nome do Trope")

    def __str__(self):
        return self.nome

    class Meta:
        verbose_name = "Trope"
        verbose_name_plural = "Tropes"


class Livro(models.Model):
    titulo = models.CharField(max_length=200, verbose_name="Título")
    serie = models.CharField(max_length=200, blank=True, null=True, verbose_name="Série/Saga")
    volume = models.IntegerField(blank=True, null=True, verbose_name="Volume/Número")
    sinopse = models.TextField(verbose_name="Sinopse/Resenha")
    num_paginas = models.IntegerField(blank=True, null=True, verbose_name="Número de Páginas")
    
    # NOVO CAMPO: Opções de status da série
    STATUS_SERIE_CHOICES = [
        ('andamento', 'Em Andamento'),
        ('completa', 'Completa'),
    ]
    status_serie = models.CharField(
        max_length=20, 
        choices=STATUS_SERIE_CHOICES, 
        blank=True, 
        null=True, 
        verbose_name="Status da Série"
    )

    # Sistema de Avaliação (Nota de 1 a 5)
    avaliacao = models.IntegerField(
        choices=[(i, str(i)) for i in range(1, 6)], 
        default=5,
        verbose_name="Avaliação"
    )
    
    capa = models.ImageField(upload_to='capas_livros/', verbose_name="Capa do Livro")
    criado_at = models.DateTimeField(auto_now_add=True, verbose_name="Cadastrado em")

    # ================= RELACIONAMENTOS =================
    # ForeignKey: Se o autor for deletado, os livros dele continuam (SET_NULL) e o campo fica vazio
    autor = models.ForeignKey(Autor, on_delete=models.SET_NULL, null=True, related_name="livros", verbose_name="Autor")
    
    # ManyToManyField: Cria a tabela intermediária automaticamente entre Livro e Genero
    generos = models.ManyToManyField(Genero, related_name="livros", verbose_name="Gêneros")

    tropes = models.ManyToManyField(Trope, related_name="livros", verbose_name="Tropes")

    def __str__(self):
        return self.titulo

    class Meta:
        verbose_name = "Livro"
        verbose_name_plural = "Livros"
        ordering = ['serie', 'volume']
        