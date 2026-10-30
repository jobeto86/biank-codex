import hashlib
import importlib.util
import io
import json
from pathlib import Path
import stat
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch
import zipfile

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('github_update', ROOT / 'scripts/update.py')
u = importlib.util.module_from_spec(spec)
spec.loader.exec_module(u)


def package(version='2026-10-29.1', extra=None, repo='example/biank'):
    files = {'VERSION': (version + '\n').encode(), 'AGENTS.md': b'core',
             'skills/a.md': b'new-a', 'skills/b.md': b'new-b'}
    files.update(extra or {})
    meta = {'schema': 1, 'version': version, 'repo': repo,
            'files': {name: hashlib.sha256(data).hexdigest() for name, data in files.items()}}
    return meta, files


def archive(meta, files, extra=None):
    stream = io.BytesIO()
    with zipfile.ZipFile(stream, 'w') as z:
        z.writestr('.biank-release.json', json.dumps(meta))
        for name, data in {**files, **(extra or {})}.items():
            z.writestr(name, data)
    return stream.getvalue()


class DistributionTest(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.workspace = Path(self.temp.name) / 'workspace'

    def installed(self):
        old, data = package('2026-09-30.1', {'skills/a.md': b'old-a', 'skills/b.md': b'old-b'})
        u.apply_package(self.workspace, old, data)
        return old, data

    def test_valid_zip_and_version(self):
        meta, data = package()
        self.assertEqual(u.validate_package(archive(meta, data)), (meta, data))

    def test_extra_and_missing_files_rejected(self):
        meta, data = package()
        with self.assertRaises(ValueError):
            u.validate_package(archive(meta, data, {'skills/extra.md': b'extra'}))
        del data['AGENTS.md']
        with self.assertRaises(ValueError):
            u.validate_package(archive(meta, data))

    def test_corrupt_content_rejected_before_any_write(self):
        self.installed()
        meta, data = package()
        data['skills/a.md'] = b'corrupt'
        with self.assertRaises(ValueError):
            u.apply_package(self.workspace, meta, data)
        self.assertEqual((self.workspace / 'skills/a.md').read_bytes(), b'old-a')
        self.assertEqual((self.workspace / 'VERSION').read_text().strip(), '2026-09-30.1')

    def test_traversal_private_absolute_and_reserved_paths(self):
        for name in ['skills/../memory/context.md', '../escape', '/tmp/escape',
                     'memory/context.md', 'config/users.md', '.env', '.mcp.json',
                     'manuales/local.md', 'skills/.env', 'skills\\..\\private',
                     'skills/CON.md', 'skills/PRN', 'skills/end.']:
            with self.subTest(name=name):
                meta, data = package(extra={name: b'private'})
                with self.assertRaises(ValueError):
                    u.validate_package(archive(meta, data))

    def test_symlink_zip_rejected(self):
        meta, data = package()
        stream = io.BytesIO()
        with zipfile.ZipFile(stream, 'w') as z:
            z.writestr('.biank-release.json', json.dumps(meta))
            for name, content in data.items():
                i = zipfile.ZipInfo(name)
                i.external_attr = ((stat.S_IFLNK | 0o777) if name == 'AGENTS.md' else (stat.S_IFREG | 0o644)) << 16
                z.writestr(i, content)
        with self.assertRaises(ValueError):
            u.validate_package(stream.getvalue())

    def test_duplicate_case_and_parent_collisions_rejected(self):
        for extra in [{'skills/A.md': b'case'}, {'skills': b'file'}]:
            meta, data = package(extra=extra)
            with self.assertRaises(ValueError):
                u.validate_package(archive(meta, data))

    def test_invalid_version_does_not_apply(self):
        for version in ['2026-02-30.1', 'banana', '2026-10-29.-1']:
            meta, data = package(version)
            with self.assertRaises(ValueError):
                u.apply_package(self.workspace, meta, data)
            self.assertFalse(self.workspace.exists())

    def test_equal_and_older_leave_all_bytes_unchanged(self):
        meta, data = package()
        self.assertTrue(u.apply_package(self.workspace, meta, data))
        for version in ['2026-10-29.1', '2026-10-28.99']:
            meta2, data2 = package(version, {'AGENTS.md': b'not applied'})
            self.assertFalse(u.apply_package(self.workspace, meta2, data2))
        self.assertEqual((self.workspace / 'AGENTS.md').read_bytes(), b'core')

    def test_two_companies_preserve_local_files_and_custom_skill(self):
        for company in ['one', 'two']:
            self.workspace = Path(self.temp.name) / company
            self.installed()
            local = {'memory/context.md': (company + ' memoria anterior áéíóú\n').encode('utf-8') * 300,
                     'memory/backlog.md': b'open task | owner | next step | evidence',
                     'memory/backlog_archivo.md': b'closed task | decision | receipt',
                     'memory/sessions/2026-10-28_previous.md': b'legacy session evidence',
                     'memory/sessions/.session_incomplete': b'legacy marker',
                     'config/users.md': b'local config',
                     'manuales/process.md': b'local manual', '.env': b'synthetic fixture',
                     '.mcp.json': b'{"local": true}', 'skills/custom.md': b'own skill'}
            for name, content in local.items():
                p = self.workspace / name
                p.parent.mkdir(parents=True, exist_ok=True)
                p.write_bytes(content)
            meta, data = package()
            self.assertTrue(u.apply_package(self.workspace, meta, data))
            for name, content in local.items():
                self.assertEqual((self.workspace / name).read_bytes(), content)
            self.assertEqual((self.workspace / 'skills/a.md').read_bytes(), b'new-a')

    def test_symlink_destination_and_parent_preserve_outside_file(self):
        for parent in [False, True]:
            self.workspace = Path(self.temp.name) / ('parent' if parent else 'file')
            self.installed()
            outside = Path(self.temp.name) / 'outside'
            outside.mkdir(exist_ok=True)
            target = outside / 'a.md'
            target.write_bytes(b'outside private')
            if parent:
                (self.workspace / 'skills/a.md').unlink()
                (self.workspace / 'skills/b.md').unlink()
                (self.workspace / 'skills').rmdir()
                (self.workspace / 'skills').symlink_to(outside, target_is_directory=True)
            else:
                (self.workspace / 'skills/a.md').unlink()
                (self.workspace / 'skills/a.md').symlink_to(target)
            with self.assertRaises(ValueError):
                u.apply_package(self.workspace, *package())
            self.assertEqual(target.read_bytes(), b'outside private')

    def test_rollback_restores_entire_old_core(self):
        old, data = self.installed()
        before = {p.relative_to(self.workspace).as_posix(): p.read_bytes()
                  for p in self.workspace.rglob('*') if p.is_file()}
        original = u._replace
        failed = False
        def fault(source, target):
            nonlocal failed
            if Path(target) == self.workspace / 'skills/b.md' and not failed:
                failed = True
                raise OSError('simulated disk failure')
            return original(source, target)
        with patch.object(u, '_replace', fault):
            with self.assertRaises(OSError):
                u.apply_package(self.workspace, *package(extra={'skills/new.md': b'new'}))
        for name, content in before.items():
            self.assertEqual((self.workspace / name).read_bytes(), content)
        self.assertFalse((self.workspace / 'skills/new.md').exists())
        self.assertFalse((self.workspace / u.JOURNAL).exists())

    def test_crash_recovers_even_when_github_is_offline(self):
        self.installed()
        meta, data = package()
        zipped = Path(self.temp.name) / 'new.zip'
        zipped.write_bytes(archive(meta, data))
        script = '''import importlib.util, pathlib, os, sys
s=importlib.util.spec_from_file_location('u',sys.argv[1]);u=importlib.util.module_from_spec(s);s.loader.exec_module(u)
w=pathlib.Path(sys.argv[2]); original=u._replace
def crash(a,b):
 if pathlib.Path(b)==w/'skills/b.md':os._exit(87)
 return original(a,b)
u._replace=crash
u.apply_package(w,*u.validate_package(pathlib.Path(sys.argv[3]).read_bytes()))
'''
        result = subprocess.run([sys.executable, '-c', script, str(ROOT / 'scripts/update.py'),
                                 str(self.workspace), str(zipped)], capture_output=True)
        self.assertEqual(result.returncode, 87, result.stderr.decode())
        self.assertTrue((self.workspace / u.JOURNAL).exists())
        with patch.object(u, 'ROOT', self.workspace), patch.object(u, 'fetch_release', side_effect=OSError('offline')):
            self.assertEqual(u.main(['--repo', 'example/biank']), 2)
        self.assertEqual((self.workspace / 'skills/a.md').read_bytes(), b'old-a')
        self.assertEqual((self.workspace / 'skills/b.md').read_bytes(), b'old-b')
        self.assertFalse((self.workspace / u.JOURNAL).exists())

    def test_new_core_path_does_not_claim_custom_file(self):
        self.installed()
        own = self.workspace / 'skills/new.md'
        own.write_bytes(b'own business skill')
        with self.assertRaises(ValueError):
            u.apply_package(self.workspace, *package(extra={'skills/new.md': b'new core'}))
        self.assertEqual(own.read_bytes(), b'own business skill')

    def test_repository_cannot_change_during_update(self):
        self.installed()
        with self.assertRaises(ValueError):
            u.apply_package(self.workspace, *package(repo='other/repository'))
        self.assertEqual((self.workspace / 'VERSION').read_text().strip(), '2026-09-30.1')

    def test_github_asset_and_tag_digests(self):
        meta, data = package()
        payload = archive(meta, data)
        release = {'draft': False, 'prerelease': False, 'published_at': '2026-10-29T12:00:00Z',
                   'tag_name': 'v2026-10-29.1', 'assets': [{'name': 'biank-core.zip',
                   'digest': 'sha256:' + hashlib.sha256(payload).hexdigest(),
                   'browser_download_url': 'https://github.com/example/biank/releases/download/v2026-10-29.1/biank-core.zip'}]}
        with patch.object(u, '_download', side_effect=[json.dumps(release).encode(), payload]):
            self.assertEqual(u.fetch_release('example/biank'), (meta, data))
        for changed in ['digest', 'browser_download_url']:
            broken = json.loads(json.dumps(release))
            broken['assets'][0][changed] = 'bad'
            with patch.object(u, '_download', return_value=json.dumps(broken).encode()):
                with self.assertRaises(ValueError):
                    u.fetch_release('example/biank')

    def test_check_only_does_not_change_workspace(self):
        self.installed()
        before = (self.workspace / 'VERSION').read_bytes()
        with patch.object(u, 'ROOT', self.workspace), patch.object(u, 'fetch_release', return_value=package()):
            self.assertEqual(u.main(['--check']), 0)
        self.assertEqual((self.workspace / 'VERSION').read_bytes(), before)


if __name__ == '__main__':
    unittest.main()
