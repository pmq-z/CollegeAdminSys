# Estado del proyecto

Este documento resume el trabajo hecho durante el proceso de auditoría y modernización, y — con la misma honestidad con la que se documentó cada hallazgo en su momento — qué queda pendiente. El objetivo es que quien retome el proyecto no tenga que redescubrir nada de esto por su cuenta.

## Resumen de arquitectura final

Ver [`docs/01-arquitectura.md`](01-arquitectura.md) para el detalle completo. En una línea: monolito modular de Django (8 apps), PostgreSQL + Redis + Nginx en contenedores Podman separados por red, sistema de diseño propio inspirado en *Marathon*, y documentación completa en español.

## Mejoras implementadas

### Build e infraestructura
- El proyecto **no compilaba**: no existía `requirements.txt` pese a que el `Dockerfile` lo requería. Se creó con versiones fijadas.
- Se migró de SQLite (bind-mount a un solo archivo) a **PostgreSQL** en contenedor separado, con SQLite como *fallback* automático para desarrollo sin contenedores.
- Se agregó **Redis** para cache y sesiones (`cached_db`: la base de datos sigue siendo la fuente de verdad).
- Se construyó la arquitectura de **4 contenedores con Nginx** como único punto de entrada, con `db`/`redis` aislados en una red privada sin puertos publicados.
- Se agregaron *healthchecks* a los 4 servicios y arranque ordenado (`depends_on: condition: service_healthy` + espera activa de respaldo en `docker-entrypoint.sh`).
- Se creó `.dockerignore` (no existía).
- La imagen ahora corre como usuario sin privilegios (antes corría como root).

### Seguridad
- `DEBUG` pasó de `True` a `False` por defecto; `SECRET_KEY`/`ALLOWED_HOSTS` ahora son obligatorias fuera de desarrollo (la app se niega a arrancar insegura en vez de hacerlo en silencio).
- **Cuatro apps completas (`alumnos_maestros`, `horarios`, `empresas`, `billetera`) no tenían ningún control de acceso** — cualquier persona sin sesión podía ver y modificar alumnos, maestros, horarios, empresas y movimientos financieros. Se corrigió con `@login_required`/`@admin_required` de forma consistente.
- Varias acciones destructivas (eliminar horario, aprobar/rechazar solicitud, registrar devolución) se disparaban con un simple `GET` — vulnerables a CSRF vía un enlace. Se convirtieron a `POST` con `@require_POST`.
- La "firma digital" de actas de calificaciones no validaba el PIN contra nada real (cualquier texto no vacío "firmaba"); ahora valida contra la contraseña real de la cuenta.
- Se corrigieron condiciones de carrera en la aprobación de préstamos (`transaction.atomic()` + `select_for_update()`) que permitían prestar el mismo ejemplar dos veces si dos aprobaciones ocurrían al mismo tiempo.
- Se agregaron guardas de estado para evitar reprocesar una solicitud ya aprobada/rechazada, o un préstamo ya devuelto.
- `grade_entry` asignaba datos de `request.POST` directo a un campo del modelo sin pasar por sus validadores — una calificación fuera de rango (o no numérica) se guardaba sin control. Ahora valida antes de guardar.
- Se agregó validación de formato de RFC, de montos positivos en `billetera`, de traslapes de horario, y de unicidad de correo en el registro de usuarios.

### UI/UX
- Se unificaron **cinco sistemas visuales desconectados** en un único shell y una única hoja de estilos, inspirados en el brutalismo industrial de *Marathon*.
- Se eliminaron todas las dependencias de CDN externas (Bootstrap, Bootstrap Icons, Material Symbols, Google Fonts).
- Se agregó navegación completa a los 8 módulos desde cualquier pantalla (antes no existía).
- Páginas de error (404/500/403/CSRF) propias, consistentes con el resto del sitio.
- Estados vacíos con contexto y acción, tablas responsivas, retroalimentación de "procesando" en envíos de formulario.

### Código
- Se eliminó código muerto: `usuarios.views.iniciar_sesion`/`cerrar_sesion` (nunca enrutadas), `calificaciones/forms.py` (referenciaba un modelo ya eliminado), `calificaciones/index.html` y `user_management.html` (mockup no funcional, nunca conectado a ninguna vista).
- Se centralizó la lógica de autorización (`es_admin`) que antes estaba duplicada entre un decorador y varios templates.
- Se corrigió un canvas de firma que aparentaba ser interactivo pero no tenía ningún JavaScript conectado.

## Deuda técnica pendiente

Ordenada de mayor a menor impacto:

1. **No hay suite de tests automatizados.** Todo lo corregido en este proceso se verificó manualmente (con Django `check`, el *test client*, y conexiones reales a Postgres/Redis en el entorno de trabajo) pero no queda como una regresión reproducible. Es, con diferencia, la brecha más importante para la salud a largo plazo del proyecto.
2. **`calificaciones` no reutiliza `Maestro`/`Alumno` de `alumnos_maestros`** — usa `User` directo, generando dos nociones distintas de "profesor"/"estudiante" en el mismo sistema (ver `docs/01-arquitectura.md`). Unificarlo requiere una migración de datos que decida cómo mapear los `User` existentes a fichas de `Maestro`/`Alumno`.
3. **`horarios`, `empresas` y `billetera` siguen siendo islas de datos** sin relación con el resto del esquema. Funcionalmente correcto hoy, pero limita reportes cruzados (por ejemplo, "horario de la materia X").
4. **`firmar-documentos/core` sigue sin integrarse** al proyecto (no está en `INSTALLED_APPS` ni en `config/urls.py`). Queda pendiente decidir si se fusiona con `calificaciones` (que ya genera actas en PDF) o se retira del repositorio.
5. **CRUD incompleto en `empresas` y `billetera`**: solo tienen alta y listado, no edición ni baja.
6. **`PerfilUsuarioForm` existe pero no está conectado a ninguna vista** — `perfil_usuario` es de solo lectura hoy; el formulario ya escrito permitiría autoedición de teléfono/dirección con poco esfuerzo.
7. **El código de doble validación de la firma digital solo se imprime a consola** — no hay integración real con un proveedor de email/SMS.
8. **Sin protección contra fuerza bruta en el login** (no hay *rate limiting* ni bloqueo tras intentos fallidos).
9. **Sin flujo de recuperación de contraseña** (requiere backend de email configurado, fuera del alcance de este pase).
10. **Sin paginación en ningún listado** — no es un problema al volumen actual de datos, pero cualquier tabla que crezca sin límite eventualmente necesitará `Paginator`.
11. **Redis sin contraseña propia** — protegido únicamente por aislamiento de red (`red_privada`), no por autenticación en la capa de aplicación.
12. **Sin CI/CD ni linter configurado.**

## Recomendaciones para desarrollo futuro

En orden sugerido de prioridad:

1. **Escribir una suite de tests**, empezando por los flujos más sensibles ya identificados en esta auditoría: autorización por rol, validación de formularios, y el flujo de aprobación de préstamos (la parte con lógica de concurrencia). Django's `TestCase` + el *test client* son suficientes; no hace falta introducir un framework adicional.
2. **Decidir el destino de `firmar-documentos/core`** antes de que crezca más deuda alrededor de dos sistemas de firma paralelos.
3. **Planificar la migración de datos** para unificar `calificaciones` con `alumnos_maestros` si el negocio realmente necesita que ambos módulos hablen de las mismas personas.
4. **Agregar `django-axes` o equivalente** para *rate limiting* de login, antes de exponer el sitio a Internet público sin restricciones de red.
5. **Configurar un proveedor de email transaccional** (SMTP/API) — desbloquea recuperación de contraseña y la entrega real del código de firma digital en un solo cambio de infraestructura.
6. **Agregar paginación** a los listados de `alumnos_maestros`, `libros` y `prestamos` en cuanto el volumen de datos lo justifique — el patrón ya es consistente entre módulos, así que aplicarlo a todos a la vez es sencillo.
7. **CI mínimo viable:** un solo workflow que corra `manage.py check` y `makemigrations --check --dry-run` en cada cambio ya atraparía la mayoría de los errores de configuración antes de que lleguen a producción.
8. **Considerar Docker secrets o `podman secret`** en vez de `.env` plano si el despliegue crece a más de un host o el nivel de exigencia de seguridad lo amerita.

## Sobre el proceso mismo

Cada fase de este trabajo (auditoría, seguridad, UI/UX, DevOps, diagramas, esta documentación) se verificó ejecutando el proyecto de verdad — no solo revisando el código: migraciones reales contra PostgreSQL, cache real contra Redis, Nginx real haciendo *proxy* a Gunicorn, renderizado real de cada plantilla tocada, y una batería de pruebas contra el *test client* de Django repetida después de cada cambio significativo para confirmar que nada de lo corregido en una fase se rompiera en la siguiente.
