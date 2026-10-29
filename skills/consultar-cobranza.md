---
name: consultar-cobranza
description: "Revisar cartera vencida, clientes morosos e interacciones de cobranza en el ERP. Solo lectura. Triggers: 'cartera vencida', 'clientes que deben', 'seguimiento a [cliente]', 'cobranza pendiente'."
---

# Skill: Consultar Cobranza

**Trigger**: "cartera vencida", "clientes que deben", "¿a quién hay que cobrarle?",
"seguimiento a [cliente]", "registra que hablé con [cliente]", "promesas de pago"

---

## Qué hace

Consulta la cartera de cobranza y registra interacciones con clientes deudores.
Las consultas son solo lectura; **registrar una interacción sí escribe** (pero no
afecta dinero, no requiere confirmación formal — solo verificar los datos).

## Flujo

### 1. Entender qué busca el usuario

- **Cartera** — quién debe, cuánto y desde cuándo
- **Seguimiento de un cliente** — historial de llamadas/promesas
- **Registrar interacción** — "le llamé, prometió pagar el viernes"

### 2. Ejecutar la tool MCP correspondiente

| Qué busca | Tool |
|-----------|------|
| Estado general de cartera | `estadoCartera` |
| Lista de clientes con adeudo | `listarClientesCobranza` |
| Interacciones previas con un cliente | `listarInteraccionesCobranza` con clienteId |
| Registrar llamada/visita/promesa | `registrarInteraccionCobranza` |
| Ventas pendientes del cliente | `ventasPendientesCliente` con clienteId |

### 3. Presentar resultados

Formato de cartera:
```
📬 Cartera de cobranza — [fecha]

| Cliente | Adeudo | Días vencido | Última interacción |
|---------|--------|--------------|--------------------|
| Nombre | $X,XXX | N días | DD/MM — prometió pagar |

Total cartera: $X,XXX · Clientes con adeudo: N
```

### 4. Registrar interacción

Al registrar, capturar: cliente, tipo (llamada/visita/mensaje), resultado,
y promesa de pago con fecha si la hubo.

```
✅ Interacción registrada.
Cliente: [nombre] · Tipo: llamada
Resultado: prometió pagar $X,XXX el [fecha]
```

### 5. Proactividad

Si el usuario consulta la cartera, ofrecer: "¿Quieres que te diga a quién
conviene llamarle hoy?" (usar `identificarOportunidadesContacto`).
