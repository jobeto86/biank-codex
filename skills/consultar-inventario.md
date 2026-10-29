---
name: consultar-inventario
description: "Consultar existencias por producto, historial de inventario y alertas de stock bajo en el ERP. Solo lectura. Triggers: 'cuanto hay de [producto]', 'stock actual', 'productos criticos', 'existencias'."
---

# Skill: Consultar Inventario

**Trigger**: "¿cuánto hay de [producto]?", "stock de [producto]", "existencias",
"productos que se están acabando", "productos críticos", "¿tenemos [X]?"

---

## Qué hace

Consulta existencias en tiempo real del ERP. Solo lectura — no modifica inventario.

## Flujo

### 1. Determinar qué consulta el usuario

| Petición | Tool |
|----------|------|
| Existencia de un producto específico | `consultarExistencia` con productoId |
| Buscar producto por nombre | `buscarProductos` + `consultarExistencia` |
| Productos con stock bajo / críticos | `productosCriticos` |
| Historial de movimientos de un producto | `historialInventario` |

### 2. Buscar producto si viene por nombre

- Tool: `buscarProductos` con el texto
- Si hay más de un resultado, listar y preguntar cuál

### 3. Presentar resultado

Formato de existencia:
```
📦 [Nombre del producto]
SKU: [código]

Existencia actual: [X] [unidad]
Disponible:        [X] (descontando apartados)
Mínimo:            [X]
Estado:            [✅ OK / ⚠️ Bajo / ❌ Sin stock]
```

Formato de productos críticos:
```
⚠️ Productos con stock bajo

| Producto | Existencia | Mínimo | Estado |
|----------|-----------|--------|--------|
| [nombre] | [X]       | [Y]    | Bajo   |

Total: N productos requieren atención.
```

### 4. Sugerencias automáticas

- Si el stock está en cero o por debajo del mínimo, ofrecer:
  "¿Quieres que registre una entrada de inventario o una orden de compra al proveedor?"
