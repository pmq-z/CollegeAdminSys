from django.db import models


class Movimiento(models.Model):
    INGRESO = 'Ingreso'
    EGRESO = 'Egreso'

    TIPO_CHOICES = [
        (INGRESO, 'Ingreso'),
        (EGRESO, 'Egreso'),
    ]

    concepto = models.CharField(max_length=150)
    monto = models.DecimalField(max_digits=10, decimal_places=2)
    tipo = models.CharField(max_length=10, choices=TIPO_CHOICES)
    fecha = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Movimiento'
        verbose_name_plural = 'Movimientos'
        ordering = ['-fecha']

    def __str__(self):
        return f'{self.tipo} - {self.concepto} (${self.monto})'
