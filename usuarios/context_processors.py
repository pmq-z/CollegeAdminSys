from .decorators import es_admin as _es_admin


def es_admin(request):
    """Inyecta `es_admin` en el contexto de todos los templates.

    Reemplaza el patrón repetido `{% if user.is_superuser or user.is_staff %}
    ... {% elif user.perfilusuario.rol == 'ADMIN' %}` que estaba copiado en
    varios templates con ligeras variaciones (y por eso propenso a errores).
    """
    return {'es_admin': _es_admin(request.user)}
