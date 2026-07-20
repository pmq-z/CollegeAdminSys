from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator

class Curso(models.Model):
    nombre = models.CharField(max_length=100)
    seccion = models.CharField(max_length=20)
    periodo = models.CharField(max_length=20, default="2026-1")
    docente = models.ForeignKey(User, on_delete=models.CASCADE, related_name='cursos_docente')
    acta_firmada = models.BooleanField(default=False)
    fecha_firma = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.nombre} ({self.seccion})"

class AlumnoCurso(models.Model):
    alumno = models.ForeignKey(User, on_delete=models.CASCADE, related_name='inscripciones_alumno')
    curso = models.ForeignKey(Curso, on_delete=models.CASCADE, related_name='inscripciones')
    asistencia_porcentaje = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(100)])
    calificacion_final = models.DecimalField(max_digits=4, decimal_places=2, null=True, blank=True, validators=[MinValueValidator(0), MaxValueValidator(10)])
    observaciones = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        unique_together = ('alumno', 'curso')