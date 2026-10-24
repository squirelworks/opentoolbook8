"""A class 4 background stores a pattern byte and a red, green, and blue byte."""

import os
import unittest
from pathlib import Path

from opentoolbook.background import background


class BackgroundTests(unittest.TestCase):
    def test_p0_pattern_and_color(self):
        path = os.environ.get("OPENTOOLBOOK_TBK")
        if not path or not os.path.isfile(path):
            self.skipTest("set OPENTOOLBOOK_TBK to 9e954d01.tbk")
        data = Path(path).read_bytes()
        found = background(data, "P0")
        self.assertEqual(found.pattern, 0xFE)
        self.assertEqual((found.red, found.green, found.blue), (0, 0, 191))


if __name__ == "__main__":
    unittest.main()
