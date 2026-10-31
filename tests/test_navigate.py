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


class ShelfTests(unittest.TestCase):
    def test_a_click_from_the_logo_book_still_searches_beside_the_lesson(self):
        with tempfile.TemporaryDirectory() as tmp:
            top = Path(tmp)
            home = top / "home"
            (home / "courses").mkdir(parents=True)
            logo = home / "courses" / "nida81.tbk"
            logo.write_bytes(FIXTURE.read_bytes())
            lesson = top / "discs" / "LF" / "9e954d01.tbk"
            lesson.parent.mkdir(parents=True)
            lesson.write_bytes(FIXTURE.read_bytes())
            (lesson.parent / "93954302.TBK").write_bytes(b"")
            nav = Navigator(logo.read_bytes(), "", logo, home, lesson)
            self.assertEqual(nav.find_book("93954302.tbk", "P0"), lesson.parent / "93954302.TBK")
            self.assertEqual(nav.find_book("9E954D01.tbk", "P400"), lesson)
            self.assertEqual(nav.roots()[:2], (lesson.parent, lesson.parent.parent))
            self.assertIn(home / "courses", nav.roots())
            alone = Navigator(logo.read_bytes(), "", logo, home)
            with self.assertRaises(MissingBook):
                alone.find_book("93954302.tbk", "P0")
            self.assertEqual(alone.lesson, logo)


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

    def test_logo_p0_has_no_button_and_its_page_click_reads_two_variables(self):
        path = _lesson()
        if path is None:
            self.skipTest("set OPENTOOLBOOK_TBK to 9e954d01.tbk")
        from opentoolbook.click import page_click
        from opentoolbook.enter import page_source
        from opentoolbook.show import button_at, show_page

        logo = path.with_name("nida81.tbk")
        data = logo.read_bytes()
        self.assertIn("go to page (nextpage) of book(lastbook)", page_source(data, "P0"))
        listed = show_page(data, "P0", 800, 600)
        self.assertEqual([item for item in listed.items if item.kind == "button"], [])
        self.assertIsNone(button_at(listed, 400, 300))
        shown = Navigator(data, "P0", logo)
        self.assertFalse(shown.click(None).moved)
        self.assertEqual((shown.page_id, shown.book), ("P0", logo))
        self.assertIsNone(page_click(data, "P310", shown.pages))
        assigned = Navigator(data, "P0", logo, variables={"NextPage": "p10", "lastbook": "9e954d01.tbk"})
        self.assertTrue(assigned.click(None).moved)
        self.assertEqual((assigned.page_id, assigned.book.name), ("P10", path.name))

    def test_the_opening_window_on_the_logo_book_finds_the_lesson(self):
        path = _lesson()
        if path is None:
            self.skipTest("set OPENTOOLBOOK_TBK to 9e954d01.tbk")
        from opentoolbook.entry import opening_page

        with tempfile.TemporaryDirectory() as tmp:
            top = Path(tmp)
            home = top / "home"
            (home / "courses").mkdir(parents=True)
            for name in ("nida81.tbk", "nc81base.sbk", "nc81recs.sbk", "nc81test.sbk", "nc81trnr.sbk"):
                (home / "courses" / name).symlink_to(path.with_name(name).resolve())
            lesson = top / "discs" / "LF" / "9e954d01.tbk"
            lesson.parent.mkdir(parents=True)
            lesson.symlink_to(path.resolve())
            entry = opening_page(lesson, home)
            self.assertEqual((entry.page_id, entry.book.name), ("P0", "nida81.tbk"))
            nav = Navigator(entry.data, entry.page_id, entry.book, home, lesson)
            self.assertEqual(nav.find_book("9e954d01.tbk", "P400"), lesson)
            self.assertEqual(nav.home, home)


if __name__ == "__main__":
    unittest.main()
