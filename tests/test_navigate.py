"""A quoted ``of book`` click uses the same search as opening a book."""

import os
import tempfile
import unittest
from pathlib import Path

from opentoolbook.navigate import MissingBook, Navigator

from lesson import companion

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
            (top / "Lessons" / "NIDA81.TBK").write_bytes(b"")
            (home / "Logo81.tbk").write_bytes(b"")
            # A folder below home is not on the shelf.
            (home / "courses" / "mrj81.TBK").write_bytes(b"")
            nav = Navigator(FIXTURE.read_bytes(), "", book, home)
            self.assertEqual(nav.find_book("nida81.tbk", "P310"), top / "Lessons" / "NIDA81.TBK")
            self.assertEqual(nav.find_book("logo81.tbk", "P0"), home / "Logo81.tbk")
            with self.assertRaises(MissingBook):
                nav.find_book("MRJ81.tbk", "P0")
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


class NidaRoundTripTests(unittest.TestCase):
    def test_selection1_then_next_or_back_returns_to_the_lesson_page(self):
        path = _lesson()
        if path is None:
            self.skipTest("set OPENTOOLBOOK_TBK to 9e954d01.tbk")
        logo = path.with_name("nida81.tbk")
        nav = Navigator(path.read_bytes(), "P300", path)
        nav.click("Selection1")
        self.assertEqual((nav.book.name, nav.page_id), ("nida81.tbk", "P310"))
        self.assertEqual(nav.variables, {"lastbook": path.name, "nextpage": "P300"})
        self.assertTrue(nav.click("Next").moved)
        self.assertEqual((nav.book, nav.page_id), (path, "P300"))
        for button in ("Next", "Back"):
            p340 = Navigator(logo.read_bytes(), "P340", logo, lesson=path, variables={"lastbook": path.name, "nextpage": "P300"})
            self.assertTrue(p340.click(button).moved)
            self.assertEqual((p340.book, p340.page_id), (path, "P300"))
            unset = Navigator(logo.read_bytes(), "P340", logo, lesson=path)
            self.assertFalse(unset.click(button).moved)
            self.assertEqual(unset.page_id, "P340")


class StartupVariableTests(unittest.TestCase):
    def test_enter_page_assignments_come_back_from_startup(self):
        from opentoolbook.entry import choose_opening

        source = 'to handle enterPage\n    system lastbook, nextpage\n    lastbook = name of this book\n    nextpage = "p10"\nend\n'
        variables: dict = {}
        page, book = choose_opening(("P1",), {}, {"P1": source}, book_name="9e954d01.tbk", variables=variables)
        self.assertEqual((page, book), ("P1", None))
        self.assertEqual(variables["lastbook"], "9e954d01.tbk")
        self.assertEqual(variables["nextpage"], "p10")


class TitleTests(unittest.TestCase):
    def test_the_title_is_the_book_file_and_the_page_id(self):
        nav = Navigator(FIXTURE.read_bytes(), "", FIXTURE)
        self.assertEqual(nav.title(), "otb-line-rect.tbk - ")
        self.assertEqual(Navigator(FIXTURE.read_bytes(), "P1").title(), "P1")

    def test_the_title_follows_open_next_and_a_book_switch(self):
        path = _lesson()
        if path is None:
            self.skipTest("set OPENTOOLBOOK_TBK to 9e954d01.tbk")
        from opentoolbook.entry import opening_page

        entry = opening_page(path)
        opened = Navigator(entry.data, entry.page_id, entry.book)
        self.assertEqual(opened.title(), "nida81.tbk - P0")
        nav = Navigator(path.read_bytes(), "P300", path)
        self.assertEqual(nav.title(), "9e954d01.tbk - P300")
        nav.click("Next")
        self.assertEqual(nav.title(), "9e954d01.tbk - P400")
        switched = Navigator(path.read_bytes(), "P300", path)
        switched.click("Selection1")
        self.assertEqual(switched.title(), "nida81.tbk - P310")

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
        logo_book = companion(path, "nida81.tbk")
        with tempfile.TemporaryDirectory() as tmp:
            top = Path(tmp)
            (top / "LF").mkdir()
            lesson = top / "LF" / "9e954d01.tbk"
            lesson.symlink_to(path.resolve())
            (top / "Nida81.TBK").symlink_to(logo_book.resolve())
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

    def test_click_handlers_are_the_book_then_its_sysbooks(self):
        path = _lesson()
        if path is None:
            self.skipTest("set OPENTOOLBOOK_TBK to 9e954d01.tbk")
        from opentoolbook.entry import opening_page

        # A book the lesson only mentions adds no handler.
        alone = Navigator(path.read_bytes(), "P10210", path)
        self.assertNotIn("handlequizclick", alone.handlers())
        self.assertIn("entersystem", alone.handlers())
        pushed = Navigator(path.read_bytes(), "P10210", path, sysbooks=opening_page(path).sysbooks)
        self.assertIn("handlequizclick", pushed.handlers())
        self.assertIn("getlogobook", pushed.handlers())

    def test_landing_on_lesson_p0_follows_its_enter_page_to_the_logo_book(self):
        path = _lesson()
        if path is None:
            self.skipTest("set OPENTOOLBOOK_TBK to 9e954d01.tbk")
        from opentoolbook.entry import opening_page

        # The lesson's own startup pushes nc81base.sbk, which holds getLogoBook, and sets __import.
        entry = opening_page(path)
        nav = Navigator(path.read_bytes(), "P0", path, props=entry.props, sysbooks=entry.sysbooks)
        nav.enter()
        self.assertEqual((nav.book.name, nav.page_id), ("nida81.tbk", "P0"))
        self.assertEqual(nav.variables["lastbook"], path.name)
        self.assertEqual(nav.variables["nextpage"], "p10")
        stays = Navigator(path.read_bytes(), "P10", path)
        stays.enter()
        self.assertEqual((stays.book, stays.page_id), (path, "P10"))
    def test_logo_p0_has_no_button_and_its_page_click_reads_two_variables(self):
        path = _lesson()
        if path is None:
            self.skipTest("set OPENTOOLBOOK_TBK to 9e954d01.tbk")
        from opentoolbook.click import page_click
        from opentoolbook.enter import page_source
        from opentoolbook.show import button_at, show_page

        logo = companion(path, "nida81.tbk")
        data = logo.read_bytes()
        self.assertIn("go to page (nextpage) of book(lastbook)", page_source(data, "P0"))
        listed = show_page(data, "P0", 800, 600)
        self.assertEqual([item for item in listed.items if item.kind == "button"], [])
        self.assertIsNone(button_at(listed, 400, 300))
        shown = Navigator(data, "P0", logo)
        self.assertFalse(shown.click(None).moved)
        self.assertEqual((shown.page_id, shown.book), ("P0", logo))
        self.assertIsNone(page_click(data, "P310", shown.pages))
        assigned = Navigator(data, "P0", logo, lesson=path, variables={"NextPage": "p10", "lastbook": "9e954d01.tbk"})
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
            home.mkdir(parents=True)
            for name in ("nida81.tbk", "nc81base.sbk", "nc81recs.sbk", "nc81test.sbk", "nc81trnr.sbk"):
                (home / name).symlink_to(companion(path, name).resolve())
            lesson = top / "discs" / "LF" / "9e954d01.tbk"
            lesson.parent.mkdir(parents=True)
            lesson.symlink_to(path.resolve())
            entry = opening_page(lesson, home)
            self.assertEqual((entry.page_id, entry.book.name), ("P0", "nida81.tbk"))
            nav = Navigator(entry.data, entry.page_id, entry.book, home, lesson)
            self.assertEqual(nav.find_book("9e954d01.tbk", "P400"), lesson)
            self.assertEqual(nav.home, home)

    def test_a_click_on_logo_p0_returns_to_p10_of_the_lesson(self):
        path = _lesson()
        if path is None:
            self.skipTest("set OPENTOOLBOOK_TBK to 9e954d01.tbk")
        from opentoolbook.entry import opening_page

        with tempfile.TemporaryDirectory() as tmp:
            top = Path(tmp)
            home = top / "home"
            home.mkdir(parents=True)
            for name in ("nida81.tbk", "nc81base.sbk", "nc81recs.sbk", "nc81test.sbk", "nc81trnr.sbk"):
                (home / name).symlink_to(companion(path, name).resolve())
            lesson = top / "discs" / "LF" / "9e954d01.tbk"
            lesson.parent.mkdir(parents=True)
            lesson.symlink_to(path.resolve())
            entry = opening_page(lesson, home)
            self.assertEqual(entry.variables["lastbook"], "9e954d01.tbk")
            self.assertEqual(entry.variables["nextpage"], "p10")
            nav = Navigator(entry.data, entry.page_id, entry.book, home, lesson, entry.variables)
            self.assertTrue(nav.click(None).moved)
            self.assertEqual((nav.page_id, nav.book), ("P10", lesson))
            self.assertIn("P10", nav.pages)


if __name__ == "__main__":
    unittest.main()
