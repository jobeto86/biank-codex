---
name: consultar-ventas
description: "Consultar ventas del ERP con filtros: lista por periodo/cliente/estado, detalle por folio, saldos pendientes de cobrar. Solo lectura, no requiere confirmacion. Triggers: 'cuanto vendimos', 'busca la venta de [cliente]', 'ventas de hoy/semana/mes', 'ventas pendientes de cobrar'."
---

# Skill: Consultar Ventas

**Trigger**: "¿cuánto vendimos?", "busca la venta de [cliente]", "ventas de hoy/semana/mes",
"¿me muestras la venta [folio]?", "ventas pendientes de cobrar"

---

## Qué hace

Consulta ventas del ERP con filtros opcionales y presenta los resultados
de forma clara para la empleada. No requiere confirmación — es solo lectura.

## Flujo

### 1. Entender qué busca el usuario

Determina si quiere:
- **Lista de ventas** — por período, cliente, estado (pendiente/saldada/cancelada)
- **Detalle de una venta** — por folio o número de venta
- **Ventas pendientes de cobrar** — saldo > 0

### 2. Ejecutar la tool MCP correspondiente

| Qué busca | Tool |
|-----------|------|
| Lista de ventas | `listarVentas` con filtros: fechaInicio, fechaFin, clienteId, estado |
| Detalle de una venta | `verVenta` con el folio o ID |
| Ventas pendientes del cliente | `ventasPendientesCliente` con clienteId |

### 3. Presentar resultados

Formato de lista (para varias ventas):
```
📋 Ventas [período/cliente]

| Folio | Fecha | Cliente | Total | Saldo | Estado |
|-------|-------|---------|-------|-------|--------|
| NV-XXX | DD/MM | Nombre | $X,XXX | $X,XXX | Pendiente |

Total encontradas: N
```

Formato de detalle (para una venta):
```
🧾 Venta [Folio]
Cliente: [nombre]
Fecha: [fecha]
Vendedor: [nombre]

Artículos:
• [producto] × [cant] = $[subtotal]
...

Subtotal: $X,XXX
IVA:      $X,XXX
Total:    $X,XXX
Pagado:   $X,XXX
Saldo:    $X,XXX

Estado: [Pendiente / Saldada / Cancelada]
```

### 4. Ofrecer siguiente acción si hay saldo pendiente

"Esta venta tiene un saldo de $[X]. ¿Quieres registrar un pago?"
