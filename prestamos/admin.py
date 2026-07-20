# Register your models here.
from django.contrib import admin
from .models import SolicitudPrestamo, Prestamo


@admin.register(SolicitudPrestamo)
class SolicitudPrestamoAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'libro', 'estado', 'fecha_solicitud')
    search_fields = ('usuario__username', 'libro__titulo')
    list_filter = ('estado', 'fecha_solicitud')


@admin.register(Prestamo)
class PrestamoAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'ejemplar', 'fecha_prestamo', 'fecha_limite', 'fecha_devolucion', 'estado')
    search_fields = ('usuario__username', 'ejemplar__libro__titulo', 'ejemplar__codigo_ejemplar')
    list_filter = ('estado', 'fecha_prestamo', 'fecha_limite')