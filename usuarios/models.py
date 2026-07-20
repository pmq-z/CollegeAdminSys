# Create your models here.
from django.db import models
from django.contrib.auth.models import User


class PerfilUsuario(models.Model):
    ROL_CHOICES = [
        ('USUARIO', 'Usuario'),
        ('ADMIN', 'Administrador'),
    ]

    ESTADO_CHOICES = [
        ('ACTIVO', 'Activo'),
        ('BAJA', 'Baja'),
    ]

    usuario = models.OneToOneField(User, on_delete=models.CASCADE)
    telefono = models.CharField(max_length=20, blank=True, null=True)
    direccion = models.CharField(max_length=255, blank=True, null=True)
    rol = models.CharField(max_length=20, choices=ROL_CHOICES, default='USUARIO')
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='ACTIVO')
    fecha_registro = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.usuario.username} - {self.rol}'