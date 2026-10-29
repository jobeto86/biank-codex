#!/usr/bin/env python3
"""Índice local de archivos declarados por el usuario (BK-1343).

Guarda sólo ruta y metadatos del filesystem. Nunca lee ni persiste contenido.
Todo queda bajo memory/ y está excluido de Git.
"""
from __future__ import annotations

import argparse
import json
import os
import sys
import unicodedata
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
MEMORY = ROOT / "memory"
CONFIG = MEMORY / "file-index-config.json"
INDEX = MEMORY / "file-index.json"
MAX_RESULTS = 25


def _load(path: Path, default):
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError, TypeError):
        return default


def _write(path: Path, value) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n",
                   encoding="utf-8")
    os.replace(tmp, path)


def _normal(text: str) -> str:
    normalized = unicodedata.normalize("NFKD", text.casefold())
    return "".join(c for c in normalized if not unicodedata.combining(c))


def configured_folders() -> list[Path]:
    raw = _load(CONFIG, {"folders": []})
    folders = raw.get("folders", []) if isinstance(raw, dict) else []
    result = []
    for value in folders:
        try:
            folder = Path(value).expanduser().resolve()
        except (OSError, TypeError):
            continue
        if folder.is_dir() and folder not in result:
            result.append(folder)
    return result


def add_folder(value: str) -> Path:
    folder = Path(value).expanduser().resolve()
    if not folder.is_dir():
        raise ValueError(f"La carpeta no existe o no es accesible: {folder}")
    broad_roots = {Path(folder.anchor).resolve(), Path.home().resolve()}
    if folder in broad_roots:
        raise ValueError(
            "Elige una carpeta concreta; no se permite indexar el disco ni "
            "todo el perfil del usuario.")
    folders = configured_folders()
    if folder not in folders:
        folders.append(folder)
    _write(CONFIG, {"folders": [str(p) for p in folders]})
    return folder


def scan() -> dict:
    folders = configured_folders()
    entries = []
    for folder in folders:
        for path in folder.rglob("*"):
            try:
                if not path.is_file() or path.is_symlink():
                    continue
                stat = path.stat()
                entries.append({
                    "name": path.name,
                    "path": str(path),
                    "folder": str(folder),
                    "extension": path.suffix.casefold(),
                    "size": stat.st_size,
                    "modified_at": datetime.fromtimestamp(
                        stat.st_mtime, timezone.utc).isoformat(),
                })
            except OSError:
                continue
    entries.sort(key=lambda item: (_normal(item["name"]), item["path"]))
    payload = {
        "schema": 1,
        "indexed_at": datetime.now(timezone.utc).isoformat(),
        "folders": [str(p) for p in folders],
        "entries": entries,
    }
    _write(INDEX, payload)
    return payload


def search(query: str) -> list[dict]:
    index = _load(INDEX, {"entries": []})
    terms = [term for term in _normal(query).split() if term]
    if not terms:
        return []
    matches = []
    for entry in index.get("entries", []):
        haystack = _normal(f'{entry.get("name", "")} {entry.get("path", "")}')
        if all(term in haystack for term in terms):
            matches.append(entry)
    return matches[:MAX_RESULTS]


def status() -> dict:
    folders = configured_folders()
    index = _load(INDEX, {})
    return {
        "configured": bool(folders),
        "folders": len(folders),
        "indexed": INDEX.is_file(),
        "entries": len(index.get("entries", [])),
        "indexed_at": index.get("indexed_at"),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Índice local de archivos de Biank")
    sub = parser.add_subparsers(dest="command", required=True)
    add = sub.add_parser("add-folder")
    add.add_argument("path")
    sub.add_parser("scan")
    find = sub.add_parser("search")
    find.add_argument("query")
    sub.add_parser("status")
    args = parser.parse_args()
    try:
        if args.command == "add-folder":
            print(json.dumps({"added": str(add_folder(args.path))}, ensure_ascii=False))
        elif args.command == "scan":
            value = scan()
            print(json.dumps({"folders": len(value["folders"]),
                              "entries": len(value["entries"])}, ensure_ascii=False))
        elif args.command == "search":
            print(json.dumps(search(args.query), ensure_ascii=False, indent=2))
        else:
            print(json.dumps(status(), ensure_ascii=False))
        return 0
    except ValueError as exc:
        print(str(exc), file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
