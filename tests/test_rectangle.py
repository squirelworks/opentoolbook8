"""Class 0x8 stores two colors and a pattern byte beside its rectangle."""

import os
import unittest
from collections import defaultdict
from pathlib import Path

from opentoolbook.rectangle import stored_rectangles

from lesson import companion


class RectangleTests(unittest.TestCase):
    def test_colors_follow_the_pattern_byte(self):
        path = os.environ.get("OPENTOOLBOOK_TBK")
        if not path or not os.path.isfile(path):
            self.skipTest("set OPENTOOLBOOK_TBK to 9e954d01.tbk")
        self._colors(Path(path).read_bytes())
        nida = companion(path, "nida81.tbk")
        self.assertTrue(nida.is_file())
        self._colors(nida.read_bytes())

    def _colors(self, data: bytes):
        found = stored_rectangles(data)
        self.assertGreaterEqual(len(found), 2)
        self.assertGreaterEqual(len({item.pattern for item in found}), 2)
        self.assertGreaterEqual(len({item.first_color for item in found}), 2)
        self.assertGreaterEqual(len({item.second_color for item in found}), 2)
        self.assertTrue(any(blue != 0 for _red, _green, blue in (item.first_color for item in found)))
        self.assertTrue(any(blue != 0 for _red, _green, blue in (item.second_color for item in found)))
        groups = defaultdict(list)
        for item in found:
            groups[item.pattern].append(item)
        largest = max(groups.values(), key=len)
        self.assertGreater(len({item.first_color for item in largest}), 1)
        self.assertGreater(len({item.second_color for item in largest}), 1)
        uniform = [
            group
            for group in groups.values()
            if len(group) >= 2
            and len({item.first_color for item in group}) == 1
            and len({item.second_color for item in group}) == 1
            and group[0].first_color != group[0].second_color
        ]
        self.assertTrue(uniform)
        for item in found:
            left, top, right, bottom = item.bounds
            self.assertGreaterEqual(right, left)
            self.assertGreaterEqual(bottom, top)
        self.assertTrue(
            any(right > left and bottom > top for left, top, right, bottom in (item.bounds for item in found))
        )


if __name__ == "__main__":
    unittest.main()
