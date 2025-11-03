import unittest
import tempfile
import os
import stat
from pathlib import Path
import importlib.util

# Load local module
spec = importlib.util.spec_from_file_location(
    "copy_static", os.path.join(os.path.dirname(__file__), "copy_static.py")
)
copy_mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(copy_mod)
copy_static_files = copy_mod.copy_static_files


class TestCopyStaticMore(unittest.TestCase):
    def make_file(self, path: Path, contents: bytes):
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(contents)

    def test_preserve_permissions_mode(self):
        with tempfile.TemporaryDirectory() as src_dir, tempfile.TemporaryDirectory() as dest_parent:
            src = Path(src_dir)
            f = src / "perm.txt"
            self.make_file(f, b"perm")
            # set mode to rw-r----- (0o640)
            f.chmod(0o640)

            dest = Path(dest_parent) / "public"
            copy_static_files(str(src), str(dest))

            src_mode = stat.S_IMODE(f.stat().st_mode)
            dst_mode = stat.S_IMODE((dest / "perm.txt").stat().st_mode)
            self.assertEqual(src_mode, dst_mode)

    def test_many_nested_files(self):
        with tempfile.TemporaryDirectory() as src_dir, tempfile.TemporaryDirectory() as dest_parent:
            src = Path(src_dir)
            # Create a nested tree with 50 files across directories
            for i in range(5):
                for j in range(10):
                    p = src / f"dir{i}" / f"file{j}.txt"
                    self.make_file(p, f"{i}-{j}".encode())

            dest = Path(dest_parent) / "public"
            copy_static_files(str(src), str(dest))

            # Check a sampling of files
            self.assertTrue((dest / "dir0" / "file0.txt").exists())
            self.assertTrue((dest / "dir4" / "file9.txt").exists())
            self.assertEqual((dest / "dir3" / "file5.txt").read_text(), "3-5")


if __name__ == '__main__':
    unittest.main()
