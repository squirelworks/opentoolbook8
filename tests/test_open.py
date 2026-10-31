"""Opening a book reports a missing file and still returns the book."""

import os
import struct
import tempfile
import unittest
from pathlib import Path

from opentoolbook.record import FOLLOW_UP
from opentoolbook.shelf import open_book

from lesson import companion


def _book_naming(extra: bytes) -> bytes:
    """One real leaf, with ``extra`` stored in the body so a name scan can see it."""
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


class OpenTests(unittest.TestCase):
    def test_missing_minstb32_does_not_stop_the_open(self):
        settled = Path("SETTLED.md").read_text(encoding="utf-8")
        self.assertIn("minstb32.dll", settled)
        self.assertIn("not fatal", settled)
        raw = _book_naming(b"minstb32.dll\x00nc81base.sbk\x00")
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            book = root / "9e954d01.tbk"
            book.write_bytes(raw)
            home = root / "home"
            home.mkdir()
            (home / "toolbook.lst").write_text("NC81BASE.SBK\nTB80R.SBK\n", encoding="latin1")
            opened = open_book(book, home)
            self.assertGreater(len(opened.book.records), 0)
            notes = {item.name: item.note for item in opened.files}
            self.assertEqual(notes["minstb32.dll"], "named, not shipped")
            self.assertEqual(notes["nc81base.sbk"], "not found")
            import contextlib
            import io

            from opentoolbook.__main__ import main

            buf = io.StringIO()
            with contextlib.redirect_stdout(buf):
                code = main(["opentoolbook", "--report", "--home", str(home), str(book)])
            self.assertEqual(code, 0)
            self.assertIn("records ", buf.getvalue())
            self.assertIn("minstb32.dll  named, not shipped", buf.getvalue())
            lesson = os.environ.get("OPENTOOLBOOK_TBK")
            if lesson and os.path.isfile(lesson):
                real = open_book(Path(lesson), home)
                real_notes = {item.name.lower(): item.note for item in real.files}
                self.assertEqual(real_notes["minstb32.dll"], "named, not shipped")
                self.assertGreater(len(real.book.records), 0)

    def test_open_resolves_named_files_and_tolerates_three_absent(self):
        from opentoolbook.shelf import search_roots

        named = (
            b"minstb32.dll",
            b"93954302.tbk",
            b"93954d01.tbk",
            b"nida81.tbk",
            b"nc81recs.sbk",
            b"nc81test.sbk",
            b"tb80anm.sbk",
            b"nc81base.sbk",
        )
        raw = _book_naming(b"\x00".join(named) + b"\x00")
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            book_dir = root / "book"
            home = root / "home"
            lessons = home / "Nida98" / "Lessons"
            student = home / "Nida98" / "Student"
            courses = home / "courses"
            for folder in (book_dir, home, lessons, student, courses):
                folder.mkdir(parents=True)
            book = book_dir / "9e954d01.tbk"
            book.write_bytes(raw)
            (book_dir / "NIDA81.TBK").write_bytes(b"beside the book")
            (home / "nida81.tbk").write_bytes(b"home copy")
            (home / "NC81RECS.SBK").write_bytes(b"home")
            (courses / "nc81recs.sbk").write_bytes(b"courses copy")
            (courses / "NC81TEST.SBK").write_bytes(b"courses")
            (lessons / "nc81test.sbk").write_bytes(b"lessons copy")
            (lessons / "TB80ANM.SBK").write_bytes(b"lessons")
            (student / "NC81BASE.SBK").write_bytes(b"student only")
            (home / "toolbook.lst").write_text(
                "NIDA81.TBK\nNC81RECS.SBK\nNC81TEST.SBK\nTB80ANM.SBK\nNC81BASE.SBK\n",
                encoding="latin1",
            )
            roots = search_roots(book, home)
            self.assertNotIn(student, roots)
            opened = open_book(book, home)
            self.assertGreater(len(opened.book.records), 0)
            found = {item.name: item.path for item in opened.files}
            notes = {item.name: item.note for item in opened.files}
            self.assertEqual(found["nida81.tbk"], book_dir / "NIDA81.TBK")
            self.assertEqual(found["nc81recs.sbk"], home / "NC81RECS.SBK")
            self.assertEqual(found["nc81test.sbk"], courses / "NC81TEST.SBK")
            self.assertEqual(found["tb80anm.sbk"], lessons / "TB80ANM.SBK")
            self.assertIsNone(found["nc81base.sbk"])
            self.assertEqual(notes["nc81base.sbk"], "not found")
            for absent in ("minstb32.dll", "93954302.tbk", "93954d01.tbk"):
                self.assertIsNone(found[absent])
                self.assertEqual(notes[absent], "named, not shipped")
            import contextlib
            import io

            from opentoolbook.__main__ import main

            buf = io.StringIO()
            with contextlib.redirect_stdout(buf):
                code = main(["opentoolbook", "--report", "--home", str(home), str(book)])
            text = buf.getvalue()
        self.assertEqual(code, 0)
        self.assertIn("records ", text)
        self.assertIn(str(lessons / "TB80ANM.SBK"), text)
        self.assertNotIn(str(student / "NC81BASE.SBK"), text)

    def test_open_keys_files_by_the_lesson_spelling(self):
        raw = _book_naming(b"MINSTB32.dll\x00TB80ANM.SBK\x00nida81.tbk\x00NIDA81.TBK\x00")
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            book = root / "9e954d01.tbk"
            book.write_bytes(raw)
            (root / "nida81.TBK").write_bytes(b"beside the book")
            home = root / "home"
            home.mkdir()
            (home / "toolbook.lst").write_text("TB80ANM.SBK\nNIDA81.TBK\n", encoding="latin1")
            opened = open_book(book, home)
            by_name = {item.name: item for item in opened.files}
            self.assertEqual(
                set(by_name),
                {"MINSTB32.dll", "TB80ANM.SBK", "nida81.tbk"},
            )
            self.assertEqual(by_name["MINSTB32.dll"].note, "named, not shipped")
            self.assertIsNone(by_name["MINSTB32.dll"].path)
            self.assertEqual(by_name["TB80ANM.SBK"].note, "not found")
            self.assertEqual(by_name["nida81.tbk"].path, root / "nida81.TBK")
            self.assertEqual(by_name["nida81.tbk"].note, "")
            lesson = os.environ.get("OPENTOOLBOOK_TBK")
            if lesson and os.path.isfile(lesson):
                real = open_book(Path(lesson), home)
                spellings = {item.name.lower(): item.name for item in real.files}
                self.assertEqual(spellings["minstb32.dll"], "MINSTB32.dll")
                self.assertEqual(spellings["tb80anm.sbk"], "TB80ANM.SBK")
                nida = companion(lesson, "nida81.tbk")
                if nida.is_file():
                    opened_nida = open_book(nida, home)
                    nida_notes = {item.name: item for item in opened_nida.files}
                    self.assertIn("nida71.tbk", nida_notes)
                    self.assertIsNone(nida_notes["nida71.tbk"].path)
                    self.assertEqual(nida_notes["nida71.tbk"].note, "named, not shipped")

    def test_open_resolves_books_in_the_parent_of_the_lesson(self):
        """A lesson resolves names beside it, then in the parent of that directory."""
        from opentoolbook.shelf import search_roots

        parent_files = (
            "nida81.tbk",
            "nc81base.sbk",
            "nc81recs.sbk",
            "nc81test.sbk",
            "nc81trnr.sbk",
        )
        missing = ("93954d01.tbk", "tb80anm.sbk", "tb80r.sbk", "minstb32.dll")
        guest = Path("/tmp/refs/guest/9e954d01.tbk")
        settled = Path("SETTLED.md").read_text(encoding="utf-8")
        self.assertIn("the parent of that directory", settled)
        with tempfile.TemporaryDirectory() as tmp:
            parent = Path(tmp)
            courses = parent / "courses"
            courses.mkdir()
            lesson = courses / "9e954d01.tbk"
            if guest.is_file():
                try:
                    os.link(guest, lesson)
                except OSError:
                    lesson.write_bytes(guest.read_bytes())
            else:
                named = (
                    b"MINSTB32.dll",
                    b"TB80ANM.SBK",
                    b"TB80R.SBK",
                    b"nc81trnr.sbk",
                    b"nc81base.sbk",
                    b"nc81recs.sbk",
                    b"nc81test.sbk",
                    b"nida81.tbk",
                    b"93954d01.TBK",
                    b"93954302.tbk",
                )
                lesson.write_bytes(_book_naming(b"\x00".join(named) + b"\x00"))
            for name in parent_files:
                (parent / name).write_bytes(b"parent " + name.encode("ascii"))
            beside = courses / "93954302.TBK"
            beside.write_bytes(b"beside the lesson")
            (parent / "93954302.tbk").write_bytes(b"parent copy loses")
            other = parent / "other"
            other.mkdir()
            (other / "93954d01.TBK").write_bytes(b"not this directory")
            (other / "nida81.tbk").write_bytes(b"not this directory")
            nested = courses / "nested"
            nested.mkdir()
            (nested / "93954d01.TBK").write_bytes(b"not a child directory")
            self.assertEqual(search_roots(lesson, None), (courses, parent))
            opened = open_book(lesson)
            found = {item.name.lower(): item for item in opened.files}
            for name in parent_files:
                self.assertEqual(found[name].path, parent / name)
                self.assertEqual(found[name].note, "")
            self.assertEqual(found["93954302.tbk"].path, beside)
            for name in missing:
                self.assertIn(name, found)
                self.assertIsNone(found[name].path)
            import contextlib
            import io

            from opentoolbook.__main__ import main

            buf = io.StringIO()
            with contextlib.redirect_stdout(buf):
                code = main(["opentoolbook", "--report", str(lesson)])
            text = buf.getvalue()
        self.assertEqual(code, 0)
        for name in parent_files:
            self.assertIn(f"{found[name].name}  {parent / name}", text)
        self.assertIn(str(beside), text)
        self.assertNotIn(str(parent / "93954302.tbk"), text)
        self.assertNotIn(str(other / "93954d01.TBK"), text)
        self.assertNotIn(str(nested / "93954d01.TBK"), text)


if __name__ == "__main__":
    unittest.main()


class UnshippedDllTests(unittest.TestCase):
    FIXTURE = Path(__file__).parent / "fixtures" / "otb-line-rect.tbk"

    def _run_main(self, argv):
        from unittest import mock

        import opentoolbook.__main__ as entry

        calls = []
        with mock.patch.object(entry, "open_page", lambda *a, **k: calls.append(a + (k.get("status"),))):
            code = entry.main(["opentoolbook", *argv])
        return code, calls

    def test_the_window_line_names_the_export_dll_once(self):
        from opentoolbook.shelf import unshipped_dll
        from opentoolbook.show import show_page

        with tempfile.TemporaryDirectory() as tmp:
            book = Path(tmp) / "lesson" / "otb-line-rect.tbk"
            book.parent.mkdir()
            book.write_bytes(self.FIXTURE.read_bytes())
            self.assertEqual(unshipped_dll(book), "MINSTB32.dll named, not shipped")
            code, calls = self._run_main(["--show", "", str(book)])
            self.assertEqual(code, 0)
            self.assertEqual(len(calls), 1)
            self.assertEqual(calls[0][-1], "MINSTB32.dll named, not shipped")
            code, calls = self._run_main([str(book)])
            self.assertEqual(code, 0)
            self.assertEqual(calls[0][1], "")
            self.assertEqual(calls[0][-1], "MINSTB32.dll named, not shipped")
            # The line does not stop the paint.
            kinds = [item.kind for item in show_page(calls[0][0], "", 600, 400).items]
            self.assertEqual(kinds[:2], ["background", "rectangle"])
            # A DLL the shelf finds, here in the parent and in another case, is not named.
            (Path(tmp) / "minstb32.DLL").write_bytes(b"")
            self.assertIsNone(unshipped_dll(book))
            code, calls = self._run_main(["--show", "", str(book)])
            self.assertIsNone(calls[0][-1])

    def test_the_lesson_opens_with_no_dll_on_disk(self):
        from opentoolbook.entry import opening_page
        from opentoolbook.shelf import find_file, search_roots, unshipped_dll
        from opentoolbook.show import show_page

        lesson = os.environ.get("OPENTOOLBOOK_TBK")
        if not lesson or not os.path.isfile(lesson):
            self.skipTest("set OPENTOOLBOOK_TBK to 9e954d01.tbk")
        path = Path(lesson)
        self.assertIsNone(find_file(search_roots(path, None), "MINSTB32.dll"))
        entry = opening_page(path)
        self.assertEqual((entry.book.name.lower(), entry.page_id), ("nida81.tbk", "P0"))
        self.assertEqual(unshipped_dll(entry.book), "MINSTB32.dll named, not shipped")
        self.assertEqual(unshipped_dll(path), "MINSTB32.dll named, not shipped")
        self.assertGreater(len(show_page(entry.data, entry.page_id, 624, 442).items), 1)
        code, calls = self._run_main([str(path)])
        self.assertEqual(code, 0)
        self.assertEqual((calls[0][1], calls[0][2], calls[0][-1]), ("P0", str(entry.book), "MINSTB32.dll named, not shipped"))


class ReportStaysHeadlessTests(unittest.TestCase):
    """After the window work, ``--report`` still prints and opens no window."""

    FIXTURE = Path(__file__).parent / "fixtures" / "otb-line-rect.tbk"
    REPORT = "records 11\nfollow-up reads 3\nnamed by the book 1\n  MINSTB32.dll\ncalls 0\n"

    def _run(self, argv):
        import contextlib
        import io
        from unittest import mock

        import opentoolbook.__main__ as entry

        out, err = io.StringIO(), io.StringIO()
        with mock.patch.object(entry, "open_page", return_value=()) as window:
            with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
                code = entry.main(["opentoolbook", *argv])
        return code, out.getvalue(), err.getvalue(), window

    def test_report_in_either_order_prints_the_report_and_no_window(self):
        book = str(self.FIXTURE)
        for argv in (["--report", book], [book, "--report"]):
            code, out, err, window = self._run(argv)
            self.assertEqual((code, out, err), (0, self.REPORT, ""), argv)
            window.assert_not_called()

    def test_bare_open_opens_the_window_and_prints_no_report(self):
        code, out, err, window = self._run([str(self.FIXTURE)])
        self.assertEqual((code, out, err), (0, "", ""))
        window.assert_called_once()
        self.assertEqual(window.call_args.args[1], "")

    def test_home_and_report_in_any_order_print_the_install_and_no_window(self):
        with tempfile.TemporaryDirectory() as tmp:
            home = Path(tmp)
            (home / "toolbook.lst").write_text("NC81BASE.SBK\n*NIDA81S.TBK\n", encoding="latin1")
            (home / "version.ini").write_text("[x]\nversion=8.1\ndate=2001\n", encoding="latin1")
            book = str(self.FIXTURE)
            outputs = set()
            for argv in (
                ["--home", str(home), "--report", book],
                ["--report", "--home", str(home), book],
                [book, "--report", "--home", str(home)],
                ["--home", str(home), book, "--report"],
            ):
                code, out, err, window = self._run(argv)
                self.assertEqual((code, err), (0, ""), argv)
                window.assert_not_called()
                outputs.add(out)
            self.assertEqual(len(outputs), 1)
            out = outputs.pop()
            self.assertTrue(out.startswith("version 8.1 2001\nrecords 11\n"))
            self.assertIn("  MINSTB32.dll  named, not shipped\n", out)
            self.assertIn("listed, not shipped\n  NIDA81S.TBK\n", out)
            # --home without a book prints the install folder and opens nothing.
            code, out, err, window = self._run(["--home", str(home)])
            self.assertEqual((code, err), (0, ""))
            window.assert_not_called()
            self.assertEqual(
                out,
                "version 8.1 2001\nshipped by the install\nrequired 1\n  NC81BASE.SBK  not found\n"
                "listed, not shipped\n  NIDA81S.TBK\n",
            )
            # --home with a book and no --report opens the window and prints nothing.
            code, out, err, window = self._run(["--home", str(home), book])
            self.assertEqual((code, out, err), (0, "", ""))
            window.assert_called_once()

    def test_the_report_runs_where_tkinter_cannot_import(self):
        import subprocess
        import sys

        script = (
            "import sys; sys.modules['tkinter'] = None\n"
            "from opentoolbook.__main__ import main\n"
            "raise SystemExit(main(['opentoolbook', sys.argv[1], '--report']))\n"
        )
        root = Path(__file__).resolve().parent.parent
        done = subprocess.run(
            [sys.executable, "-c", script, str(self.FIXTURE)],
            cwd=root,
            capture_output=True,
            text=True,
            timeout=60,
        )
        self.assertEqual((done.returncode, done.stdout, done.stderr), (0, self.REPORT, ""))

    def test_the_report_names_no_title_and_no_window_state(self):
        code, out, _err, window = self._run(["--report", str(self.FIXTURE)])
        self.assertEqual(code, 0)
        window.assert_not_called()
        self.assertNotIn(" - ", out)
        self.assertEqual(len(out.splitlines()), 5)
