# Create your views here.
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST

from .models import Libro, Ejemplar
from .forms import LibroForm, EjemplarForm
from usuarios.decorators import admin_required


@login_required
def lista_libros(request):
    libros = Libro.objects.all()

    busqueda = request.GET.get('buscar')

    if busqueda:
        libros = libros.filter(titulo__icontains=busqueda)

    return render(request, 'libros/lista_libros.html', {
        'libros': libros
    })

@admin_required
def crear_libro(request):
    if request.method == 'POST':
        form = LibroForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect('lista_libros')
    else:
        form = LibroForm()

    return render(request, 'libros/formulario_libro.html', {
        'form': form,
        'titulo': 'Registrar libro'
    })

@admin_required
def editar_libro(request, libro_id):
    libro = get_object_or_404(Libro, id=libro_id)

    if request.method == 'POST':
        form = LibroForm(request.POST, instance=libro)

        if form.is_valid():
            form.save()
            return redirect('lista_libros')
    else:
        form = LibroForm(instance=libro)

    return render(request, 'libros/formulario_libro.html', {
        'form': form,
        'titulo': 'Editar libro'
    })

@admin_required
@require_POST
def eliminar_libro(request, libro_id):
    libro = get_object_or_404(Libro, id=libro_id)

    libro.estado = 'BAJA'
    libro.save()

    return redirect('lista_libros')

## EJEMPLARES

@admin_required
def lista_ejemplares(request):
    ejemplares = Ejemplar.objects.all()

    return render(request, 'libros/lista_ejemplares.html', {
        'ejemplares': ejemplares
    })

@admin_required
def crear_ejemplar(request):
    if request.method == 'POST':
        form = EjemplarForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect('lista_ejemplares')
    else:
        form = EjemplarForm()

    return render(request, 'libros/formulario_ejemplar.html', {
        'form': form,
        'titulo': 'Registrar ejemplar'
    })

@admin_required
def editar_ejemplar(request, ejemplar_id):
    ejemplar = get_object_or_404(Ejemplar, id=ejemplar_id)

    if request.method == 'POST':
        form = EjemplarForm(request.POST, instance=ejemplar)

        if form.is_valid():
            form.save()
            return redirect('lista_ejemplares')
    else:
        form = EjemplarForm(instance=ejemplar)

    return render(request, 'libros/formulario_ejemplar.html', {
        'form': form,
        'titulo': 'Editar ejemplar'
    })

@admin_required
@require_POST
def eliminar_ejemplar(request, ejemplar_id):
    ejemplar = get_object_or_404(Ejemplar, id=ejemplar_id)
    ejemplar.estado = 'BAJA'
    ejemplar.save()

    return redirect('lista_ejemplares')