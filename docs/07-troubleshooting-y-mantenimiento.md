# Troubleshooting y mantenimiento

*Todos los comandos de este documento usan `docker compose`; son idénticos con `podman compose` — solo cambia el nombre del binario.*

## Problemas comunes

### El contenedor `db` no arranca / se reinicia en bucle

**Síntoma:** `docker compose ps` muestra `db` reiniciándose o en estado *unhealthy*.

**Causa más común:** falta `POSTGRES_PASSWORD` en `.env`. El servicio está configurado para fallar rápido y explícito (`POSTGRES_PASSWORD: ${POSTGRES_PASSWORD:?Definí POSTGRES_PASSWORD en .env}`) en vez de arrancar con una contraseña vacía o por defecto.

```bash
docker compose logs db
```

### `web` se queda esperando y nunca migra

**Síntoma:** los logs de `web` repiten "Esperando a que la base de datos... acepte conexiones" indefinidamente.

**Causas posibles:**
1. `db` no pasó su healthcheck todavía — normal los primeros segundos, revisar con `docker compose ps`.
2. `POSTGRES_HOST`/`POSTGRES_DB`/`POSTGRES_USER` no coinciden entre `db` y `web` — en Compose, `web` recibe `POSTGRES_HOST=db` automáticamente (hostname = nombre del servicio), pero `POSTGRES_DB`/`POSTGRES_USER`/`POSTGRES_PASSWORD` deben ser **los mismos** en ambos servicios porque salen del mismo `.env`.

### `ImproperlyConfigured: DJANGO_SECRET_KEY es obligatoria`

Esto es intencional, no un bug: con `DJANGO_DEBUG=False`, la aplicación se niega a arrancar sin `DJANGO_SECRET_KEY` y `DJANGO_ALLOWED_HOSTS` definidas, en vez de correr insegura por accidente. Solución: completar `.env` (ver [`docs/02-instalacion-y-despliegue.md`](02-instalacion-y-despliegue.md)).

### El sitio carga sin ningún estilo (HTML plano)

**Causas posibles:**
1. `collectstatic` no corrió — revisar logs de `web`, debería decir "N static files copied".
2. El volumen `static_files` no está montado en `nginx` — revisar `docker-compose.yml`, el servicio `nginx` debe montar el mismo volumen que `web` en `/app/staticfiles`.
3. Corriendo con `manage.py runserver` local: verificar que `STATICFILES_DIRS`/`STATIC_ROOT` apunten donde se espera (`config/settings.py`).

### `/healthz/` devuelve `{"status": "error", "database": false}` (503)

La app está corriendo pero no puede hablar con la base de datos. Revisar:
```bash
docker compose logs db
docker compose exec web python manage.py dbshell   # si conecta, el problema es de la app, no de Postgres
```

### "No tenés permiso para acceder a esta sección" al hacer algo que debería poder

El usuario no tiene `rol='ADMIN'` en su `PerfilUsuario`, ni es `is_staff`/`is_superuser`. Verificar desde el shell:

```bash
docker compose exec web python manage.py shell
>>> from django.contrib.auth.models import User
>>> u = User.objects.get(username='...')
>>> u.perfilusuario.rol
>>> u.perfilusuario.rol = 'ADMIN'; u.perfilusuario.save()
```

### "El código de doble validación o la firma son incorrectos" al firmar un acta

Desde la auditoría de seguridad, el campo "PIN" de la firma digital exige la **contraseña real de la cuenta** del docente, no un texto arbitrario (ver [`docs/03-autenticacion-y-permisos.md`](03-autenticacion-y-permisos.md)). Si el docente olvidó su contraseña, no hay atajo — debe recuperarla como cualquier otro login.

### Página "Formulario expirado" / error CSRF

Aparece cuando un formulario quedó abierto en el navegador más tiempo del que dura la sesión, o si las cookies se bloquearon. Solución para quien lo reporta: volver a iniciar sesión y reintentar. No es un bug de la aplicación en sí — es el comportamiento esperado de la protección CSRF.

## Ver logs

```bash
docker compose logs -f web        # solo la app
docker compose logs -f            # todos los servicios
docker compose logs --tail 100 nginx
```

Django registra a `stdout` (no a archivos) a propósito: en contenedores, el runtime (Podman/journald) ya se encarga de recolectar y rotar logs — ver `LOGGING` en `config/settings.py`.

## Tareas de mantenimiento

### Respaldar la base de datos

```bash
docker compose exec db pg_dump -U sistema_escolar sistema_escolar > respaldo_$(date +%Y%m%d).sql
```

### Restaurar un respaldo

```bash
cat respaldo_20260101.sql | docker compose exec -T db psql -U sistema_escolar sistema_escolar
```

### Rotar `DJANGO_SECRET_KEY`

Cambiar el valor invalida **todas** las sesiones activas (todo el mundo tiene que volver a iniciar sesión) pero no afecta los datos. Generar una nueva:

```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```
Actualizar `.env` y reiniciar `web`: `docker compose up -d --force-recreate web`.

### Limpiar sesiones expiradas

Con `SESSION_ENGINE = cached_db`, la tabla `django_session` acumula filas de sesiones vencidas si nadie las limpia:

```bash
docker compose exec web python manage.py clearsessions
```

Recomendado como tarea periódica (cron semanal) en un despliegue real — no está automatizado todavía.

### Actualizar dependencias

```bash
pip list --outdated                         # dentro del venv o del contenedor
# actualizar requirements.txt manualmente, respetando los rangos de versión
docker compose build web
docker compose up -d web
```

Revisar el *changelog* de Django antes de saltar de versión menor (5.2 → 5.3, etc.), especialmente por cambios en `MIDDLEWARE` o `SECURE_*`.

### Reconstruir todo desde cero (perder datos, solo para desarrollo)

```bash
docker compose down -v   # el -v borra los volúmenes: postgres_data, redis_data, static_files
docker compose up --build
```
