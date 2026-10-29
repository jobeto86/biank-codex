---
name: gestion-manuales
description: "Redactar, estructurar, validar y guardar manuales operativos y politicas internas de la empresa en manuales/ bajo el estandar OKF. Triggers: 'crea el manual de...', 'documenta nuestra politica de...', 'carga este manual', 'como manejamos las devoluciones' (cuando no existe manual aun)."
---

# Skill: Gestión y Carga de Manuales de Empresa (Estándar OKF)

> **Propósito**: Guía a Biank para redactar, estructurar, validar y guardar manuales operativos y políticas internas de la empresa en `manuales/` bajo la especificación **Open Knowledge Format (OKF)**.
> **Autoridad**: Requiere rol **admin** para guardar el archivo definitivo.

---

## 1. Triggers conversacionales

- "Ayúdame a crear el manual de X"
- "Quiero guardar la política de Y"
- "Redacta el proceso de Z para mi empresa"
- "Agrega un manual a mi empresa"

---

## 2. Flujo de Trabajo (Paso a Paso)

```mermaid
graph TD
    A[Usuario solicita crear/editar manual] --> B{¿Es Admin?}
    B -- No --> C[Registrar sugerencia en memory/backlog.md y avisar]
    B -- Sí --> D[Entrevistar y estructurar información]
    D --> E[Formatear en Markdown OKF con Frontmatter]
    E --> F[Mostrar borrador al Admin para aprobación]
    F -- Aprobado --> G[Guardar en manuales/slug-manual.md]
    G --> H[Ejecutar scripts/validate_okf.py]
```

### Paso 1: Verificación de Rol
1. Consultar `config/users.md` (si no existe, pregunta al usuario su rol, créalo con esa respuesta y sigue) para verificar si el usuario es `admin`.
2. Si es `operador`:
   - Decir con amabilidad: *"Solo un administrador puede autorizar nuevos manuales. Guardaré tu propuesta en mi lista de pendientes para que un admin la revise."*
   - Registrar la propuesta en `memory/backlog.md`.

### Paso 2: Entrevista y Estructuración de Información
Si es `admin`, guiar la conversación preguntando:
1. **Título del manual o política.**
2. **Sinónimos o términos alternativos** con los que el equipo llamará a este tema (`aliases`).
3. **Reglas de negocio concretas** (montos, días, condiciones, responsables).
4. **Excepciones permitidas.**

### Paso 3: Formateo en Estándar OKF
Generar el contenido Markdown aplicando estrictamente la cabecera YAML Frontmatter OKF:

```markdown
---
id: manual_<slug_kebab_case>
type: manual
domain: work
aliases: [<lista_de_sinonimos_separados_por_coma>]
tags: [<tags_relevantes>]
last_updated: YYYY-MM-DD
status: active
related: []                     # IDs OKF relacionados; vacío es válido
---

# <Título del Manual>

> <Resumen de 1-2 oraciones sobre el propósito del manual>

## 1. Reglas Operativas
- ...

## 2. Condiciones y Límites
- ...
```

### Paso 4: Confirmación y Guardado
1. Mostrar el borrador formateado al admin.
2. Tras la aprobación explícita, guardar en `manuales/<slug_kebab_case>.md`.
3. Ejecutar la validación OKF:
   ```bash
   python scripts/validate_okf.py
   ```
4. Confirmar con entusiasmo Biank:
   ```
      ╭───────────╮
      │  ^   ^   │
      │     ◡     │
      ╰───────────╯
         B I A N K
   ```
   *"¡Listo jefe! El manual de <Nombre> quedó guardado con el estándar OKF en `manuales/<archivo>.md`. Desde ahora lo consultaré automáticamente antes de cualquier proceso relacionado."*
