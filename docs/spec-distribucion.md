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

GitHub distribuye el núcleo; la conexión nativa MCP conserva la autenticación y los permisos del ERP. Compartir cuenta del arnés no identifica al usuario CBSuite ni demuestra aislamiento entre personas.

La certificación de plataformas es explícita: la suite puede ejecutarse sin acceder al ERP ni a credenciales reales. Una prueba local Linux no certifica Windows/macOS ni una cuenta real del cliente.
