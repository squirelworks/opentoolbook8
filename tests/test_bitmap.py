"""A button bitmap is an 8-byte prefix and then a BM file in the huge table."""

import os
import unittest
from pathlib import Path

from opentoolbook.bitmap import button_bitmap, huge_bitmaps


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


if __name__ == "__main__":
    unittest.main()
