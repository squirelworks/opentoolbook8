"""Class 0x10 stores its points in the record. They sit in the source rectangle."""

import unittest
from pathlib import Path

from opentoolbook.polygon import stored_polygons
from lesson import logic_families_path


class PolygonTests(unittest.TestCase):
    def test_stored_points_lie_in_the_source_rectangle(self):
        path = logic_families_path()
        if path is None:
            self.skipTest("set OPENTOOLBOOK_TBK to 9e954d01.tbk")
        data = path.read_bytes()
        found = stored_polygons(data)
        self.assertGreaterEqual(len(found), 2)
        counts = {len(item.points) for item in found}
        self.assertGreaterEqual(len(counts), 2)
        for item in found:
            left, top, right, bottom = item.source
            self.assertGreater(right, left)
            self.assertGreater(bottom, top)
            for x, y in item.points:
                self.assertGreaterEqual(x, left)
                self.assertLessEqual(x, right)
                self.assertGreaterEqual(y, top)
                self.assertLessEqual(y, bottom)


if __name__ == "__main__":
    unittest.main()
