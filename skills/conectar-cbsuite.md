---
name: conectar-cbsuite
description: "Verificar o recuperar el acceso a CBSuite con la conexión MCP nativa y autorizada del arnés. Triggers: 'no te conectas', 'reconéctate', herramientas ausentes o error de autenticación."
---

# Conectar o recuperar CBSuite

Endpoint: `https://cbsuite.cbinteligencia.com/mcp`. La carpeta contiene instrucciones;
la conexión y sus credenciales pertenecen al arnés y a la cuenta que la persona autorice.

## 1. Comprobar el acceso disponible

Consulta el catálogo realmente disponible. Usa el descubrimiento del servidor
si una herramienta no aparece; el prefijo puede variar entre arneses. No confundas
una lista inicial parcial con la ausencia de la operación.

Con las herramientas de CBSuite disponibles, consulta `obtenerMiPerfil`,
`listarMisMembresias` y `tenantActual`. Confirma usuario y empresa antes de operar;
usa el `tenantSlug` autorizado de forma explícita cuando la firma lo permita o exija.
Una cuenta compartida del proveedor de modelos no identifica al usuario de CBSuite.

## 2. Si falta conexión o autorización

Distingue lo observado: servidor no registrado, herramientas aún no cargadas,
sesión no autenticada, permisos insuficientes o módulo desactivado. Son estados distintos.

Guía el alta y consentimiento por el flujo nativo del arnés. El login se realiza
fuera del chat. No solicites contraseñas ni tokens, copies almacenes OAuth o generes
archivos de credenciales. No sustituyas `.mcp.json` ni conexiones que funcionan.

### Codex: CLI

Comprueba primero el registro con `codex mcp list`. Si ya existe CBSuite, usa su
nombre real y recupera esa conexión; no crees un duplicado ni cambies su origen.
Sólo si falta y el usuario autoriza conectarlo:

```sh
codex mcp add cbsuite --url https://cbsuite.cbinteligencia.com/mcp
```

El alta puede iniciar OAuth. Si la conexión todavía requiere autenticación, usa
`codex mcp login cbsuite` para abrir el consentimiento del arnés; no vuelvas a
autorizar una conexión ya válida. Si se registró con otro nombre, usa ése. No copies
tokens del navegador al chat ni a la carpeta. Después comprueba el servidor con
`/mcp` y verifica las herramientas reales.

### Codex: aplicación de escritorio o extensión

En Settings → MCP servers, comprueba si ya existe CBSuite. Para una conexión nueva
autorizada: Add server, transporte Streamable HTTP y el endpoint indicado arriba.
Guarda, reinicia la conexión/cliente según lo que indique la interfaz y selecciona
Authenticate cuando requiera OAuth. En la extensión, la entrada MCP servers está
en el menú de configuración; sigue las opciones de esa versión.

Estas superficies comparten configuración para el mismo host Codex; no las
registres por separado si la conexión ya está disponible. Fuente de los pasos:
[documentación oficial de MCP en Codex](https://learn.chatgpt.com/docs/extend/mcp).

### Claude Code, Antigravity u otro arnés

Usa su configuración MCP y autorización nativa vigentes, con el endpoint anterior.
Consulta la documentación del cliente si necesitas pasos concretos; no inventes
comandos o menús ni supongas que la conexión de Codex se comparte con otro arnés.
No ejecutes scripts de login heredados de una instalación antigua de Biank.

## 3. Confirmar después de autorizar

Vuelve a consultar perfil, membresías y tenant. Sólo una respuesta real confirma
acceso; un login completado o un servidor registrado no demuestra herramientas
cargadas. Si requiere una conversación nueva, indícalo sin afirmar que ya funciona.

La disponibilidad pública del endpoint tampoco acredita la sesión del cliente.
Si el acceso funciona pero una operación se rechaza por rol o módulo, informa ese
límite y usa el flujo autorizado de soporte que el MCP realmente ofrezca. No eludas
la restricción con otra cuenta ni pruebes capturas sobre datos reales.
