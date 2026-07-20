from decimal import Decimal

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from usuarios.decorators import admin_required
from .forms import MovimientoForm
from .models import Movimiento


@login_required
def billetera_list(request):
    movimientos = Movimiento.objects.all()
    ingresos = sum((m.monto for m in movimientos if m.tipo == Movimiento.INGRESO), Decimal('0'))
    egresos = sum((m.monto for m in movimientos if m.tipo == Movimiento.EGRESO), Decimal('0'))
    return render(request, 'billetera/billetera_list.html', {
        'movimientos': movimientos,
        'saldo': ingresos - egresos,
    })


@admin_required
def movimiento_create(request):
    form = MovimientoForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'Movimiento registrado correctamente.')
        return redirect('billetera_list')
    return render(request, 'billetera/movimiento_form.html', {'form': form})
