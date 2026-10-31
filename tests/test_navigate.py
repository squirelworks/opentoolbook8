"""A quoted ``of book`` click uses the same search as opening a book."""

import os
import tempfile
import unittest
from pathlib import Path

from opentoolbook.navigate import MissingBook, Navigator

FIXTURE = Path(__file__).parent / "fixtures" / "otb-line-rect.tbk"
LESSON = os.environ.get("OPENTOOLBOOK_TBK")


def _lesson():
    if not LESSON or not os.path.isfile(LESSON):
        return None
    return Path(LESSON)


class SearchTests(unittest.TestCase):
    def test_book_directory_parent_and_home_folders_regardless_of_case(self):
        with tempfile.TemporaryDirectory() as tmp:
            top = Path(tmp)
            lesson = top / "Lessons" / "LF"
            lesson.mkdir(parents=True)
            book = lesson / "9e954d01.tbk"
            book.write_bytes(FIXTURE.read_bytes())
            home = top / "home"
            (home / "courses").mkdir(parents=True)
            (home / "Nida98" / "Lessons").mkdir(parents=True)
            (top / "Lessons" / "NIDA81.TBK").write_bytes(b"")
            (home / "courses" / "Logo81.tbk").write_bytes(b"")
            (home / "Nida98" / "Lessons" / "mrj81.TBK").write_bytes(b"")
            nav = Navigator(FIXTURE.read_bytes(), "", book, home)
            self.assertEqual(nav.find_book("nida81.tbk", "P310"), top / "Lessons" / "NIDA81.TBK")
            self.assertEqual(nav.find_book("logo81.tbk", "P0"), home / "courses" / "Logo81.tbk")
            self.assertEqual(nav.find_book("MRJ81.tbk", "P0"), home / "Nida98" / "Lessons" / "mrj81.TBK")
            (lesson / "nida81.tbk").write_bytes(b"")
            self.assertEqual(nav.find_book("nida81.tbk", "P310"), lesson / "nida81.tbk")

    def test_a_missing_book_names_the_file_and_the_page(self):
        with tempfile.TemporaryDirectory() as tmp:
            book = Path(tmp) / "a" / "lesson.tbk"
            book.parent.mkdir()
            book.write_bytes(FIXTURE.read_bytes())
            nav = Navigator(FIXTURE.read_bytes(), "", book)
            with self.assertRaises(MissingBook) as caught:
                nav.find_book("nida71.tbk", "P310")
            self.assertIn("nida71.tbk", str(caught.exception))
            self.assertIn("P310", str(caught.exception))
            self.assertIsInstance(caught.exception, ValueError)


class HistoryTests(unittest.TestCase):
    def test_nothing_shown_before_is_a_viewer_back_that_stays(self):
        nav = Navigator(FIXTURE.read_bytes(), "", FIXTURE)
        self.assertEqual(nav.history, [])
        self.assertFalse(nav.back())
        self.assertFalse(nav.click("nothing").moved)
        self.assertEqual(nav.history, [])

    def test_viewer_back_pops_the_shown_pages_not_the_stored_list(self):
        path = _lesson()
        if path is None:
            self.skipTest("set OPENTOOLBOOK_TBK to 9e954d01.tbk")
        nav = Navigator(path.read_bytes(), "P300", path)
        nav.click("Next")
        self.assertEqual(nav.page_id, "P400")
        self.assertTrue(nav.back())
        self.assertEqual((nav.book, nav.page_id), (path, "P300"))
        nav.click("Selection1")
        self.assertEqual((nav.book.name, nav.page_id), ("nida81.tbk", "P310"))
        self.assertEqual(nav.pages[nav.pages.index("P310") - 1], "P0")
        self.assertTrue(nav.back())
        self.assertEqual((nav.book, nav.page_id), (path, "P300"))
        self.assertIn("P400", nav.pages)
        self.assertFalse(nav.back())
        stored = Navigator(path.read_bytes(), "P400", path)
        stored.click("Back")
        self.assertEqual(stored.page_id, "P300")


class LessonTests(unittest.TestCase):
    def test_selection1_on_p300_opens_p310_of_nida81_in_the_parent(self):
        path = _lesson()
        if path is None:
            self.skipTest("set OPENTOOLBOOK_TBK to 9e954d01.tbk")
        companion = path.with_name("nida81.tbk")
        with tempfile.TemporaryDirectory() as tmp:
            top = Path(tmp)
            (top / "LF").mkdir()
            lesson = top / "LF" / "9e954d01.tbk"
            lesson.symlink_to(path.resolve())
            (top / "Nida81.TBK").symlink_to(companion.resolve())
            nav = Navigator(lesson.read_bytes(), "P300", lesson)
            clicked = nav.click("Selection1")
            self.assertTrue(clicked.moved)
            self.assertEqual(nav.page_id, "P310")
            self.assertEqual(nav.book, top / "Nida81.TBK")
            self.assertIn("P310", nav.pages)
            back = Navigator(lesson.read_bytes(), "P300", lesson)
            self.assertTrue(back.click("Next").moved)
            self.assertEqual((back.page_id, back.book), ("P400", lesson))
            (top / "Nida81.TBK").unlink()
            missing = Navigator(lesson.read_bytes(), "P300", lesson)
            with self.assertRaises(MissingBook) as caught:
                missing.click("Selection1")
            self.assertIn("nida81.tbk", str(caught.exception))
            self.assertIn("P310", str(caught.exception))
            self.assertEqual((missing.page_id, missing.book), ("P300", lesson))

    def test_next_from_p300_runs_the_book_enter_page_for_p400(self):
        path = _lesson()
        if path is None:
            self.skipTest("set OPENTOOLBOOK_TBK to 9e954d01.tbk")

        def page_number(nav):
            listed = nav.display(400, 300)
            self.assertEqual(listed.page_id, nav.page_id)
            return [item.text for item in listed.items if item.kind == "field" and item.name.lower() == "page#"]

        nav = Navigator(path.read_bytes(), "P300", path)
        self.assertEqual(page_number(nav), ["P300"])
        self.assertTrue(nav.click("Next").moved)
        self.assertEqual(nav.page_id, "P400")
        self.assertEqual(page_number(nav), ["P400"])
        back = Navigator(path.read_bytes(), "P100", path)
        self.assertTrue(back.click("Back").moved)
        self.assertEqual(back.page_id, "P10")
        first = [item.text for item in back.display(400, 300).items if item.kind == "field" and item.name.lower() == "first"]
        self.assertEqual(first, ["Hello Student, this lesson is about:"])
        switched = Navigator(path.read_bytes(), "P300", path)
        switched.click("Selection1")
        self.assertEqual((switched.book.name, switched.page_id), ("nida81.tbk", "P310"))
        self.assertEqual(page_number(switched), ["P310"])

    def test_landing_on_lesson_p0_follows_its_enter_page_to_the_logo_book(self):
        path = _lesson()
        if path is None:
            self.skipTest("set OPENTOOLBOOK_TBK to 9e954d01.tbk")
        nav = Navigator(path.read_bytes(), "P0", path)
        nav.enter()
        self.assertEqual((nav.book.name, nav.page_id), ("nida81.tbk", "P0"))
        self.assertEqual(nav.variables["lastbook"], path.name)
        self.assertEqual(nav.variables["nextpage"], "p10")
        stays = Navigator(path.read_bytes(), "P10", path)
        stays.enter()
        self.assertEqual((stays.book, stays.page_id), (path, "P10"))


if __name__ == "__main__":
    unittest.main()
