#!/usr/bin/env python3
"""Update only the versioned Biank core from a verified public GitHub release.

No ERP/GitHub credential is read or written. Python 3.10+, standard library only.
"""
import argparse
import contextlib
import datetime
import hashlib
import io
import json
import os
from pathlib import Path, PurePosixPath
import re
import shutil
import stat
import sys
import tempfile
import urllib.parse
import urllib.request
import zipfile

ROOT = Path(__file__).absolute().parent.parent
METADATA = ".biank-release.json"
JOURNAL = ".biank-update-journal.json"
MAX_FILE = 2 * 1024 * 1024
MAX_TOTAL = 20 * 1024 * 1024
MAX_FILES = 1000
ROOT_FILES = {"AGENTS.md", "CLAUDE.md", "VERSION", "core.manifest", "README.md",
              "setup.py", "setup.sh", "setup.bat", "setup.ps1"}
CORE_DIRS = {"identity", "protocols", "scripts", "skills", "templates", "docs"}
REPO_PATTERN = re.compile(r"[A-Za-z0-9][A-Za-z0-9_.-]*/[A-Za-z0-9][A-Za-z0-9_.-]*\Z")
VERSION_PATTERN = re.compile(r"(\d{4})-(\d{2})-(\d{2})(?:\.(\d+))?\Z")


def parse_version(value):
    match = VERSION_PATTERN.fullmatch(value) if isinstance(value, str) else None
    if not match:
        raise ValueError("Versión inválida; se requiere YYYY-MM-DD[.revisión].")
    year, month, day, revision = match.groups()
    date = datetime.date(int(year), int(month), int(day))
    return date.year, date.month, date.day, int(revision or 0)


def _core_path(name):
    if not isinstance(name, str) or not name or "\\" in name or ":" in name:
        raise ValueError("Ruta de núcleo inválida.")
    parts = name.split("/")
    if any(not part or part in (".", "..") or part.startswith(".") or part.endswith((".", " "))
           or any(ord(c) < 32 or c in '<>"|?*' for c in part) for part in parts):
        raise ValueError("Ruta privada, absoluta o no normalizada rechazada.")
    if PurePosixPath(name).is_absolute() or "/".join(parts) != name:
        raise ValueError("Ruta absoluta o no normalizada rechazada.")
    reserved = {"CON", "PRN", "AUX", "NUL"} | {f"{prefix}{n}" for prefix in ("COM", "LPT") for n in range(1, 10)}
    if any(part.split(".", 1)[0].upper() in reserved for part in parts):
        raise ValueError("Nombre de archivo reservado en Windows.")
    if len(parts) == 1:
        allowed = name in ROOT_FILES
    else:
        allowed = parts[0] in CORE_DIRS
    if not allowed:
        raise ValueError("Archivo fuera del núcleo distribuible.")
    return name


def _json_loads(content):
    def pairs(items):
        result = {}
        for key, value in items:
            if key in result:
                raise ValueError("Clave JSON duplicada rechazada.")
            result[key] = value
        return result
    return json.loads(content, object_pairs_hook=pairs)


def _validate_snapshot(metadata, files):
    if not isinstance(metadata, dict) or type(metadata.get("schema")) is not int or metadata["schema"] != 1:
        raise ValueError("Formato de release desconocido.")
    parse_version(metadata.get("version"))
    if not isinstance(metadata.get("repo"), str) or not REPO_PATTERN.fullmatch(metadata["repo"]):
        raise ValueError("Repositorio de release inválido.")
    hashes = metadata.get("files")
    if not isinstance(hashes, dict) or not 1 <= len(hashes) <= MAX_FILES or set(hashes) != set(files):
        raise ValueError("El paquete no coincide exactamente con su manifiesto.")
    if "VERSION" not in files:
        raise ValueError("El paquete no contiene VERSION.")
    casefolded = set()
    total = 0
    for name, expected in hashes.items():
        _core_path(name)
        if name.casefold() in casefolded:
            raise ValueError("Rutas duplicadas o incompatibles con Windows.")
        casefolded.add(name.casefold())
        if not isinstance(expected, str) or not re.fullmatch(r"[0-9a-f]{64}", expected):
            raise ValueError("SHA-256 inválido en manifiesto.")
        content = files[name]
        if not isinstance(content, bytes) or len(content) > MAX_FILE:
            raise ValueError("Archivo de núcleo demasiado grande o inválido.")
        total += len(content)
        if total > MAX_TOTAL or hashlib.sha256(content).hexdigest() != expected:
            raise ValueError("La integridad del paquete no coincide con el manifiesto.")
    names = set(files)
    for name in names:
        if any("/".join(name.split("/")[:n]) in names for n in range(1, len(name.split("/")))):
            raise ValueError("Una ruta de archivo también figura como directorio.")
    legacy = metadata.get("legacyFiles", {})
    if not isinstance(legacy, dict) or len(legacy) > MAX_FILES:
        raise ValueError("Huellas de migración legada inválidas.")
    for name, digests in legacy.items():
        _core_path(name)
        if name not in files or not isinstance(digests, list) or not 1 <= len(digests) <= 50:
            raise ValueError("Huellas de migración legada inválidas.")
        if any(not isinstance(digest, str) or not re.fullmatch(r"[0-9a-f]{64}", digest) for digest in digests):
            raise ValueError("SHA-256 de migración legada inválido.")
    if files["VERSION"].decode("utf-8").strip() != metadata["version"]:
        raise ValueError("VERSION no coincide con la release.")


def validate_package(data):
    """Return (metadata, files) only for an exact, bounded, verified ZIP."""
    if not isinstance(data, bytes) or len(data) > MAX_TOTAL + 2 * 1024 * 1024:
        raise ValueError("Paquete ZIP demasiado grande o inválido.")
    with zipfile.ZipFile(io.BytesIO(data)) as archive:
        entries = archive.infolist()
        names = [entry.filename for entry in entries]
        if len(names) > MAX_FILES + 1 or len(set(names)) != len(names) or METADATA not in names:
            raise ValueError("ZIP con entradas duplicadas, excesivas o sin manifiesto.")
        total = 0
        for entry in entries:
            mode = entry.external_attr >> 16
            if entry.is_dir() or stat.S_ISLNK(mode) or entry.flag_bits & 1:
                raise ValueError("El ZIP no admite directorios, symlinks ni cifrado.")
            if stat.S_IFMT(mode) not in (0, stat.S_IFREG):
                raise ValueError("Tipo de archivo ZIP no permitido.")
            if entry.filename != METADATA:
                _core_path(entry.filename)
            if entry.file_size > MAX_FILE:
                raise ValueError("Archivo ZIP demasiado grande.")
            total += entry.file_size
            if total > MAX_TOTAL:
                raise ValueError("Contenido ZIP demasiado grande.")
        metadata = _json_loads(archive.read(METADATA))
        files = {name: archive.read(name) for name in names if name != METADATA}
    _validate_snapshot(metadata, files)
    return metadata, files


def _safe_workspace(workspace):
    workspace = Path(os.path.abspath(workspace))
    for path in (workspace, *workspace.parents):
        if path.is_symlink():
            raise ValueError("El workspace o sus padres no pueden ser symlinks.")
    if workspace.exists() and not workspace.is_dir():
        raise ValueError("El workspace no es un directorio.")
    return workspace


def _target(workspace, relative):
    if relative not in (METADATA, JOURNAL, ".biank-update.lock", ".biank-installed.json"):
        _core_path(relative)
    path = workspace
    for part in relative.split("/"):
        path = path / part
        if path.is_symlink():
            raise ValueError("Un archivo o directorio destino es un symlink.")
        if path != workspace / relative and path.exists() and not path.is_dir():
            raise ValueError("Un padre de archivo no es un directorio.")
    if path.exists() and not path.is_file():
        raise ValueError("El archivo destino no es regular.")
    return path


def _replace(source, target):
    """Single injection point for transactional fault tests."""
    os.replace(source, target)


def _sync_directory(path):
    if os.name != "nt":
        descriptor = os.open(path, os.O_RDONLY)
        try:
            os.fsync(descriptor)
        finally:
            os.close(descriptor)


def _atomic_write(path, content):
    path.parent.mkdir(parents=True, exist_ok=True)
    descriptor, temporary = tempfile.mkstemp(prefix=".biank-write-", dir=path.parent)
    try:
        with os.fdopen(descriptor, "wb") as stream:
            stream.write(content)
            stream.flush()
            os.fsync(stream.fileno())
        _replace(temporary, path)
        _sync_directory(path.parent)
    finally:
        Path(temporary).unlink(missing_ok=True)


def _write_journal(workspace, journal):
    _atomic_write(_target(workspace, JOURNAL), json.dumps(journal, sort_keys=True).encode("utf-8"))


@contextlib.contextmanager
def _locked(workspace):
    lock_path = _target(workspace, ".biank-update.lock")
    with lock_path.open("a+b") as stream:
        try:
            if os.name == "nt":
                import msvcrt
                stream.seek(0)
                if not stream.read(1):
                    stream.write(b"0")
                    stream.flush()
                stream.seek(0)
                msvcrt.locking(stream.fileno(), msvcrt.LK_NBLCK, 1)
            else:
                import fcntl
                fcntl.flock(stream, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except OSError as error:
            raise RuntimeError("Ya hay una actualización de Biank en curso.") from error
        try:
            yield
        finally:
            if os.name == "nt":
                stream.seek(0)
                msvcrt.locking(stream.fileno(), msvcrt.LK_UNLCK, 1)
            else:
                fcntl.flock(stream, fcntl.LOCK_UN)


def _recover(workspace):
    journal_path = _target(workspace, JOURNAL)
    if not journal_path.exists():
        return
    journal = _json_loads(journal_path.read_text(encoding="utf-8"))
    name = journal.get("directory", "")
    if not isinstance(name, str) or not re.fullmatch(r"\.biank-update-[A-Za-z0-9_-]+", name):
        raise RuntimeError("Journal de recuperación inválido; no se modifica el workspace.")
    directory = workspace / name
    if directory.is_symlink() or not directory.is_dir():
        raise RuntimeError("Falta el respaldo de una actualización interrumpida.")
    if journal.get("phase") not in ("pending", "committed"):
        raise RuntimeError("Estado de recuperación desconocido.")
    before = journal.get("before")
    if not isinstance(before, dict) or not before or len(before) > MAX_FILES + 1:
        raise RuntimeError("Journal de recuperación incompleto.")
    # Validate every target/backup before touching any of them.
    targets = {}
    for relative, existed in before.items():
        if relative != METADATA:
            _core_path(relative)
        if type(existed) is not bool:
            raise RuntimeError("Journal de recuperación inválido.")
        target = _target(workspace, relative)
        backup = directory / "backup" / relative
        if existed and journal.get("phase") != "committed":
            current = directory
            for part in ("backup", *relative.split("/")):
                current = current / part
                if current.is_symlink():
                    raise RuntimeError("Respaldo de recuperación inseguro.")
            if not backup.is_file():
                raise RuntimeError("Respaldo de recuperación incompleto.")
        targets[relative] = target
    if journal.get("phase") != "committed":
        for relative, target in targets.items():
            if before[relative]:
                backup = directory / "backup" / relative
                _atomic_write(target, backup.read_bytes())
                shutil.copystat(backup, target)
            else:
                target.unlink(missing_ok=True)
        _sync_directory(workspace)
    # Remove journal first: failure after this point only leaves harmless backup files.
    journal_path.unlink()
    _sync_directory(workspace)
    shutil.rmtree(directory)


def _newer(workspace, version):
    version_path = _target(workspace, "VERSION")
    if not version_path.exists():
        return True
    return parse_version(version) > parse_version(version_path.read_text(encoding="utf-8").strip())


def recover_pending(workspace):
    """Restore an interrupted transaction before any network operation."""
    workspace = _safe_workspace(workspace)
    if _target(workspace, JOURNAL).exists():
        with _locked(workspace):
            _recover(workspace)


def _local_metadata(workspace):
    path = _target(workspace, METADATA)
    if not path.exists():
        return None
    metadata = _json_loads(path.read_text(encoding="utf-8"))
    if not isinstance(metadata, dict) or metadata.get("schema") != 1:
        raise ValueError("Los metadatos locales no son válidos; no se modifica la instalación.")
    if not isinstance(metadata.get("repo"), str) or not REPO_PATTERN.fullmatch(metadata["repo"]):
        raise ValueError("El origen de la instalación no es válido.")
    parse_version(metadata.get("version"))
    if not isinstance(metadata.get("files"), dict):
        raise ValueError("Falta el manifiesto de la instalación local.")
    return metadata


def _same_origin(previous, metadata):
    if previous is not None and previous["repo"] != metadata["repo"]:
        raise ValueError("El origen del paquete difiere del instalado; se requiere una migración explícita.")


def apply_package(workspace, metadata, files):
    """Apply all core files or restore all of them; return False for no upgrade."""
    _validate_snapshot(metadata, files)
    workspace = _safe_workspace(workspace)
    _target(workspace, METADATA)
    journal_path = _target(workspace, JOURNAL)
    if not journal_path.exists():
        _same_origin(_local_metadata(workspace), metadata)
        if not _newer(workspace, metadata["version"]):
            return False
    workspace.mkdir(parents=True, exist_ok=True)
    with _locked(workspace):
        _recover(workspace)
        previous = _local_metadata(workspace)
        _same_origin(previous, metadata)
        if not _newer(workspace, metadata["version"]):
            return False
        ordered = sorted(name for name in files if name != "VERSION") + [METADATA, "VERSION"]
        contents = dict(files)
        contents[METADATA] = (json.dumps(metadata, sort_keys=True, indent=2) + "\n").encode("utf-8")
        targets = {name: _target(workspace, name) for name in ordered}
        # New core paths must not claim existing local/custom files.
        previous_files = previous["files"] if previous is not None else {}
        for name in files:
            target = targets[name]
            if name == "VERSION" or name in previous_files or not target.exists():
                continue
            current = target.read_bytes()
            if current == contents[name]:
                continue
            legacy_hashes = metadata.get("legacyFiles", {}).get(name, []) if previous is None else []
            if hashlib.sha256(current).hexdigest() not in legacy_hashes:
                raise ValueError("Un archivo local colisiona con una ruta nueva o legada no reconocida del core; se conserva. Instala en una carpeta nueva o solicita una migración explícita.")
        directory = Path(tempfile.mkdtemp(prefix=".biank-update-", dir=workspace))
        journal = {"directory": directory.name, "phase": "pending", "before": {}}
        try:
            for name in ordered:
                staged = directory / "stage" / name
                _atomic_write(staged, contents[name])
                existed = targets[name].exists()
                journal["before"][name] = existed
                if existed:
                    backup = directory / "backup" / name
                    backup.parent.mkdir(parents=True, exist_ok=True)
                    shutil.copy2(targets[name], backup)
                    with backup.open("rb") as stream:
                        os.fsync(stream.fileno())
            # Persist backup directory entries before making the journal durable.
            for folder in sorted((p for p in directory.rglob("*") if p.is_dir()),
                                 key=lambda p: len(p.parts), reverse=True):
                _sync_directory(folder)
            _sync_directory(directory)
            _write_journal(workspace, journal)
            for name in ordered:
                # Revalidate symlinks immediately before replacing a destination.
                target = _target(workspace, name)
                target.parent.mkdir(parents=True, exist_ok=True)
                _replace(directory / "stage" / name, target)
                _sync_directory(target.parent)
            journal["phase"] = "committed"
            _write_journal(workspace, journal)
        except BaseException:
            if journal_path.exists():
                _recover(workspace)
            else:
                shutil.rmtree(directory)
            raise
        _recover(workspace)
    return True


class _GitHubRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, request, fp, code, message, headers, new_url):
        parsed = urllib.parse.urlsplit(new_url)
        allowed = {"github.com", "api.github.com", "release-assets.githubusercontent.com", "objects.githubusercontent.com"}
        if parsed.scheme != "https" or parsed.hostname not in allowed or parsed.username or parsed.password:
            raise ValueError("Redirección de descarga fuera de GitHub rechazada.")
        return super().redirect_request(request, fp, code, message, headers, new_url)


def _download(url, limit):
    request = urllib.request.Request(url, headers={"Accept": "application/vnd.github+json", "User-Agent": "Biank-Core-Updater/1"})
    opener = urllib.request.build_opener(_GitHubRedirect())
    with opener.open(request, timeout=20) as response:
        data = response.read(limit + 1)
    if len(data) > limit:
        raise ValueError("Respuesta de GitHub demasiado grande.")
    return data


def fetch_release(repo):
    if not isinstance(repo, str) or not REPO_PATTERN.fullmatch(repo):
        raise ValueError("Indica el repositorio público como owner/repo.")
    release = _json_loads(_download(f"https://api.github.com/repos/{repo}/releases/latest", MAX_FILE))
    if release.get("draft") or release.get("prerelease") or not release.get("published_at"):
        raise ValueError("No se acepta una release sin publicación estable.")
    assets = [asset for asset in release.get("assets", []) if asset.get("name") == "biank-core.zip"]
    if len(assets) != 1:
        raise ValueError("La release no contiene un único biank-core.zip.")
    asset = assets[0]
    digest = asset.get("digest", "")
    if not isinstance(digest, str) or not re.fullmatch(r"sha256:[0-9a-f]{64}", digest):
        raise ValueError("GitHub no informa un SHA-256 verificable del paquete.")
    url = asset.get("browser_download_url", "")
    parsed = urllib.parse.urlsplit(url)
    if parsed.scheme != "https" or parsed.netloc != "github.com" or not parsed.path.startswith(f"/{repo}/releases/download/"):
        raise ValueError("La URL de descarga no pertenece al repositorio esperado.")
    data = _download(url, MAX_TOTAL + 2 * 1024 * 1024)
    if hashlib.sha256(data).hexdigest() != digest[7:]:
        raise ValueError("El ZIP descargado no coincide con el digest de GitHub.")
    metadata, files = validate_package(data)
    if metadata["repo"] != repo or release.get("tag_name") != "v" + metadata["version"]:
        raise ValueError("El paquete no corresponde al repositorio/tag solicitado.")
    return metadata, files


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", help="Repositorio público owner/repo; nunca requiere token")
    parser.add_argument("--check", action="store_true", help="Sólo comprobar; no aplicar")
    parser.add_argument("--package", type=Path, help="ZIP local para instalación o prueba")
    args = parser.parse_args(argv)
    try:
        workspace = _safe_workspace(ROOT)
        recover_pending(workspace)
        previous = _local_metadata(workspace)
        repo = args.repo
        if previous is not None:
            if repo and repo != previous["repo"]:
                raise ValueError("--repo no puede cambiar el origen de una instalación existente.")
            repo = previous["repo"]
        if args.package:
            metadata, files = validate_package(args.package.read_bytes())
            if repo and metadata["repo"] != repo:
                raise ValueError("El paquete local pertenece a otro repositorio.")
        else:
            if not repo:
                raise ValueError("Falta el repositorio de distribución; usa --repo owner/repo.")
            metadata, files = fetch_release(repo)
        if args.check:
            newer = _newer(workspace, metadata["version"])
            print("[Biank] " + ("Disponible: " if newer else "Sin actualización: ") + metadata["version"])
        elif apply_package(workspace, metadata, files):
            print("[Biank] Actualizado a " + metadata["version"] + ". Relee identidad e índice antes de operar.")
        else:
            print("[Biank] Ya estás en esta versión o una posterior.")
        return 0
    except Exception as error:
        pending = Path(ROOT) / JOURNAL
        if pending.exists():
            print("[Biank] Recuperación pendiente: no operes con este núcleo hasta reparar la actualización. " + str(error), file=sys.stderr)
        else:
            print("[Biank] Actualización omitida; se conserva el núcleo local. " + str(error), file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
