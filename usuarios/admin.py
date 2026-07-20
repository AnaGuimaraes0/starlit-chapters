from django.contrib import admin
from .models import Profile

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'privacidade')
    search_fields = ('user__username',)
    filter_horizontal = ('seguindo',)
