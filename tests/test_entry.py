"""The bare command opens the book's opening page. ``--report`` prints the report."""

import os
import struct
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from opentoolbook.entry import choose_opening, opening_page
from opentoolbook.record import FOLLOW_UP

from lesson import companion

FIXTURE = Path(__file__).parent / "fixtures" / "otb-line-rect.tbk"

ENTER_APPLICATION = """
to handle enterApplication
    system logical __import
    __import = false
    forward
end
"""

ENTER_SYSTEM = """
to handle enterSystem cmdLine
    if "nc81base.sbk" is not in sysBooks
        get initializeBase(cmdLine)
    end
    get openSession()
    if it is 1 then
        get gotoPageList()
    end if
    forward
end
"""

OPEN_SESSION = """
to get openSession
    system int __studentRecords
    if __studentRecords <> 1 then
        return 0
    end if
    go to page "P999"
    return 1
end
"""

GO_LIST = """
to get gotoPageList
    go to page "P888"
end
"""

PAGE = """
to handle enterPage
    system logical __import
    if __import = false then
        if sysLevel = "reader" then
            go to page "P0" of book getLogoBook()
        else
            go to page "P1"
        end if
    end if
end
"""

LOGO = """
to get getLogoBook
    bookname = "nida81.tbk"
    if fileExists32("logo81.tbk") = 1 then
        bookname = "logo81.tbk"
    else
        if fileExists32("mrj81.tbk") = 1 then
            bookname = "mrj81.tbk"
        end if
    end if
    return bookname
end
"""


def _handlers():
    return {
        "enterapplication": ENTER_APPLICATION,
        "entersystem": ENTER_SYSTEM,
        "opensession": OPEN_SESSION,
        "gotopagelist": GO_LIST,
        "getlogobook": LOGO,
    }


def _book_naming(extra: bytes) -> bytes:
    key = 0x1000
    body = b"\x00\x10xx" + extra
    length = len(body)
    stored = struct.pack("<HH", key, length - 2) + body[4:]
    level0, level1, level2, leaf, body_at = 0x200, 0x400, 0x600, 0x800, 0xA00
    data = bytearray(body_at + length + FOLLOW_UP)
    data[0:4] = b"\x03JBO"
    struct.pack_into("<I", data, 0x10E, level0)
    struct.pack_into("<I", data, level0, level1)
    struct.pack_into("<I", data, level1, level2)
    struct.pack_into("<I", data, level2, leaf)
    slot = leaf + 0x18
    struct.pack_into("<I", data, slot, body_at)
    struct.pack_into("<H", data, slot + 8, 0x4001)
    struct.pack_into("<H", data, slot + 0x0C, length)
    data[slot + 0x16] = 0x11
    data[body_at:body_at + length] = stored
    return bytes(data)


class ChooseOpeningTests(unittest.TestCase):
    def test_startup_go_to_page_beats_the_first_stored_page(self):
        handlers = {"entersystem": 'to handle enterSystem\ngo to page "Start"\nend\n'}
        self.assertEqual(choose_opening(("P0", "Start"), handlers), ("Start", None))

    def test_no_startup_navigation_uses_the_first_stored_page(self):
        self.assertEqual(choose_opening(("P0", "P9"), {}), ("P0", None))

    def test_a_book_with_no_page_is_an_error(self):
        with self.assertRaises(ValueError) as caught:
            choose_opening((), {})
        self.assertIn("no stored page", str(caught.exception))
        self.assertIn("startup handlers", str(caught.exception))

    def test_reader_branch_opens_the_logo_book_and_skips_the_session_page(self):
        page, book = choose_opening(("P0", "P1", "P10"), _handlers(), {"P0": PAGE})
        self.assertEqual(page, "P0")
        self.assertEqual(book, "nida81.tbk")

    def test_a_logo_file_the_report_would_find_is_the_book(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "LOGO81.TBK").write_bytes(b"logo")
            page, book = choose_opening(
                ("P0", "P1"),
                _handlers(),
                {"P0": PAGE},
                roots=(root,),
            )
        self.assertEqual((page, book), ("P0", "logo81.tbk"))

    def test_a_missing_book_handler_names_what_was_missing(self):
        handlers = dict(_handlers())
        del handlers["getlogobook"]
        with self.assertRaises(ValueError) as caught:
            choose_opening(("P0", "P1"), handlers, {"P0": PAGE})
        message = str(caught.exception)
        self.assertIn("getLogoBook", message)
        self.assertIn("P0", message)

    def test_enter_page_in_the_same_book_is_followed(self):
        scripts = {
            "P0": 'to handle enterPage\ngo to page "P10"\nend\n',
            "P10": 'to handle enterPage\ngo to page "P2"\nend\n',
        }
        self.assertEqual(choose_opening(("P0", "P10", "P2"), {}, scripts), ("P2", None))

    def test_opensession_alone_is_not_a_startup_message(self):
        handlers = {"opensession": 'to get openSession\ngo to page "P2"\nend\n'}
        self.assertEqual(choose_opening(("P0", "P2"), handlers), ("P0", None))

    def test_enter_book_runs_after_enter_application(self):
        handlers = {
            "enterapplication": 'to handle enterApplication\ngo to page "P1"\nend\n',
            "enterbook": 'to handle enterBook\ngo to page "P2"\nend\n',
        }
        self.assertEqual(choose_opening(("P0", "P1", "P2"), handlers), ("P2", None))


class OpeningPageTests(unittest.TestCase):
    def test_an_instructor_book_opens_on_its_stored_page(self):
        entry = opening_page(FIXTURE)
        self.assertEqual(entry.page_id, "")
        self.assertEqual(entry.book, FIXTURE)
        self.assertEqual(entry.data, FIXTURE.read_bytes())

    def test_a_book_with_no_stored_page_names_what_is_missing(self):
        with tempfile.TemporaryDirectory() as tmp:
            book = Path(tmp) / "empty.tbk"
            book.write_bytes(_book_naming(b"nida81.tbk\x00"))
            with self.assertRaises(ValueError) as caught:
                opening_page(book)
        message = str(caught.exception)
        self.assertIn("empty.tbk", message)
        self.assertIn("no stored page", message)

    def test_the_lesson_opens_on_the_logo_page(self):
        path = os.environ.get("OPENTOOLBOOK_TBK")
        if not path or not os.path.isfile(path):
            self.skipTest("set OPENTOOLBOOK_TBK to 9e954d01.tbk")
        lesson = Path(path)
        entry = opening_page(lesson)
        self.assertEqual(entry.page_id, "P0")
        self.assertIn(entry.book.name.lower(), {"nida81.tbk", "logo81.tbk", "mrj81.tbk"})
        self.assertNotEqual(entry.book.resolve(), lesson.resolve())
        self.assertGreater(len(entry.data), 1000)
        nida = companion(lesson, "nida81.tbk")
        if nida.is_file():
            shell = opening_page(nida)
            self.assertEqual(shell.page_id, "P0")
            self.assertEqual(shell.book.resolve(), nida.resolve())


class CommandTests(unittest.TestCase):
    def test_the_bare_command_opens_the_viewer_and_does_not_print_the_report(self):
        from opentoolbook.__main__ import main

        with patch("opentoolbook.__main__.open_page", return_value=()) as open_page:
            code = main(["opentoolbook", str(FIXTURE)])
        self.assertEqual(code, 0)
        self.assertEqual(open_page.call_args.args[1], "")
        self.assertEqual(open_page.call_args.args[2], str(FIXTURE))
        self.assertEqual(open_page.call_args.args[0], FIXTURE.read_bytes())

    def test_report_flags_print_the_report_in_either_order(self):
        import contextlib
        import io

        from opentoolbook.__main__ import main

        with tempfile.TemporaryDirectory() as tmp:
            book = Path(tmp) / "lesson.tbk"
            book.write_bytes(_book_naming(b"nida81.tbk\x00enterApplication\x00"))
            texts = []
            for argv in (
                ["opentoolbook", "--report", str(book)],
                ["opentoolbook", str(book), "--report"],
            ):
                buf = io.StringIO()
                with contextlib.redirect_stdout(buf):
                    code = main(argv)
                self.assertEqual(code, 0)
                texts.append(buf.getvalue())
        for text in texts:
            self.assertIn("records ", text)
            self.assertIn("follow-up reads ", text)
            self.assertIn("nida81.tbk", text)
            self.assertIn("enterapplication", text)
        self.assertEqual(texts[0], texts[1])

    def test_a_bare_book_with_no_page_does_not_print_the_report(self):
        import contextlib
        import io

        from opentoolbook.__main__ import main

        with tempfile.TemporaryDirectory() as tmp:
            book = Path(tmp) / "empty.tbk"
            book.write_bytes(_book_naming(b"nida81.tbk\x00"))
            out = io.StringIO()
            err = io.StringIO()
            with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
                code = main(["opentoolbook", str(book)])
        self.assertEqual(code, 2)
        self.assertNotIn("records ", out.getvalue())
        self.assertIn("empty.tbk", err.getvalue())
        self.assertIn("no stored page", err.getvalue())

    def test_help_names_report_and_the_opening_page(self):
        import contextlib
        import io

        from opentoolbook.__main__ import main

        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            with self.assertRaises(SystemExit) as caught:
                main(["opentoolbook", "--help"])
        self.assertEqual(caught.exception.code, 0)
        text = buf.getvalue()
        self.assertIn("--report", text)
        self.assertIn("opening page", text)
        self.assertNotIn("print a report and do not open a window", text.lower())


if __name__ == "__main__":
    unittest.main()
