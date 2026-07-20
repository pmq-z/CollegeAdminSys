# Create your models here.
from django.db import models
from django.contrib.auth.models import User
from libros.models import Libro, Ejemplar


class SolicitudPrestamo(models.Model):
    ESTADO_CHOICES = [
        ('PENDIENTE', 'Pendiente'),
        ('APROBADA', 'Aprobada'),
        ('RECHAZADA', 'Rechazada'),
        ('CANCELADA', 'Cancelada'),
    ]

    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    libro = models.ForeignKey(Libro, on_delete=models.CASCADE)
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='PENDIENTE')
    fecha_solicitud = models.DateTimeField(auto_now_add=True)
    observaciones = models.TextField(blank=True, null=True)

    def __str__(self):
        return f'{self.usuario.username} solicita {self.libro.titulo}'


class Prestamo(models.Model):
    ESTADO_CHOICES = [
        ('ACTIVO', 'Activo'),
        ('DEVUELTO', 'Devuelto'),
        ('VENCIDO', 'Vencido'),
    ]

    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    ejemplar = models.ForeignKey(Ejemplar, on_delete=models.CASCADE)
    solicitud = models.ForeignKey(
        SolicitudPrestamo,
        on_delete=models.SET_NULL,
        blank=True,
        null=True
    )
    fecha_prestamo = models.DateTimeField(auto_now_add=True)
    fecha_limite = models.DateTimeField()
    fecha_devolucion = models.DateTimeField(blank=True, null=True)
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='ACTIVO')
    observaciones = models.TextField(blank=True, null=True)

    def __str__(self):
        return f'{self.ejemplar.libro.titulo} prestado a {self.usuario.username}'