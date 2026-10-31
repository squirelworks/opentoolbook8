"""The line-style byte at +0x22 is the stroke width of a line, shape, or polygon."""

import unittest
from collections import Counter
from pathlib import Path

from opentoolbook.field import _segments
from opentoolbook.page import _objects
from opentoolbook.show import _device_width, line_width, show_page

from lesson import companion, logic_families_path

LINE = 0x0E


def _lesson():
    return logic_families_path()


def _record(style: int) -> bytes:
    record = bytearray(53)
    record[0x22] = style
    return bytes(record)


def _line_styles(data: bytes) -> Counter:
    return Counter(
        data[at + 0x22]
        for segment in _segments(data)
        for at, kind in _objects(data, segment)
        if kind == LINE
    )


class LineWidthTests(unittest.TestCase):
    def test_the_style_byte_names_the_width(self):
        self.assertEqual(line_width(_record(4), 0), 1)
        self.assertEqual(line_width(_record(5), 0), 2)
        self.assertEqual(line_width(_record(6), 0), 3)
        self.assertEqual(line_width(_record(9), 0), 8)

    def test_none_is_no_stroke_and_dotted_is_one_pixel(self):
        self.assertEqual(line_width(_record(1), 0), 0)
        self.assertEqual(line_width(_record(2), 0), 1)

    def test_a_style_not_read_yet_stays_one_pixel(self):
        for style in (0, 3, 7, 8, 10, 255):
            self.assertEqual(line_width(_record(style), 0), 1)

    def test_the_width_scales_with_the_page(self):
        self.assertEqual(_device_width(2, 1.0), 2)
        self.assertEqual(_device_width(3, 2.0), 6)
        self.assertEqual(_device_width(1, 0.4), 1)
        self.assertEqual(_device_width(0, 1.0), 1)


@unittest.skipUnless(_lesson(), "set OPENTOOLBOOK_TBK to Logic Families")
class LessonWidthTests(unittest.TestCase):
    def setUp(self):
        self.data = _lesson().read_bytes()

    def test_every_lesson_line_stores_a_style(self):
        self.assertEqual(_line_styles(self.data), Counter({4: 516, 2: 10, 5: 2}))

    def test_p1110_draws_a_two_pixel_line(self):
        listed = show_page(self.data, "P1110", 800, 600)
        widths = Counter((item.kind, item.width) for item in listed.items if item.kind in ("line", "ellipse"))
        self.assertEqual(widths[("line", 2)], 1)
        self.assertEqual(widths[("ellipse", 2)], 1)

    def test_nida_lines(self):
        nida = companion(_lesson(), "nida81.tbk")
        if not nida.is_file():
            self.skipTest("nida81.tbk is not beside the lesson")
        data = nida.read_bytes()
        self.assertEqual(_line_styles(data), Counter({4: 11, 1: 6, 5: 4, 6: 3}))
        listed = show_page(data, "P12000", 800, 600)
        self.assertIn(3, [item.width for item in listed.items if item.kind == "line"])
        console = show_page(data, "P22100", 800, 600)
        unstroked = [item for item in console.items if item.kind == "class 0xD"]
        self.assertTrue(unstroked)
        self.assertTrue(all(item.width == 0 for item in unstroked))


if __name__ == "__main__":
    unittest.main()
