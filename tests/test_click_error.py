"""A missing book is one sentence, whether the open or a click finds it missing."""

import contextlib
import io
import os
import tempfile
import unittest
from pathlib import Path
from unittest import mock

from opentoolbook.navigate import Navigator
from opentoolbook.shelf import MissingBook, missing_sentence
from opentoolbook.show import click_reported

FIXTURE = Path(__file__).parent / "fixtures" / "otb-line-rect.tbk"


def _lesson():
    path = os.environ.get("OPENTOOLBOOK_TBK")
    if not path or not os.path.isfile(path):
        return None
    return Path(path)


def _main(argv, window=None):
    import opentoolbook.__main__ as entry

    out, err = io.StringIO(), io.StringIO()
    patch = mock.patch.object(entry, "open_page", window or (lambda *a, **k: ()))
    with patch, contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
        code = entry.main(["opentoolbook", *argv])
    return code, out.getvalue(), err.getvalue()


class SentenceTests(unittest.TestCase):
    def test_the_sentence_names_the_file_and_the_page(self):
        self.assertEqual(
            missing_sentence("nida81.tbk", "P310"),
            "nida81.tbk was not found; P310 of that book does not open",
        )
        error = MissingBook("nida81.tbk", "P310")
        self.assertIsInstance(error, ValueError)
        self.assertEqual(str(error), missing_sentence("nida81.tbk", "P310"))

    def test_the_click_raises_the_open_error_class(self):
        with tempfile.TemporaryDirectory() as tmp:
            book = Path(tmp) / "a" / "lesson.tbk"
            book.parent.mkdir()
            book.write_bytes(FIXTURE.read_bytes())
            with self.assertRaises(MissingBook) as clicked:
                Navigator(FIXTURE.read_bytes(), "", book).find_book("logo81.tbk", "P0")
        self.assertEqual(str(clicked.exception), "logo81.tbk was not found; P0 of that book does not open")


class Nida71Tests(unittest.TestCase):
    """``nida81.tbk`` names ``nida71.tbk``. That file is not shipped and stays missing."""

    def test_a_click_that_quotes_nida71_is_the_missing_book_error(self):
        from opentoolbook.click import run_handler

        source = (
            "to handle buttonClick\n"
            '\tgo to page "P12060" of book "nida71.tbk"\n'
            "end\n"
        )
        follow = run_handler(source, ("P12001",), "P12001")
        self.assertEqual((follow.page_id, follow.book), ("P12060", "nida71.tbk"))
        with tempfile.TemporaryDirectory() as tmp:
            top = Path(tmp)
            book = top / "LF" / "nida81.tbk"
            book.parent.mkdir()
            book.write_bytes(FIXTURE.read_bytes())
            home = top / "home"
            for folder in (home, home / "courses"):
                folder.mkdir(parents=True)
            nav = Navigator(FIXTURE.read_bytes(), "", book, home)
            with self.assertRaises(MissingBook) as caught:
                nav.find_book(follow.book, follow.page_id)
        self.assertEqual(
            str(caught.exception),
            "nida71.tbk was not found; P12060 of that book does not open",
        )
        self.assertEqual(caught.exception.name, "nida71.tbk")
        self.assertEqual(len(caught.exception.roots), 3)

    def test_retry_on_all_four_pages_of_nida81_prints_the_error_and_stays(self):
        path = _lesson()
        if path is None:
            self.skipTest("set OPENTOOLBOOK_TBK to 9e954d01.tbk")
        nida = path.with_name("nida81.tbk")
        from opentoolbook.shelf import find_file, search_roots

        self.assertIsNone(find_file(search_roots(nida, None), "nida71.tbk"))
        data = nida.read_bytes()
        sentence = "nida71.tbk was not found; P12060 of that book does not open"
        for page in ("P12000", "P12001", "P12002", "P12003"):
            with self.subTest(page=page):
                nav = Navigator(data, page, nida)
                errors: list[str] = []
                stream = io.StringIO()
                self.assertIsNone(click_reported(nav, "Retry", errors, stream))
                self.assertEqual(errors, [sentence])
                self.assertEqual(stream.getvalue(), sentence + "\n")
                self.assertEqual((nav.page_id, nav.book), (page, nida))


class CommandTests(unittest.TestCase):
    def test_show_on_a_missing_book_prints_the_sentence_and_exits_2(self):
        with tempfile.TemporaryDirectory() as tmp:
            code, out, err = _main(["--show", "P310", str(Path(tmp) / "nida81.tbk")])
        self.assertEqual(code, 2)
        self.assertEqual(err, "nida81.tbk was not found; P310 of that book does not open\n")
        self.assertNotIn("Traceback", err)

    def test_show_on_a_page_the_book_lacks_prints_one_line_and_exits_2(self):
        def window(data, page_id, *rest, **kw):
            from opentoolbook.show import show_page

            show_page(data, page_id, 100, 100)
            return ()

        code, _out, err = _main(["--show", "P999", str(FIXTURE)], window)
        self.assertEqual(code, 2)
        self.assertEqual(err, "no page P999\n")

    def test_a_click_error_in_the_window_makes_the_exit_non_zero(self):
        sentence = missing_sentence("nida71.tbk", "P0")
        code, _out, err = _main(["--show", "", str(FIXTURE)], lambda *a, **k: (sentence,))
        self.assertEqual(code, 1)
        code, _out, err = _main(["--show", "", str(FIXTURE)])
        self.assertEqual(code, 0)


class LessonClickTests(unittest.TestCase):
    def test_selection1_without_nida81_prints_the_sentence_and_stays(self):
        path = _lesson()
        if path is None:
            self.skipTest("set OPENTOOLBOOK_TBK to 9e954d01.tbk")
        with tempfile.TemporaryDirectory() as tmp:
            lesson = Path(tmp) / "LF" / "9e954d01.tbk"
            lesson.parent.mkdir()
            lesson.symlink_to(path.resolve())
            nav = Navigator(lesson.read_bytes(), "P300", lesson)
            errors: list[str] = []
            stream = io.StringIO()
            self.assertIsNone(click_reported(nav, "Selection1", errors, stream))
            sentence = "nida81.tbk was not found; P310 of that book does not open"
            self.assertEqual(stream.getvalue(), sentence + "\n")
            self.assertEqual(errors, [sentence])
            self.assertEqual((nav.page_id, nav.book), ("P300", lesson))
            moved = click_reported(nav, "Next", errors, stream)
            self.assertTrue(moved.moved)
            self.assertEqual(nav.page_id, "P400")
            self.assertEqual(len(errors), 1)

    def test_the_open_without_nida81_prints_the_same_sentence(self):
        from opentoolbook.entry import opening_page

        path = _lesson()
        if path is None:
            self.skipTest("set OPENTOOLBOOK_TBK to 9e954d01.tbk")
        with tempfile.TemporaryDirectory() as tmp:
            lesson = Path(tmp) / "LF" / "9e954d01.tbk"
            lesson.parent.mkdir()
            lesson.symlink_to(path.resolve())
            for name in ("nc81base.sbk", "nc81recs.sbk", "nc81test.sbk", "nc81trnr.sbk"):
                (lesson.parent / name).symlink_to(path.with_name(name).resolve())
            with self.assertRaises(MissingBook) as opened:
                opening_page(lesson)
            sentence = "nida81.tbk was not found; P0 of that book does not open"
            self.assertEqual(str(opened.exception), sentence)
            code, _out, err = _main([str(lesson)])
            self.assertEqual(code, 2)
            self.assertEqual(err, sentence + "\n")


if __name__ == "__main__":
    unittest.main()
