import re

from django import forms

from .models import Empresa

# Patrón general de RFC mexicano: 3-4 letras/ampersand + 6 dígitos (fecha) +
# 3 caracteres alfanuméricos (homoclave). No valida el dígito verificador
# real (requeriría el algoritmo completo del SAT), pero detecta el error más
# común: texto que claramente no tiene forma de RFC.
RFC_PATTERN = re.compile(r'^[A-ZÑ&]{3,4}\d{6}[A-Z0-9]{3}$')


class EmpresaForm(forms.ModelForm):
    class Meta:
        model = Empresa
        fields = ['razon_social', 'rfc', 'giro', 'telefono', 'correo', 'activa']
        widgets = {
            'razon_social': forms.TextInput(attrs={'class': 'form-control'}),
            'rfc': forms.TextInput(attrs={'class': 'form-control'}),
            'giro': forms.TextInput(attrs={'class': 'form-control'}),
            'telefono': forms.TextInput(attrs={'class': 'form-control'}),
            'correo': forms.EmailInput(attrs={'class': 'form-control'}),
            'activa': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

    def clean_rfc(self):
        rfc = self.cleaned_data['rfc'].strip().upper()
        if not RFC_PATTERN.match(rfc):
            raise forms.ValidationError('El RFC no tiene un formato válido (ej. ABC120101XYZ).')
        return rfc
