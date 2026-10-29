import importlib.util
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch


ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location(
    "file_index", ROOT / "scripts" / "file_index.py")
file_index = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(file_index)


class FileIndexBk1343Test(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        base = Path(self.temp.name)
        self.docs = base / "Documentos"
        self.docs.mkdir()
        self.config = base / "config.json"
        self.index = base / "index.json"
        self.paths = patch.multiple(file_index, CONFIG=self.config, INDEX=self.index)
        self.paths.start()

    def tearDown(self):
        self.paths.stop()
        self.temp.cleanup()

    def test_requiere_carpeta_existente_y_declarada(self):
        with self.assertRaises(ValueError):
            file_index.add_folder(str(self.docs / "inexistente"))
        added = file_index.add_folder(str(self.docs))
        self.assertEqual(self.docs.resolve(), added)
        self.assertEqual([str(self.docs.resolve())],
                         json.loads(self.config.read_text())["folders"])

    def test_rechaza_raiz_y_perfil_completo(self):
        with patch.object(file_index.Path, "home", return_value=self.docs):
            with self.assertRaisesRegex(ValueError, "carpeta concreta"):
                file_index.add_folder(str(self.docs))
        with self.assertRaisesRegex(ValueError, "carpeta concreta"):
            file_index.add_folder(Path(self.docs.anchor))

    def test_indexa_metadatos_pero_nunca_contenido(self):
        secret = "contenido-que-jamas-debe-quedar-en-el-indice"
        document = self.docs / "Cotización Santiago.pdf"
        document.write_text(secret, encoding="utf-8")
        file_index.add_folder(str(self.docs))
        payload = file_index.scan()
        serialized = json.dumps(payload, ensure_ascii=False)
        self.assertEqual(1, len(payload["entries"]))
        self.assertNotIn(secret, serialized)
        self.assertEqual(".pdf", payload["entries"][0]["extension"])
        self.assertIn("modified_at", payload["entries"][0])

    def test_busqueda_es_tolerante_a_acentos(self):
        target = self.docs / "Cotización Santiago.pdf"
        target.write_bytes(b"no leer")
        file_index.add_folder(str(self.docs))
        file_index.scan()
        result = file_index.search("cotizacion santiago")
        self.assertEqual(str(target), result[0]["path"])

    def test_status_no_escanea_carpetas(self):
        file_index.add_folder(str(self.docs))
        with patch.object(Path, "rglob", side_effect=AssertionError("no escanear")):
            current = file_index.status()
        self.assertTrue(current["configured"])
        self.assertFalse(current["indexed"])

    # TSK-634: the folder installer does not install harness hooks. The old
    # warm_context wiring contract is superseded by the real installation
    # tests in test_installation_github.py; file-index behavior above remains.


if __name__ == "__main__":
    unittest.main()
