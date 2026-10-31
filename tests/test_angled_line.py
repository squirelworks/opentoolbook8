"""A class 0x13 angled line is on the display list as its stored points."""

import os
import struct
import unittest
from pathlib import Path

from opentoolbook.field import _Segment, page_ids
from opentoolbook.polyline import POLYLINE_BYTES, stored_polylines
from opentoolbook.show import _paint, show_page

from lesson import companion

LESSON = os.environ.get("OPENTOOLBOOK_TBK")


def _record(points, stroke=(64, 64, 255), fill=(191, 0, 0)):
    """One 55-byte class 0x13 record, its points 3 bytes past it, in a segment at base 0."""
    at = 0x20
    data = bytearray(at + POLYLINE_BYTES + 3 + 4 * len(points) + 8)
    struct.pack_into("<H", data, at, 7)
    data[at + 0x17:at + 0x1A] = bytes(stroke)
    data[at + 0x1B:at + 0x1E] = bytes(fill)
    xs = [x for x, _y in points]
    ys = [y for _x, y in points]
    struct.pack_into("<hhhh", data, at + 0x25, min(xs), min(ys), max(xs), max(ys))
    struct.pack_into("<H", data, at + 0x2D, len(points))
    struct.pack_into("<H", data, at + 0x2F, at + POLYLINE_BYTES + 3)
    for index, point in enumerate(points):
        struct.pack_into("<hh", data, at + POLYLINE_BYTES + 3 + 4 * index, *point)
    return bytes(data), _Segment(1, 6, len(data) - 6, 0), at


FIXTURE = Path(__file__).parent / "fixtures" / "otb-line-rect.tbk"


class SyntheticAngledLineTests(unittest.TestCase):
    def test_the_instructor_line_is_the_one_stored_list(self):
        data = FIXTURE.read_bytes()
        stored = stored_polylines(data)
        self.assertEqual([line.points for line in stored], [((2040, 2955), (240, 5295))])
        lines = [item for item in show_page(data, "", 200, 100).items if item.kind == "angled line"]
        self.assertEqual([item.points for item in lines], [stored[0].points])
        self.assertEqual(lines[0].object_id, 1)
        self.assertEqual(lines[0].stroke, (0, 0, 0))
        self.assertIsNone(lines[0].fill)

    def test_the_paint_is_the_stored_points_in_the_first_color(self):
        points = ((6045, 3600), (6015, 3552), (6008, 3549), (5985, 3516))
        data, segment, at = _record(points)
        painted = _paint(data, segment, None, 0, set(), at, 0x13)
        self.assertEqual(painted.kind, "angled line")
        self.assertEqual(painted.object_id, 7)
        self.assertEqual(painted.points, points)
        self.assertEqual(painted.stroke, (64, 64, 255))
        self.assertIsNone(painted.fill)

    def test_a_list_past_the_segment_is_not_painted(self):
        data, segment, at = _record(((1, 2), (3, 4)))
        broken = bytearray(data)
        struct.pack_into("<H", broken, at + 0x2D, 900)
        self.assertIsNone(_paint(bytes(broken), segment, None, 0, set(), at, 0x13))


class LessonAngledLineTests(unittest.TestCase):
    def _every_page(self, data):
        found = set()
        for page_id in page_ids(data):
            for item in show_page(data, page_id, 400, 300).items:
                if item.kind == "angled line":
                    found.add(item.points)
        return found

    def test_every_class_0x13_record_is_painted(self):
        if not LESSON or not os.path.isfile(LESSON):
            self.skipTest("set OPENTOOLBOOK_TBK to 9e954d01.tbk")
        for name, count in ((Path(LESSON), 66), (companion(LESSON, "nida81.tbk"), 14)):
            data = name.read_bytes()
            stored = stored_polylines(data)
            self.assertEqual(len(stored), count)
            self.assertEqual(self._every_page(data), {line.points for line in stored})

    def test_p1140_strokes_them_in_the_first_color(self):
        if not LESSON or not os.path.isfile(LESSON):
            self.skipTest("set OPENTOOLBOOK_TBK to 9e954d01.tbk")
        data = Path(LESSON).read_bytes()
        lines = [item for item in show_page(data, "P1140", 400, 300).items if item.kind == "angled line"]
        self.assertTrue(lines)
        for item in lines:
            self.assertIsNone(item.fill)
            self.assertIsNotNone(item.stroke)
            self.assertGreaterEqual(len(item.points), 2)


if __name__ == "__main__":
    unittest.main()
