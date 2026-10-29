#!/usr/bin/env python3
"""Install a verified Biank core without changing local data or credentials."""
import argparse
import importlib.util
import json
from pathlib import Path
import sys

PACKAGE_ROOT = Path(__file__).absolute().parent
spec = importlib.util.spec_from_file_location("biank_update", PACKAGE_ROOT / "scripts" / "update.py")
update = importlib.util.module_from_spec(spec)
spec.loader.exec_module(update)


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--workspace", type=Path, default=PACKAGE_ROOT)
    parser.add_argument("--package", type=Path, help="Instalar desde ZIP verificado")
    args = parser.parse_args(argv)
    try:
        if args.package:
            metadata, files = update.validate_package(args.package.read_bytes())
        else:
            metadata_path = update._target(PACKAGE_ROOT, update.METADATA)
            metadata = update._json_loads(metadata_path.read_text(encoding="utf-8"))
            files = {name: update._target(PACKAGE_ROOT, name).read_bytes() for name in metadata["files"]}
            update._validate_snapshot(metadata, files)
        workspace = update._safe_workspace(args.workspace)
        marker = update._target(workspace, ".biank-installed.json")
        # Validate local directory destinations before any installation or mkdir.
        for name in ("memory", "config", "manuales", "entregables"):
            path = workspace / name
            if path.is_symlink() or (path.exists() and not path.is_dir()):
                raise ValueError("Un directorio local es un symlink o archivo; no se modifica.")
        changed = update.apply_package(workspace, metadata, files)
        installed = update._local_metadata(workspace)
        if installed is None:
            raise ValueError("La carpeta aún no tiene un núcleo reconocido; instala en una carpeta nueva.")
        installed_files = {name: update._target(workspace, name).read_bytes()
                           for name in installed["files"]}
        update._validate_snapshot(installed, installed_files)
        for name in ("memory", "config", "manuales", "entregables"):
            (workspace / name).mkdir(parents=True, exist_ok=True)
        marker_content = {"schema": 1, "version": installed["version"], "repo": installed["repo"]}
        update._atomic_write(marker, (json.dumps(marker_content, sort_keys=True) + "\n").encode("utf-8"))
        print("Biank " + installed["version"] + (" instalado en " if changed else " verificado en ") + str(workspace))
        print("Abre esta carpeta con tu arnés. La conexión MCP se autoriza en el arnés; no se crean credenciales.")
        return 0
    except Exception as error:
        print("Instalación omitida: " + str(error), file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
