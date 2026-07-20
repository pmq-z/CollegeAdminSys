from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from usuarios.decorators import admin_required
from .forms import AlumnoForm, InscripcionForm, MaestroForm, MateriaForm
from .models import Alumno, Inscripcion, Maestro, Materia


@login_required
def index(request):
    context = {
        'total_alumnos': Alumno.objects.filter(activo=True).count(),
        'total_maestros': Maestro.objects.filter(activo=True).count(),
        'total_materias': Materia.objects.filter(activa=True).count(),
        'total_inscripciones': Inscripcion.objects.filter(activo=True).count(),
        'alumnos_recientes': Alumno.objects.filter(activo=True).order_by('-fecha_creacion')[:5],
    }
    return render(request, 'alumnos_maestros/index.html', context)


@login_required
def alumno_list(request):
    q = request.GET.get('q', '').strip()
    alumnos = Alumno.objects.all()
    if q:
        alumnos = alumnos.filter(
            Q(nombre__icontains=q)
            | Q(apellido_paterno__icontains=q)
            | Q(apellido_materno__icontains=q)
            | Q(correo__icontains=q)
            | Q(matricula__icontains=q)
        )
    return render(request, 'alumnos_maestros/alumno_list.html', {'alumnos': alumnos, 'q': q})


@admin_required
def alumno_create(request):
    form = AlumnoForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        alumno = form.save()
        messages.success(request, f'Alumno {alumno.matricula} registrado correctamente.')
        return redirect('alumno_list')
    return render(request, 'alumnos_maestros/alumno_form.html', {'form': form, 'titulo': 'Nuevo alumno'})


@admin_required
def alumno_update(request, pk):
    alumno = get_object_or_404(Alumno, pk=pk)
    form = AlumnoForm(request.POST or None, instance=alumno)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'Alumno actualizado correctamente.')
        return redirect('alumno_list')
    return render(request, 'alumnos_maestros/alumno_form.html', {'form': form, 'titulo': 'Editar alumno', 'alumno': alumno})


@admin_required
@require_POST
def alumno_deactivate(request, pk):
    alumno = get_object_or_404(Alumno, pk=pk)
    alumno.activo = False
    alumno.save(update_fields=['activo'])
    messages.success(request, 'Alumno desactivado correctamente.')
    return redirect('alumno_list')


@login_required
def maestro_list(request):
    q = request.GET.get('q', '').strip()
    maestros = Maestro.objects.all()
    if q:
        maestros = maestros.filter(
            Q(nombre__icontains=q)
            | Q(apellido_paterno__icontains=q)
            | Q(apellido_materno__icontains=q)
            | Q(correo__icontains=q)
            | Q(numero_empleado__icontains=q)
        )
    return render(request, 'alumnos_maestros/maestro_list.html', {'maestros': maestros, 'q': q})


@admin_required
def maestro_create(request):
    form = MaestroForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        maestro = form.save()
        messages.success(request, f'Maestro {maestro.numero_empleado} registrado correctamente.')
        return redirect('maestro_list')
    return render(request, 'alumnos_maestros/maestro_form.html', {'form': form, 'titulo': 'Nuevo maestro'})


@admin_required
def maestro_update(request, pk):
    maestro = get_object_or_404(Maestro, pk=pk)
    form = MaestroForm(request.POST or None, instance=maestro)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'Maestro actualizado correctamente.')
        return redirect('maestro_list')
    return render(request, 'alumnos_maestros/maestro_form.html', {'form': form, 'titulo': 'Editar maestro', 'maestro': maestro})


@admin_required
@require_POST
def maestro_deactivate(request, pk):
    maestro = get_object_or_404(Maestro, pk=pk)
    maestro.activo = False
    maestro.save(update_fields=['activo'])
    messages.success(request, 'Maestro desactivado correctamente.')
    return redirect('maestro_list')


@login_required
def materia_list(request):
    q = request.GET.get('q', '').strip()
    materias = Materia.objects.select_related('maestro_responsable')
    if q:
        materias = materias.filter(
            Q(clave__icontains=q)
            | Q(nombre__icontains=q)
            | Q(carrera__icontains=q)
            | Q(maestro_responsable__nombre__icontains=q)
            | Q(maestro_responsable__apellido_paterno__icontains=q)
            | Q(maestro_responsable__apellido_materno__icontains=q)
        )
    return render(request, 'alumnos_maestros/materia_list.html', {'materias': materias, 'q': q})


@admin_required
def materia_create(request):
    form = MateriaForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'Materia registrada correctamente.')
        return redirect('materia_list')
    return render(request, 'alumnos_maestros/materia_form.html', {'form': form, 'titulo': 'Nueva materia'})


@admin_required
def materia_update(request, pk):
    materia = get_object_or_404(Materia, pk=pk)
    form = MateriaForm(request.POST or None, instance=materia)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'Materia actualizada correctamente.')
        return redirect('materia_list')
    return render(request, 'alumnos_maestros/materia_form.html', {'form': form, 'titulo': 'Editar materia', 'materia': materia})


@admin_required
@require_POST
def materia_deactivate(request, pk):
    materia = get_object_or_404(Materia, pk=pk)
    materia.activa = False
    materia.save(update_fields=['activa'])
    messages.success(request, 'Materia desactivada correctamente.')
    return redirect('materia_list')


@login_required
def inscripcion_list(request):
    q = request.GET.get('q', '').strip()
    inscripciones = Inscripcion.objects.select_related('alumno', 'materia')
    if q:
        inscripciones = inscripciones.filter(
            Q(alumno__nombre__icontains=q)
            | Q(alumno__apellido_paterno__icontains=q)
            | Q(alumno__apellido_materno__icontains=q)
            | Q(alumno__matricula__icontains=q)
            | Q(materia__nombre__icontains=q)
            | Q(materia__clave__icontains=q)
            | Q(periodo_escolar__icontains=q)
        )
    return render(request, 'alumnos_maestros/inscripcion_list.html', {'inscripciones': inscripciones, 'q': q})


@admin_required
def inscripcion_create(request):
    form = InscripcionForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'Inscripcion registrada correctamente.')
        return redirect('inscripcion_list')
    return render(request, 'alumnos_maestros/inscripcion_form.html', {'form': form, 'titulo': 'Nueva inscripcion'})


@admin_required
@require_POST
def inscripcion_deactivate(request, pk):
    inscripcion = get_object_or_404(Inscripcion, pk=pk)
    inscripcion.activo = False
    inscripcion.save(update_fields=['activo'])
    messages.success(request, 'Inscripcion desactivada correctamente.')
    return redirect('inscripcion_list')
