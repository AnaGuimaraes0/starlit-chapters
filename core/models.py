from django.db import models
from django.contrib.auth.models import User

# =================================================================
# 2. MODELOS DE CATEGORIZAÇÃO UNIVERSAL
# =================================================================
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

# NOVO MODELO: Alerta de Gatilho
class AlertaGatilho(models.Model):
    nome = models.CharField(max_length=100, unique=True, verbose_name="Alerta de Gatilho")
    descricao = models.TextField(blank=True, null=True, verbose_name="Descrição (Opcional)")

    def __str__(self):
        return self.nome

    class Meta:
        verbose_name = "Alerta de Gatilho"
        verbose_name_plural = "Alertas de Gatilho"


# =================================================================
# 3. O LIVRO (Catálogo Colaborativo)
# =================================================================
class Livro(models.Model):
    titulo = models.CharField(max_length=200, verbose_name="Título")
    serie = models.CharField(max_length=200, blank=True, null=True, verbose_name="Série/Saga")
    volume = models.IntegerField(blank=True, null=True, verbose_name="Volume/Número")
    
    sinopse = models.TextField(verbose_name="Sinopse Oficial")
    num_paginas = models.IntegerField(blank=True, null=True, verbose_name="Número de Páginas")
    isbn = models.CharField(max_length=13, unique=True, blank=True, null=True, verbose_name="ISBN")
    
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

    capa = models.ImageField(upload_to='capas_livros/', verbose_name="Capa do Livro")
    criado_at = models.DateTimeField(auto_now_add=True, verbose_name="Cadastrado em")

    # ==========================================
    # Estratégia de Moderação
    # ==========================================
    criado_por = models.ForeignKey(
        User, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        related_name="livros_cadastrados",
        verbose_name="Cadastrado por"
    )
    aprovado = models.BooleanField(
        default=False, 
        verbose_name="Aprovado pela Moderação",
        help_text="Se marcado, o livro aparecerá na busca global para todos os usuários."
    )

    # RELACIONAMENTOS
    autor = models.ForeignKey(Autor, on_delete=models.SET_NULL, null=True, related_name="livros", verbose_name="Autor")
    generos = models.ManyToManyField(Genero, related_name="livros", blank=True, verbose_name="Gêneros")
    tropes = models.ManyToManyField(Trope, related_name="livros", blank=True, verbose_name="Tropes")
    alertas_gatilho = models.ManyToManyField(AlertaGatilho, related_name="livros", blank=True, verbose_name="Alertas de Gatilho")

    def __str__(self):
        return self.titulo

    class Meta:
        verbose_name = "Livro"
        verbose_name_plural = "Livros"
        ordering = ['serie', 'volume']


# =================================================================
# 4. DIÁRIO DE LEITURA (A interação do usuário)
# =================================================================
class ReadingEntry(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='diarios')
    livro = models.ForeignKey(Livro, on_delete=models.CASCADE, related_name='diarios')
    
    STATUS_CHOICES = [
        ('lendo', 'Lendo'),
        ('lido', 'Lido'),
        ('quero_ler', 'Quero Ler'),
        ('abandonado', 'Abandonado'),
    ]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='quero_ler', verbose_name="Status de Leitura")
    
    # A sua avaliação e resenha vieram para cá!
    avaliacao = models.IntegerField(
        choices=[(i, str(i)) for i in range(1, 6)], 
        blank=True, 
        null=True,
        verbose_name="Avaliação"
    )
    resenha = models.TextField(blank=True, null=True, verbose_name="Resenha / Opinião Pessoal")
    
    data_inicio = models.DateField(blank=True, null=True, verbose_name="Data de Início")
    data_fim = models.DateField(blank=True, null=True, verbose_name="Data de Conclusão")
    
    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('user', 'livro')
        verbose_name = "Diário de Leitura"
        verbose_name_plural = "Diários de Leitura"

    def __str__(self):
        return f"{self.user.username} - {self.livro.titulo}"