from django import forms

from .models import Movimiento


class MovimientoForm(forms.ModelForm):
    class Meta:
        model = Movimiento
        fields = ['concepto', 'monto', 'tipo']
        widgets = {
            'concepto': forms.TextInput(attrs={'class': 'form-control'}),
            'monto': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'min': '0.01'}),
            'tipo': forms.Select(attrs={'class': 'form-select'}),
        }

    def clean_monto(self):
        # DecimalField por sí solo acepta negativos; un movimiento con monto
        # negativo o en cero no tiene sentido de negocio y descuadraría el saldo.
        monto = self.cleaned_data['monto']
        if monto <= 0:
            raise forms.ValidationError('El monto debe ser mayor a cero.')
        return monto
