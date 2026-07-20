# Register your models here.
from django.contrib import admin
from .models import Libro, Ejemplar


@admin.register(Libro)
class LibroAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'autor', 'categoria', 'isbn', 'estado', 'fecha_registro')
    search_fields = ('titulo', 'autor', 'categoria', 'isbn')
    list_filter = ('estado', 'categoria')


@admin.register(Ejemplar)
class EjemplarAdmin(admin.ModelAdmin):
    list_display = ('codigo_ejemplar', 'libro', 'estado', 'ubicacion', 'fecha_registro')
    search_fields = ('codigo_ejemplar', 'libro__titulo')
    list_filter = ('estado',)