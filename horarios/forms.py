from django import forms
from .models import Horario


class HorarioForm(forms.ModelForm):

    class Meta:
        model = Horario
        fields = [
            'dia',
            'hora_inicio',
            'hora_fin',
            'estado'
        ]

        widgets = {

            'dia': forms.Select(
                attrs={
                    'class': 'form-select'
                }
            ),

            'hora_inicio': forms.TimeInput(
                attrs={
                    'class': 'form-control',
                    'type': 'time'
                }
            ),

            'hora_fin': forms.TimeInput(
                attrs={
                    'class': 'form-control',
                    'type': 'time'
                }
            ),

            'estado': forms.CheckboxInput(
                attrs={
                    'class': 'form-check-input'
                }
            )

        }

        labels = {

            'dia': 'Día',

            'hora_inicio': 'Hora de inicio',

            'hora_fin': 'Hora de finalización',

            'estado': 'Horario activo'

        }

        help_texts = {

            'dia': '',

            'hora_inicio': '',

            'hora_fin': '',

            'estado': ''

        }

    def clean(self):
        cleaned_data = super().clean()
        dia = cleaned_data.get('dia')
        hora_inicio = cleaned_data.get('hora_inicio')
        hora_fin = cleaned_data.get('hora_fin')

        if hora_inicio and hora_fin and hora_fin <= hora_inicio:
            raise forms.ValidationError('La hora de finalización debe ser posterior a la hora de inicio.')

        if dia and hora_inicio and hora_fin:
            # Dos horarios del mismo día se traslapan si uno empieza antes de
            # que el otro termine (y viceversa); sin este chequeo se podían
            # registrar dos clases al mismo tiempo sin ningún aviso.
            traslapes = Horario.objects.filter(
                dia=dia,
                hora_inicio__lt=hora_fin,
                hora_fin__gt=hora_inicio,
            )
            if self.instance.pk:
                traslapes = traslapes.exclude(pk=self.instance.pk)
            if traslapes.exists():
                raise forms.ValidationError('Ya existe un horario que se traslapa con este día y horas.')

        return cleaned_data