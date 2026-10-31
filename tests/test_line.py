"""Class 0x0E stores two endpoints. The rectangle at +0x0F is not those points."""

import unittest
from pathlib import Path

from opentoolbook.line import stored_lines
from lesson import logic_families_path


class LineTests(unittest.TestCase):
    def test_every_line_has_two_endpoints(self):
        path = logic_families_path()
        if path is None:
            self.skipTest("set OPENTOOLBOOK_TBK to 9e954d01.tbk")
        data = path.read_bytes()
        found = stored_lines(data)
        self.assertGreaterEqual(len(found), 2)
        pairs = set()
        axis_in_a_wide_box = 0
        for item in found:
            self.assertEqual(len(item.endpoints), 2)
            (x1, y1), (x2, y2) = item.endpoints
            self.assertNotEqual((x1, y1), (x2, y2))
            pairs.add(item.endpoints)
            left, top, right, bottom = item.bounds
            self.assertLessEqual(left, right)
            self.assertLessEqual(top, bottom)
            for x, y in item.endpoints:
                self.assertGreaterEqual(x, left)
                self.assertLessEqual(x, right)
                self.assertGreaterEqual(y, top)
                self.assertLessEqual(y, bottom)
            if (x1 == x2 or y1 == y2) and right > left and bottom > top:
                axis_in_a_wide_box += 1
        self.assertGreaterEqual(len(pairs), 2)
        self.assertGreaterEqual(axis_in_a_wide_box, 1)


if __name__ == "__main__":
    unittest.main()
