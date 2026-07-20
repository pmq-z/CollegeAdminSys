from django.contrib import admin

from .models import Movimiento


@admin.register(Movimiento)
class MovimientoAdmin(admin.ModelAdmin):
    list_display = ('concepto', 'tipo', 'monto', 'fecha')
    list_filter = ('tipo',)
    search_fields = ('concepto',)
