---
name: actualizarme
description: "Consultar y aplicar versiones publicadas del core de Biank desde GitHub, conservando contenido local. Triggers: 'actualízate', 'busca actualizaciones', 'hay versión nueva', 'estás al día'."
---

# Actualizar el core

La fuente es el repositorio registrado por el instalador en `.biank-release.json`. No se usa MCP para distribuir archivos del agente.

## Consultar

Ejecuta `python scripts/update.py --check`. Sólo comprueba la versión publicada; no aplica cambios. Usa `python3` si ése es el ejecutable disponible.

## Aplicar

Ejecuta `python scripts/update.py`. El actualizador descarga una release versionada de GitHub y valida el paquete antes de sustituir los archivos del core. Conserva memoria, configuración, credenciales, documentos, manuales y archivos propios fuera del manifiesto. Una versión igual o anterior no se aplica.

Lee la salida antes de informar el resultado. Si se actualizó, vuelve a leer `AGENTS.md`, `identity/BIANK.md` y `skills/INDEX.md` para usar las instrucciones nuevas. No confundas una comprobación con una instalación.

Si falla una consulta o descarga y no queda `.biank-update-journal.json`, conserva el diagnóstico y usa la versión local que siga utilizable. La presencia de ese journal indica recuperación pendiente: ejecuta el actualizador probado para recuperarla y no operes mientras falle o siga pendiente. No borres el journal ni completes una actualización descargando y sobreescribiendo archivos a mano.

No pidas credenciales de GitHub ni de CBSuite por chat. Si la fuente requiere un acceso que no está disponible, informa el bloqueo al administrador. No cambies de repositorio ni modifiques configuraciones del arnés para resolverlo.

Las habilidades propias de la empresa se guardan como archivos separados, fuera de los nombres que el core distribuye. No edites una skill del core para guardar datos de un cliente: la siguiente versión puede reemplazarla.
