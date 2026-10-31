"""``TB80.INI`` search and ``startupSysBooks`` seeding."""

from __future__ import annotations

import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from opentoolbook.entry import opening_page
from opentoolbook.tb80ini import find_tb80_ini, read_tb80_ini

FIXTURE = Path(__file__).parent / "fixtures" / "otb-line-rect.tbk"


class FindTb80Ini(unittest.TestCase):
    def test_book_folder_wins_over_windows_paths(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            book = root / "lesson" / "demo.tbk"
            book.parent.mkdir()
            book.write_bytes(b"x")
            (book.parent / "TB80.INI").write_text("startupSysBooks=a.sbk\n", encoding="latin1")
            windows = root / "windows"
            runtime = windows / "asym" / "runtime"
            runtime.mkdir(parents=True)
            (runtime / "tb80.ini").write_text("startupSysBooks=b.sbk\n", encoding="latin1")
            (windows / "TB80.INI").write_text("startupSysBooks=c.sbk\n", encoding="latin1")
            found = find_tb80_ini(book, windows=windows)
            self.assertEqual(found, book.parent / "TB80.INI")
            self.assertEqual(read_tb80_ini(book, windows=windows).startup_sysbooks, ("a.sbk",))

    def test_windows_asym_runtime_then_windows(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            book = root / "lesson" / "demo.tbk"
            book.parent.mkdir()
            book.write_bytes(b"x")
            windows = root / "windows"
            runtime = windows / "asym" / "runtime"
            runtime.mkdir(parents=True)
            (runtime / "TB80.INI").write_text(
                "startupSysBooks=runtime.sbk,Extra.SBK\nstartupBook=start.tbk\n"
                "startupWidth=640\nstartupHeight=480\n",
                encoding="latin1",
            )
            (windows / "tb80.ini").write_text("startupSysBooks=win.sbk\n", encoding="latin1")
            settings = read_tb80_ini(book, windows=windows)
            self.assertEqual(settings.startup_sysbooks, ("runtime.sbk", "extra.sbk"))
            self.assertEqual(settings.startup_book, "start.tbk")
            self.assertEqual(settings.startup_width, 640)
            self.assertEqual(settings.startup_height, 480)
            (runtime / "TB80.INI").unlink()
            settings = read_tb80_ini(book, windows=windows)
            self.assertEqual(settings.startup_sysbooks, ("win.sbk",))

    def test_explicit_ini_skips_the_search(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            book = root / "demo.tbk"
            book.write_bytes(b"x")
            (root / "TB80.INI").write_text("startupSysBooks=folder.sbk\n", encoding="latin1")
            override = root / "other.ini"
            override.write_text("startupSysBooks=override.sbk\n", encoding="latin1")
            settings = read_tb80_ini(book, override=override)
            self.assertEqual(settings.path, override)
            self.assertEqual(settings.startup_sysbooks, ("override.sbk",))

    def test_missing_ini_keeps_defaults(self):
        with tempfile.TemporaryDirectory() as tmp:
            book = Path(tmp) / "demo.tbk"
            book.write_bytes(b"x")
            settings = read_tb80_ini(book)
            self.assertIsNone(settings.path)
            self.assertEqual(settings.startup_sysbooks, ())
            self.assertIsNone(settings.startup_book)
            self.assertIsNone(settings.startup_width)
            self.assertIsNone(settings.startup_height)


class StartupSysBooks(unittest.TestCase):
    def test_fixture_without_ini_has_empty_sysbooks(self):
        entry = opening_page(FIXTURE)
        self.assertEqual(entry.sysbooks, ())

    def test_startup_sysbooks_seed_before_bound_books(self):
        with tempfile.TemporaryDirectory() as tmp:
            folder = Path(tmp)
            book = folder / "demo.tbk"
            book.write_bytes(FIXTURE.read_bytes())
            (folder / "TB80.INI").write_text("startupSysBooks=seed.sbk,Other.SBK\n", encoding="latin1")
            with patch("opentoolbook.entry.bound_sysbooks", return_value=("Bound.SBK", "seed.sbk")):
                entry = opening_page(book)
            self.assertEqual(entry.sysbooks, ("seed.sbk", "other.sbk", "bound.sbk"))

    def test_ini_override_seeds_opening_page(self):
        with tempfile.TemporaryDirectory() as tmp:
            folder = Path(tmp)
            book = folder / "demo.tbk"
            book.write_bytes(FIXTURE.read_bytes())
            ini = folder / "custom.ini"
            ini.write_text("startupSysBooks=fromini.sbk\n", encoding="latin1")
            entry = opening_page(book, ini=ini)
            self.assertEqual(entry.sysbooks, ("fromini.sbk",))


if __name__ == "__main__":
    unittest.main()
