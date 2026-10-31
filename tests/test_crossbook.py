"""Two checked-in books open across a book boundary without the private lesson."""

import contextlib
import io
import os
import shutil
import tempfile
import unittest
from pathlib import Path
from unittest import mock

from opentoolbook.enter import page_source
from opentoolbook.entry import opening_page
from opentoolbook.field import page_ids
from opentoolbook.page import page_records
from opentoolbook.record import Book
from opentoolbook.show import show_page

import crossbook

FIXTURES = Path(__file__).parent / "fixtures"
SOURCE = FIXTURES / "otb-line-rect.tbk"
BOOK_A = FIXTURES / crossbook.BOOK_A
BOOK_B = FIXTURES / crossbook.BOOK_B


def _no_lesson():
    env = dict(os.environ)
    env.pop("OPENTOOLBOOK_TBK", None)
    return mock.patch.dict(os.environ, env, clear=True)


class CrossBookFixtureTests(unittest.TestCase):
    def test_the_checked_in_books_are_the_builder_output(self):
        built = crossbook.build()
        self.assertEqual(BOOK_A.read_bytes(), built[crossbook.BOOK_A])
        self.assertEqual(BOOK_B.read_bytes(), built[crossbook.BOOK_B])

    def test_book_a_enter_page_quotes_p0_of_book_b(self):
        data = BOOK_A.read_bytes()
        self.assertEqual(page_ids(data), ("",))
        source = page_source(data, "")
        self.assertIn('go to page "P0" of book "otb_cross_b.tbk"', source)
        self.assertTrue(source.lower().startswith("to handle enterpage"))
        self.assertEqual(page_ids(BOOK_B.read_bytes()), ("P0",))
        self.assertEqual(page_source(BOOK_B.read_bytes(), "P0"), "")

    def test_opening_a_lands_on_p0_of_b_with_no_lesson(self):
        with _no_lesson():
            entry = opening_page(BOOK_A)
        self.assertEqual(entry.page_id, "P0")
        self.assertEqual(entry.book, BOOK_B)
        self.assertEqual(entry.data, BOOK_B.read_bytes())
        self.assertEqual(opening_page(BOOK_B).page_id, "P0")
        self.assertEqual(opening_page(BOOK_B).book, BOOK_B)

    def test_b_in_the_parent_in_another_case_is_found_by_the_shelf(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            lessons = root / "Lessons"
            lessons.mkdir()
            shutil.copy(BOOK_A, lessons / crossbook.BOOK_A)
            shutil.copy(BOOK_B, root / crossbook.BOOK_B.upper())
            entry = opening_page(lessons / crossbook.BOOK_A)
            self.assertEqual(entry.page_id, "P0")
            self.assertEqual(entry.book, root / crossbook.BOOK_B.upper())

    def test_a_missing_b_names_the_file_and_the_page(self):
        with tempfile.TemporaryDirectory() as tmp:
            alone = Path(tmp) / "alone" / crossbook.BOOK_A
            alone.parent.mkdir()
            shutil.copy(BOOK_A, alone)
            with self.assertRaises(ValueError) as caught:
                opening_page(alone)
        self.assertIn("otb_cross_b.tbk", str(caught.exception))
        self.assertIn("P0", str(caught.exception))

    def test_the_report_names_b_beside_a(self):
        from opentoolbook.__main__ import main

        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            code = main(["opentoolbook", "--report", str(BOOK_A)])
        self.assertEqual(code, 0)
        self.assertIn("otb_cross_b.tbk", buf.getvalue())

    def test_the_paint_and_the_records_are_the_line_rect_book(self):
        source = SOURCE.read_bytes()
        original = show_page(source, "", 400, 300)
        for data, page_id in ((BOOK_A.read_bytes(), ""), (BOOK_B.read_bytes(), "P0")):
            shown = show_page(data, page_id, 400, 300)
            self.assertEqual(shown.items, original.items)
            self.assertEqual(shown.scale, original.scale)
            self.assertEqual(page_records(data, page_id).objects, page_records(source, "").objects)
            self.assertEqual(len(Book(data).records), len(Book(source).records))


if __name__ == "__main__":
    unittest.main()
