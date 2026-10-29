---
name: consultar-caja
description: "Consultar saldo actual de caja y movimientos del periodo en el ERP. Solo lectura. Triggers: 'cuanto hay en caja', 'movimientos de hoy', 'saldo de caja', 'corte de caja'."
---

# Skill: Consultar Caja

**Trigger**: "¿cuánto hay en caja?", "saldo de caja", "movimientos de hoy",
"¿cuadra la caja?", "movimientos de [caja] de [fecha]"

---

## Qué hace

Consulta el saldo y los movimientos de caja. Solo lectura — no requiere confirmación.

## Flujo

### 1. Entender qué busca el usuario

- **Saldo actual** — cuánto hay en cada caja ahora
- **Movimientos** — entradas y salidas de un período
- **Verificación** — si la caja cuadra contra lo registrado

### 2. Ejecutar la tool MCP correspondiente

| Qué busca | Tool |
|-----------|------|
| Saldo actual | `saldoCajaActual` |
| Movimientos del período | `listarMovimientosCaja` con fechaInicio, fechaFin, tipoCaja |
| Verificación de caja | `verificarCaja` |

### 3. Presentar resultados

Formato de saldo:
```
🏦 Saldo de cajas — [fecha y hora]

| Caja | Saldo |
|------|-------|
| Efectivo | $X,XXX |
| Banco | $X,XXX |

Total: $X,XXX
```

Formato de movimientos:
```
🏦 Movimientos [caja] — [período]

| Hora | Concepto | Entrada | Salida |
|------|----------|---------|--------|
| HH:MM | Abono venta NV-XXX | $X,XXX | — |
| HH:MM | Pago proveedor | — | $X,XXX |

Entradas: $X,XXX · Salidas: $X,XXX · Neto: $X,XXX
```

### 4. Alertar si algo no cuadra

Si la verificación detecta diferencias, decirlo claro:
"⚠️ La caja [X] tiene una diferencia de $[Y]. ¿Quieres revisar los movimientos?"
