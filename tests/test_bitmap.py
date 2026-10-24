"""A button bitmap is an 8-byte prefix and then a BM file in the huge table."""

import os
import struct
import unittest
from pathlib import Path

from opentoolbook.bitmap import (
    button_bitmap,
    button_border,
    button_bounds,
    button_picture_ids,
    huge_bitmaps,
    stored_button_borders,
    stored_button_bounds,
)
from opentoolbook.record import Book


class BitmapTests(unittest.TestCase):
    def test_resource_155(self):
        path = os.environ.get("OPENTOOLBOOK_TBK")
        if not path or not os.path.isfile(path):
            self.skipTest("set OPENTOOLBOOK_TBK to 9e954d01.tbk")
        data = Path(path).read_bytes()
        bitmap = button_bitmap(data, 155)
        self.assertEqual(bitmap.stored_id, 156)
        self.assertEqual(bitmap.offset, 0x50117)
        self.assertEqual(bitmap.width, 580)
        self.assertEqual(bitmap.height, 158)
        self.assertEqual(bitmap.bpp, 8)

    def test_huge_table_lists_the_bitmaps_it_holds(self):
        path = os.environ.get("OPENTOOLBOOK_TBK")
        if not path or not os.path.isfile(path):
            self.skipTest("set OPENTOOLBOOK_TBK to 9e954d01.tbk")
        data = Path(path).read_bytes()
        found = huge_bitmaps(data)
        self.assertEqual(
            [(item.resource_id, item.offset, item.width, item.height, item.bpp) for item in found],
            [
                (148, 0x2577, 581, 157, 8),
                (150, 0x18FF7, 580, 387, 8),
                (155, 0x50117, 580, 158, 8),
                (164, 0x1BE627, 580, 158, 8),
            ],
        )
        kept = next(item for item in found if item.resource_id == 155)
        self.assertEqual(kept.offset, 0x50117)
        self.assertEqual((kept.width, kept.height, kept.bpp), (580, 158, 8))
        self.assertEqual(len(found), 4)

    def test_button_picture_id_is_a_stored_resource_id(self):
        path = os.environ.get("OPENTOOLBOOK_TBK")
        if not path or not os.path.isfile(path):
            self.skipTest("set OPENTOOLBOOK_TBK to 9e954d01.tbk")
        data = Path(path).read_bytes()
        pictures = button_picture_ids(data)
        resources = _type1_resource_ids(data)
        self.assertGreater(len(set(pictures)), 1)
        self.assertGreater(len(pictures), len(set(pictures)))
        self.assertTrue(all((picture - 1) in resources for picture in pictures))
        self.assertTrue(any(picture not in resources for picture in pictures))
        stored = {item.stored_id for item in huge_bitmaps(data)}
        self.assertTrue(stored <= set(pictures))


class ButtonBoundsTests(unittest.TestCase):
    def test_bounds_are_the_rectangle_at_0x0f(self):
        path = os.environ.get("OPENTOOLBOOK_TBK")
        if not path or not os.path.isfile(path):
            self.skipTest("set OPENTOOLBOOK_TBK to 9e954d01.tbk")
        data = Path(path).read_bytes()
        next_bounds = button_bounds(data, "P300", "Next")
        choice_bounds = button_bounds(data, "P10210", "A")
        self.assertEqual(next_bounds, (8907, 6210, 9342, 6630))
        self.assertEqual(choice_bounds, (2430, 1635, 2715, 1920))
        self.assertNotEqual(next_bounds, choice_bounds)
        self._ordered(data)
        nida = Path(path).with_name("nida81.tbk")
        self.assertTrue(nida.is_file())
        self._ordered(nida.read_bytes())

    def _ordered(self, data: bytes):
        found = stored_button_bounds(data)
        self.assertGreaterEqual(len(found), 2)
        self.assertGreaterEqual(len(set(found)), 2)
        for left, top, right, bottom in found:
            self.assertLessEqual(left, right)
            self.assertLessEqual(top, bottom)


class ButtonBorderTests(unittest.TestCase):
    def test_border_is_the_byte_at_0x27(self):
        path = os.environ.get("OPENTOOLBOOK_TBK")
        if not path or not os.path.isfile(path):
            self.skipTest("set OPENTOOLBOOK_TBK to 9e954d01.tbk")
        data = Path(path).read_bytes()
        self.assertEqual(button_border(data, "P300", "Next"), 1)
        self.assertEqual(button_border(data, "P10210", "A"), 9)
        self.assertNotEqual(button_border(data, "P300", "Next"), button_border(data, "P10210", "A"))
        lesson = stored_button_borders(data)
        self.assertGreaterEqual(lesson.count(1), 2)
        self.assertGreaterEqual(lesson.count(9), 2)
        self.assertGreaterEqual(lesson.count(7), 2)
        nida = Path(path).with_name("nida81.tbk")
        self.assertTrue(nida.is_file())
        other = stored_button_borders(nida.read_bytes())
        self.assertGreaterEqual(other.count(1), 2)
        self.assertGreaterEqual(other.count(7), 2)
        self.assertTrue(set(other) <= {1, 7})


def _type1_resource_ids(data: bytes) -> set[int]:
    """Fourth word of each type-1 directory entry. Independent of the picture read."""
    book = Book(data)
    records = {item.key: item for item in book.records}
    directory = struct.unpack_from("<I", data, book.header + 8 + 6 * 4)[0]
    segment = records[directory >> 16]
    body = segment.position - 6 + (directory & 0xFFFF)
    count = struct.unpack_from("<H", data, body + 2)[0]
    table_handle = (directory & 0xFFFF0000) | struct.unpack_from("<H", data, body + 0x0E)[0]
    table_segment = records[table_handle >> 16]
    table = table_segment.position - 6 + (table_handle & 0xFFFF)
    return {
        struct.unpack_from("<HHHH", data, table + index * 8)[3]
        for index in range(count)
    }


if __name__ == "__main__":
    unittest.main()
