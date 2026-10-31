"""Class 0x13 stores a point list. Its bounds are the extrema of those points."""

import os
import unittest
from pathlib import Path

from opentoolbook.polyline import stored_polylines

from lesson import companion


class PolylineTests(unittest.TestCase):
    def test_stored_points_are_their_bounds(self):
        path = os.environ.get("OPENTOOLBOOK_TBK")
        if not path or not os.path.isfile(path):
            self.skipTest("set OPENTOOLBOOK_TBK to 9e954d01.tbk")
        self._bounds_are_the_points(Path(path).read_bytes())
        nida = companion(path, "nida81.tbk")
        self.assertTrue(nida.is_file())
        self._bounds_are_the_points(nida.read_bytes())

    def _bounds_are_the_points(self, data: bytes):
        found = stored_polylines(data)
        self.assertGreaterEqual(len(found), 2)
        self.assertGreaterEqual(len({len(item.points) for item in found}), 2)
        for item in found:
            self.assertGreaterEqual(len(item.points), 2)
            xs = [x for x, _y in item.points]
            ys = [y for _x, y in item.points]
            self.assertEqual(item.bounds, (min(xs), min(ys), max(xs), max(ys)))


if __name__ == "__main__":
    unittest.main()
