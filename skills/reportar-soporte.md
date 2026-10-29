---
name: reportar-soporte
description: "Reportar al equipo de soporte una falla o error del SISTEMA (el ERP calcula mal, no deja hacer algo, da error), o dejarle una tarea formal a un compañero dentro del sistema. También se activa POR MÍ MISMA cuando, operando el sistema, detecto un fallo o un hueco (algo que el usuario necesita y el ERP no ofrece) y le ofrezco levantar el reporte. Levanta el reporte en el ERP con crearTicket. Triggers: 'esto está mal', 'el sistema no me deja', 'da error', 'repórtalo a soporte', 'avísale al equipo técnico', 'asígnale una tarea a [persona]' — y disparo interno: una tool del sistema me devuelve error, un dato/cálculo no cuadra, o el usuario me pide algo que el sistema no sabe hacer."
---

# Skill: Reportar a Soporte

**Trigger**: "esto está mal", "el sistema no calcula bien", "no me deja timbrar/guardar",
"me da un error", "repórtalo a soporte", "avísale al equipo que hace el sistema",
"pásale esto a los técnicos" — y para tareas: "asígnale una tarea a [compañero]",
"dile a [compañero] que…" (dentro del sistema).

---

## Qué hace

Levanta un reporte formal en el ERP para el **equipo de soporte técnico** (los que
construyen y mantienen el sistema). Dos usos:

1. **Falla del sistema** — algo del ERP no funciona como debe: un cálculo equivocado,
   un botón que no responde, un error al timbrar/guardar, una pantalla que se traba.
2. **Tarea para un compañero** — dejarle una tarea formal a otra persona de la empresa
   que también usa el sistema (queda registrada y él la ve en su sesión).

> **Esto NO es lo mismo que "algo no jala conmigo".** Si el problema es que **yo** no me
> conecto, mis datos no cargan o mis herramientas dan error de conexión → esa es la skill
> **`diagnostico`** / **`conectar-cbsuite`** (es MI instalación, no el sistema). Esta skill
> es para cuando **el ERP** (ventas, inventario, nómina, facturación, cobranza) tiene un
> comportamiento equivocado. En la duda: ¿fallo yo, o falla el dato/cálculo del sistema?

---

## Alcance (importante)

- Reporto y doy seguimiento a los reportes **de esta empresa** — los que se levantan aquí.
- El equipo de soporte los recibe y los resuelve. **Yo no veo reportes de otras empresas
  ni administro la cola global** — eso es del equipo técnico, no mío. Yo levanto y sigo
  lo mío, nada más.

---

## Detección proactiva (yo la propongo, sin que me lo pidan)

No siempre espero a que el usuario diga "esto está mal". Cuando **operando el sistema
por mi cuenta** me topo con un problema, **lo ofrezco** — nunca levanto el reporte en
silencio, siempre pregunto primero.

**Cuándo lo ofrezco** (solo ante algo claro, no ante cualquier fricción menor):

1. **Fallo del sistema** — una herramienta del ERP me devuelve un error del *sistema*
   (no de mi conexión), o me trae un dato/cálculo que claramente no cuadra: un saldo
   imposible, un total que no suma, una factura que no coincide con sus renglones.
2. **Hueco del sistema** — el usuario me pide algo razonable que el ERP **no sabe hacer
   todavía**: una operación que no está soportada, un reporte que no existe, una
   capacidad que falta.

> **Regla de oro: ante la duda, no molesto.** Solo ofrezco cuando el fallo o el hueco es
> inequívoco. Prefiero callar a llenar la cola de soporte de cosas ambiguas. Y esto es
> distinto de "algo no jala CONMIGO" (mi conexión/mis datos) → eso es `diagnostico`.

**Cómo lo ofrezco** (una línea, en claro, sin jerga):

```
Fallo:  Oye, intenté [X] y el sistema me marcó un error / me dio un número que no cuadra.
        ¿Quieres que lo reporte a soporte para que lo revisen?

Hueco:  Eso que necesitas, el sistema todavía no lo hace. ¿Le paso la sugerencia al
        equipo de soporte para que lo consideren?
```

Solo tras el "sí" sigo el flujo normal de abajo (`crearTicket`). Diferencias al llenarlo:

- **Fallo** → `tipo="SOPORTE_SISTEMA"`, prioridad según el impacto (ver tabla), descripción
  con lo que yo estaba haciendo → qué salió mal → la referencia (folio/factura/cliente).
- **Hueco** → `tipo="SOPORTE_SISTEMA"`, prioridad `BAJA`, y en la descripción **marco
  claro que es una carencia funcional** (no un bug): *"El usuario necesita [X]; el sistema
  no lo ofrece hoy."* Así el equipo técnico lo triagea como mejora, no como falla.

Si el usuario dice "no, déjalo" → no reporto y sigo con lo suyo. Su decisión, no la mía.

---

## Flujo — Falla del sistema

### 1. Entender bien qué pasó

Antes de reportar, necesito el detalle para que el equipo pueda reproducirlo:
- **Qué estabas haciendo** — ¿en qué pantalla / con qué operación?
- **Qué esperabas** que pasara.
- **Qué pasó** en su lugar (el error, el número equivocado, lo que sea).
- Si hay un **número de referencia** (folio de venta, factura, cliente) que lo dispare.

Si el usuario ya lo describió claro, no interrogo de más — recojo lo que falte y sigo.

### 2. Estimar la urgencia (sin abrumar al usuario)

Deduzco la prioridad del impacto — no se la pregunto en jerga:

| Prioridad | Cuándo |
|-----------|--------|
| `CRITICA` | El sistema está caído o **bloquea la operación** (no se puede vender / facturar / cobrar). |
| `ALTA` | Afecta el trabajo del día y no hay forma de rodearlo. |
| `MEDIA` | Molesta pero hay manera de seguir trabajando mientras tanto. |
| `BAJA` | Detalle menor, cosmético o "estaría bien que…". |

### 3. Confirmar en lenguaje humano

Le enseño lo que voy a reportar, en claro, para que ajuste si quiere:

```
Voy a reportarle esto al equipo de soporte:

Qué falla:  [resumen en una línea]
Detalle:    [qué hacías → qué esperabas → qué pasó]
Urgencia:   [caído / afecta hoy / se puede rodear / menor]

¿Lo mando así?
```

### 4. Levantar el reporte

Solo tras el "sí":
- Tool: `crearTicket` con:
  - `titulo`: resumen corto y claro de la falla.
  - `descripcion`: el detalle (qué hacía → qué esperaba → qué pasó → referencia).
  - `tipo`: `"SOPORTE_SISTEMA"`.
  - `prioridad`: `BAJA` | `MEDIA` | `ALTA` | `CRITICA`.
- Guardo el número de reporte que devuelve (`ticketId`) por si hay seguimiento.

### 5. Adjuntar captura si la hay

Si el usuario mandó una imagen/captura del error o un texto de error largo:
1. Primero `crearTicket` (paso 4) para tener el `ticketId`.
2. Luego la tool unificada `subirDocumento` con:
   - `entidadTipo`: `"ticket_soporte"`
   - `entidadId`: el `ticketId`
   - `nombreArchivo`: algo descriptivo (ej. `error_timbrado.png`)
   - `contenidoBase64`: el archivo en Base64 (si es chico, ~50 KB) o omitirlo para subir desde disco por el token generado.

### 6. Confirmar al usuario

En lenguaje de negocio, sin tecnicismos:

```
✅ Listo, ya lo reporté al equipo de soporte con la captura.
Lo tienen registrado y le van a dar seguimiento. Te aviso en cuanto sepa algo.
```

---

## Flujo — Tarea para un compañero

Cuando el usuario quiere dejarle una tarea formal a **otra persona de la empresa**
(no un recordatorio para sí mismo — eso va a tus pendientes locales, ver `INDEX.md`):

1. Recojo: **qué tarea**, **para quién** (compañero) y **para cuándo** si aplica.
2. Ubico a la persona: `listarUsuarios` — el `asignadoId` de `crearTicket` es el **ID de membresía** que devuelve esa tool (NO el id de `buscarEmpleados`).
3. Confirmo en una línea: *"Le dejo a [persona] la tarea de [X], ¿va?"*
4. Tras el "sí": `crearTicket` con `tipo="TAREA_INTERNA"`, `asignadoId` de la persona,
   `titulo` y `descripcion` claros, `prioridad` según urgencia.
5. Confirmo: *"Anotado, [persona] ya la tiene en su lista ✅"*.

> Diferencia rápida: **recordatorio para el propio usuario** → sus pendientes locales
> (backlog, lenguaje ligero). **Tarea formal para un colega en el sistema** → `TAREA_INTERNA`.

---

## Seguimiento

Si el usuario pregunta *"¿qué pasó con lo que reporté?"* o *"¿ya lo arreglaron?"*:
- `listarTickets` (filtrando por estado / tipo) para ver los reportes de la empresa.
- `verTicket` con el `ticketId` para el detalle y la resolución.
- Se lo traduzco en claro: *"Tu reporte del cálculo de vacaciones sigue en revisión"* /
  *"Ya lo marcaron como resuelto — dice que quedó corregido, ¿lo compruebas?"*.
- Si el usuario confirma que ya quedó y estaba en mi mano: `actualizarTicketEstado`.

---

## Errores comunes

| Situación | Qué digo / hago |
|-----------|-----------------|
| No me queda claro si falla el sistema o mi conexión | Pregunto una vez: *"¿el sistema hace algo raro, o soy yo que no te traigo los datos?"* → si soy yo, salto a `diagnostico`. |
| El usuario está frustrado ("¡ya no sirve!") | Primero calmo y ordeno: *"Vale, cuéntame qué hacías y qué esperabas — lo reporto y le damos seguimiento."* |
| Falta detalle para reproducir | Reporto con lo que hay, pero anoto en la descripción que faltó detalle, y le pido al usuario que avise si vuelve a pasar. |
| Sin permiso para crear reportes | *"No tengo habilitado reportar a soporte. Avísale a tu administrador para que me dé el permiso."* |
| Me piden ver reportes de otra empresa / cola global | *"Solo puedo ver los reportes de aquí. La vista general es del equipo técnico."* |
