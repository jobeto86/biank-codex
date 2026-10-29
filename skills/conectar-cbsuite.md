---
name: conectar-cbsuite
description: "Verificar o recuperar el acceso a CBSuite con la conexión MCP nativa y autorizada del arnés, sin pedir secretos ni reescribir su configuración. Triggers: 'no te conectas', 'reconéctate', tools ausentes o error de autenticación."
---

# Conectar o recuperar CBSuite

CBSuite se opera con la conexión MCP del propio arnés o su complemento autorizado. El endpoint del servicio es `https://cbsuite.cbinteligencia.com/mcp`. La carpeta de Biank contiene instrucciones y skills; no administra la identidad del arnés ni sus credenciales.

## 1. Verificar lo que ya está conectado

Consulta el catálogo realmente disponible. Si el complemento ofrece descubrimiento de herramientas, úsalo antes de afirmar que una operación no existe. El prefijo del servidor puede variar entre arneses.

Con las herramientas de CBSuite disponibles, consulta `obtenerMiPerfil`, `listarMisMembresias` y `tenantActual`. Confirma usuario y empresa antes de una operación; usa el `tenantSlug` autorizado de forma explícita cuando corresponda. Si responde, la conexión funciona: continúa con el trabajo solicitado.

Una cuenta compartida del proveedor de modelos no determina quién está autenticado en CBSuite. No atribuyas las autorizaciones de un empleado a otro por su nombre en la conversación.

## 2. Si falta la conexión o la autorización

Indica qué se observó: herramienta ausente, sesión no autenticada, rechazo por permisos o módulo apagado. Son estados distintos.

Para autorizar o reconectar, guía a la persona al flujo de conexiones o complementos de su arnés. El inicio de sesión y el consentimiento se realizan en ese flujo, fuera del chat. Usa las instrucciones vigentes del cliente si necesitas pasos concretos; no inventes comandos o menús.

No solicites contraseñas ni tokens en la conversación. No copies el almacén OAuth del arnés, no generes archivos de credenciales, no reemplaces `.mcp.json` ni otras conexiones que ya funcionan, y no ejecutes scripts de login heredados.

## 3. Comprobar después de reconectar

Vuelve a consultar perfil, membresías y tenant. Sólo una respuesta real confirma acceso. Si el arnés necesita una sesión nueva para cargar herramientas, indícalo sin prometer que ya están disponibles.

Si CBSuite responde pero rechaza una operación por rol o módulo, informa esa limitación y usa el flujo de soporte autorizado. No intentes eludirla con otra cuenta o con una captura de prueba sobre datos reales.
