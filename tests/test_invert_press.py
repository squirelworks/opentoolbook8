"""While a button is held down it draws its invert picture. Letting go is the up picture."""

import os
import unittest
from pathlib import Path

from opentoolbook.bitmap import button_invert_picture, button_picture
from opentoolbook.show import DisplayList, Paint, pressed, show_page

LESSON = os.environ.get("OPENTOOLBOOK_TBK")
FIXTURE = Path(__file__).parent / "fixtures" / "otb-line-rect.tbk"


class SyntheticPressTests(unittest.TestCase):
    def test_a_button_without_an_invert_picture_is_unchanged(self):
        listed = DisplayList("", 9000, 6000, 600, 400, 1, (Paint("button", 1, "Go", (0, 0, 10, 10), picture_id=5),))
        self.assertEqual(pressed(FIXTURE.read_bytes(), listed, "Go"), listed)

    def test_another_name_is_unchanged(self):
        listed = DisplayList("", 9000, 6000, 600, 400, 1, (Paint("button", 1, "Go", picture_id=5, invert_id=6),))
        self.assertEqual(pressed(FIXTURE.read_bytes(), listed, "Stop"), listed)


class LessonPressTests(unittest.TestCase):
    def test_p10210_a_holds_bitmap_116_and_lets_go_to_115(self):
        if not LESSON or not os.path.isfile(LESSON):
            self.skipTest("set OPENTOOLBOOK_TBK to 9e954d01.tbk")
        data = Path(LESSON).read_bytes()
        listed = show_page(data, "P10210", 400, 300)
        held = pressed(data, listed, "A")
        before = next(item for item in listed.items if item.name == "A")
        during = next(item for item in held.items if item.name == "A")
        self.assertEqual(button_invert_picture(data, "P10210", "A"), 117)
        self.assertEqual((during.picture_id, during.picture_role), (117, "invert"))
        self.assertEqual(during.picture_id - 1, 116)
        self.assertIsNotNone(during.picture)
        self.assertEqual((before.picture_id, before.picture_role), (button_picture(data, "P10210", "A"), "up"))
        self.assertEqual(before.picture_id, 116)
        others = [(a, b) for a, b in zip(listed.items, held.items) if a.name != "A"]
        self.assertTrue(all(a == b for a, b in others))

    def test_menu_frame_has_no_invert_picture(self):
        if not LESSON or not os.path.isfile(LESSON):
            self.skipTest("set OPENTOOLBOOK_TBK to 9e954d01.tbk")
        data = Path(LESSON).read_bytes()
        listed = show_page(data, "P300", 400, 300)
        self.assertEqual(pressed(data, listed, "MenuFrame"), listed)


if __name__ == "__main__":
    unittest.main()
