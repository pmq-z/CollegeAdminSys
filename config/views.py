from django.contrib.auth.decorators import login_required
from django.db import connection
from django.http import JsonResponse
from django.shortcuts import render


def csrf_failure(request, reason=""):
    """Reemplaza la página de error CSRF por defecto de Django (HTML propio,
    sin relación visual con el resto del sitio) por una consistente con el
    sistema de diseño. El caso más común es un formulario abierto por mucho
    tiempo cuya sesión ya expiró.
    """
    return render(request, '403_csrf.html', {'reason': reason}, status=403)


def healthcheck(request):
    """Verifica que la app responde y que puede hablar con la base de datos.

    Sin autenticación a propósito: lo consultan Podman/el balanceador, no personas.
    """
    try:
        connection.ensure_connection()
        db_ok = True
    except Exception:
        db_ok = False

    status = 200 if db_ok else 503
    return JsonResponse({'status': 'ok' if db_ok else 'error', 'database': db_ok}, status=status)


@login_required
def home(request):
    modulos = [
        {
            'nombre': 'Alumnos y Maestros',
            'descripcion': 'Altas, bajas y edición de alumnos, maestros, materias e inscripciones.',
            'url': 'dashboard',
        },
        {
            'nombre': 'Calificaciones',
            'descripcion': 'Captura de calificaciones, firma digital de actas y reporte en PDF.',
            'url': 'calificaciones_dashboard',
        },
        {
            'nombre': 'Horarios',
            'descripcion': 'Registro y edición de horarios de clase.',
            'url': 'horarios_index',
        },
        {
            'nombre': 'Empresas',
            'descripcion': 'Registro de empresas vinculadas a la escuela.',
            'url': 'empresa_list',
        },
        {
            'nombre': 'Billetera',
            'descripcion': 'Movimientos de ingresos y egresos con saldo acumulado.',
            'url': 'billetera_list',
        },
        {
            'nombre': 'Biblioteca',
            'descripcion': 'Administración de libros, ejemplares, solicitudes y préstamos.',
            'url': 'lista_libros',
        },
    ]

    return render(request, 'home.html', {'modulos': modulos})