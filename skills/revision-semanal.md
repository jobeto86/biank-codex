---
name: revision-semanal
description: "Auto-auditoria semanal de Biank: archiva pendientes cerrados, revisa salud del backlog (stale, vencidos), detecta trabajo REPETITIVO en las sesiones de la semana y propone al admin convertirlo en una habilidad nueva. Triggers: 'revision semanal', 'auditate', 'revisa tu semana', 'que aprendiste esta semana', o proactivamente al arrancar si han pasado 7+ dias desde la ultima revision (fecha en memory/context.md)."
---

# Skill: Revisión Semanal (auto-auditoría)

**Trigger**: "revisión semanal", "audítate", "revisa tu semana", "¿qué aprendiste
esta semana?" — **o proactivamente**: al arrancar sesión, si la fecha de "Última
revisión semanal" en `memory/context.md` tiene **7 días o más** (o no existe),
ofrécela: *"Ya pasó una semana desde mi última revisión — ¿la corremos? Toma 2
minutos y me ayuda a trabajar mejor para ustedes."* Si el usuario dice que no,
no insistas — reofrece en la siguiente sesión.

> Es tu ritual de mantenimiento y aprendizaje. No requiere admin para correr,
> pero **proponer habilidades nuevas sí se aprueba con el admin** (§4 de identidad).

---

## Qué hace (4 pasos, en orden)

### 1. Archivar lo cerrado

Filas del backlog con **más de 7 días en hecho ✅** → muévelas a
`memory/backlog_archivo.md` con la fecha de cierre. Reporta: *"Archivé N
pendientes cerrados."*

### 2. Salud del backlog

- **Vencidos**: filas con "Seguir el" en el pasado y aún abiertas → tráelas:
  *"Estos 3 seguimientos ya se pasaron de fecha — ¿los movemos o ya se resolvieron?"*
- **Estancados**: filas en **esperando** sin movimiento en 14+ días → pregunta
  si siguen vivas o hay que escalar.
- **Sin fecha**: pendientes sin "Seguir el" → propón una fecha.

### 3. Cazar trabajo repetitivo (el paso de oro)

Lee las sesiones de la semana (`memory/sessions/` de los últimos 7 días) y busca
**patrones que se repitieron 3+ veces**:

- La misma secuencia de consultas/operaciones (ej. "cada lunes piden ventas de
  la semana + cartera vencida + saldo de caja" → eso es un *reporte de lunes*).
- El mismo tipo de captura manual (ej. "3 veces esta semana subieron recibos y
  pidieron extraer datos con los mismos campos").
- La misma pregunta que requirió los mismos 4 pasos para responderse.

Por cada patrón encontrado, **propón convertirlo en habilidad**:

> *"Noté que esta semana me pidieron 3 veces [X, con los mismos pasos]. ¿Quieren
> que lo aprenda como flujo fijo? Así solo dirían '[frase corta]' y lo hago
> completo de una."*

- Si el usuario acepta y es **admin** → documenta el flujo en `protocols/`
  siguiendo `protocols/crear-flujo.md`.
- Si es **operador** → anota la propuesta en el backlog (fila "proponer
  habilidad [X] al admin") y menciónala cuando el admin esté en sesión.

### 4. Registrar y fechar

- Insights de la semana que aún no estén en `memory/context.md` → agrégalos (§9).
- Actualiza en `memory/context.md` la línea: `Última revisión semanal: YYYY-MM-DD`
  (créala en "Notas operativas" si no existe).
- Resumen final al usuario en 3-5 líneas: qué archivaste, qué está vencido,
  qué propusiste aprender.

## Reglas

- **Máximo 5 minutos** de interacción — es mantenimiento, no ceremonia.
- No propongas habilidades por cosas que pasaron **una sola vez** — el umbral
  es repetición real (3+). Una herramienta que nadie pidió es ruido.
- El paso 3 es **propuesta, no ejecución**: crear el protocolo requiere
  aprobación del admin, siempre.
- Todo en lenguaje de negocio: "pendientes", "seguimientos", "flujos" — nunca
  "backlog", "skill" ni "auditoría" frente al usuario.
