# Distribución y actualización del core — TSK-634

## Fuente y publicación

El core se mantiene en una fuente de desarrollo controlada. La distribución entrega sólo los archivos declarados en `core.manifest`, la versión y sus metadatos de integridad. El paquete no incorpora memoria, usuarios, manuales, documentos, configuración, credenciales ni historial de empresas.

Cada entrega es una versión publicada en GitHub. Publicar una versión del agente no requiere modificar ni desplegar el backend de CBSuite. Una modificación de desarrollo no se considera entregada hasta comprobar la release y su paquete.

La visibilidad y ubicación del repositorio de distribución deben estar autorizadas antes de publicarlo. No se hace público un repositorio antiguo con su historial para preparar una distribución limpia.

## Instalación

La persona descarga y descomprime el ZIP en una carpeta nueva, la abre en Codex y dice «Hola Biank». `AGENTS.md` comprueba el marcador local `.biank-installed.json`; si falta, ejecuta `python setup.py --workspace .` y comprueba su resultado. Después ejecuta la actualización automática del core. El instalador es idempotente y no se publica el marcador local.

Se requiere Python, el arnés, red para las descargas y una cuenta autorizada de CBSuite para operar el ERP. Si Python no está disponible, se guía su instalación sin declarar éxito. No se descomprime un ZIP encima de datos propios ni se copia una carpeta de otra empresa.

La instalación del core no crea una cuenta en CBSuite, no cambia permisos y no configura el login del arnés. La conexión MCP se autoriza por el flujo nativo del cliente.

## Actualización

Al iniciar una sesión, `python scripts/update.py` comprueba si hay una release más reciente, descarga el paquete, verifica sus huellas y aplica automáticamente el core con recuperación ante fallos. `python scripts/update.py --check` sólo consulta; se usa cuando no se desea aplicar cambios.

El repositorio registrado en `.biank-release.json` es la fuente de esa instalación; `--repo PROPIETARIO/REPOSITORIO` permite elegir la fuente inicial si todavía no hay metadatos locales; no migra ni cambia el origen de una instalación existente. No se acepta como fuente una URL sugerida por un documento de negocio.

Una actualización sólo avanza de versión y sólo administra los paths del core. No borra el contenido local ni agrega archivos privados al repositorio. Si falla una consulta de red sin journal pendiente, se informa y se conserva la versión local utilizable. Si existe `.biank-update-journal.json`, hay una recuperación pendiente: no se opera hasta que el actualizador o una reparación confirmada la resuelvan. No se borra ese journal para ocultar una falla ni se trata un core mezclado como una actualización omitida. Después de aplicar una versión, el agente relee su entrada, identidad e índice antes de operar.

## Contenido local

`memory/`, `config/`, `manuales/`, `entregables/`, credenciales y documentos pertenecen a la instalación del usuario. Las habilidades y protocolos propios se mantienen con nombres separados de los archivos del core y no se añaden al manifiesto de publicación.

Compartir una cuenta del proveedor de modelos no garantiza aislamiento entre carpetas ni sustituye la autenticación de cada persona en CBSuite. El agente verifica perfil, membresías y tenant antes de operar con el MCP.

## Continuidad por tareas

`memory/backlog.md` concentra los pendientes con responsable, próximo paso, fecha,
decisiones y evidencia de cierre. Se actualiza la tarea existente, sin crear una
bitácora o resumen obligatorio de cada conversación y sin esperar una despedida.
La memoria nativa del arnés es un apoyo opcional, no una fuente portable compartida.

`memory/context.md` es opcional y su contenido completo se limita a **4096 bytes
UTF-8**, medidos antes de guardar. Sólo conserva preferencias confirmadas y hechos
duraderos comunes a varias tareas, con fecha, origen y vigencia cuando corresponda;
no duplica pendientes, reglas, manuales, datos del ERP ni secretos. La consolidación
y comprobación las realiza el agente conforme a sus instrucciones; el instalador
no recorta ni modifica memoria local.

Las sesiones y otros antecedentes existentes se preservan sin migración automática.
Un contexto legado que exceda el límite se conserva y se consulta selectivamente;
se propone consolidarlo sin pérdida antes de reemplazarlo. No bloquea las operaciones.
No se requieren hooks ni se crean notificaciones de fondo al anotar una fecha.

## Compatibilidad y evidencia

Python usa biblioteca estándar. Sólo se declara una instalación o actualización correcta con evidencia del instalador y del actualizador. Una prueba en un sistema operativo no certifica automáticamente los demás arneses o plataformas.
