# Desarrollo y contribución

## Flujo de trabajo local

Para desarrollar, no hace falta levantar los 4 contenedores en cada cambio — es más lento que necesario. El flujo recomendado:

```bash
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt
export DJANGO_DEBUG=True
python manage.py migrate
python manage.py runserver
```

Esto usa SQLite y cache en memoria (ver [`docs/02-instalacion-y-despliegue.md`](02-instalacion-y-despliegue.md)) — suficiente para trabajar en la mayoría de los módulos. Solo levantar Podman completo cuando el cambio realmente involucra Postgres, Redis o Nginx específicamente (por ejemplo, una migración de datos grande, o un cambio en `nginx/default.conf`).

Antes de dar un cambio por terminado:

```bash
python manage.py check                        # detecta errores de configuración/modelos
python manage.py makemigrations --check --dry-run   # confirma que no faltan migraciones
```

## Convenciones del proyecto

### Nomenclatura

- Nombres de modelos, campos, vistas y URLs **en español** (`Alumno`, `matricula`, `alumno_list`) — es la convención ya establecida en todo el proyecto; no mezclar con inglés en código nuevo.
- Cada app sigue el patrón `<entidad>_list`, `<entidad>_create`, `<entidad>_update`, `<entidad>_deactivate` para operaciones CRUD. Un módulo nuevo debería seguir el mismo patrón salvo que haya una razón concreta para desviarse.

### Comentarios

Los comentarios explican **por qué**, no qué. El código ya dice qué hace; un comentario que solo repite eso es ruido.

```python
# Bien:
# Se usa una transacción para garantizar la consistencia entre ambas operaciones.
with transaction.atomic():
    ...

# Mal (no aporta nada que el código no diga):
# Incrementa la variable i.
i += 1
```

Comentarios en español (LATAM), concisos, solo donde la lógica, una decisión de arquitectura, un *workaround* o un supuesto no sean evidentes con solo leer el código.

### Autorización

Toda vista nueva que deba restringirse a administradores usa `usuarios.decorators.admin_required` — no reimplementar el chequeo de rol a mano. Para lectura pública con una acción puntual restringida (como `horarios.views.index`), usar `usuarios.decorators.es_admin(request.user)` directamente. Ver [`docs/03-autenticacion-y-permisos.md`](03-autenticacion-y-permisos.md).

### Acciones que cambian estado

Toda vista que borra, aprueba, rechaza o modifica un registro existente:
1. Se decora con `@require_POST` (además de la autorización que corresponda).
2. Se dispara desde un `<form method="post">` con `{% csrf_token %}` en la plantilla — nunca desde un `<a href>`.

### Validación de formularios

Las reglas de negocio que no son "tipo de dato" (fechas que no se traslapan, montos positivos, formato de RFC) viven en `clean()`/`clean_<campo>()` del formulario, no en la vista. La plantilla debe mostrar `{{ form.non_field_errors }}` y los errores de cada campo — un formulario nuevo que no los muestre es un bug de UX, no un detalle menor (ver el hallazgo correspondiente en `docs/09-estado-del-proyecto.md`).

### UI

Ninguna plantilla nueva define `<style>` propio ni carga un framework por CDN. Todo componente visual sale de `static/css/design-system.css` (ver [`docs/06-sistema-de-diseno.md`](06-sistema-de-diseno.md)). Si hace falta un componente que no existe todavía, se agrega ahí — no como una solución puntual en la plantilla que lo necesita.

## Cómo agregar un módulo nuevo

1. `python manage.py startapp <nombre>`.
2. Agregar a `INSTALLED_APPS` en `config/settings.py`.
3. Definir modelos, correr `makemigrations`/`migrate`.
4. Vistas siguiendo el patrón CRUD de la sección anterior, protegidas con `admin_required`/`login_required` según corresponda.
5. Templates que extiendan `{% extends 'base.html' %}` usando `{% block page_title %}` y `{% block content %}` — no crear un `base.html` propio del módulo.
6. Agregar el enlace correspondiente al menú lateral en `templates/base.html`.
7. Incluir las URLs del módulo en `config/urls.py`.

## Guía de contribución

Este proyecto no tiene todavía un histórico de convenciones de Git propias (ramas, mensajes de commit) que documentar como "ya establecidas" — lo siguiente es una recomendación razonable para adoptar de acá en adelante, no una regla que ya estuviera en uso:

- **Ramas:** `feature/<descripcion-corta>`, `fix/<descripcion-corta>`.
- **Commits:** mensaje en español, en modo imperativo ("Agrega validación de RFC", no "Agregando" ni "Agregué").
- **Antes de abrir un cambio:** correr `manage.py check` y `makemigrations --check --dry-run` (ver arriba).
- **Alcance:** un cambio hace una cosa. Si al revisar un `diff` aparecen dos temas sin relación, probablemente debería ser dos cambios separados.

## Lo que falta para un flujo de desarrollo maduro

Documentado con honestidad para quien continúe el proyecto:

- **No hay suite de tests automatizados.** Es la brecha más importante — ver recomendaciones detalladas en [`docs/09-estado-del-proyecto.md`](09-estado-del-proyecto.md).
- **No hay CI configurado** (GitHub Actions o equivalente) que corra `check`/tests automáticamente en cada cambio.
- **No hay linter/formateador configurado** (`ruff`, `black` o similar) — el estilo actual es consistente porque se mantuvo con cuidado manualmente, no porque una herramienta lo exija.
