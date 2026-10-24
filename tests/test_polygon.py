"""A class 0x10 polygon is its mapped points, not its bounds rectangle."""

import os
import unittest
from pathlib import Path

from opentoolbook.polygon import polygon_points

# P430 object 136. Eleven points of a pin tip, placed on the bounds.
PIN = (
    (4497, 6262),
    (4599, 6262),
    (4599, 6349),
    (4579, 6373),
    (4568, 6412),
    (4558, 6436),
    (4538, 6436),
    (4528, 6412),
    (4532, 6373),
    (4497, 6349),
    (4497, 6325),
)


class PolygonTests(unittest.TestCase):
    def test_p430_object_136_has_eleven_points(self):
        path = os.environ.get("OPENTOOLBOOK_TBK")
        if not path or not os.path.isfile(path):
            self.skipTest("set OPENTOOLBOOK_TBK to 9e954d01.tbk")
        data = Path(path).read_bytes()
        points = polygon_points(data, "P430", 136)
        self.assertEqual(points, PIN)
        self.assertEqual(len(points), 11)
        rectangle = ((4497, 6262), (4599, 6262), (4599, 6436), (4497, 6436))
        self.assertNotEqual(points, rectangle)


if __name__ == "__main__":
    unittest.main()
