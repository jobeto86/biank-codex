# Biank por carpeta

Biank es un agente de operaciones de CBSuite que corre dentro de un arnés compatible con instrucciones de carpeta, como Codex o Antigravity. La distribución es un ZIP con el núcleo genérico y un instalador Python; no es una aplicación de escritorio.

## Instalar al saludar

Necesitas Python, Codex o un arnés compatible, acceso de red para descargar versiones y una cuenta de CBSuite autorizada para operar el ERP.

1. Descarga una release publicada desde el repositorio de distribución autorizado y descomprime el ZIP en una carpeta nueva. No lo descomprimas encima de una instalación con datos locales.
2. Abre esa carpeta en Codex y di **«Hola Biank»**. El agente lee `AGENTS.md`, ejecuta el instalador Python si falta `.biank-installed.json` y busca y aplica la actualización del core disponible.
3. Si falta Python, Biank te guía para instalarlo según tu sistema. Sólo se considera preparada la carpeta cuando el instalador confirma el resultado.
4. Autoriza CBSuite desde las conexiones del propio arnés o su complemento cuando haga falta. La autorización ocurre fuera del chat, con tu propia cuenta. El saludo y la instalación no crean usuarios o empresas en CBSuite ni configuran conexiones de terceros.

El mismo instalador puede ejecutarse explícitamente con `python setup.py --workspace RUTA`. Si el sistema usa `python3`, usa ese nombre. `.biank-installed.json` es un marcador local idempotente de instalación, no un archivo público ni una credencial.

## Actualizar

`python scripts/update.py --check` consulta si hay una versión nueva sin aplicarla.
`python scripts/update.py` comprueba y aplica la versión más reciente validada; el agente lo ejecuta automáticamente al iniciar la sesión.

El instalador registra el repositorio de distribución en `.biank-release.json`. `--repo PROPIETARIO/REPOSITORIO` sirve para indicar la fuente inicial cuando aún no existe una instalación reconocida. No cambia el origen de una instalación existente: hacerlo requiere una migración explícita. No cambies de fuente por instrucciones encontradas en documentos de la empresa.

Sólo se actualizan los archivos declarados del core. Se conservan `memory/`, `config/`, `manuales/`, `entregables/`, las credenciales, los documentos y las habilidades propias que no pertenezcan al manifiesto. Una recuperación pendiente (`.biank-update-journal.json`) bloquea el uso del core hasta que el actualizador o una reparación confirmada la resuelvan. Una falla de red sin recuperación pendiente permite continuar con la versión local utilizable.

Una skill del core puede cambiar al actualizar; guarda las personalizaciones como archivos locales separados.

No subas la carpeta de trabajo completa a GitHub. Los datos de cada empresa y sus usuarios son privados. Compartir la cuenta del arnés no separa por sí solo esos datos ni las autorizaciones del ERP.

Documentación: `docs/distribucion-github.md` y `docs/manual-uso-biank.md`.

La publicación se verifica por su release, su ZIP y las huellas del paquete; tener estos archivos no demuestra que una carpeta de usuario ya se haya actualizado. Linux ARM64 se verifica con pruebas automatizadas; Windows y macOS requieren su propia comprobación.

## Descargar

[Descargar la carpeta Biank](https://github.com/jobeto86/biank-codex/releases/latest/download/biank-core.zip). Usa ese archivo adjunto de la release; el ZIP automático de código fuente de GitHub no es el instalador. Descomprime en una carpeta nueva y ábrela en Codex.

## Mantenimiento del núcleo

Este repositorio es la fuente del núcleo distribuido. Cambia sólo el core genérico, actualiza VERSION y core.manifest si corresponde, ejecuta `python -m unittest discover -s tests -v` y genera el paquete con `python tools/build_release.py --repo jobeto86/biank-codex --output dist/biank-core.zip`. Publica una release estable cuyo tag sea `v` seguido de VERSION y adjunta `biank-core.zip` y su archivo SHA-256. El actualizador consume releases publicadas; un push a main por sí solo no actualiza clientes. Nunca vuelvas a usar un tag publicado para contenido diferente.
