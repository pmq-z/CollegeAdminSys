from datetime import timedelta

from django.contrib import messages
from django.db import transaction
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from django.views.decorators.http import require_POST

from .models import SolicitudPrestamo, Prestamo
from .forms import SolicitudPrestamoForm, PrestamoForm
from libros.models import Ejemplar

from django.contrib.auth.decorators import login_required
from usuarios.decorators import admin_required

## Vista para solicitar prestamo
@login_required(login_url='login')
def solicitar_prestamo(request):
    if request.method == 'POST':
        form = SolicitudPrestamoForm(request.POST)

        if form.is_valid():
            solicitud = form.save(commit=False)
            solicitud.usuario = request.user
            solicitud.estado = 'PENDIENTE'
            solicitud.save()

            return redirect('lista_solicitudes')
    else:
        form = SolicitudPrestamoForm()

    return render(request, 'prestamos/formulario_solicitud.html', {
        'form': form,
        'titulo': 'Solicitar préstamo'
    })

## para que el admin vea las solicitudes de prestamo y pueda aprobarlas o rechazarlas
@admin_required
def lista_solicitudes(request):
    solicitudes = SolicitudPrestamo.objects.all().order_by('-fecha_solicitud')

    return render(request, 'prestamos/lista_solicitudes.html', {
        'solicitudes': solicitudes
    })

### Para que el admin apruebe la solicitud
@admin_required
@require_POST
def aprobar_solicitud(request, solicitud_id):
    solicitud = get_object_or_404(SolicitudPrestamo, id=solicitud_id)

    # Sin este chequeo, recargar la página o repetir la petición podría
    # generar un segundo préstamo para una solicitud ya resuelta.
    if solicitud.estado != 'PENDIENTE':
        messages.error(request, 'Esta solicitud ya fue procesada.')
        return redirect('lista_solicitudes')

    # select_for_update bloquea la fila del ejemplar durante la transacción:
    # sin esto, dos aprobaciones simultáneas podrían leer el mismo ejemplar
    # como disponible y prestarlo dos veces.
    with transaction.atomic():
        ejemplar = Ejemplar.objects.select_for_update().filter(
            libro=solicitud.libro,
            estado='DISPONIBLE'
        ).first()

        if ejemplar is None:
            solicitud.observaciones = 'No hay ejemplares disponibles en este momento.'
            solicitud.save(update_fields=['observaciones'])
            messages.warning(request, 'No hay ejemplares disponibles para este libro.')
            return redirect('lista_solicitudes')

        Prestamo.objects.create(
            usuario=solicitud.usuario,
            ejemplar=ejemplar,
            solicitud=solicitud,
            fecha_limite=timezone.now() + timedelta(days=7),
            estado='ACTIVO'
        )

        ejemplar.estado = 'PRESTADO'
        ejemplar.save(update_fields=['estado'])

        solicitud.estado = 'APROBADA'
        solicitud.save(update_fields=['estado'])

    return redirect('prestamos_activos')

##Para rechazarla
@admin_required
@require_POST
def rechazar_solicitud(request, solicitud_id):
    solicitud = get_object_or_404(SolicitudPrestamo, id=solicitud_id)

    if solicitud.estado != 'PENDIENTE':
        messages.error(request, 'Esta solicitud ya fue procesada.')
        return redirect('lista_solicitudes')

    solicitud.estado = 'RECHAZADA'
    solicitud.save(update_fields=['estado'])

    return redirect('lista_solicitudes')

##Para registrar el prestamo sin necesidad de una solicitud previa
@admin_required
def registrar_prestamo(request):
    if request.method == 'POST':
        form = PrestamoForm(request.POST)

        if form.is_valid():
            with transaction.atomic():
                prestamo = form.save(commit=False)
                prestamo.estado = 'ACTIVO'
                prestamo.save()

                ejemplar = prestamo.ejemplar
                ejemplar.estado = 'PRESTADO'
                ejemplar.save(update_fields=['estado'])

                if prestamo.solicitud:
                    prestamo.solicitud.estado = 'APROBADA'
                    prestamo.solicitud.save(update_fields=['estado'])

            return redirect('prestamos_activos')
    else:
        form = PrestamoForm()

    return render(request, 'prestamos/formulario_prestamo.html', {
        'form': form,
        'titulo': 'Registrar préstamo'
    })

##Prestamos activos
@admin_required
def prestamos_activos(request):
    prestamos = Prestamo.objects.filter(estado='ACTIVO').order_by('-fecha_prestamo')

    return render(request, 'prestamos/prestamos_activos.html', {
        'prestamos': prestamos
    })

##Registrar devolucion
@admin_required
@require_POST
def registrar_devolucion(request, prestamo_id):
    prestamo = get_object_or_404(Prestamo, id=prestamo_id)

    if prestamo.estado != 'ACTIVO':
        messages.error(request, 'Este préstamo ya fue devuelto.')
        return redirect('prestamos_activos')

    with transaction.atomic():
        prestamo.estado = 'DEVUELTO'
        prestamo.fecha_devolucion = timezone.now()
        prestamo.save(update_fields=['estado', 'fecha_devolucion'])

        ejemplar = prestamo.ejemplar
        ejemplar.estado = 'DISPONIBLE'
        ejemplar.save(update_fields=['estado'])

    return redirect('prestamos_activos')