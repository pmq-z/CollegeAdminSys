# Sistema de diseño

## Historial de versiones

| Versión | Dirección visual | Estado |
|---|---|---|
| v1 | Oscura, brutalista industrial, inspirada en *Marathon* (Bungie, 1994) | Reemplazada |
| v2 | Clara, minimalista-brutalista, inspirada en la tecnología Tau (Warhammer 40.000) | **Actual** |

Este documento describe la v2. Se conserva la sección histórica al final para quien necesite el contexto de por qué cambió.

## Punto de partida (previo a la v1)

Antes de cualquier rediseño, el proyecto tenía **cinco sistemas visuales desconectados** funcionando en paralelo: la plantilla raíz, un shell propio de `alumnos_maestros`, un shell propio de `calificaciones` (tema claro, tipo SaaS genérico), y varias páginas (`horarios`, `empresas`, `billetera`) sin plantilla compartida, cada una cargando su propio Bootstrap desde un CDN distinto. La v1 unificó todo eso en un sistema de tokens único; la v2 cambia la paleta y la geometría de ese mismo sistema unificado, sin volver a fragmentarlo.

## Dirección visual v2: minimalista-brutalista, inspirada en Tau

Por pedido explícito: modo claro, minimalista pero con formas brutalistas, con estética de la facción Tau de Warhammer 40.000. La traducción de esos tres pedidos a decisiones concretas:

- **Claro**: fondo hueso cálido (no blanco puro — evoca la cerámite de la armadura Tau), paneles en blanco casi puro por encima de ese fondo.
- **Brutalista**: los bordes siguen siendo gruesos y de alto contraste, sin esquinas redondeadas, sin sombras difuminadas — los mismos principios de geometría dura de la v1, solo que ahora en paleta clara en vez de oscura.
- **Minimalista**: menos peso tipográfico que la v1 (700 en vez de 800), sombras duras reservadas para estados de interacción puntuales en vez de aplicarse por todos lados, más aire entre elementos.
- **Tau**: paleta de dos acentos — azul de energía (`--tau-blue`) y naranja de marca de casta (`--tau-orange`) — y un motivo de firma hexagonal (la geometría más asociada a la tecnología Tau) que reemplaza los corchetes tipo HUD de la v1.

No se reproduce ningún asset con derechos de autor de Warhammer 40.000 — se toman prestados principios de paleta y geometría (colores tierra + azul, hexágonos), no imágenes, logotipos ni marcas registradas.

## Tokens

### Color

| Token | Valor | Uso |
|---|---|---|
| `--bone` | `#f2efe6` | Fondo base de página |
| `--paper` | `#fbfaf7` | Superficie de tarjetas/paneles |
| `--line` | `#17181a` | Bordes, texto principal |
| `--ink-dim` | `#5b5d5a` | Texto secundario |
| `--ink-faint` | `#8b8d82` | Texto terciario / placeholders |
| `--tau-blue` | `#1d7fa6` | Acento primario — energía/armadura |
| `--tau-orange` | `#c85a1e` | Acento secundario — marca de casta |
| `--danger` / `--success` / `--warn` | `#ac2b21` / `#3f7d5c` / `#a97614` | Estados funcionales |

Dos acentos restringidos (igual que en la v1), solo que recoloreados: `--tau-blue` para acción primaria y foco, `--tau-orange` para acción secundaria — nunca decorativos sin motivo.

### Tipografía

Sin fuentes externas — mismo motivo que en la v1: rendimiento y cero dependencia de CDN. Encabezados en mayúsculas con tracking (`0.045em`, más contenido que el `0.06-0.08em` de la v1: parte del ajuste "minimalista"). El cuerpo de texto se mantiene en case normal y sin tratamiento — la excepción textual del brief se mantiene igual que antes. Los datos e identificadores siguen en la pila monoespaciada.

### Geometría

- **Cero `border-radius`** en toda la UI rectangular. Igual que en la v1, la única excepción son los indicadores circulares de estado (funcionalmente redondos, no una elección decorativa).
- **El hexágono como única forma no rectangular permitida**: es geométrico y técnico, no orgánico — coherente con "brutalista" aunque no sea un ángulo recto. Se usa en el ícono de marca (contenedor completo) y como acento de esquina en `.panel-bracket` (un pequeño marcador, no la tarjeta entera — el contenido sigue siendo un rectángulo legible).
- **Sombras duras** (`box-shadow` sin blur) reservadas para hover de tarjetas de módulo y estados activos — con más moderación que en la v1, coherente con "minimalista".

## Estructura y componentes

Sin cambios respecto a la v1: mismo shell único (`templates/base.html`), mismos nombres de clase (`.btn`, `.card`, `.badge`, `.table-wrap`, `.form-group`, etc.). El cambio es enteramente de tokens — colores, geometría del motivo de firma — no de estructura. Esto fue posible porque la v1 ya centralizaba todo en variables CSS sin colores hardcodeados en las plantillas; reemplazar `design-system.css` bastó para re-temizar casi todo el sitio automáticamente.

**Una excepción real que sí hubo que corregir a mano**: el canvas de firma manuscrita en `calificaciones/digital_signature.html` tomaba el color del trazo de `getComputedStyle(...).getPropertyValue('--bone')` — en la v1 esa variable era el texto claro (visible sobre fondo oscuro); en la v2 pasó a ser el fondo claro de página, por lo que el trazo hubiera quedado casi invisible sobre el canvas (también claro). Se corrigió para usar `--ink` (el color de tinta/texto oscuro de la v2).

## Migración de nombres de variables

Varias plantillas referenciaban variables de la v1 directamente en `style=""` inline (no solo a través de clases). Se migraron sistemáticamente:

| v1 | v2 |
|---|---|
| `--void` | `--bone` |
| `--void-raised` / `--panel-raised` | `--paper-raised` |
| `--steel` | `--line` |
| `--steel-dim` | `--line-soft` |
| `--bone-dim` (texto) | `--ink-dim` |
| `--bone-faint` (texto) | `--ink-faint` |
| `--signal` | `--tau-blue` |
| `--cyan` | `--tau-blue` |

## Qué se dejó pendiente

- Pulido de detalle fino en `calificaciones` (la vista previa de documento en la firma digital sigue con tonos crema hardcodeados, pensados para contrastar contra un fondo oscuro — hoy contrastan menos al ser toda la página clara, pero siguen leyéndose bien como "papel").
- Nuevas capturas/mockups reales con la paleta v2 para reemplazar cualquier documentación visual que aún muestre la v1.

---

## Apéndice histórico: dirección v1 (Marathon, oscura)

Se conserva por trazabilidad. La v1 usaba fondo casi negro (`--void: #0a0b0d`), texto blanco cálido (`--bone: #eae6da`), acento ámbar (`--signal: #ff6a1f`) y cian (`--cyan: #22d3c9`), con un motivo de firma de corchetes tipo HUD en las esquinas de paneles clave. La lógica de diseño (brutalismo, un solo archivo de tokens, sin CDN externos, accesibilidad por contraste) es la misma que hereda la v2 — lo que cambió es la paleta, el peso tipográfico y el motivo de firma.
