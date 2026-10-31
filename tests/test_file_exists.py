"""``fileExists32`` is the shelf: 1 when the report's search finds the name."""

import os
import shutil
import tempfile
import unittest
from pathlib import Path

from opentoolbook.entry import choose_opening
from opentoolbook.send import Chain, send_message
from opentoolbook.shelf import file_exists32, search_roots

from test_entry import LOGO


class FileExistsTests(unittest.TestCase):
    def test_the_shelf_answers(self):
        with tempfile.TemporaryDirectory() as tmp:
            lessons = Path(tmp, "Lessons")
            lessons.mkdir()
            Path(tmp, "MRJ81.TBK").write_bytes(b"")
            roots = search_roots(lessons / "lesson.tbk", None)
            self.assertEqual(file_exists32(roots, "mrj81.tbk"), 1)
            self.assertEqual(file_exists32(roots, "logo81.tbk"), 0)

    def test_get_logo_book_follows_the_shelf(self):
        chain = Chain((("nc81base.sbk", {"getlogobook": LOGO}),))
        with tempfile.TemporaryDirectory() as tmp:
            roots = (Path(tmp),)
            self.assertEqual(send_message(chain, "getLogoBook", roots=roots).value, "nida81.tbk")
            Path(tmp, "mrj81.tbk").write_bytes(b"")
            self.assertEqual(send_message(chain, "getLogoBook", roots=roots).value, "mrj81.tbk")
            Path(tmp, "Logo81.tbk").write_bytes(b"")
            self.assertEqual(send_message(chain, "getLogoBook", roots=roots).value, "logo81.tbk")

    def test_it_is_a_value_too(self):
        with tempfile.TemporaryDirectory() as tmp:
            Path(tmp, "here.tbk").write_bytes(b"")
            handlers = {
                "entersystem": (
                    'to handle enterSystem\n'
                    '  found = fileExists32("HERE.TBK")\n'
                    '  get fileExists32("gone.tbk")\n'
                    '  if fileExists32("gone.tbk") <> 1 then\n'
                    '    if found = 1 then\n'
                    '      go to page "P2"\n'
                    '    end if\n'
                    '  end if\nend\n'
                ),
            }
            self.assertEqual(
                choose_opening(("P0", "P2"), handlers, roots=(Path(tmp),)),
                ("P2", None),
            )


class LessonLogoTests(unittest.TestCase):
    def _lesson(self):
        path = os.environ.get("OPENTOOLBOOK_TBK")
        if not path or not os.path.isfile(path):
            self.skipTest("set OPENTOOLBOOK_TBK to 9e954d01.tbk")
        lesson = Path(path)
        needed = {}
        for name in ("nida81.tbk", "nc81base.sbk", "nc81recs.sbk", "nc81test.sbk", "nc81trnr.sbk"):
            found = None
            for root in search_roots(lesson, None):
                for item in root.iterdir() if root.is_dir() else ():
                    if item.name.lower() == name:
                        found = item
                        break
                if found:
                    break
            if found is None:
                self.skipTest(f"{name} is not beside the lesson")
            needed[name] = found
        return lesson, needed

    def test_mrj81_without_logo81_opens_mrj81_and_neither_opens_nida81(self):
        from opentoolbook.entry import opening_page

        lesson, needed = self._lesson()
        with tempfile.TemporaryDirectory() as tmp:
            folder = Path(tmp)
            shutil.copy(lesson, folder / "9e954d01.tbk")
            for name, source in needed.items():
                shutil.copy(source, folder / name)
            self.assertEqual(opening_page(folder / "9e954d01.tbk").book.name, "nida81.tbk")
            shutil.copy(needed["nida81.tbk"], folder / "mrj81.tbk")
            entry = opening_page(folder / "9e954d01.tbk")
            self.assertEqual((entry.book.name, entry.page_id), ("mrj81.tbk", "P0"))


if __name__ == "__main__":
    unittest.main()
