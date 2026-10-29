#!/usr/bin/env python3
"""Build a distribution from the explicit core allowlist, never from the Git tree."""
import argparse
import hashlib
import importlib.util
import io
import json
from pathlib import Path, PurePosixPath
import re
import zipfile

ROOT = Path(__file__).resolve().parents[1]
ROOT_FILES = {'AGENTS.md', 'CLAUDE.md', 'VERSION', 'core.manifest', 'README.md',
              'setup.py', 'setup.sh', 'setup.bat', 'setup.ps1'}
CORE_DIRS = {'identity', 'protocols', 'scripts', 'skills', 'templates', 'docs'}


def build(root, output, repo, legacy_directories=()):
    root, output = Path(root), Path(output)
    if not re.fullmatch(r'[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+', repo):
        raise ValueError('Repositorio inválido: se requiere owner/repo')
    entries = ['VERSION', 'core.manifest']
    for line in (root / 'core.manifest').read_text(encoding='utf8').splitlines():
        line = line.strip()
        if line and not line.startswith('#'):
            if line in entries:
                raise ValueError('Manifiesto con archivo duplicado')
            entries.append(line)
    files = {}
    for name in entries:
        p = PurePosixPath(name)
        if (str(p) != name or p.is_absolute() or '..' in p.parts or '\\' in name
                or (name not in ROOT_FILES and p.parts[0] not in CORE_DIRS)
                or any(part.startswith('.') for part in p.parts)):
            raise ValueError('Ruta fuera del núcleo permitido')
        path = root / name
        if any(parent.is_symlink() for parent in [path, *path.parents]):
            raise ValueError('Symlink no distribuible')
        data = path.read_bytes()
        data.decode('utf8')
        files[name] = data
    metadata = {'schema': 1, 'version': files['VERSION'].decode().strip(), 'repo': repo,
                'files': {name: hashlib.sha256(data).hexdigest() for name, data in sorted(files.items())}}
    legacy = {}
    known = root / 'tools' / 'legacy-core-hashes.json'
    if known.exists():
        for name, hashes in json.loads(known.read_text(encoding='utf8')).items():
            if name in files:
                legacy[name] = set(hashes)
    for directory in legacy_directories:
        directory = Path(directory)
        for name in files:
            path = directory / name
            if path.is_file() and not any(p.is_symlink() for p in [path, *path.parents]):
                legacy.setdefault(name, set()).add(hashlib.sha256(path.read_bytes()).hexdigest())
    if legacy:
        metadata['legacyFiles'] = {name: sorted(hashes) for name, hashes in sorted(legacy.items())}
    files['.biank-release.json'] = (json.dumps(metadata, indent=2, sort_keys=True) + '\n').encode()
    buffer = io.BytesIO()
    with zipfile.ZipFile(buffer, 'w', compression=zipfile.ZIP_DEFLATED) as archive:
        for name, data in sorted(files.items()):
            info = zipfile.ZipInfo(name, date_time=(2026, 1, 1, 0, 0, 0))
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0o100644 << 16
            archive.writestr(info, data)
    spec = importlib.util.spec_from_file_location('biank_update', root / 'scripts/update.py')
    update = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(update)
    update.validate_package(buffer.getvalue())
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_bytes(buffer.getvalue())
    digest = hashlib.sha256(buffer.getvalue()).hexdigest()
    output.with_suffix(output.suffix + '.sha256').write_text(digest + '  ' + output.name + '\n')
    return metadata, digest


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--repo', required=True)
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--legacy-core-dir', type=Path, action='append', default=[])
    args = parser.parse_args()
    meta, digest = build(ROOT, args.output, args.repo, args.legacy_core_dir)
    print(json.dumps({'version': meta['version'], 'files': len(meta['files']),
                      'zip': str(args.output), 'sha256': digest}, ensure_ascii=False))
