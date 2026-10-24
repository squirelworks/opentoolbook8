"""A button bitmap is an 8-byte prefix and then a BM file in the huge table."""

import os
import unittest
from pathlib import Path

from opentoolbook.bitmap import button_bitmap


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


if __name__ == "__main__":
    unittest.main()
