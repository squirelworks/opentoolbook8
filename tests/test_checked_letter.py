"""A letter click on a quiz page checks that letter and unchecks the rest."""

import os
import unittest
from pathlib import Path

from opentoolbook.navigate import Navigator
from opentoolbook.show import Paint, _checked, show_page

LESSON = os.environ.get("OPENTOOLBOOK_TBK")


def _lesson():
    if not LESSON or not os.path.isfile(LESSON):
        return None
    return Path(LESSON)


def _letters(listed):
    return {
        item.name: (item.picture_id, item.picture_role)
        for item in listed.items
        if item.kind == "button" and item.name in ("A", "B", "C", "D")
    }


class CheckedStateTests(unittest.TestCase):
    def test_the_click_state_wins_over_the_stored_bit(self):
        items = (
            Paint("button", 1, "A", picture_id=10, picture_role="up", up_id=10, checked_id=12),
            Paint("button", 2, "B", picture_id=22, picture_role="checked", up_id=20, checked_id=22),
            Paint("button", 3, "C", picture_id=30, picture_role="up", up_id=30, checked_id=None),
            Paint("field", 4, "A", text="A"),
        )
        out = _checked(b"", items, {"a": True, "b": False, "c": True})
        self.assertEqual((out[0].picture_id, out[0].picture_role), (12, "checked"))
        self.assertEqual((out[1].picture_id, out[1].picture_role), (20, "up"))
        # No checked picture: the up picture stays.
        self.assertEqual((out[2].picture_id, out[2].picture_role), (30, "up"))
        self.assertIs(out[3], items[3])

    def test_no_click_state_leaves_the_list_alone(self):
        items = (Paint("button", 1, "A", picture_id=10, picture_role="up", up_id=10, checked_id=12),)
        self.assertEqual(_checked(b"", items, {"OK": True}), items)


@unittest.skipUnless(_lesson(), "set OPENTOOLBOOK_TBK to Logic Families")
class LessonLetterClickTests(unittest.TestCase):
    def setUp(self):
        self.data = _lesson().read_bytes()

    def test_clicking_a_on_p10210_draws_picture_118_for_a(self):
        nav = Navigator(self.data, "P10210")
        before = _letters(show_page(self.data, "P10210", 800, 600))
        self.assertEqual(before["A"], (116, "up"))
        clicked = nav.click("A")
        self.assertFalse(clicked.moved)
        self.assertTrue(clicked.checked)
        self.assertEqual(nav.page_id, "P10210")
        after = _letters(show_page(self.data, nav.page_id, 800, 600, checked=nav.checked_buttons()))
        self.assertEqual(after["A"], (118, "checked"))
        self.assertEqual(after["B"], (119, "up"))
        self.assertEqual(after["C"], (122, "up"))
        self.assertEqual(after["D"], (125, "up"))

    def test_a_second_letter_unchecks_the_first(self):
        nav = Navigator(self.data, "P10210")
        nav.click("A")
        nav.click("b")
        after = _letters(show_page(self.data, nav.page_id, 800, 600, checked=nav.checked_buttons()))
        self.assertEqual(after["A"], (116, "up"))
        self.assertEqual(after["B"][1], "checked")

    def test_a_click_unchecks_a_letter_stored_checked(self):
        stored = _letters(show_page(self.data, "P10211", 800, 600))
        self.assertEqual(stored["B"][1], "checked")
        nav = Navigator(self.data, "P10211")
        nav.click("A")
        after = _letters(show_page(self.data, nav.page_id, 800, 600, checked=nav.checked_buttons()))
        self.assertEqual(after["A"][1], "checked")
        self.assertEqual(after["B"][1], "up")

    def test_the_state_stays_with_its_page(self):
        nav = Navigator(self.data, "P10210")
        nav.click("A")
        nav.click("Next")
        self.assertEqual(nav.page_id, "P10211")
        self.assertEqual(nav.checked_buttons(), {})
        nav.click("Back")
        self.assertEqual(nav.page_id, "P10210")
        self.assertTrue(nav.checked_buttons()["a"])


if __name__ == "__main__":
    unittest.main()
