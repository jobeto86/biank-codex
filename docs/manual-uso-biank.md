# Manual de uso de Biank

Biank te ayuda a consultar y operar CBSuite desde tu arnés, con las herramientas
y permisos que tu cuenta tenga disponibles. La carpeta aporta identidad,
seguimiento y mantenimiento; las operaciones y procesos de la empresa vienen del MCP.

## Arrancar

1. Descarga `biank-core.zip` de una release publicada y descomprímelo en una carpeta
   nueva. No lo descomprimas encima de documentos de trabajo.
2. Abre la carpeta en tu arnés compatible y di **«Hola Biank»**, o pide directamente
   lo que necesitas. El agente sigue `AGENTS.md` (`CLAUDE.md` remite a esa entrada).
3. Necesitas Python 3.10 o posterior. El agente ejecuta el instalador si hace falta
   y busca una actualización del core. Confirma el resultado antes de darlo por listo.
4. Autoriza tu propia cuenta de CBSuite en la conexión nativa MCP del arnés.
   Biank verifica usuario, membresías y empresa antes de operar. El saludo no crea
   cuentas, no configura tu suscripción y no reemplaza esa autorización.

Los pasos concretos de conexión están en `skills/conectar-cbsuite.md`. Si falta
Python o falla la conexión, Biank explica lo observado; no recibe tu contraseña.

## Qué puedes pedir

Habla con preguntas y resultados concretos: «¿cuánto vendimos esta semana?»,
«¿qué quedó pendiente con López?», «¿qué dice nuestro proceso de compras?» o
«prepara este registro para revisarlo». Biank descubre la herramienta y consulta
el proceso de la empresa cuando corresponde, sin recetas de operación congeladas
en la carpeta. Las capacidades dependen de tu cuenta, empresa y conexión reales.

Las consultas son de lectura. Para modificar datos, Biank muestra el cambio y espera
confirmación; verifica después el resultado. Una consulta parcial no se presenta
como el total de la empresa, y tu intención de pagar no se toma como comprobante.

Si proporcionas un recibo o documento, puedes pedir que lo lea y prepare un resumen.
Registrarlo en el ERP requiere las herramientas disponibles, sus datos necesarios
y tu confirmación; adjuntar un archivo no registra automáticamente una compra.

## Sólo tres skills locales

- **Conectar CBSuite:** verificar o recuperar la conexión nativa y tu identidad.
- **Actualizarse:** consultar o aplicar una release verificada de GitHub.
- **Diagnóstico:** comprobar instalación y acceso sin alterar datos del ERP.

Ventas, caja, inventario, cobranza, compras y soporte se resuelven con el MCP.
Los manuales y flujos compartidos de la empresa se consultan y gestionan en la wiki
o fuente del tenant por MCP, según permisos y aprobación. La carpeta no distribuye
protocolos genéricos de negocio ni exige crear una skill para cada operación.

Si necesitas documentar un proceso nuevo, Biank prepara el borrador, comprueba la
fuente y los permisos disponibles y sólo lo guarda después de aprobación. Si falta
acceso, informa la limitación; no afirma que quedó publicado ni cambia de cuenta.

## Pendientes y memoria

«Recuérdame marcarle el viernes a López» se guarda en el pendiente correspondiente,
con responsable, próximo paso y fecha. Acuerdos y comprobantes quedan en esa misma
tarea, sin duplicarla por cambiar de conversación. Biank trae lo del día cuando
vuelves a trabajar con ella. Los avisos fuera del chat requieren una programación
confirmada; anotar una fecha no crea una notificación.

No necesitas despedirte para conservar el seguimiento. Puedes pedir «¿qué tenemos
pendiente?», «¿qué acordamos?» o revisar semanalmente los asuntos: se archiva lo
cerrado y se repasan fechas y responsables. No se genera una bitácora de cada charla.

Una memoria opcional de hasta **4096 bytes UTF-8** conserva preferencias confirmadas
y hechos duraderos útiles para varios asuntos, con fecha y origen. El agente debe
consolidarla y medirla antes de guardar, sin duplicar tareas, manuales o datos del ERP
ni guardar secretos. Puedes preguntar qué recuerda, corregirlo o pedir que lo olvide.

## Qué pasa al actualizar

Se preservan tus tareas, documentos, configuración, entregables y personalizaciones.
Los archivos de sesiones o recetas antiguas no se borran automáticamente. Un contexto
anterior mayor de 4096 bytes se conserva y consulta selectivamente; se propone
consolidarlo sin pérdida antes de reemplazarlo y no bloquea el trabajo.

En instalaciones anteriores pueden seguir archivos de skills y protocolos retirados.
El índice vigente sólo activa las tres skills auxiliares; esas recetas antiguas no
se usan como instrucciones de operación. Los documentos locales siguen siendo
antecedentes, no contratos de las herramientas ni permisos adicionales.

El historial y la memoria nativa dependen del arnés; no se supone que se compartan
entre Codex, Claude Code y Antigravity. Las entradas de la carpeta están preparadas
para esos arneses, pero la evidencia de instalación Linux ARM64 no certifica Windows,
macOS ni el primer arranque real de cada cliente.

## Si algo falla

Di «revisa tu instalación» o «no te conectas». Biank diferencia problemas de Python,
paquete, red, autenticación y permisos, y reporta lo comprobado. No borres la carpeta
de trabajo ni compartas sus archivos de acceso como intento de reparación.
