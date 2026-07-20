from django.db import models


class Empresa(models.Model):
    razon_social = models.CharField(max_length=150)
    rfc = models.CharField(max_length=13, unique=True)
    giro = models.CharField(max_length=120, blank=True)
    telefono = models.CharField(max_length=20, blank=True)
    correo = models.EmailField(blank=True)
    activa = models.BooleanField(default=True)
    fecha_registro = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Empresa'
        verbose_name_plural = 'Empresas'
        ordering = ['razon_social']

    def __str__(self):
        return self.razon_social
