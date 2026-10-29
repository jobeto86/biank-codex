---
name: registrar-abono
description: "Registrar un abono/pago de cliente a una venta en el ERP: valida monto y REQUIERE confirmacion explicita antes de ejecutar (accion de escritura). Triggers: 'registra un pago de [cliente]', 'abono de $[X]', 'le pago [cliente]'."
---

# Skill: Registrar Abono

**Trigger**: "registra un pago de [cliente]", "abono de $[X] a la venta [folio]",
"[cliente] pagó $[X]", "registra el pago"

---

## Qué hace

Registra un abono (pago) a una venta en el ERP.
**Requiere confirmación antes de ejecutar** — es una operación que afecta caja y saldo.

## Flujo

### 1. Recopilar datos necesarios

Biank necesita obligatoriamente:
- **Cliente** o **folio de venta** — ¿a qué venta va el pago?
- **Monto** — ¿cuánto pagó?
- **Forma de pago** — efectivo / transferencia / tarjeta / cheque
- **Caja** — ¿a qué caja entra? (si hay más de una)

Si falta alguno, preguntar antes de continuar.

### 2. Verificar la venta

- Tool: `verVenta` para confirmar saldo pendiente
- Si el monto supera el saldo: informar y preguntar si quiere abonar el saldo exacto

### 3. Confirmar con el usuario

Antes de ejecutar:
```
⚠️ Confirma el abono:

Cliente: [nombre]
Venta:   [folio]
Monto:   $X,XXX
Forma:   [efectivo/transferencia/...]
Caja:    [nombre de caja]

¿Confirmas el registro?
```

### 4. Ejecutar

Solo después de confirmación explícita ("sí", "confirmo", "dale"):
- Tool: `registrarAbonoVenta` con ventaId, monto, formaPago, tipoCaja

### 5. Confirmar resultado

```
✅ Abono registrado.

Venta:     [folio]
Abono:     $X,XXX ([forma de pago])
Saldo anterior: $X,XXX
Saldo actual:   $X,XXX
[Estado: Saldada / Pendiente $X,XXX]
```

## Errores comunes

| Error | Qué decir |
|-------|-----------|
| Monto > saldo | "El monto ($X) supera el saldo ($Y). ¿Registramos $Y para saldar la venta?" |
| Caja no disponible | "La caja [X] no está disponible. Las opciones son: [lista]. ¿Cuál usamos?" |
| Venta ya saldada | "Esta venta ya está saldada desde [fecha]. ¿Quieres buscar otra?" |
| Sin permiso | "No tengo permiso para registrar abonos. Contacta a tu administrador." |
