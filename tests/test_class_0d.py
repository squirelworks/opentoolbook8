"""Class 0xD stores bounds and two colors where class 0x8 does. The window paints the bounds."""

import struct
import unittest
from pathlib import Path

from opentoolbook.field import _Segment, _segments, page_ids
from opentoolbook.page import _objects
from opentoolbook.show import _paint, show_page

from lesson import companion, logic_families_path


def _records(data: bytes, kind: int):
    for segment in _segments(data):
        for at, found in _objects(data, segment):
            if found == kind:
                yield at


class SyntheticClassDTests(unittest.TestCase):
    def test_the_paint_is_the_bounds_in_the_class_0x8_colors(self):
        data = bytearray(6 + 45)
        at = 6
        struct.pack_into("<H", data, at, 279)
        struct.pack_into("<hhhh", data, at + 0x0F, 7282, 4176, 7495, 4259)
        data[at + 0x17:at + 0x1A] = bytes((96, 96, 96))
        data[at + 0x1B:at + 0x1E] = bytes((255, 0, 0))
        data[at + 0x25] = 254
        painted = _paint(bytes(data), _Segment(1, 6, 45, 0), None, 0, set(), at, 0xD)
        self.assertEqual(painted.kind, "class 0xD")
        self.assertEqual(painted.bounds, (7282, 4176, 7495, 4259))
        self.assertEqual(painted.fill, (255, 0, 0))
        self.assertEqual(painted.stroke, (96, 96, 96))
        self.assertEqual(painted.pattern, 254)
        data[at + 0x25] = 253
        self.assertIsNone(_paint(bytes(data), _Segment(1, 6, 45, 0), None, 0, set(), at, 0xD).fill)


class NidaClassDTests(unittest.TestCase):
    def test_the_fourteen_records_repeat_the_class_0x8_layout(self):
        if logic_families_path() is None:
            self.skipTest("set OPENTOOLBOOK_TBK to 9e954d01.tbk")
        path = logic_families_path()
        lesson = path.read_bytes()
        self.assertEqual(list(_records(lesson, 0xD)), [])
        data = companion(path, "nida81.tbk").read_bytes()
        found = list(_records(data, 0xD))
        self.assertEqual(len(found), 14)
        for at in found:
            left, top, right, bottom = struct.unpack_from("<hhhh", data, at + 0x0F)
            self.assertLess(left, right)
            self.assertLess(top, bottom)
            self.assertEqual(data[at + 0x1A], 0)
            self.assertEqual(data[at + 0x1E], 0)
            self.assertEqual(data[at + 0x25], 254)
            self.assertEqual(struct.unpack_from("<H", data, at + 0x28), struct.unpack_from("<H", data, at + 0x2A))

        shown = show_page(data, "P22100", 400, 300)
        painted = [item for item in shown.items if item.kind == "class 0xD"]
        self.assertEqual(len(painted), 14)
        first = next(item for item in painted if item.object_id == 279)
        self.assertEqual(first.bounds, (7282, 4176, 7495, 4259))
        self.assertEqual(first.stroke, (96, 96, 96))
        self.assertEqual(first.fill, (255, 0, 0))
        others = [
            item
            for page_id in page_ids(data)
            if page_id != "P22100"
            for item in show_page(data, page_id, 400, 300).items
            if item.kind == "class 0xD"
        ]
        self.assertEqual(others, [])


if __name__ == "__main__":
    unittest.main()
