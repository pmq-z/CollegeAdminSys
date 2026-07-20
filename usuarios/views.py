# Create your views here.
from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required

from .forms import RegistroUsuarioForm
from .models import PerfilUsuario


def registro_usuario(request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        form = RegistroUsuarioForm(request.POST)

        if form.is_valid():
            usuario = form.save()

            PerfilUsuario.objects.create(
                usuario=usuario,
                telefono=form.cleaned_data.get('telefono'),
                direccion=form.cleaned_data.get('direccion'),
                rol='USUARIO',
                estado='ACTIVO'
            )

            login(request, usuario)

            return redirect('lista_libros')
    else:
        form = RegistroUsuarioForm()

    return render(request, 'usuarios/registro.html', {
        'form': form
    })


@login_required
def perfil_usuario(request):
    perfil, creado = PerfilUsuario.objects.get_or_create(
        usuario=request.user,
        defaults={
            'rol': 'USUARIO',
            'estado': 'ACTIVO'
        }
    )

    return render(request, 'usuarios/perfil.html', {
        'perfil': perfil
    })