"""File names and call names a book mentions, and the install list."""

import os
import unittest
from pathlib import Path

from opentoolbook.shelf import named_calls, named_files, on_disk, parse_install_list

LIST = """NC81BASE.SBK
*NIDA81S.TBK
TB80BAS.DLL
"""


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


class SpecimenTests(unittest.TestCase):
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
