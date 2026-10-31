"""Right and Left press the page's Next and Back buttons."""

import os
import unittest
from pathlib import Path

from opentoolbook.navigate import Navigator
from opentoolbook.show import Paint, key_button, press_key, show_page

FIXTURE = Path(__file__).parent / "fixtures" / "otb-line-rect.tbk"


def _lesson():
    path = os.environ.get("OPENTOOLBOOK_TBK")
    if not path or not os.path.isfile(path):
        return None
    return Path(path)


class KeyButtonTests(unittest.TestCase):
    def test_a_page_without_next_or_back_ignores_the_keys(self):
        data = FIXTURE.read_bytes()
        listed = show_page(data, "", 600, 400)
        nav = Navigator(data, "", FIXTURE)
        for key in ("Right", "Left", "Up", "space"):
            self.assertIsNone(key_button(listed, key))
            self.assertIsNone(press_key(nav, listed, key))
        self.assertEqual(nav.page_id, "")

    def test_the_key_names_the_button_as_the_page_spells_it(self):
        from dataclasses import replace

        listed = show_page(FIXTURE.read_bytes(), "", 600, 400)
        buttons = (Paint("button", 1, "NEXT"), Paint("field", 2, "Back"), Paint("button", 3, "back"))
        listed = replace(listed, items=listed.items + buttons)
        self.assertEqual(key_button(listed, "Right"), "NEXT")
        # A field named Back is not a button.
        self.assertEqual(key_button(listed, "Left"), "back")


class LessonKeyTests(unittest.TestCase):
    def test_right_and_left_on_p300(self):
        path = _lesson()
        if path is None:
            self.skipTest("set OPENTOOLBOOK_TBK to 9e954d01.tbk")
        data = path.read_bytes()
        right = Navigator(data, "P300", path)
        listed = right.display(624, 442)
        self.assertEqual(key_button(listed, "Right"), "Next")
        self.assertTrue(press_key(right, listed, "Right").moved)
        self.assertEqual(right.page_id, "P400")
        left = Navigator(data, "P300", path)
        self.assertEqual(key_button(listed, "Left"), "Back")
        self.assertTrue(press_key(left, left.display(624, 442), "Left").moved)
        self.assertEqual(left.page_id, "P100")
        # The key and the button are the same path.
        clicked = Navigator(data, "P300", path)
        clicked.click("Next")
        self.assertEqual(clicked.page_id, right.page_id)

    def test_right_on_a_quiz_page_uses_the_background_next(self):
        path = _lesson()
        if path is None:
            self.skipTest("set OPENTOOLBOOK_TBK to 9e954d01.tbk")
        nav = Navigator(path.read_bytes(), "P10210", path)
        listed = nav.display(624, 442)
        self.assertEqual(key_button(listed, "Right"), "Next")
        self.assertTrue(press_key(nav, listed, "Right").moved)
        self.assertEqual(nav.page_id, "P10211")


if __name__ == "__main__":
    unittest.main()
