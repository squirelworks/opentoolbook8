"""buttonClick opens a quoted page. It does not invent the next question."""

import os
import unittest
from pathlib import Path

from opentoolbook.click import follow_click, quiz_background, run_handler
from opentoolbook.field import page_ids
from opentoolbook.show import show_page

from lesson import companion

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
        followed = run_handler(SELECTION, PAGES, "P300")
        self.assertEqual(followed.page_id, "P310")
        self.assertEqual(followed.book, "nida81.tbk")
        self.assertNotEqual(followed.page_id, "P400")
        same = run_handler('go to page "P400"\n', PAGES, "P300")
        self.assertEqual((same.page_id, same.book), ("P400", None))
        paren = run_handler('go to page("P410")\n', PAGES, "P400")
        self.assertEqual(paren.page_id, "P410")
        back = run_handler("send previous\n", PAGES, "P300")
        self.assertEqual(back.page_id, "P100")
        nxt = run_handler("send next\n", PAGES, "P300")
        self.assertEqual(nxt.page_id, "P400")
        bare = run_handler("go to page nextpage of book lastbook\n", PAGES, "P300")
        self.assertEqual(bare.page_id, "P300")
        self.assertIsNone(bare.book)

    def test_two_names_in_parentheses_read_the_assigned_variables(self):
        line = "go to page (nextpage) of book(lastbook)\n"
        stayed = run_handler(line, PAGES, "P300")
        self.assertEqual((stayed.page_id, stayed.book), ("P300", None))
        half = run_handler(line, PAGES, "P300", {"nextpage": "p10"})
        self.assertEqual((half.page_id, half.book), ("P300", None))
        both = run_handler(line, PAGES, "P300", {"nextpage": "p10", "lastbook": "9e954d01.tbk"})
        self.assertEqual((both.page_id, both.book), ("p10", "9e954d01.tbk"))
        alone = run_handler("go to page (nextpage)\n", PAGES, "P300", {"nextpage": "P400"})
        self.assertEqual((alone.page_id, alone.book), ("P400", None))
        number = run_handler(line, PAGES, "P300", {"nextpage": 0, "lastbook": "x.tbk"})
        self.assertEqual(number.page_id, "P300")

    def test_a_handler_assigns_the_two_names_and_the_bare_form_follows_them(self):
        variables: dict = {}
        run_handler(SELECTION, PAGES, "P300", variables, "9e954d01.tbk")
        self.assertEqual(variables, {"lastbook": "9e954d01.tbk", "nextpage": "P300"})
        bare = "go to page nextpage of book lastbook\n"
        back = run_handler(bare, ("P310", "P340"), "P340", variables, "nida81.tbk")
        self.assertEqual((back.page_id, back.book), ("P300", "9e954d01.tbk"))
        quoted = run_handler('nextpage = "p1300"\ngo to page nextpage\n', PAGES, "P300", {}, "a.tbk")
        self.assertEqual((quoted.page_id, quoted.book), ("p1300", None))
        empty = run_handler(bare, PAGES, "P300", {}, "a.tbk")
        self.assertEqual((empty.page_id, empty.book), ("P300", None))
        other = run_handler('nextpage = getNext()\ngo to page nextpage\n', PAGES, "P300", {}, "a.tbk")
        self.assertEqual(other.page_id, "P300")

    def test_an_unquoted_call_does_not_change_the_page(self):
        stayed = run_handler("get notInTheBooks()\n", PAGES, "P300")
        self.assertEqual(stayed.page_id, "P300")
        self.assertIsNone(stayed.book)


class LessonClickTests(unittest.TestCase):
    def test_p300_buttons_open_the_pages_the_handlers_name(self):
        path = _lesson()
        if path is None:
            self.skipTest("set OPENTOOLBOOK_TBK to 9e954d01.tbk")
        data = path.read_bytes()
        ids = page_ids(data)
        nxt = follow_click(data, "P300", "Next", ids)
        self.assertEqual((nxt.page_id, nxt.book), ("P400", None))
        back = follow_click(data, "P300", "Back", ids)
        self.assertEqual(back.page_id, ids[ids.index("P300") - 1])
        self.assertEqual(back.page_id, "P100")
        chosen = follow_click(data, "P300", "Selection1", ids)
        self.assertEqual((chosen.page_id, chosen.book), ("P310", "nida81.tbk"))
        other = companion(path, "nida81.tbk").read_bytes()
        self.assertIn("P310", page_ids(other))
        shown = show_page(other, "P310", 400, 300)
        self.assertEqual(shown.page_id, "P310")
        self.assertTrue(any(item.kind == "field" and "IBM PC Compatible Computer" in (item.text or "") for item in shown.items))
        self.assertNotIn("correct", [item.name.lower() for item in shown.items if item.kind == "rectangle"])
        self.assertIsNone(follow_click(data, "P10210", "OK", ids))
        self.assertTrue(quiz_background(data, "P10210"))
        self.assertFalse(quiz_background(data, "P300"))


if __name__ == "__main__":
    unittest.main()
