"""The private-lesson tests find companions the way the shelf does."""

import os
import tempfile
import unittest
from pathlib import Path
from unittest import mock

from lesson import companion, lesson_path


class LessonShelfTests(unittest.TestCase):
    def test_unset_or_missing_variable_is_no_lesson(self):
        with mock.patch.dict(os.environ, {}, clear=False):
            os.environ.pop("OPENTOOLBOOK_TBK", None)
            self.assertIsNone(lesson_path())
        with tempfile.TemporaryDirectory() as tmp:
            with mock.patch.dict(os.environ, {"OPENTOOLBOOK_TBK": str(Path(tmp) / "absent.tbk")}):
                self.assertIsNone(lesson_path())

    def test_a_disc_layout_reads_companions_beside_and_in_the_parent_in_any_case(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            lessons = root / "Lessons"
            lessons.mkdir()
            book = lessons / "9e954d01.tbk"
            book.write_bytes(b"lesson")
            (lessons / "NC81RECS.SBK").write_bytes(b"recs")
            (root / "NIDA81.TBK").write_bytes(b"logo")
            (root / "nc81recs.sbk").write_bytes(b"parent copy loses")
            with mock.patch.dict(os.environ, {"OPENTOOLBOOK_TBK": str(book)}):
                self.assertEqual(lesson_path(), book)
            self.assertEqual(companion(book, "nc81recs.sbk"), lessons / "NC81RECS.SBK")
            self.assertEqual(companion(str(book), "nida81.tbk"), root / "NIDA81.TBK")
            missing = companion(book, "nc81trnr.sbk")
            self.assertEqual(missing, lessons / "nc81trnr.sbk")
            self.assertFalse(missing.is_file())


if __name__ == "__main__":
    unittest.main()
