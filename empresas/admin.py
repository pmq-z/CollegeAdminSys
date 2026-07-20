from django.contrib import admin

from .models import Empresa


@admin.register(Empresa)
class EmpresaAdmin(admin.ModelAdmin):
    list_display = ('razon_social', 'rfc', 'giro', 'telefono', 'activa')
    search_fields = ('razon_social', 'rfc', 'giro')
    list_filter = ('activa',)
