from django import forms

from .models import Alumno, Inscripcion, Maestro, Materia


class StyledModelForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            widget = field.widget
            if isinstance(widget, forms.CheckboxInput):
                widget.attrs.update({'class': 'form-check'})
            else:
                widget.attrs.update({'class': 'form-control'})


class AlumnoForm(StyledModelForm):
    class Meta:
        model = Alumno
        fields = [
            'nombre',
            'apellido_paterno',
            'apellido_materno',
            'correo',
            'telefono',
            'carrera',
            'semestre',
            'grupo',
            'turno',
            'estatus_academico',
            'observaciones',
            'activo',
        ]
        widgets = {
            'observaciones': forms.Textarea(attrs={'rows': 4}),
        }


class MaestroForm(StyledModelForm):
    class Meta:
        model = Maestro
        fields = [
            'nombre',
            'apellido_paterno',
            'apellido_materno',
            'correo',
            'telefono',
            'especialidad',
            'area_academica',
            'estatus_laboral',
            'puede_capturar_calificaciones',
            'puede_registrar_asistencias',
            'puede_generar_reportes',
            'observaciones',
            'activo',
        ]
        widgets = {
            'observaciones': forms.Textarea(attrs={'rows': 4}),
        }


class MateriaForm(StyledModelForm):
    class Meta:
        model = Materia
        fields = [
            'clave',
            'nombre',
            'descripcion',
            'creditos',
            'carrera',
            'semestre',
            'cupo_maximo',
            'maestro_responsable',
            'activa',
        ]
        widgets = {
            'descripcion': forms.Textarea(attrs={'rows': 4}),
        }


class InscripcionForm(StyledModelForm):
    class Meta:
        model = Inscripcion
        fields = [
            'alumno',
            'materia',
            'periodo_escolar',
            'activo',
        ]

    def clean(self):
        cleaned_data = super().clean()
        alumno = cleaned_data.get('alumno')
        materia = cleaned_data.get('materia')
        periodo_escolar = cleaned_data.get('periodo_escolar')
        activo = cleaned_data.get('activo')

        if alumno and materia and periodo_escolar and activo:
            existe = Inscripcion.objects.filter(
                alumno=alumno,
                materia=materia,
                periodo_escolar=periodo_escolar,
                activo=True,
            )
            if self.instance.pk:
                existe = existe.exclude(pk=self.instance.pk)
            if existe.exists():
                raise forms.ValidationError(
                    'Ya existe una inscripcion activa para este alumno, materia y periodo escolar.'
                )
        return cleaned_data
