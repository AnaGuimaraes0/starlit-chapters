from django.db import models
from django.contrib.auth.models import User

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
