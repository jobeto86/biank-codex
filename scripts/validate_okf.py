#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
validate_okf.py — Auditoría de cumplimiento del estándar Open Knowledge Format (OKF) en manuales de Biank-Agent.
Usa únicamente la librería estándar de Python (sin dep pip).
"""
import os
import sys
import re

REQUIRED_OKF_KEYS = ["id", "type", "domain", "aliases", "tags", "last_updated", "status", "related"]

def parse_simple_yaml(yaml_str):
    data = {}
    for line in yaml_str.splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        if ":" in line:
            key, val = line.split(":", 1)
            key = key.strip()
            val = val.strip()
            # Clean comments
            if " #" in val:
                val = val.split(" #", 1)[0].strip()
            data[key] = val
    return data

def validate_file(filepath, root_dir):
    rel_path = os.path.relpath(filepath, root_dir)
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    if not content.startswith("---"):
        return False, f"Sin cabecera YAML frontmatter (debe iniciar con ---)"

    parts = content.split("---", 2)
    if len(parts) < 3:
        return False, f"Cabecera YAML frontmatter no cerrada correctamente con ---"

    yaml_block = parts[1]
    parsed_yaml = parse_simple_yaml(yaml_block)

    missing = [k for k in REQUIRED_OKF_KEYS if k not in parsed_yaml]
    if missing:
        return False, f"Llaves OKF faltantes en YAML: {missing}"

    return True, "OKF Válido"

def main():
    root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    manuales_dir = os.path.join(root_dir, "manuales")

    if not os.path.exists(manuales_dir):
        print(f"⚠️ No se encontró el directorio {manuales_dir}")
        sys.exit(0)

    files = [os.path.join(manuales_dir, f) for f in os.listdir(manuales_dir) if f.endswith(".md") and f != "README.md"]

    print("=== Auditoría OKF para Manuales Biank ===")
    print(f"Manuales encontrados: {len(files)}")

    errors = 0
    for f in files:
        rel_p = os.path.relpath(f, root_dir)
        valid, msg = validate_file(f, root_dir)
        if valid:
            print(f"✅ {rel_p} -> {msg}")
        else:
            print(f"❌ {rel_p} -> {msg}")
            errors += 1

    if errors > 0:
        print(f"\n⚠️ Hallazgos detectados: {errors} manual(es) no cumplen con el estándar OKF.")
        sys.exit(1)
    else:
        print("\n✨ Todos los manuales de la empresa cumplen con el estándar OKF.")
        sys.exit(0)

if __name__ == "__main__":
    main()
