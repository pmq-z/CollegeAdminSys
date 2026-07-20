from django.contrib import admin
from .models import Curso, AlumnoCurso

@admin.register(Curso)
class CursoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'seccion', 'periodo', 'docente', 'acta_firmada')
    list_filter = ('periodo', 'acta_firmada')
    search_fields = ('nombre', 'seccion', 'docente__username')

@admin.register(AlumnoCurso)
class AlumnoCursoAdmin(admin.ModelAdmin):
    list_display = ('alumno', 'curso', 'calificacion_final', 'asistencia_porcentaje')
    list_filter = ('curso',)
    search_fields = ('alumno__username', 'alumno__first_name')