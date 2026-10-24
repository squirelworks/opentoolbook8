"""A button bitmap is an 8-byte prefix and then a BM file in the huge table."""

import os
import struct
import unittest
from pathlib import Path

from opentoolbook.bitmap import button_bitmap, button_picture_ids, huge_bitmaps
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
