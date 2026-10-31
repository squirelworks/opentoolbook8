"""The NIDA menu, the disc table, the key disk, and the install list."""

import os
import unittest
from pathlib import Path

from opentoolbook.nida import discs_for, parse_cailt, parse_catalog, parse_settings, parse_shifts, read_keydisk, zip_names_for
from opentoolbook.shelf import find_file, named_calls, named_files, on_disk, parse_install_list

MENU = """<?xml version="1.0"?>
<Document type="nida:m3search" version="1.0">
  <Menu courseid="DEMO" title="Demo course">
    <Menu title="Mod 01">
      <Item title="First lesson" lessonid="10001001" />
    </Menu>
    <Menu title="Mod 02">
      <Menu title="Nested">
        <Item title="Second lesson" lessonid="9E954D01" />
      </Menu>
    </Menu>
  </Menu>
</Document>
"""

CAILT = """$ Nida CAI CD Lookup Table
9E954??* DIE??V03
9E954D0?* DIE-EXACT
93951??* DCX??V03, STX00V03
9395R??*
"""

LIST = """NC81BASE.SBK
*NIDA81S.TBK
TB80BAS.DLL
"""


class CatalogTests(unittest.TestCase):
    def test_course_modules_and_lessons(self):
        catalog = parse_catalog(MENU)
        self.assertEqual(len(catalog.courses), 1)
        course = catalog.courses[0]
        self.assertEqual(course.course_id, "DEMO")
        self.assertEqual(len(course.modules), 2)
        self.assertEqual(course.modules[1].children[0].lessons[0].lesson_id, "9E954D01")
        self.assertEqual(catalog.lesson_ids(), ("10001001", "9E954D01"))

    def test_rejects_a_different_document(self):
        with self.assertRaises(ValueError):
            parse_catalog("<Document type='other'/>")


class DiscTests(unittest.TestCase):
    def setUp(self):
        self.rules = parse_cailt(CAILT)

    def test_the_more_specific_pattern_wins(self):
        self.assertEqual(discs_for(self.rules, "9E954D01"), ("DIE-EXACT",))
        self.assertEqual(discs_for(self.rules, "9e954abc.tbk"), ("DIE??V03",))

    def test_several_discs_and_an_empty_rule(self):
        self.assertEqual(discs_for(self.rules, "93951100"), ("DCX??V03", "STX00V03"))
        self.assertEqual(discs_for(self.rules, "9395R99"), ())
        self.assertEqual(discs_for(self.rules, "00000000"), ())


class KeyDiskTests(unittest.TestCase):
    def test_rating_folder(self):
        import tempfile

        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "INFO.TXT").write_text("A rating.\n", encoding="latin1")
            (root / "shifts.s4").write_text(
                "[Shift]\nShift=3\nStart=19:00\nEnd=01:00\n03/17/2005\n[Closed]\n3/19/2005=1\n",
                encoding="latin1",
            )
            (root / "criteria.s5").write_text("emHxslloWzb=639;emIllgKzgs=X:\\Rmvg;", encoding="latin1")
            (root / "CLASS.S3").write_bytes(b"\x01\x00\x0drest")
            disk = read_keydisk(root)
        self.assertEqual(disk.info, "A rating.")
        self.assertIsNotNone(disk.shift)
        self.assertEqual(disk.shift.shift, "3")
        self.assertEqual(disk.shift.start, "19:00")
        self.assertEqual(disk.shift.closed, ("3/19/2005",))
        self.assertEqual(disk.shift.notes, ("03/17/2005",))
        self.assertEqual(disk.settings[1], ("emIllgKzgs", "X:\\Rmvg"))
        self.assertEqual(disk.records, (("class.s3", 1, 7),))

    def test_settings_keep_the_encoded_pairs(self):
        pairs = parse_settings("emOne=1;emTwo=X:\\Abc;")
        self.assertEqual(pairs, (("emOne", "1"), ("emTwo", "X:\\Abc")))
        self.assertEqual(parse_shifts("[Shift]\nShift=1\nStart=08:00\nEnd=16:00\n").shift, "1")


class ShelfTests(unittest.TestCase):
    def test_names_and_calls_in_a_book(self):
        data = b"\x00nc81base.sbk\x00initializebase\x00openSession\x00Version: 2.004.TBK\x00"
        self.assertEqual(named_files(data), ("nc81base.sbk",))
        self.assertEqual(named_calls(data), ("initializebase", "opensession"))

    def test_install_list_marks_the_starred_file_optional(self):
        files = parse_install_list(LIST)
        self.assertEqual([(item.name, item.optional) for item in files], [
            ("NC81BASE.SBK", False),
            ("NIDA81S.TBK", True),
            ("TB80BAS.DLL", False),
        ])

    def test_presence_is_case_insensitive(self):
        import tempfile

        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "nc81base.sbk").write_bytes(b"")
            present, missing = on_disk(root, ("NC81BASE.SBK", "nida81.tbk"))
        self.assertEqual(present, ("NC81BASE.SBK",))
        self.assertEqual(missing, ("nida81.tbk",))


class FixtureTests(unittest.TestCase):
    def test_names_calls_catalog_directory_and_die_zip(self):
        files = (
            "93954302.tbk",
            "93954d01.tbk",
            "minstb32.dll",
            "nc81base.sbk",
            "nc81recs.sbk",
            "nc81test.sbk",
            "nc81trnr.sbk",
            "nida81.tbk",
            "tb80anm.sbk",
            "tb80r.sbk",
        )
        calls = (
            "enterapplication",
            "entersystem",
            "gotopagelist",
            "initializebase",
            "initializerecs",
            "initializetest",
            "initializetrnr",
            "opensession",
        )
        blob = b"\x00".join(name.encode("ascii") for name in files + calls)
        blob += b"\x00Version: 2.004.TBK\x00class.s3\x00id.s3\x00criteria.s4\x00m00001.s3\x00login.m3\x00"
        self.assertEqual(named_files(blob), files)
        self.assertEqual(named_calls(blob), calls)
        book = os.environ.get("OPENTOOLBOOK_TBK")
        if book and os.path.isfile(book):
            data = Path(book).read_bytes()
            self.assertEqual(named_files(data), files)
            self.assertEqual(named_calls(data), calls)
        rules = parse_cailt("9E954??* DIE??V03\n")
        self.assertEqual(discs_for(rules, "9E954D01"), ("DIE??V03",))
        self.assertEqual(zip_names_for(rules, "9E954D01"), ("die0dv03.zip",))
        import contextlib
        import io
        import tempfile

        from opentoolbook.__main__ import main

        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "courses.xml").write_text(MENU, encoding="latin1")
            (root / "programs.xml").write_text(
                MENU.replace('lessonid="9E954D01"', 'lessonid="93950199"'),
                encoding="latin1",
            )
            (root / "TB80ANM.SBK").write_bytes(b"")
            found = find_file((root,), "tb80anm.sbk")
            self.assertEqual(found, root / "TB80ANM.SBK")
            buf = io.StringIO()
            with contextlib.redirect_stdout(buf):
                code = main(["opentoolbook", "--catalog", str(root)])
            text = buf.getvalue()
        self.assertEqual(code, 0)
        self.assertIn("courses.xml unique lesson ids 2", text)
        self.assertIn("programs.xml unique lesson ids 2", text)
        self.assertIn("only in programs.xml 1", text)
        self.assertIn("93950199", text)


ONE_LESSON = """<?xml version="1.0"?>
<Document type="nida:m3search" version="1.0">
  <Menu courseid="LF" title="Logic Families">
    <Menu title="Mod 01">
      <Item title="Logic Families" lessonid="9E954D01" />
    </Menu>
  </Menu>
</Document>
"""

FIXTURE = Path(__file__).parent / "fixtures" / "otb-line-rect.tbk"


def _main(argv):
    import contextlib
    import io
    from unittest import mock

    import opentoolbook.__main__ as entry

    calls = []
    out, err = io.StringIO(), io.StringIO()
    window = mock.patch.object(entry, "open_page", lambda *a, **k: calls.append(a))
    with window, contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
        code = entry.main(["opentoolbook", *argv])
    return code, calls, out.getvalue(), err.getvalue()


class CatalogOpenTests(unittest.TestCase):
    def test_open_resolves_the_lesson_id_under_the_catalog_folder(self):
        import tempfile

        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "courses"
            root.mkdir()
            catalog = root / "courses.xml"
            catalog.write_text(ONE_LESSON, encoding="latin1")
            lesson = root / "9E954D01.TBK"
            lesson.write_bytes(FIXTURE.read_bytes())
            for target in (str(catalog), str(root)):
                code, calls, out, err = _main(["--catalog", target, "--open", "9E954D01"])
                self.assertEqual((code, out, err), (0, "", ""))
                self.assertEqual(len(calls), 1)
                data, page_id, book = calls[0][:3]
                self.assertEqual((data, page_id, book), (FIXTURE.read_bytes(), "", str(lesson)))
            code, calls, _out, _err = _main(["--catalog", str(catalog), "--open", "9e954d01"])
            self.assertEqual(code, 0)
            self.assertEqual(calls[0][2], str(lesson))
            # The lesson in the parent of the catalog folder is the shelf's second root.
            lesson.rename(Path(tmp) / "9e954d01.tbk")
            code, calls, _out, _err = _main(["--catalog", str(catalog), "--open", "9E954D01"])
            self.assertEqual((code, calls[0][2]), (0, str(Path(tmp) / "9e954d01.tbk")))
            # --home/Nida98/Lessons is searched too.
            home = Path(tmp) / "home"
            (home / "Nida98" / "Lessons").mkdir(parents=True)
            (Path(tmp) / "9e954d01.tbk").rename(home / "Nida98" / "Lessons" / "9e954d01.tbk")
            code, calls, _out, err = _main(["--catalog", str(catalog), "--open", "9E954D01"])
            self.assertEqual((code, calls), (2, []))
            self.assertEqual(err, "9e954d01.tbk was not found; lesson 9E954D01 does not open\n")
            code, calls, _out, _err = _main(
                ["--catalog", str(catalog), "--open", "9E954D01", "--home", str(home)]
            )
            self.assertEqual(calls[0][2], str(home / "Nida98" / "Lessons" / "9e954d01.tbk"))
            self.assertEqual(calls[0][3], str(home))

    def test_a_missing_lesson_names_its_cailt_disc(self):
        import tempfile

        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "courses"
            root.mkdir()
            catalog = root / "courses.xml"
            catalog.write_text(ONE_LESSON, encoding="latin1")
            code, calls, _out, err = _main(["--catalog", str(catalog), "--open", "9E954D01"])
            self.assertEqual((code, calls), (2, []))
            self.assertEqual(err, "9e954d01.tbk was not found; lesson 9E954D01 does not open\n")
            home = Path(tmp) / "home"
            home.mkdir()
            (home / "Cailt.dat").write_text(CAILT, encoding="latin1")
            code, calls, out, err = _main(
                ["--catalog", str(catalog), "--open", "9E954D01", "--home", str(home)]
            )
            self.assertEqual((code, calls, out), (2, [], ""))
            self.assertEqual(
                err,
                "9e954d01.tbk was not found; lesson 9E954D01 does not open; "
                "CAILT.DAT puts it on disc DIE-EXACT\n",
            )
            (home / "Cailt.dat").write_text("9E954??* DIE??V03, STX00V03\n", encoding="latin1")
            code, calls, _out, err = _main(
                ["--catalog", str(catalog), "--open", "9E954D01", "--home", str(home)]
            )
            self.assertEqual((code, calls), (2, []))
            self.assertTrue(err.endswith("; CAILT.DAT puts it on discs DIE??V03, STX00V03\n"))
            (home / "Cailt.dat").write_text("93951??* DCX??V03\n", encoding="latin1")
            code, calls, _out, err = _main(
                ["--catalog", str(catalog), "--open", "9E954D01", "--home", str(home)]
            )
            self.assertTrue(err.endswith("; CAILT.DAT names no disc for it\n"))
            # Beside the catalog the table is on the shelf without --home.
            (home / "Cailt.dat").rename(root / "CAILT.DAT")
            (root / "CAILT.DAT").write_text(CAILT, encoding="latin1")
            code, calls, _out, err = _main(["--catalog", str(root), "--open", "9e954d01"])
            self.assertEqual((code, calls), (2, []))
            self.assertTrue(err.endswith("; CAILT.DAT puts it on disc DIE-EXACT\n"))

    def test_an_id_the_catalog_does_not_list_is_an_error(self):
        import tempfile

        with tempfile.TemporaryDirectory() as tmp:
            catalog = Path(tmp) / "courses.xml"
            catalog.write_text(ONE_LESSON, encoding="latin1")
            (Path(tmp) / "10001001.tbk").write_bytes(FIXTURE.read_bytes())
            code, calls, out, err = _main(["--catalog", str(catalog), "--open", "10001001"])
        self.assertEqual((code, calls, out), (2, [], ""))
        self.assertEqual(err, "10001001 is not a lesson in the catalog\n")

    def test_without_open_the_catalog_printout_is_unchanged(self):
        import tempfile

        with tempfile.TemporaryDirectory() as tmp:
            catalog = Path(tmp) / "courses.xml"
            catalog.write_text(ONE_LESSON, encoding="latin1")
            (Path(tmp) / "9e954d01.tbk").write_bytes(FIXTURE.read_bytes())
            code, calls, out, err = _main(["--catalog", str(catalog)])
        self.assertEqual((code, calls, err), (0, [], ""))
        self.assertEqual(
            out,
            "courses 1\nlessons 1\ncourses.xml unique lesson ids 1\nLF\tLogic Families\t1\n",
        )

    def test_open_needs_a_catalog(self):
        code, calls, _out, _err = _main(["--open", "9E954D01"])
        self.assertEqual((code, calls), (2, []))

    def test_open_the_real_lesson_from_a_catalog(self):
        import tempfile

        path = os.environ.get("OPENTOOLBOOK_TBK")
        if not path or not os.path.isfile(path):
            self.skipTest("set OPENTOOLBOOK_TBK to 9e954d01.tbk")
        catalog_dir = Path(path).parent
        with tempfile.TemporaryDirectory() as tmp:
            catalog = Path(tmp) / "courses.xml"
            catalog.write_text(ONE_LESSON, encoding="latin1")
            code, calls, _out, err = _main(
                ["--catalog", str(catalog), "--open", "9E954D01", "--home", str(catalog_dir)]
            )
        self.assertEqual((code, err), (0, ""))
        self.assertEqual(calls[0][1], "P0")
        self.assertEqual(Path(calls[0][2]).name.lower(), "nida81.tbk")


class SpecimenNidaTests(unittest.TestCase):
    def test_lesson_names_the_shell(self):
        path = os.environ.get("OPENTOOLBOOK_TBK")
        if not path or not os.path.isfile(path):
            self.skipTest("set OPENTOOLBOOK_TBK to the lesson book")
        data = Path(path).read_bytes()
        self.assertIn("nida81.tbk", named_files(data))
        self.assertIn("nc81base.sbk", named_files(data))
        self.assertIn("93954302.tbk", named_files(data))
        self.assertNotIn("004.tbk", named_files(data))
        calls = named_calls(data)
        for name in ("initializebase", "initializerecs", "initializetest", "opensession"):
            self.assertIn(name, calls)


if __name__ == "__main__":
    unittest.main()
