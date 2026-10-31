"""buttonClick opens a quoted page. It does not invent the next question."""

import os
import unittest
from pathlib import Path

from opentoolbook.click import quiz_background
from opentoolbook.field import page_ids
from opentoolbook.show import show_page

from engine_run import run
from lesson import companion
from opentoolbook.navigate import Navigator

LESSON = os.environ.get("OPENTOOLBOOK_TBK")
PAGES = ("P100", "P300", "P400", "P410")

SELECTION = """
TO HANDLE buttonClick
	system lastbook
	system nextpage
	lastbook=name of this book
	nextpage=name of this page

		go to page "P310" of book "nida81.tbk"
	break
	send next

END
"""


def _lesson():
    if not LESSON or not os.path.isfile(LESSON):
        return None
    return Path(LESSON)


class HandlerTests(unittest.TestCase):
    def test_a_quoted_page_opens_and_break_stops_send_next(self):
        followed = run(SELECTION, PAGES, "P300", book="9e954d01.tbk")
        self.assertEqual((followed.page_id, followed.book), ("P310", "nida81.tbk"))
        same = run('go to page "P400"\n', PAGES, "P300")
        self.assertEqual((same.page_id, same.book), ("P400", None))
        paren = run('go to page("P410")\n', PAGES, "P400")
        self.assertEqual(paren.page_id, "P410")
        back = run("send previous\n", PAGES, "P300")
        self.assertEqual(back.page_id, "P100")
        nxt = run("send next\n", PAGES, "P300")
        self.assertEqual(nxt.page_id, "P400")

    def test_a_handler_assigns_the_two_system_names_and_another_reads_them(self):
        variables: dict = {}
        run(SELECTION, PAGES, "P300", variables=variables, book="9e954d01.tbk")
        self.assertEqual(variables, {"lastbook": "9e954d01.tbk", "nextpage": "P300"})
        bare = "system nextpage, lastbook\ngo to page nextpage of book lastbook\n"
        back = run(bare, ("P310", "P340"), "P340", variables=variables, book="nida81.tbk")
        self.assertEqual((back.page_id, back.book), ("P300", "9e954d01.tbk"))
        local = run('nextpage = "p400"\ngo to page nextpage\n', PAGES, "P300")
        self.assertEqual((local.page_id, local.book), ("P400", None))


class LessonClickTests(unittest.TestCase):
    def test_p300_buttons_open_the_pages_the_handlers_name(self):
        path = _lesson()
        if path is None:
            self.skipTest("set OPENTOOLBOOK_TBK to 9e954d01.tbk")
        data = path.read_bytes()
        ids = page_ids(data)
        nav = Navigator(data, "P300", path)
        self.assertTrue(nav.click("Next").moved)
        self.assertEqual((nav.page_id, nav.book), ("P400", path))
        self.assertTrue(nav.click("Back").moved)
        self.assertEqual(nav.page_id, "P300")
        nav.click("Selection1")
        self.assertEqual((nav.page_id, nav.book.name), ("P310", "nida81.tbk"))
        other = companion(path, "nida81.tbk").read_bytes()
        self.assertIn("P310", page_ids(other))
        shown = show_page(other, "P310", 400, 300)
        self.assertEqual(shown.page_id, "P310")
        self.assertTrue(any(item.kind == "field" and "IBM PC Compatible Computer" in (item.text or "") for item in shown.items))
        self.assertNotIn("correct", [item.name.lower() for item in shown.items if item.kind == "rectangle"])
        self.assertTrue(quiz_background(data, "P10210"))
        self.assertFalse(quiz_background(data, "P300"))


if __name__ == "__main__":
    unittest.main()
