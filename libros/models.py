# Create your models here.
from django.db import models


class Libro(models.Model):
    ESTADO_CHOICES = [
        ('ACTIVO', 'Activo'),
        ('BAJA', 'Baja'),
    ]

    titulo = models.CharField(max_length=150)
    autor = models.CharField(max_length=150)
    editorial = models.CharField(max_length=150, blank=True, null=True)
    anio_publicacion = models.IntegerField(blank=True, null=True)
    categoria = models.CharField(max_length=100, blank=True, null=True)
    isbn = models.CharField(max_length=30, unique=True, blank=True, null=True)
    descripcion = models.TextField(blank=True, null=True)
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='ACTIVO')
    fecha_registro = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.titulo


class Ejemplar(models.Model):
    ESTADO_CHOICES = [
        ('DISPONIBLE', 'Disponible'),
        ('PRESTADO', 'Prestado'),
        ('DAÑADO', 'Dañado'),
        ('BAJA', 'Baja'),
    ]

    libro = models.ForeignKey(Libro, on_delete=models.CASCADE, related_name='ejemplares')
    codigo_ejemplar = models.CharField(max_length=50, unique=True)
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='DISPONIBLE')
    ubicacion = models.CharField(max_length=100, blank=True, null=True)
    fecha_registro = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.codigo_ejemplar} - {self.libro.titulo}'