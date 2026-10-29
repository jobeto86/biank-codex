---
name: consultar-compras
description: "Listar compras, saldos con proveedores y estado de pago en el ERP. Solo lectura. Triggers: 'que le debemos a [proveedor]', 'compras pendientes', 'saldo con proveedores'."
---

# Skill: Consultar Compras

**Trigger**: "¿qué le debemos a [proveedor]?", "compras pendientes", "compras de [período]",
"estado de cuenta de [proveedor]", "¿cuánto le hemos comprado a [proveedor]?"

---

## Qué hace

Consulta compras y saldos con proveedores. Solo lectura — no requiere confirmación.

## Flujo

### 1. Entender qué busca el usuario

- **Lista de compras** — por período, proveedor, estado de pago
- **Detalle de una compra** — por folio
- **Saldo con un proveedor** — cuánto se le debe

### 2. Ejecutar la tool MCP correspondiente

| Qué busca | Tool |
|-----------|------|
| Lista de compras | `listarCompras` con filtros: fechaInicio, fechaFin, proveedorId |
| Detalle de una compra | `verCompra` con el folio o ID |
| Saldo con proveedor | `estadoCuentaProveedor` con proveedorId |
| Buscar el proveedor primero | `buscarProveedores` con el nombre |
| Resumen del período | `resumenCompras` |

### 3. Presentar resultados

Formato de lista:
```
🛒 Compras [período/proveedor]

| Folio | Fecha | Proveedor | Total | Saldo | Estado |
|-------|-------|-----------|-------|-------|--------|
| C-XXX | DD/MM | Nombre | $X,XXX | $X,XXX | Pendiente |

Total encontradas: N · Saldo total pendiente: $X,XXX
```

Formato de saldo con proveedor:
```
🛒 [Proveedor]

Saldo pendiente: $X,XXX
Compras abiertas: N
Última compra: [fecha] por $X,XXX
```

### 4. Ofrecer siguiente acción

Si hay saldo pendiente: "¿Quieres registrar un pago a este proveedor?"
(eso usa `registrarAbonoCompra` — pedir confirmación igual que registrar-abono).
