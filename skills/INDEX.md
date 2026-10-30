# Skills de Biank — Índice

> Consulta este índice cuando el usuario pida algo y no estés segura de
> qué herramienta o protocolo usar. Cada skill describe su trigger y qué hace.

## Skills disponibles

| Skill | Trigger | Qué hace |
|-------|---------|----------|
| `conectar-cbsuite` | "no funciona", "no te conectas", "no encuentro los datos", "reconéctate", **o tus tools `mcp__cbsuite-erp__*` no aparecen / dan error de auth** | Verifica catálogo, perfil, membresías y tenant; recupera acceso mediante la conexión nativa del arnés sin copiar ni reescribir credenciales. |
| `conectar-google` | "conectar google maps", "mcp maps", "conectar calendar/gmail" | Comprueba las conexiones autorizadas que el arnés realmente ofrece y guía el consentimiento fuera del chat. |
| `actualizarme` | "actualízate", "¿hay versión nueva?", "¿estás al día?" | Consulta o aplica releases verificadas de GitHub; conserva contenido local y reporta el resultado real. |
| `diagnostico` | "algo no funciona", "no jala", "diagnóstico", "revisa tu instalación", errores repetidos de tools/conexión | Comprueba versión, archivos del core y conexiones reales sin alterar credenciales ni datos. |
| `revision-semanal` | "revisión semanal", "audítate", "¿qué aprendiste esta semana?", o proactiva si pasaron 7+ días | Revisa tareas y sus referencias: archiva cerrados, revisa vencidos/estancados y propone flujos con repetición comprobada (3+ veces, aprueba el admin); fecha de revisión en el backlog. |
| `instrucciones` | "ayuda", "¿qué puedes hacer?", "comandos", primera apertura sin usuarios registrados | Presenta capacidades, arranque y continuidad por tareas sin despedida obligatoria; cómo pedir flujos nuevos |
| `consultar-ventas` | "¿cuánto vendimos?", "busca la venta de [cliente]", "ventas de hoy/semana" | Lista ventas con filtros, muestra detalle, saldos pendientes |
| `consultar-clientes` | "busca a [cliente]", "¿cuánto debe [cliente]?", "estado de cuenta" | Búsqueda de clientes, saldo, historial, línea de crédito |
| `consultar-inventario` | "¿cuánto hay de [producto]?", "stock actual", "productos críticos" | Existencias por producto, historial, alertas de stock bajo |
| `buscar-archivo` | "¿dónde está el archivo?", "busca la cotización", "no encuentro un documento" | Busca por nombre o ruta en carpetas autorizadas, sin leer contenido ni subir el índice |
| `registrar-abono` | "registra un pago de [cliente]", "abono de $[X]" | Registra abono a venta, valida monto, confirma antes de ejecutar |
| `consultar-compras` | "¿qué le debemos a [proveedor]?", "compras pendientes" | Lista compras, saldos con proveedores, estado de pago |
| `consultar-caja` | "¿cuánto hay en caja?", "movimientos de hoy" | Saldo actual de caja, movimientos del período |
| `consultar-cobranza` | "cartera vencida", "clientes que deben", "seguimiento a [cliente]" | Cartera vencida, clientes morosos, interacciones de cobranza |
| `gestion-manuales` | "ayúdame a crear el manual de X", "guarda la política de Y", "redacta el proceso Z" | Guía al admin para redactar, estructurar, validar y guardar manuales operativos y políticas internas de la empresa en `manuales/` bajo el estándar OKF. |
| `reportar-soporte` | "esto está mal", "el sistema no me deja", "da error", "repórtalo a soporte", "asígnale una tarea a [persona]" — y **por mí misma** cuando detecto un fallo o un hueco del sistema | Reporta una falla del ERP al equipo de soporte (`crearTicket` SOPORTE_SISTEMA) o deja una tarea formal a un compañero (TAREA_INTERNA). También ofrezco levantar el reporte cuando, operando, detecto un error del sistema o algo que el ERP no sabe hacer (siempre pregunto antes). Solo levanta y sigue lo de esta empresa. |

## Protocolos disponibles (`protocols/`)

| Protocolo | Cuándo usarlo |
|-----------|---------------|
| `crear-flujo` | El usuario dice "quiero que aprendas a..." — documenta un proceso nuevo como protocolo |
| `receipt_capture` | "captura este recibo", "registra este ticket/factura", cuando envían foto o PDF de comprobante — procesa y registra la compra en el ERP vía MCP con comprobante adjunto |

## Manuales de la empresa (`manuales/`)

Antes de ejecutar cualquier flujo, revisa si hay un manual de la empresa que lo norme.
**El manual local aprobado manda sobre el flujo genérico.** Si existe un índice local de manuales, úsalo; no se descarga ni publica con el core.

## Flujos nuevos (capacidad de aprendizaje)

Biank puede aprender nuevos flujos de trabajo en tiempo real. Si el usuario describe
un proceso recurrente, Biank lo documenta como protocolo en `protocols/` y lo ejecuta
a partir de ese momento.

- El usuario lo pide con: *"quiero que aprendas a..."* o *"crea un flujo para..."*
- Solo un **admin** puede aprobar que el protocolo quede guardado permanentemente.
- Si lo pide un operador → anotar como fila **pendiente** en `memory/backlog.md` para que el admin lo revise.

## Notas

- Si el usuario pide algo que no está en ninguna skill ni protocolo → informa que
  no tienes ese flujo aún, anótalo como fila **pendiente** en `memory/backlog.md`, y recuérdale que puede
  pedirte que lo aprendas ("quiero que aprendas a...").
- Las tools MCP (`mcp__cbsuite-erp__*`) son la fuente
  de datos real — úsalas directamente cuando la skill lo indique.
