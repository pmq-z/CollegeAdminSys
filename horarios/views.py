from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Case, When, Value, IntegerField
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST

from usuarios.decorators import admin_required, es_admin
from .models import Horario
from .forms import HorarioForm


# Página principal: la lectura es para cualquier usuario autenticado, pero
# solo un administrador puede dar de alta un horario nuevo desde este mismo formulario.
@login_required
def index(request):

    if request.method == 'POST':
        if not es_admin(request.user):
            messages.error(request, 'No tienes permiso para registrar horarios.')
            return redirect('horarios_index')

        form = HorarioForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect('horarios_index')

    else:
        form = HorarioForm()

    # Ordenar los días correctamente
    horarios = Horario.objects.annotate(
        orden_dia=Case(
            When(dia='Lunes', then=Value(1)),
            When(dia='Martes', then=Value(2)),
            When(dia='Miércoles', then=Value(3)),
            When(dia='Jueves', then=Value(4)),
            When(dia='Viernes', then=Value(5)),
            When(dia='Sábado', then=Value(6)),
            When(dia='Domingo', then=Value(7)),
            output_field=IntegerField(),
        )
    ).order_by('orden_dia', 'hora_inicio')

    # Estadísticas
    total = Horario.objects.count()
    activos = Horario.objects.filter(estado=True).count()
    inactivos = Horario.objects.filter(estado=False).count()

    return render(request, 'horarios/index.html', {
        'form': form,
        'horarios': horarios,
        'total': total,
        'activos': activos,
        'inactivos': inactivos,
    })


# Editar horario
@admin_required
def editar(request, id):

    horario = get_object_or_404(Horario, id=id)

    if request.method == 'POST':

        form = HorarioForm(request.POST, instance=horario)

        if form.is_valid():
            form.save()
            return redirect('horarios_index')

    else:

        form = HorarioForm(instance=horario)

    return render(request, 'horarios/editar.html', {
        'form': form
    })


# Eliminar horario. Requiere POST: un GET nunca debe borrar datos (evita que
# un enlace, un crawler o un ataque CSRF disparen la eliminación).
@admin_required
@require_POST
def eliminar(request, id):

    horario = get_object_or_404(Horario, id=id)

    horario.delete()

    return redirect('horarios_index')