from django.db import models

class Horario(models.Model):

    # Opciones para el día de la semana
    DIAS_SEMANA = [
        ('Lunes', 'Lunes'),
        ('Martes', 'Martes'),
        ('Miércoles', 'Miércoles'),
        ('Jueves', 'Jueves'),
        ('Viernes', 'Viernes'),
        ('Sábado', 'Sábado'),
        ('Domingo', 'Domingo'),
    ]

    # Día del horario
    dia = models.CharField(
        max_length=15,
        choices=DIAS_SEMANA
    )

    # Hora de inicio
    hora_inicio = models.TimeField()

    # Hora de finalización
    hora_fin = models.TimeField()

    # Estado del horario
    estado = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.dia} | {self.hora_inicio} - {self.hora_fin}"