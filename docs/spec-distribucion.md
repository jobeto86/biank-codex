# Contrato de distribución por carpeta

Aprobado en TSK-634, 2026-10-29. Sustituye la distribución del core por MCP; no reactiva Biank Desktop.

| Regla | Comportamiento | Evidencia |
|---|---|---|
| BCG-01 | Sólo núcleo genérico declarado en core.manifest; no memoria, configuración, credenciales ni datos de empresas. | Paquete reproducible y prueba de preservación en dos workspaces. |
| BCG-02 | ZIP versionado, manifiesto exacto con SHA-256 y digest del asset de GitHub; sin consumir main directamente. | validate_package y pruebas de GitHub asset/tag/digest. |
| BCG-03 | Versiones monotónicas y origen fijado; ninguna actualización puede cambiar el repositorio instalado implícitamente. | Pruebas de versión igual/anterior y cambio de origen rechazado. |
| BCG-04 | Aplicación completa con staging, backup, VERSION al final y journal; recuperación antes de acceder a la red. | Fallo intermedio y caída de proceso con recuperación offline. |
| BCG-05 | Rechazar traversal, rutas privadas, symlinks, duplicados y colisiones con nuevas rutas del core. | Pruebas de paths, ZIP, destinos y skills locales. |
| BCG-06 | Instalación idempotente validada antes de marcar éxito; no crear ni cambiar credenciales o configuración del arnés. | Instalación de ZIP real, repetición y origen corrupto/same-version incompleto. |
| BCG-07 | Migración desde contenido genérico conocido por huella, sin adoptar archivos locales desconocidos. | legacyFiles y prueba positiva/negativa de migración. |
| BCG-08 | Primera apertura: instalar y actualizar; después releer identidad/índice. Red caída conserva versión local; journal pendiente bloquea operaciones hasta recuperar. | Instrucciones AGENTS y pruebas de recuperación. |
| BCG-09 | El backlog conserva tareas, responsable, próximo paso/fecha, decisiones relevantes y evidencia de cierre. Se actualiza la tarea existente; no se crea otra por cada conversación ni por operaciones completadas dentro del turno. | Revisión de identidad, bienvenida, revisión semanal y manual. |
| BCG-10 | No se exige crear, cargar ni cerrar resúmenes de sesiones; no depende de despedidas ni hooks. Historial del arnés para conversación, archivos anteriores sólo como antecedentes cuando sean necesarios. | Auditoría de instrucciones y preservación de sesiones y marcadores anteriores al actualizar. |
| BCG-11 | Contexto local opcional, máximo 4096 bytes UTF-8 contando todo el archivo: preferencias confirmadas, hechos duraderos y convenciones que aplican a varias tareas, con fecha, origen y vigencia cuando aplique. Sin duplicar reglas, tareas, historial, manuales, ERP ni secretos. Consolidar y medir antes de guardar; no truncar ni borrar contexto anterior que exceda el límite. | Revisión de instrucciones y preservación byte a byte de memoria anterior sobredimensionada durante una actualización. |
| BCG-12 | Guardar continuidad al confirmar resultados/decisiones, sin esperar al cierre ni interponer registros en la operación. Memoria nativa sólo como apoyo opcional; no se presume compartida entre arneses. Sin recordatorios en segundo plano salvo programación confirmada. | Auditoría de drift entre arranque, identidad, skills y documentación. |
| BCG-13 | Se distribuyen sólo tres skills auxiliares: conectar CBSuite, actualizar el core y diagnosticar. Sin skills operativas, recetas de parámetros, protocolos genéricos de negocio, indexador ni validador de manuales en el ZIP. Identidad, backlog y memoria breve quedan en instrucciones del core. | Inspección del manifiesto y del ZIP construido. |
| BCG-14 | El catálogo MCP autorizado y sus firmas vigentes definen las operaciones; los procesos de la empresa se consultan por MCP/wiki del tenant. Descubrir capacidades antes de declarar ausencia; no inventar procesos, parámetros, permisos ni automatismos. El índice vigente enumera sólo las tres skills auxiliares; recetas de core anteriores conservadas en instalaciones existentes no se cargan ni se ejecutan como instrucciones. Datos y personalizaciones se preservan sin borrado automático. | Auditoría de instrucciones y actualización desde paquetes anteriores conservando archivos locales y recetas retiradas fuera del nuevo manifiesto. |

BCG-09..12: cambio de continuidad autorizado directamente por Roberto en esta conversación,
2026-10-29 («Adelante»), tras aprobar backlog y memoria breve sin bitácora obligatoria.
No autoriza eliminar ni migrar automáticamente datos históricos del usuario.

BCG-13..14: reducción a tres skills auxiliares y operaciones vía MCP/wiki autorizada
directamente por Roberto en esta conversación, 2026-10-29 («Adelante»).
La reducción retira archivos del paquete nuevo; no añade borrados al actualizador.

GitHub distribuye el núcleo; la conexión nativa MCP conserva la autenticación y los permisos del ERP. Compartir cuenta del arnés no identifica al usuario CBSuite ni demuestra aislamiento entre personas.

La certificación de plataformas es explícita: la suite puede ejecutarse sin acceder al ERP ni a credenciales reales. Una prueba local Linux no certifica Windows/macOS ni una cuenta real del cliente.
