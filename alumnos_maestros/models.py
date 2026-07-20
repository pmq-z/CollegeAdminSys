from django.db import models
from django.utils import timezone


class Alumno(models.Model):
    ESTATUS_ACTIVO = 'Activo'
    ESTATUS_BAJA_TEMPORAL = 'Baja temporal'
    ESTATUS_BAJA_DEFINITIVA = 'Baja definitiva'
    ESTATUS_EGRESADO = 'Egresado'

    ESTATUS_CHOICES = [
        (ESTATUS_ACTIVO, 'Activo'),
        (ESTATUS_BAJA_TEMPORAL, 'Baja temporal'),
        (ESTATUS_BAJA_DEFINITIVA, 'Baja definitiva'),
        (ESTATUS_EGRESADO, 'Egresado'),
    ]

    TURNO_CHOICES = [
        ('Matutino', 'Matutino'),
        ('Vespertino', 'Vespertino'),
        ('Mixto', 'Mixto'),
    ]

    matricula = models.CharField(max_length=20, unique=True, blank=True)
    nombre = models.CharField(max_length=100)
    apellido_paterno = models.CharField(max_length=100)
    apellido_materno = models.CharField(max_length=100, blank=True)
    correo = models.EmailField(unique=True)
    telefono = models.CharField(max_length=20, blank=True)
    carrera = models.CharField(max_length=120)
    semestre = models.PositiveSmallIntegerField()
    grupo = models.CharField(max_length=20)
    turno = models.CharField(max_length=20, choices=TURNO_CHOICES)
    estatus_academico = models.CharField(
        max_length=30,
        choices=ESTATUS_CHOICES,
        default=ESTATUS_ACTIVO,
    )
    observaciones = models.TextField(blank=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    activo = models.BooleanField(default=True)

    class Meta:
        verbose_name = 'Alumno'
        verbose_name_plural = 'Alumnos'
        ordering = ['apellido_paterno', 'apellido_materno', 'nombre']

    def save(self, *args, **kwargs):
        if not self.matricula:
            self.matricula = self._generar_matricula()
        super().save(*args, **kwargs)

    @classmethod
    def _generar_matricula(cls):
        year = timezone.localdate().year
        prefijo = f'ALU-{year}-'
        ultimo = cls.objects.filter(matricula__startswith=prefijo).order_by('-matricula').first()
        consecutivo = 1
        if ultimo:
            consecutivo = int(ultimo.matricula.split('-')[-1]) + 1
        return f'{prefijo}{consecutivo:04d}'

    def __str__(self):
        return f'{self.matricula} - {self.nombre} {self.apellido_paterno}'


class Maestro(models.Model):
    ESTATUS_ACTIVO = 'Activo'
    ESTATUS_INACTIVO = 'Inactivo'
    ESTATUS_PERMISO_TEMPORAL = 'Permiso temporal'

    ESTATUS_CHOICES = [
        (ESTATUS_ACTIVO, 'Activo'),
        (ESTATUS_INACTIVO, 'Inactivo'),
        (ESTATUS_PERMISO_TEMPORAL, 'Permiso temporal'),
    ]

    numero_empleado = models.CharField(max_length=20, unique=True, blank=True)
    nombre = models.CharField(max_length=100)
    apellido_paterno = models.CharField(max_length=100)
    apellido_materno = models.CharField(max_length=100, blank=True)
    correo = models.EmailField(unique=True)
    telefono = models.CharField(max_length=20, blank=True)
    especialidad = models.CharField(max_length=120)
    area_academica = models.CharField(max_length=120)
    estatus_laboral = models.CharField(
        max_length=30,
        choices=ESTATUS_CHOICES,
        default=ESTATUS_ACTIVO,
    )
    puede_capturar_calificaciones = models.BooleanField(default=True)
    puede_registrar_asistencias = models.BooleanField(default=True)
    puede_generar_reportes = models.BooleanField(default=False)
    observaciones = models.TextField(blank=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    activo = models.BooleanField(default=True)

    class Meta:
        verbose_name = 'Maestro'
        verbose_name_plural = 'Maestros'
        ordering = ['apellido_paterno', 'apellido_materno', 'nombre']

    def save(self, *args, **kwargs):
        if not self.numero_empleado:
            self.numero_empleado = self._generar_numero_empleado()
        super().save(*args, **kwargs)

    @classmethod
    def _generar_numero_empleado(cls):
        year = timezone.localdate().year
        prefijo = f'DOC-{year}-'
        ultimo = cls.objects.filter(numero_empleado__startswith=prefijo).order_by('-numero_empleado').first()
        consecutivo = 1
        if ultimo:
            consecutivo = int(ultimo.numero_empleado.split('-')[-1]) + 1
        return f'{prefijo}{consecutivo:04d}'

    def __str__(self):
        return f'{self.numero_empleado} - {self.nombre} {self.apellido_paterno}'


class Materia(models.Model):
    clave = models.CharField(max_length=20, unique=True)
    nombre = models.CharField(max_length=120)
    descripcion = models.TextField(blank=True)
    creditos = models.PositiveSmallIntegerField()
    carrera = models.CharField(max_length=120)
    semestre = models.PositiveSmallIntegerField()
    cupo_maximo = models.PositiveSmallIntegerField()
    maestro_responsable = models.ForeignKey(
        Maestro,
        on_delete=models.PROTECT,
        related_name='materias',
    )
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    activa = models.BooleanField(default=True)

    class Meta:
        verbose_name = 'Materia'
        verbose_name_plural = 'Materias'
        ordering = ['carrera', 'semestre', 'nombre']

    def __str__(self):
        return f'{self.clave} - {self.nombre}'


class Inscripcion(models.Model):
    alumno = models.ForeignKey(Alumno, on_delete=models.PROTECT, related_name='inscripciones')
    materia = models.ForeignKey(Materia, on_delete=models.PROTECT, related_name='inscripciones')
    periodo_escolar = models.CharField(max_length=30)
    fecha_inscripcion = models.DateTimeField(auto_now_add=True)
    activo = models.BooleanField(default=True)

    class Meta:
        verbose_name = 'Inscripcion'
        verbose_name_plural = 'Inscripciones'
        ordering = ['-fecha_inscripcion']
        constraints = [
            models.UniqueConstraint(
                fields=['alumno', 'materia', 'periodo_escolar'],
                condition=models.Q(activo=True),
                name='inscripcion_activa_unica',
            ),
        ]

    def __str__(self):
        return f'{self.alumno} / {self.materia} / {self.periodo_escolar}'
