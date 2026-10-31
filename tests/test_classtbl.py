"""Bound system books in the class table, and sysBooks on open."""

import os
import tempfile
import unittest
from pathlib import Path

from opentoolbook.classtbl import bound_sysbooks
from opentoolbook.entry import add_bound_sysbooks

FIXTURE = Path(__file__).with_name("fixtures") / "otb-line-rect.tbk"


class BoundTests(unittest.TestCase):
    def test_a_book_with_no_class_table_object_is_bound_to_nothing(self):
        self.assertEqual(bound_sysbooks(FIXTURE.read_bytes()), ())
        self.assertEqual(bound_sysbooks(b"not a book"), ())

    def test_open_appends_only_names_sysbooks_lacks(self):
        with tempfile.TemporaryDirectory() as tmp:
            from unittest.mock import patch

            from opentoolbook import entry

            with patch.object(entry, "bound_sysbooks", return_value=("TB80R.SBK", "TB80HYP.SBK")):
                listed = add_bound_sysbooks(["tb80r.sbk"], b"", (Path(tmp),))
        self.assertEqual(listed, ["tb80r.sbk", "tb80hyp.sbk"])

    def test_the_lesson_is_bound_to_tb80anm_and_tb80r(self):
        path = os.environ.get("OPENTOOLBOOK_TBK")
        if not path or not os.path.isfile(path):
            self.skipTest("set OPENTOOLBOOK_TBK to 9e954d01.tbk")
        from opentoolbook.entry import opening_page

        lesson = Path(path)
        self.assertEqual(bound_sysbooks(lesson.read_bytes()), ("TB80ANM.SBK", "TB80R.SBK"))
        # The script never pushes tb80anm.sbk. It is in sysBooks only through the bound list.
        self.assertIn("tb80anm.sbk", opening_page(lesson).sysbooks)


if __name__ == "__main__":
    unittest.main()
