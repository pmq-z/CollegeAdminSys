# Register your models here.
from django.contrib import admin
from .models import PerfilUsuario


@admin.register(PerfilUsuario)
class PerfilUsuarioAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'rol', 'estado', 'telefono', 'fecha_registro')
    search_fields = ('usuario__username', 'usuario__first_name', 'usuario__last_name', 'telefono')
    list_filter = ('rol', 'estado')