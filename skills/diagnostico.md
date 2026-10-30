---
name: diagnostico
description: "Revisar versión local, actualizaciones y herramientas realmente conectadas sin modificar credenciales ni datos del ERP. Triggers: 'algo no funciona', 'diagnóstico', 'revisa tu instalación', errores repetidos de conexión o capacidades."
---

# Diagnóstico de la carpeta

1. Lee `VERSION` y confirma `AGENTS.md`, `identity/BIANK.md`, `skills/INDEX.md`,
   `scripts/update.py` y las tres skills del índice vigente. No uses instaladores
   o scripts antiguos para completar archivos faltantes.
2. Ejecuta `python scripts/update.py --check` para consultar la versión publicada.
   Usa `python3` si corresponde. Una falla de red no prueba daño de la instalación;
   reporta la salida observada y comprueba si hay journal pendiente.
3. Para acceso al ERP, sigue `skills/conectar-cbsuite.md`: catálogo real, perfil,
   membresías y tenant. Distingue conexión ausente, sesión vencida, permisos y módulo.
4. Si faltan archivos del core o el paquete se rechaza, conserva el error y pide
   al administrador una release válida. La reparación usa el instalador probado
   y preserva contenido local; no borres un journal para ocultar una recuperación.
5. Si falta una operación, usa el descubrimiento disponible y consulta su firma
   real. Para procesos internos, usa la wiki del tenant por MCP cuando esté
   disponible. No busques una receta operativa local ni atribuyas una capacidad
   a una actualización sin comprobarla.

No leas ni imprimas secretos. No borres memoria, manuales, configuración,
personalizaciones ni credenciales como diagnóstico. Las recetas retiradas del core
pueden seguir en una instalación anterior: su presencia no las activa ni justifica
borrarlas. No modifiques el ERP para probar una hipótesis. Reporta el resultado
observado, el alcance de la verificación y el siguiente paso concreto.
