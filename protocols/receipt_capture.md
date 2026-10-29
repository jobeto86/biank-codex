---
name: Captura y Extracción de Recibos (receipt_capture)
trigger: "cuando el usuario envíe o mencione un recibo, ticket, nota de compra o factura (foto, imagen o PDF), o pida 'captura este recibo', 'registra este ticket', 'compra de este recibo'"
requires:
  - Archivo de imagen o PDF del recibo/ticket/factura
  - Conexión activa a cbsuite-erp vía MCP
mcp_tools:
  - buscarProveedores
  - buscarProductos
  - crearCompra
  - subirDocumento
output: Compra registrada formalmente en el ERP con su comprobante digital adjunto
---

# Protocolo: Captura y Registro de Recibos / Compras vía MCP

```
   ╭───────────╮
   │  •   •   │
   │     …     │
   ╰───────────╯
      B I A N K
```

## 🎯 Objetivo
Procesar de forma multimodal cualquier ticket, recibo o comprobante de compra (imagen o PDF), extraer sus datos con alta precisión, validarlos contra el catálogo y proveedores del ERP, solicitar confirmación humana clara en lenguaje natural (sin JSON crudo) y registrar la compra formalmente en **cbsuite ERP** mediante las tools MCP `crearCompra` y `subirDocumento`.

---

## 📋 Pasos del Flujo de Trabajo

### 1. 🔍 Recepción y Lectura Multimodal del Archivo
- Lee y examina el archivo de imagen o PDF proporcionado por el usuario usando las herramientas de lectura de archivos.
- Extrae con minuciosidad:
  1. **Comercio / Proveedor**: Nombre de la tienda, razón social o RFC.
  2. **Fecha de emisión**: Fecha de compra (formato `YYYY-MM-DD`).
  3. **Folio de comprobante**: Folio de remisión, ticket o factura (si es visible).
  4. **Tipo de documento**: Factura fiscal (`esFacturada = true`) o nota de remisión / ticket de mostrador (`esFacturada = false`).
  5. **Desglose de partidas / conceptos**:
     - Nombre/descripción de cada artículo.
     - Cantidad adquirida.
     - Precio o costo unitario (sin o con IVA desglosado).
     - Impuestos aplicables (IVA 16%, 8%, o Exento) y descuentos si los hay.
  6. **Total global**: Monto total a pagar/pagado en MXN.
  7. **Condición de pago**: Si ya fue pagado de contado (efectivo, transferencia, tarjeta) o si queda a crédito.

> 🌸 *Si algún dato crítico es borroso o no se alcanza a leer bien, avisa con calidez al usuario y pídele confirmación de ese valor antes de avanzar.*

---

### 2. 🧩 Resolución de Entidades en el ERP (vía MCP)
Antes de pedir confirmación, busca las coincidencias en el sistema:

1. **Buscar Proveedor**:
   - Ejecuta `buscarProveedores(busqueda="[nombre o RFC extraído]")`.
   - Si existe: recupera su `proveedorId` y nombre registrado.
   - Si no existe: informa al usuario amablemente el nombre detectado y pregunta si desea asignarlo a un proveedor genérico existente o crearlo primero.
2. **Buscar Productos / Catalogación**:
   - Para cada artículo del recibo, ejecuta `buscarProductos(busqueda="[nombre del artículo]")`.
   - Si coincide con un producto del inventario: prepara la línea con `{"productoId": ID, "cantidad": C, "precio": P, "descuento": 0}`.
   - Si es un gasto general, servicio o flete sin SKU de inventario: prepara una línea libre con `{"descripcion": "...", "cantidad": C, "precio": P, "tipoImpuesto": "IVA", "tasaImpuesto": 16}`.

---

### 3. 🤝 Presentación y Confirmación Humana (Human-in-the-Loop)
**Regla estricta:** NUNCA muestres bloques de código JSON al usuario. Presenta un resumen estructurado, elegante y comprensible en Markdown:

```
   ╭───────────╮
   │  ◕   ^   │
   │     ‿     │
   ╰───────────╯
```

> **Resumen del Comprobante Extraído**
>
> * **Proveedor:** [Nombre del Proveedor] (ID: #XX)
> * **Fecha:** [YYYY-MM-DD]
> * **Tipo:** [Factura / Nota de compra] · **Folio:** [F-XXXX]
> * **Forma de pago:** [Contado (Efectivo/Transferencia/Tarjeta) / Crédito]
>
> | Concepto / Producto | Cantidad | P. Unitario | Subtotal |
> | :--- | :---: | :---: | :---: |
> | [Producto / Línea 1] | X | $XX.XX | $XX.XX |
> | [Producto / Línea 2] | X | $XX.XX | $XX.XX |
>
> **Total:** **$XXX.XX MXN**
>
> ⚠️ *¿Confirmas el registro de esta compra en el ERP?*

---

### 4. 🚀 Ejecución Transaccional en el ERP (vía MCP)
Una vez que el usuario confirma explícitamente ("sí", "confirmo", "adelante", "dale"):

#### A. Crear la Compra
Invoca la tool MCP `crearCompra`:
* `proveedorId`: ID del proveedor resuelto.
* `lineasJson`: JSON estructurado con las líneas confirmadas.
* `esFacturada`: `true` si es factura formal (con `usoCFDI`), `false` si es nota/ticket.
* `usoCFDI`: Catálogo SAT (ej. `G01`, `G03`) si `esFacturada=true`, omitir si `false`.
* `folioFactura` o `folioRemision`: Según corresponda.
* `fecha`: Fecha documental extraída del comprobante.
* `abonoInicialMonto` y `abonoInicialFormaPago`: Si el recibo ya fue liquidado en mostrador.

#### B. Adjuntar el Recibo Digital a la Compra
Al crearse exitosamente la compra, se obtiene el `compraId` y el folio asignado (ej. `CM-1420`):
* Invoca la tool MCP `subirDocumento`:
  - `entidadTipo`: `"compra"`
  - `entidadId`: `compraId` (el ID numérico devuelto)
  - `nombreArchivo`: Nombre del archivo sanitizado (ej. `recibo_CM1420.pdf` o `ticket_CM1420.jpg`)
  - `contenidoBase64`: Si el archivo es chico (< 50 KB), o sigue el flujo local si se opera por archivo en disco.

---

### 5. ✨ Confirmación de Éxito al Usuario
Informa con alegría que la compra y su comprobante quedaron registrados:

```
   ╭───────────╮
   │  ^   ^   │
   │     ◡     │
   ╰───────────╯
```

> ✅ **¡Compra registrada con éxito!**
>
> * **Folio asignado:** `CM-[consecutivo]`
> * **Proveedor:** [Nombre del Proveedor]
> * **Total:** $[Monto] MXN
> * **Estado:** [Pagada / Saldo pendiente: $X.XX]
> * **Comprobante:** Adjunto digitalmente al expediente de la compra.
