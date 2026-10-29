import importlib.util
import io
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest
import zipfile

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('builder', ROOT / 'tools/build_release.py')
builder = importlib.util.module_from_spec(spec)
spec.loader.exec_module(builder)
spec = importlib.util.spec_from_file_location('update', ROOT / 'scripts/update.py')
u = importlib.util.module_from_spec(spec)
spec.loader.exec_module(u)


class InstallationTest(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.zipped = self.root / 'biank-core.zip'
        self.meta, self.digest = builder.build(ROOT, self.zipped, 'example/biank')
        self.source = self.root / 'extracted'
        with zipfile.ZipFile(self.zipped) as z:
            z.extractall(self.source)

    def run_setup(self, target):
        return subprocess.run([sys.executable, str(self.source / 'setup.py'), '--workspace', str(target)],
                              capture_output=True, text=True, timeout=30)

    def test_reproducible_package_contains_no_private_paths_or_history(self):
        other = self.root / 'second.zip'
        _, digest = builder.build(ROOT, other, 'example/biank')
        self.assertEqual(digest, self.digest)
        meta, data = u.validate_package(self.zipped.read_bytes())
        for name in data:
            self.assertFalse(name.startswith(('memory/', 'config/', 'manuales/', '.git', '.env', '.mcp', 'seed/')))
        self.assertNotIn('mcp-bridge.js', data)
        self.assertNotIn('scripts/login.py', data)
        self.assertIn('scripts/update.py', data)
        self.assertIn('setup.py', data)
        self.assertIn('AGENTS.md', data)

    def test_fresh_extracted_folder_installs_then_is_idempotent(self):
        result = self.run_setup(self.source)
        self.assertEqual(result.returncode, 0, result.stderr)
        for directory in ['memory', 'config', 'manuales', 'entregables']:
            self.assertTrue((self.source / directory).is_dir())
        marker = json.loads((self.source / '.biank-installed.json').read_text())
        self.assertEqual(marker['version'], self.meta['version'])
        self.assertFalse((self.source / '.mcp.json').exists())
        self.assertFalse((self.source / '.env').exists())
        (self.source / 'memory/context.md').write_text('own memory')
        second = self.run_setup(self.source)
        self.assertEqual(second.returncode, 0, second.stderr)
        self.assertEqual((self.source / 'memory/context.md').read_text(), 'own memory')

    def test_install_into_existing_workspace_preserves_config(self):
        target = self.root / 'client'
        (target / 'memory').mkdir(parents=True)
        (target / 'memory/context.md').write_text('client notes')
        (target / '.mcp.json').write_text('{"native":"connection"}')
        result = self.run_setup(target)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual((target / 'memory/context.md').read_text(), 'client notes')
        self.assertEqual((target / '.mcp.json').read_text(), '{"native":"connection"}')
        self.assertTrue((target / '.biank-installed.json').exists())

    def test_corrupt_source_never_marks_installed(self):
        (self.source / 'skills/INDEX.md').write_text('corrupted')
        target = self.root / 'client'
        result = self.run_setup(target)
        self.assertEqual(result.returncode, 2)
        self.assertFalse((target / '.biank-installed.json').exists())
        self.assertFalse((target / 'AGENTS.md').exists())

    def test_same_version_missing_core_does_not_mark_verified(self):
        target = self.root / 'client'
        target.mkdir()
        (target / 'VERSION').write_text(self.meta['version'])
        result = self.run_setup(target)
        self.assertEqual(result.returncode, 2)
        self.assertFalse((target / '.biank-installed.json').exists())

    def test_known_legacy_hash_migrates_but_unknown_collision_does_not(self):
        legacy = self.root / 'legacy-source'
        legacy.mkdir()
        (legacy / 'AGENTS.md').write_bytes(b'known old generic core')
        zip_path = self.root / 'migration.zip'
        builder.build(ROOT, zip_path, 'example/biank', [legacy])
        meta, data = u.validate_package(zip_path.read_bytes())
        target = self.root / 'legacy-client'
        target.mkdir()
        (target / 'VERSION').write_text('2026-09-30.1')
        (target / 'AGENTS.md').write_bytes(b'known old generic core')
        (target / 'memory').mkdir()
        (target / 'memory/context.md').write_text('own memory')
        self.assertTrue(u.apply_package(target, meta, data))
        self.assertEqual((target / 'memory/context.md').read_text(), 'own memory')
        unknown = self.root / 'custom-client'
        unknown.mkdir()
        (unknown / 'VERSION').write_text('2026-09-30.1')
        (unknown / 'AGENTS.md').write_bytes(b'own custom instruction')
        with self.assertRaises(ValueError):
            u.apply_package(unknown, meta, data)
        self.assertEqual((unknown / 'AGENTS.md').read_bytes(), b'own custom instruction')


if __name__ == '__main__':
    unittest.main()
