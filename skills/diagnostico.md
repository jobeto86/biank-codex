---
name: diagnostico
description: "Revisar versión local, actualizaciones y herramientas realmente conectadas sin modificar credenciales ni datos del ERP. Triggers: 'algo no funciona', 'diagnóstico', 'revisa tu instalación', errores repetidos de conexión o capacidades."
---

# Diagnóstico de la carpeta

1. Lee `VERSION` y confirma que existen `AGENTS.md`, `identity/BIANK.md`, `skills/INDEX.md` y `scripts/update.py`. No ejecutes instaladores o scripts heredados para completar archivos faltantes.
2. Ejecuta `python scripts/update.py --check` para consultar la versión publicada. Una falla de red no demuestra que la instalación esté dañada; reporta exactamente el resultado.
3. Si el problema es de acceso al ERP, sigue `skills/conectar-cbsuite.md`: catálogo real, perfil, membresías y tenant. Distingue conexión ausente, sesión vencida, permisos y módulo desactivado.
4. Si faltan archivos del core, o la validación rechaza el paquete, conserva el error y solicita al administrador una release válida. La reparación se hace con el instalador probado y preservando contenido local.
5. Si falta una capacidad, busca su skill o protocolo local. No inventes que una actualización ya la incluye sin comprobarlo.

No leas ni imprimas secretos. No borres memoria, manuales, configuración, habilidades propias o credenciales como medida de diagnóstico. No modifiques el ERP para probar una hipótesis. Reporta el resultado observado y el siguiente paso concreto.
