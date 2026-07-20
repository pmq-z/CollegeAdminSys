from django.contrib import admin

from .models import Horario


@admin.register(Horario)
class HorarioAdmin(admin.ModelAdmin):
    list_display = ('dia', 'hora_inicio', 'hora_fin', 'estado')
    list_filter = ('dia', 'estado')
