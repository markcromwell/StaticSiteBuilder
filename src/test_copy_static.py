import unittest
import tempfile
import os
import io
import sys
from pathlib import Path
import importlib.util
from copy_static import copy_static_files

class TestCopyStaticFiles(unittest.TestCase):
    def make_file(self, path: Path, contents: bytes):
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(contents)

    def test_simple_copy_preserves_files_and_contents(self):
        with tempfile.TemporaryDirectory() as src_dir, tempfile.TemporaryDirectory() as tmp_dest_parent:
            src = Path(src_dir)
            self.make_file(src / "a.txt", b"hello")
            self.make_file(src / "sub" / "b.txt", b"world")

            dest = Path(tmp_dest_parent) / "public"
            copy_static_files(str(src), str(dest))

            self.assertTrue((dest / "a.txt").exists())
            self.assertTrue((dest / "sub" / "b.txt").exists())
            self.assertEqual((dest / "a.txt").read_bytes(), b"hello")
            self.assertEqual((dest / "sub" / "b.txt").read_bytes(), b"world")

    def test_missing_source_is_noop_and_prints_message(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            dest = Path(tmpdir) / "public"
            fake_src = Path(tmpdir) / "does_not_exist"

            # Capture logging output instead of stdout (module uses logging)
            import logging
            stream = io.StringIO()
            handler = logging.StreamHandler(stream)
            logger = logging.getLogger('copy_static')
            logger.addHandler(handler)
            logger.setLevel(logging.INFO)
            try:
                copy_static_files(str(fake_src), str(dest))
                handler.flush()
                out = stream.getvalue()
            finally:
                logger.removeHandler(handler)

            self.assertFalse(dest.exists())
            self.assertIn("No static directory found", out)

    def test_dest_is_file_raises_value_error(self):
        with tempfile.TemporaryDirectory() as src_dir, tempfile.TemporaryDirectory() as tmpdir:
            src = Path(src_dir)
            self.make_file(src / "a.txt", b"x")
            dest_file = Path(tmpdir) / "not_a_dir"
            dest_file.write_bytes(b"i am a file")
            with self.assertRaises(ValueError):
                copy_static_files(str(src), str(dest_file))

    def test_existing_dest_deleted_and_recreated(self):
        with tempfile.TemporaryDirectory() as src_dir, tempfile.TemporaryDirectory() as tmpdir:
            src = Path(src_dir)
            self.make_file(src / "a.txt", b"1")

            dest = Path(tmpdir) / "public"
            # create dest with a file that should be removed
            dest.mkdir()
            (dest / "old.txt").write_bytes(b"old")

            copy_static_files(str(src), str(dest))
            self.assertTrue((dest / "a.txt").exists())
            self.assertFalse((dest / "old.txt").exists())

if __name__ == '__main__':
    unittest.main()
