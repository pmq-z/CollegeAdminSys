from django.shortcuts import redirect
from django.contrib import messages
from functools import wraps

from .models import PerfilUsuario


def es_admin(user):
    """Determina si un usuario tiene privilegios administrativos.

    Se centraliza acá porque la misma regla se necesitaba en el decorador,
    en templates (para mostrar/ocultar acciones) y en vistas que mezclan
    lectura pública con una acción restringida (p. ej. horarios.index).
    """
    if not user.is_authenticated:
        return False

    if user.is_superuser or user.is_staff:
        return True

    try:
        return user.perfilusuario.rol == 'ADMIN'
    except PerfilUsuario.DoesNotExist:
        return False


def admin_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login')

        if es_admin(request.user):
            return view_func(request, *args, **kwargs)

        messages.error(request, 'No tienes permiso para acceder a esta sección.')
        return redirect('lista_libros')

    return wrapper