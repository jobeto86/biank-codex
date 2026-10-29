---
name: buscar-archivo
description: "Encontrar archivos locales por nombre o ruta, sin leer contenido. Triggers: 'dónde está el archivo', 'busca la cotización', 'encuentra el PDF', 'no encuentro un documento'."
---

# Buscar archivos locales

Esta skill encuentra documentos en carpetas que el usuario autorizó. El índice es local:
guarda nombre, ruta, extensión, tamaño y fecha; nunca contenido y nunca se sube.

## Primera configuración

1. Explica qué metadatos se guardan y pide al usuario elegir una carpeta concreta.
2. Sólo después de su consentimiento ejecuta:
   `python scripts/file_index.py add-folder "RUTA"`
3. Construye el índice con `python scripts/file_index.py scan`.
4. No agregues la raíz del disco ni el perfil completo del usuario.

## Buscar

1. Si no hay índice, consulta `python scripts/file_index.py status` y ofrece configurarlo.
2. Ejecuta `python scripts/file_index.py search "TEXTO"`.
3. Responde con máximo cinco coincidencias claras: nombre, carpeta y fecha.
4. Si no aparece, ofrece volver a escanear; no inventes una ubicación.

## Reglas

- No abras ni leas el contenido para mejorar resultados.
- No indexices carpetas no declaradas.
- No copies el índice a conversaciones, Git, MCP ni servicios externos.
- El nombre del archivo puede ser sensible: muestra sólo resultados pertinentes a la consulta.
