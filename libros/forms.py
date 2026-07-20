from django import forms
from .models import Libro, Ejemplar


class LibroForm(forms.ModelForm):
    class Meta:
        model = Libro
        fields = [
            'titulo',
            'autor',
            'editorial',
            'anio_publicacion',
            'categoria',
            'isbn',
            'descripcion',
            'estado',
        ]

        labels = {
            'titulo': 'Título',
            'autor': 'Autor',
            'editorial': 'Editorial',
            'anio_publicacion': 'Año de publicación',
            'categoria': 'Categoría',
            'isbn': 'ISBN',
            'descripcion': 'Descripción',
            'estado': 'Estado',
        }

        widgets = {
            'titulo': forms.TextInput(attrs={'class': 'form-control'}),
            'autor': forms.TextInput(attrs={'class': 'form-control'}),
            'editorial': forms.TextInput(attrs={'class': 'form-control'}),
            'anio_publicacion': forms.NumberInput(attrs={'class': 'form-control'}),
            'categoria': forms.TextInput(attrs={'class': 'form-control'}),
            'isbn': forms.TextInput(attrs={'class': 'form-control'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'estado': forms.Select(attrs={'class': 'form-control'}),
        }


class EjemplarForm(forms.ModelForm):
    class Meta:
        model = Ejemplar
        fields = [
            'libro',
            'codigo_ejemplar',
            'estado',
            'ubicacion',
        ]

        labels = {
            'libro': 'Libro',
            'codigo_ejemplar': 'Código del ejemplar',
            'estado': 'Estado',
            'ubicacion': 'Ubicación',
        }

        widgets = {
            'libro': forms.Select(attrs={'class': 'form-control'}),
            'codigo_ejemplar': forms.TextInput(attrs={'class': 'form-control'}),
            'estado': forms.Select(attrs={'class': 'form-control'}),
            'ubicacion': forms.TextInput(attrs={'class': 'form-control'}),
        }