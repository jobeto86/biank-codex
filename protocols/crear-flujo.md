---
name: Crear Flujo de Trabajo Nuevo
trigger: "quiero que aprendas a...", "crea un flujo para...", "necesito que hagas [proceso] automáticamente"
requires: [descripción del proceso por parte del usuario]
output: protocolo nuevo en protocols/ (aprobado) o borrador _borrador_[slug].md + fila pendiente en memory/backlog.md (operador)
---

# Protocolo: Crear Flujo de Trabajo Nuevo

## Objetivo

Documentar un proceso recurrente del usuario como protocolo ejecutable,
para que Biank lo repita de forma consistente en sesiones futuras.

## Pasos

### 1. Entrevistar al usuario

Preguntar lo mínimo para entender el flujo:
- ¿Qué dispara el proceso? (frase, evento, día de la semana)
- ¿Cuáles son los pasos, en orden?
- ¿Qué datos necesita cada paso?
- ¿Hay algún paso que requiera confirmación antes de ejecutar?
- ¿Cómo se ve el resultado final esperado?

Si el flujo toca dinero u operaciones irreversibles → el paso de confirmación
es **obligatorio**, no opcional.

### 2. Verificar contra manuales de la empresa

Revisar `manuales/` — si existe un manual que norme este proceso,
el flujo nuevo debe respetarlo. Si lo contradice, avisar al usuario.

### 3. Redactar el protocolo

Usar el mismo formato de los protocolos existentes en `protocols/` (frontmatter `name`/`description` + Objetivo + Pasos + reglas de la empresa citando su manual si existe).

### 4. Validar con el usuario

Mostrar el protocolo redactado y preguntar:
*"¿Así queda el flujo? ¿Falta o sobra algún paso?"*

Ajustar hasta que el usuario apruebe.

### 5. Guardar según el rol

- **admin** → guardar en `protocols/`, agregar fila a `protocols/INDEX_local.md`
  (crearlo si no existe — ⚠️ NO en `skills/INDEX.md`: ese archivo lo sobreescribe el auto-update
  en cada versión y el registro del cliente se perdería), confirmar: *"✅ Listo, ya sé hacer [flujo]. Pídemelo cuando quieras."*
- **operador** → guardar el borrador en `protocols/_borrador_[slug].md` (el prefijo
  `_borrador_` indica que NO está activo — no ejecutarlo hasta que un admin lo apruebe
  renombrándolo) + agregar fila **pendiente** en `memory/backlog.md`
  ("Aprobar flujo [slug]", Quién: admin), y avisar:
  *"Quedó documentado — necesito que un admin lo apruebe para activarlo."*

### 6. Primera ejecución supervisada

La primera vez que se ejecute el flujo nuevo, ir paso a paso confirmando
con el usuario. A partir de la segunda, ejecutar normal.
