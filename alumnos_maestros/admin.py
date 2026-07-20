from django.contrib import admin

from .models import Alumno, Inscripcion, Maestro, Materia


@admin.register(Alumno)
class AlumnoAdmin(admin.ModelAdmin):
    list_display = ('matricula', 'nombre', 'apellido_paterno', 'correo', 'carrera', 'semestre', 'grupo', 'estatus_academico', 'activo')
    search_fields = ('matricula', 'nombre', 'apellido_paterno', 'apellido_materno', 'correo')
    list_filter = ('activo', 'estatus_academico', 'carrera', 'semestre', 'turno')
    readonly_fields = ('matricula', 'fecha_creacion')


@admin.register(Maestro)
class MaestroAdmin(admin.ModelAdmin):
    list_display = ('numero_empleado', 'nombre', 'apellido_paterno', 'correo', 'area_academica', 'estatus_laboral', 'activo')
    search_fields = ('numero_empleado', 'nombre', 'apellido_paterno', 'apellido_materno', 'correo')
    list_filter = ('activo', 'estatus_laboral', 'area_academica')
    readonly_fields = ('numero_empleado', 'fecha_creacion')


@admin.register(Materia)
class MateriaAdmin(admin.ModelAdmin):
    list_display = ('clave', 'nombre', 'carrera', 'semestre', 'creditos', 'cupo_maximo', 'maestro_responsable', 'activa')
    search_fields = ('clave', 'nombre', 'carrera', 'maestro_responsable__nombre', 'maestro_responsable__apellido_paterno')
    list_filter = ('activa', 'carrera', 'semestre')
    readonly_fields = ('fecha_creacion',)


@admin.register(Inscripcion)
class InscripcionAdmin(admin.ModelAdmin):
    list_display = ('alumno', 'materia', 'periodo_escolar', 'fecha_inscripcion', 'activo')
    search_fields = ('alumno__matricula', 'alumno__nombre', 'alumno__apellido_paterno', 'materia__clave', 'materia__nombre', 'periodo_escolar')
    list_filter = ('activo', 'periodo_escolar', 'materia')
    readonly_fields = ('fecha_inscripcion',)
