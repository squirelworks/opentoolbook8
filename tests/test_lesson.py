"""The private-lesson tests find companions the way the shelf does."""

import os
import tempfile
import unittest
from pathlib import Path
from unittest import mock

from lesson import companion, lesson_path, logic_families_path


class LessonShelfTests(unittest.TestCase):
    def test_unset_or_missing_variable_is_no_lesson(self):
        with mock.patch.dict(os.environ, {}, clear=False):
            os.environ.pop("OPENTOOLBOOK_TBK", None)
            self.assertIsNone(lesson_path())
            self.assertIsNone(logic_families_path())
        with tempfile.TemporaryDirectory() as tmp:
            with mock.patch.dict(os.environ, {"OPENTOOLBOOK_TBK": str(Path(tmp) / "absent.tbk")}):
                self.assertIsNone(lesson_path())
                self.assertIsNone(logic_families_path())

    def test_another_book_is_a_lesson_path_but_not_logic_families(self):
        with tempfile.TemporaryDirectory() as tmp:
            other = Path(tmp) / "nida81.tbk"
            other.write_bytes(b"logo")
            with mock.patch.dict(os.environ, {"OPENTOOLBOOK_TBK": str(other)}):
                self.assertEqual(lesson_path(), other)
                self.assertIsNone(logic_families_path())

    def test_a_disc_layout_reads_companions_beside_and_in_the_parent_in_any_case(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            lessons = root / "Lessons"
            lessons.mkdir()
            book = lessons / "9e954d01.tbk"
            book.write_bytes(b"lesson")
            (lessons / "NC81RECS.SBK").write_bytes(b"recs")
            (lessons / "NC81TEST.SBK").write_bytes(b"test")
            (root / "NIDA81.TBK").write_bytes(b"logo")
            (root / "nc81recs.sbk").write_bytes(b"parent copy loses")
            with mock.patch.dict(os.environ, {"OPENTOOLBOOK_TBK": str(book)}):
                self.assertEqual(lesson_path(), book)
                self.assertEqual(logic_families_path(), book)
            upper = lessons / "9E954D01.TBK"
            book.rename(upper)
            with mock.patch.dict(os.environ, {"OPENTOOLBOOK_TBK": str(upper)}):
                self.assertEqual(logic_families_path(), upper)
            # Exact lower-case beside the lesson misses the disc spelling.
            self.assertFalse((lessons / "nc81recs.sbk").is_file())
            self.assertFalse((lessons / "nc81test.sbk").is_file())
            self.assertEqual(companion(upper, "nc81recs.sbk"), lessons / "NC81RECS.SBK")
            self.assertEqual(companion(upper, "nc81test.sbk"), lessons / "NC81TEST.SBK")
            self.assertEqual(companion(str(upper), "nida81.tbk"), root / "NIDA81.TBK")
            self.assertEqual(companion(upper, "nc81recs.sbk").read_bytes(), b"recs")
            self.assertEqual(companion(upper, "nc81test.sbk").read_bytes(), b"test")
            missing = companion(upper, "nc81trnr.sbk")
            self.assertEqual(missing, lessons / "nc81trnr.sbk")
            self.assertFalse(missing.is_file())


if __name__ == "__main__":
    unittest.main()
