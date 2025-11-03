import unittest
import tempfile
import os
import stat
import sys
from pathlib import Path
import importlib.util

# Load local module
spec = importlib.util.spec_from_file_location(
    "copy_static", os.path.join(os.path.dirname(__file__), "copy_static.py")
)
copy_mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(copy_mod)
copy_static_files = copy_mod.copy_static_files


class TestCopyStaticExtra(unittest.TestCase):
    def make_file(self, path: Path, contents: bytes):
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(contents)

    def test_symlink_source_copies_target_contents(self):
        with tempfile.TemporaryDirectory() as src_dir, tempfile.TemporaryDirectory() as dest_parent:
            src = Path(src_dir)
            target = src / "real.txt"
            self.make_file(target, b"from-symlink")
            link = src / "link.txt"
            try:
                link.symlink_to(target)
            except (OSError, NotImplementedError):
                self.skipTest("Symlinks not supported on this platform/user")

            dest = Path(dest_parent) / "public"
            copy_static_files(str(src), str(dest))
            self.assertTrue((dest / "link.txt").exists())
            self.assertEqual((dest / "link.txt").read_bytes(), b"from-symlink")

    def test_large_file_copy(self):
        with tempfile.TemporaryDirectory() as src_dir, tempfile.TemporaryDirectory() as dest_parent:
            src = Path(src_dir)
            big = src / "big.bin"
            # create ~2MB file
            data = b"x" * (2 * 1024 * 1024)
            self.make_file(big, data)
            dest = Path(dest_parent) / "public"
            copy_static_files(str(src), str(dest))
            self.assertEqual((dest / "big.bin").stat().st_size, big.stat().st_size)

    def test_permission_error_propagates_or_skips_if_root(self):
        # If running as root permission errors won't occur predictably; skip then
        if hasattr(os, 'geteuid') and os.geteuid() == 0:
            self.skipTest("Running as root; permission error test skipped")

        with tempfile.TemporaryDirectory() as src_dir, tempfile.TemporaryDirectory() as dest_parent:
            src = Path(src_dir)
            f = src / "no_read.txt"
            self.make_file(f, b"secret")
            # remove read permission
            f.chmod(0)
            dest = Path(dest_parent) / "public"
            try:
                with self.assertRaises((PermissionError, OSError)):
                    copy_static_files(str(src), str(dest))
            finally:
                # restore permissions so tempfile cleanup works
                try:
                    f.chmod(stat.S_IRUSR | stat.S_IWUSR)
                except Exception:
                    pass

    def test_metadata_preserved_mtime(self):
        with tempfile.TemporaryDirectory() as src_dir, tempfile.TemporaryDirectory() as dest_parent:
            src = Path(src_dir)
            f = src / "meta.txt"
            self.make_file(f, b"meta")
            # set a custom mtime
            import time
            old_mtime = int(time.time()) - 3600
            os.utime(f, (old_mtime, old_mtime))

            dest = Path(dest_parent) / "public"
            copy_static_files(str(src), str(dest))
            src_stat = f.stat()
            dst_stat = (dest / "meta.txt").stat()
            # mtime may be float; compare integer seconds
            self.assertEqual(int(src_stat.st_mtime), int(dst_stat.st_mtime))


if __name__ == '__main__':
    unittest.main()
