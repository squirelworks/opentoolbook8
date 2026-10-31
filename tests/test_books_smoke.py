"""Optional smoke: every ``.tbk`` under ``OPENTOOLBOOK_BOOKS`` opens and paints.

Unset, or a missing directory, skips. Each book runs startup, then
``show_page`` of the opening page. Any exception fails that book.
"""

from __future__ import annotations

import os
import shutil
import tempfile
import unittest
from pathlib import Path
from unittest import mock

from opentoolbook.entry import opening_page
from opentoolbook.show import show_page
from opentoolbook.size import page_size


def _books_dir() -> Path | None:
    value = os.environ.get("OPENTOOLBOOK_BOOKS")
    if not value:
        return None
    path = Path(value)
    if not path.is_dir():
        return None
    return path


def _tbk_files(folder: Path) -> tuple[Path, ...]:
    return tuple(sorted(path for path in folder.iterdir() if path.is_file() and path.suffix.lower() == ".tbk"))


def _open_and_paint(book: Path, home: Path | None) -> None:
    entry = opening_page(book, home)
    width, height = page_size(entry.data)
    view_w = max(1, width // 15)
    view_h = max(1, height // 15)
    listed = show_page(entry.data, entry.page_id, view_w, view_h)
    if listed is None:
        raise AssertionError("show_page returned None")


@unittest.skipIf(_books_dir() is None, "set OPENTOOLBOOK_BOOKS to a folder of .tbk files")
class BooksFolderSmokeTests(unittest.TestCase):
    def test_every_tbk_opens_startup_and_paints_the_opening_page(self):
        folder = _books_dir()
        books = _tbk_files(folder)
        self.assertTrue(books, f"no .tbk files in {folder}")
        failures: list[str] = []
        for book in books:
            try:
                _open_and_paint(book, folder)
            except Exception as exc:  # noqa: BLE001 — smoke reports every book
                failures.append(f"{book.name}: {type(exc).__name__}: {exc}")
        self.assertEqual(failures, [], "\n".join(failures))


class BooksFolderHelperTests(unittest.TestCase):
    def test_unset_or_missing_folder_is_no_books_dir(self):
        with mock.patch.dict(os.environ, {}, clear=False):
            os.environ.pop("OPENTOOLBOOK_BOOKS", None)
            self.assertIsNone(_books_dir())
        with tempfile.TemporaryDirectory() as tmp:
            missing = str(Path(tmp) / "absent")
            with mock.patch.dict(os.environ, {"OPENTOOLBOOK_BOOKS": missing}):
                self.assertIsNone(_books_dir())

    def test_a_folder_of_fixtures_opens_and_paints(self):
        fixtures = Path(__file__).parent / "fixtures"
        with tempfile.TemporaryDirectory() as tmp:
            folder = Path(tmp)
            for name in ("otb-line-rect.tbk", "otb-pie.tbk", "otb_cross_a.tbk", "otb_cross_b.tbk"):
                shutil.copy(fixtures / name, folder / name)
            with mock.patch.dict(os.environ, {"OPENTOOLBOOK_BOOKS": str(folder)}):
                self.assertEqual(_books_dir(), folder)
                self.assertEqual(len(_tbk_files(folder)), 4)
                for book in _tbk_files(folder):
                    _open_and_paint(book, folder)
                    entry = opening_page(book, folder)
                    width, height = page_size(entry.data)
                    listed = show_page(entry.data, entry.page_id, max(1, width // 15), max(1, height // 15))
                    self.assertGreaterEqual(len(listed.items), 1, book.name)


if __name__ == "__main__":
    unittest.main()
