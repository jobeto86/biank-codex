---
name: consultar-clientes
description: "Buscar clientes en el ERP: saldo, estado de cuenta, historial y linea de credito. Solo lectura. Triggers: 'busca a [cliente]', 'cuanto debe [cliente]', 'estado de cuenta de [cliente]', 'datos del cliente'."
---

# Skill: Consultar Clientes

**Trigger**: "busca a [cliente]", "¿cuánto debe [cliente]?", "estado de cuenta de [cliente]",
"¿tiene crédito disponible?", "historial de [cliente]"

---

## Qué hace

Busca clientes en el ERP y presenta su situación financiera actual —
saldo, límite de crédito, historial de compras, estado de morosidad.

## Flujo

### 1. Buscar al cliente

Si el usuario da un nombre (parcial o completo):
- Tool: `buscarClientes` con el texto de búsqueda
- Si retorna más de un resultado, presentar lista y preguntar cuál es

Si el usuario da el folio o ID:
- Tool: `resumenEstrategicoCliente` o `estadoCuentaCliente` directamente

### 2. Determinar qué quiere saber

| Petición | Tool |
|----------|------|
| Saldo actual / estado de cuenta | `estadoCuentaCliente` |
| Resumen financiero completo | `resumenFinancieroCliente` |
| Verificar si puede comprar a crédito | `verificarCreditoCliente` |
| Historial de compras / ventas | `ventasPendientesCliente` |

### 3. Presentar resultado

Formato de estado de cuenta:
```
👤 [Nombre del cliente]
RFC: [RFC]
Teléfono: [tel]

💳 Crédito
Límite:       $X,XXX
Usado:        $X,XXX
Disponible:   $X,XXX
Estado:       [Al corriente / Suspendido / Moroso]

📋 Saldo pendiente: $X,XXX
Ventas con adeudo: N
```

### 4. Alertas automáticas

- Si el cliente está suspendido o moroso, indicarlo claramente con ⚠️
- Si tiene ventas vencidas (>30 días), mencionarlo y ofrecer registrar interacción de cobranza
