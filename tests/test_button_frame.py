"""The button border byte draws a frame, a smaller frame, or none."""

import os
import unittest
from pathlib import Path

from opentoolbook.show import _frame, show_page

from lesson import companion

LESSON = os.environ.get("OPENTOOLBOOK_TBK")


def _lesson():
    if not LESSON or not os.path.isfile(LESSON):
        return None
    return Path(LESSON)


def _button(listed, name):
    found = [item for item in listed.items if item.kind == "button" and item.name == name]
    return found[0]


class FrameTests(unittest.TestCase):
    def test_push_button_frames_the_bounds(self):
        self.assertEqual(_frame(7, (100, 200, 400, 500)), (100, 200, 400, 500))

    def test_radio_button_3d_frames_a_smaller_box(self):
        self.assertEqual(_frame(9, (100, 200, 400, 500)), (115, 215, 385, 485))

    def test_a_tiny_radio_button_does_not_turn_inside_out(self):
        self.assertEqual(_frame(9, (0, 0, 10, 40)), (5, 5, 5, 35))

    def test_none_and_other_bytes_draw_no_frame(self):
        for border in (0, 1, 2, 8, 255):
            self.assertIsNone(_frame(border, (0, 0, 300, 300)))
        self.assertIsNone(_frame(7, None))


@unittest.skipUnless(_lesson(), "set OPENTOOLBOOK_TBK to Logic Families")
class LessonFrameTests(unittest.TestCase):
    def setUp(self):
        self.data = _lesson().read_bytes()

    def test_next_on_p300_has_no_frame(self):
        self.assertIsNone(_button(show_page(self.data, "P300", 800, 600), "Next").frame)

    def test_letter_a_on_p10210_has_the_smaller_frame(self):
        button = _button(show_page(self.data, "P10210", 800, 600), "A")
        self.assertEqual(button.bounds, (2430, 1635, 2715, 1920))
        self.assertEqual(button.frame, (2445, 1650, 2700, 1905))
        self.assertEqual(button.stroke, (0, 0, 0))

    def test_the_ok_button_on_p30000_frames_its_bounds(self):
        listed = show_page(self.data, "P30000", 800, 600)
        framed = [item for item in listed.items if item.kind == "button" and item.frame == item.bounds]
        self.assertEqual([item.bounds for item in framed], [(4111, 3945, 5323, 4245)])

    def test_a_nida_push_button_has_a_frame(self):
        nida = companion(LESSON, "nida81.tbk")
        if not nida.is_file():
            self.skipTest("nida81.tbk is not beside the lesson")
        retry = _button(show_page(nida.read_bytes(), "P12000", 800, 600), "Retry")
        self.assertEqual(retry.bounds, (603, 2295, 3339, 2721))
        self.assertEqual(retry.frame, retry.bounds)
        self.assertEqual(retry.stroke, (0, 0, 0))


if __name__ == "__main__":
    unittest.main()
