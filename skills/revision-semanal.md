---
name: revision-semanal
description: "Revisión semanal de pendientes: archiva cerrados, revisa vencidos y estancados, y propone flujos repetitivos con evidencia del backlog y fuentes autorizadas. Triggers: 'revision semanal', 'auditate', 'revisa tu semana', 'que aprendiste esta semana', o al arrancar si hay backlog y pasaron 7+ dias desde la revisión registrada en él."
---

# Skill: Revisión semanal

**Trigger**: "revisión semanal", "audítate", "revisa tu semana", "¿qué aprendiste
esta semana?". Al arrancar, si existe `memory/backlog.md` y su última revisión tiene
7+ días, o no tiene fecha, ofrece una vez revisarlo. Si el usuario declina, no
insistas. No necesita crear contexto, leer sesiones ni cerrar una conversación.

## Qué hacer

### 1. Archivar tareas cerradas

Filas con más de 7 días en **hecho ✅**, acreditados por su fecha de cierre →
muévelas a `memory/backlog_archivo.md`, preservando identificador, responsable,
decisiones y referencias de evidencia. Verifica que quedaron completas antes de
retirarlas del backlog activo; evita duplicar identificadores ya archivados.
No inventes fechas: si no se conoce la fecha de cierre, conserva la fila.
No elimines tareas abiertas, históricos, comprobantes ni archivos de sesiones.

### 2. Revisar pendientes

- **Vencidos:** seguimiento en el pasado y tarea aún abierta → presenta el siguiente
  paso y propone una nueva fecha o pregunta por el resultado; no cierres por intención.
- **Estancados:** esperando sin movimiento comprobado en 14+ días → pregunta si hay
  respuesta o hace falta escalar. Sin fecha de movimiento, no inventes la antigüedad.
- **Incompletos:** falta responsable, próximo paso o fecha → propone completarlos.
- **Duplicados:** conserva la tarea canónica y sus antecedentes; no borres filas
  dudosas ni mezcles tareas distintas sin aclarar su relación.

Una confirmación precisa del usuario puede cerrar el seguimiento y queda citada
como tal. No demuestra que una operación haya sido registrada en el ERP.

### 3. Proponer mejoras con evidencia

Revisa las tareas pertinentes y sus referencias autorizadas. Consulta sólo los
antecedentes necesarios para la pregunta; no recorras `memory/sessions/` ni el
historial completo para alimentar esta revisión. Si hay evidencia de un mismo
flujo repetido 3+ veces, propón documentarlo; no deduzcas repeticiones que no puedas
comprobar ni crees una bitácora para conseguirlas.

Crear un protocolo requiere aprobación del admin y seguir `protocols/crear-flujo.md`.
Si lo pide un operador, registra la propuesta en la tarea correspondiente para el
admin. No acumules hipótesis o insights automáticos en `memory/context.md`.

### 4. Guardar lo útil

Actualiza las tareas afectadas sin crear otra tarea por haber revisado el backlog.
Registra **Última revisión semanal: YYYY-MM-DD** en una única línea de metadatos del
propio `memory/backlog.md`; sustituye la anterior, no agregues un historial de revisiones.
La documentación local de esta revisión autorizada no pide otra confirmación; los
cambios de negocio y protocolos conservan sus propias confirmaciones.

Entrega un resumen de 3–5 líneas: qué se archivó, qué sigue pendiente y qué mejora
se propuso. No generes un resumen de sesión aparte ni dependas de una despedida.

## Límites

- No más de 5 minutos de interacción ni propuestas por una ocurrencia aislada.
- Memoria breve sólo para preferencias o hechos duraderos confirmados, bajo las
  reglas de `identity/BIANK.md` §8; no se modifica por rutina semanal.
- La revisión ocurre durante esta conversación. No promete avisos de fondo sin
  una programación autorizada y confirmada.
- Habla de pendientes, seguimientos y flujos, sin jerga interna de archivos.
