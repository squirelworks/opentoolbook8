"""Class 0x11 object 80 on page P1140 stores a point pair. The arc is not filled."""

import os
import unittest
from pathlib import Path

from opentoolbook.arc import arc_points


class ArcTests(unittest.TestCase):
    def test_p1140_object_80_points(self):
        path = os.environ.get("OPENTOOLBOOK_TBK")
        if not path or not os.path.isfile(path):
            self.skipTest("set OPENTOOLBOOK_TBK to 9e954d01.tbk")
        data = Path(path).read_bytes()
        self.assertEqual(arc_points(data, "P1140", 80), ((1866, 5065), (1815, 4620)))


if __name__ == "__main__":
    unittest.main()
