from django import forms
from .models import SolicitudPrestamo, Prestamo
from libros.models import Ejemplar


class SolicitudPrestamoForm(forms.ModelForm):
    class Meta:
        model = SolicitudPrestamo
        fields = [
            'libro',
            'observaciones',
        ]

        labels = {
            'libro': 'Libro',
            'observaciones': 'Observaciones',
        }

        widgets = {
            'libro': forms.Select(attrs={'class': 'form-control'}),
            'observaciones': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }


class PrestamoForm(forms.ModelForm):
    class Meta:
        model = Prestamo
        fields = [
            'usuario',
            'ejemplar',
            'solicitud',
            'fecha_limite',
            'observaciones',
        ]

        labels = {
            'usuario': 'Usuario',
            'ejemplar': 'Ejemplar',
            'solicitud': 'Solicitud relacionada',
            'fecha_limite': 'Fecha límite de devolución',
            'observaciones': 'Observaciones',
        }

        widgets = {
            'usuario': forms.Select(attrs={'class': 'form-control'}),
            'ejemplar': forms.Select(attrs={'class': 'form-control'}),
            'solicitud': forms.Select(attrs={'class': 'form-control'}),
            'fecha_limite': forms.DateTimeInput(
                attrs={
                    'class': 'form-control',
                    'type': 'datetime-local'
                }
            ),
            'observaciones': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['ejemplar'].queryset = Ejemplar.objects.filter(estado='DISPONIBLE')
        self.fields['solicitud'].required = False