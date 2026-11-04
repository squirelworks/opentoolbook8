"""Line style 2 (the export's dotted) is drawn dashed: Tk's dash (3, 3), Wine's cosmetic PS_DOT."""

import unittest
from collections import Counter

from opentoolbook.show import DOTTED_DASH, Paint, _draw_item, line_dash, show_page

from lesson import logic_families_path


def _record(style: int) -> bytes:
    record = bytearray(53)
    record[0x22] = style
    return bytes(record)


class Canvas:
    def __init__(self):
        self.lines = []

    def create_line(self, *args, **kwargs):
        self.lines.append(kwargs)

    def __getattr__(self, name):
        if name.startswith("create_"):
            return lambda *a, **k: None
        raise AttributeError(name)


def _drawn(item: Paint) -> dict:
    canvas = Canvas()
    _draw_item(canvas, 1.0, item, [])
    return canvas.lines[0]


class SyntheticDottedTests(unittest.TestCase):
    def test_style_2_is_the_dot_pattern(self):
        self.assertEqual(line_dash(_record(2), 0), (3, 3))
        self.assertEqual(DOTTED_DASH, (3, 3))

    def test_other_styles_are_solid(self):
        for style in (1, 4, 5, 6, 9, 0, 7):
            self.assertEqual(line_dash(_record(style), 0), ())

    def test_a_dotted_line_gets_the_dash_option(self):
        line = Paint("line", 1, "", (0, 0, 150, 0), stroke=(0, 0, 0), points=((0, 0), (150, 0)), dash=(3, 3))
        self.assertEqual(_drawn(line)["dash"], (3, 3))

    def test_a_solid_line_gets_no_dash_option(self):
        line = Paint("line", 1, "", (0, 0, 150, 0), stroke=(0, 0, 0), points=((0, 0), (150, 0)))
        self.assertNotIn("dash", _drawn(line))

    def test_an_angled_line_dashes_too(self):
        line = Paint("angled line", 1, "", (0, 0, 150, 150), stroke=(0, 0, 0),
                     points=((0, 0), (150, 0), (150, 150)), dash=(3, 3))
        self.assertEqual(_drawn(line)["dash"], (3, 3))


@unittest.skipUnless(logic_families_path(), "set OPENTOOLBOOK_TBK to 9e954d01.tbk")
class LessonDottedTests(unittest.TestCase):
    def setUp(self):
        self.data = logic_families_path().read_bytes()

    def test_the_ten_dotted_lines_are_on_p1205_and_p1970(self):
        from opentoolbook.field import page_ids
        found = Counter()
        for page_id in page_ids(self.data):
            for item in show_page(self.data, page_id, 800, 600).items:
                if item.kind == "line" and item.dash:
                    found[page_id] += 1
        self.assertEqual(found, Counter({"P1205": 5, "P1970": 5}))

    def test_p1205_line_10_is_dashed_and_one_pixel(self):
        line = next(item for item in show_page(self.data, "P1205", 800, 600).items
                    if item.kind == "line" and item.object_id == 10)
        self.assertEqual((line.points, line.width, line.dash), (((1740, 3795), (7755, 3795)), 1, (3, 3)))
        self.assertEqual(_drawn(line)["dash"], (3, 3))

    def test_a_style_4_line_on_p1110_is_solid(self):
        lines = [item for item in show_page(self.data, "P1110", 800, 600).items if item.kind == "line"]
        self.assertTrue(lines)
        for line in lines:
            self.assertEqual(line.dash, ())
            self.assertNotIn("dash", _drawn(line))


if __name__ == "__main__":
    unittest.main()
