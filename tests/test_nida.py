"""The NIDA menu, the disc table, the key disk, and the install list."""

import os
import unittest
from pathlib import Path

from opentoolbook.nida import discs_for, parse_cailt, parse_catalog, parse_settings, parse_shifts, read_keydisk
from opentoolbook.shelf import named_calls, named_files, on_disk, parse_install_list

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
