from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

# =================================================================
# 1. PERFIL DO USUÁRIO (Extensão para o lado social)
# =================================================================
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    bio = models.TextField(blank=True, null=True, verbose_name="Biografia")
    
    PRIVACY_CHOICES = [
        ('publico', 'Público'),
        ('privado', 'Privado'),
        ('amigos', 'Apenas Amigos'),
    ]
    privacidade = models.CharField(
        max_length=20, 
        choices=PRIVACY_CHOICES, 
        default='publico',
        verbose_name="Privacidade da Conta"
    )
    
    seguindo = models.ManyToManyField(
        'self', 
        symmetrical=False, 
        related_name='seguidores', 
        blank=True
    )

    def __str__(self):
        return f"Perfil de {self.user.username}"

# =================================================================
# MODELO DE PERFIL (Extensão do Usuário)
# =================================================================
class Perfil(models.Model):
    # Relacionamento 1 para 1: Cada User tem exatamente 1 Perfil
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='perfil')
    
    # Foto de perfil (Avatar)
    avatar = models.ImageField(upload_to='avatars/', default='avatars/default.png', blank=True, null=True)
    
    # Biografia literária
    bio = models.TextField(max_length=500, blank=True, help_text="Conte um pouco sobre suas leituras e tropos favoritos.")
    
    # Preferências de leitura (opcional para personalizações futuras)
    generos_favoritos = models.CharField(max_length=200, blank=True, help_text="Ex: Alta Fantasia, Romance Épico, Dark Romance")

    def __str__(self):
        return f"Perfil de {self.user.username}"


# =================================================================
# SIGNALS (Gatilhos Automáticos)
# =================================================================
# Quando um User for salvo, este receptor dispara automaticamente
@receiver(post_save, sender=User)
def criar_ou_atualizar_perfil_usuario(sender, instance, created, **kwargs):
    if created:
        Perfil.objects.create(user=instance)
    # Garante que o perfil seja salvo sempre que o usuário for atualizado
    instance.perfil.save()
