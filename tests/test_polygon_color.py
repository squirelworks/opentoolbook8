"""Class 0x10 stores two colors and a pattern byte beside its points."""

import struct
import unittest
from collections import defaultdict
from pathlib import Path

from opentoolbook.polygon import stored_polygon_colors

from lesson import companion, logic_families_path


class PolygonColorTests(unittest.TestCase):
    def test_colors_follow_the_pattern_byte(self):
        path = logic_families_path()
        if path is None:
            self.skipTest("set OPENTOOLBOOK_TBK to 9e954d01.tbk")
        self._colors(Path(path).read_bytes(), uniform=True)
        nida = companion(path, "nida81.tbk")
        self.assertTrue(nida.is_file())
        self._colors(nida.read_bytes(), uniform=False)

    def _colors(self, data: bytes, *, uniform: bool):
        found = stored_polygon_colors(data)
        self.assertGreaterEqual(len(found), 2)
        self.assertTrue(all(self._pattern(item.pattern) for item in found))
        self.assertTrue(any(red for red, _green, _blue in (item.second_color for item in found)))
        self.assertTrue(any(blue for _red, _green, blue in (item.first_color for item in found)))
        self.assertTrue(any(blue for _red, _green, blue in (item.second_color for item in found)))
        self.assertTrue(any(item.pattern not in struct.pack("<hhhh", *item.bounds) for item in found))
        groups = defaultdict(list)
        for item in found:
            groups[item.pattern].append(item)
        largest = max(groups.values(), key=len)
        self.assertGreater(len({item.first_color for item in largest}), 1)
        self.assertGreater(len({item.second_color for item in largest}), 1)
        if uniform:
            seconds = []
            for group in groups.values():
                if len(group) < 2:
                    continue
                first = {item.first_color for item in group}
                second = {item.second_color for item in group}
                if len(first) == 1 and len(second) == 1 and next(iter(first)) != next(iter(second)):
                    seconds.append(next(iter(second)))
            self.assertGreaterEqual(len(set(seconds)), 2)
        else:
            self.assertGreaterEqual(len({item.first_color for item in found}), 2)
            self.assertGreaterEqual(len({item.second_color for item in found}), 2)
            self.assertTrue(any(item.first_color != item.second_color for item in found))
            self.assertTrue(any(item.first_color == item.second_color for item in found))
        for item in found:
            left, top, right, bottom = item.bounds
            self.assertGreater(right, left)
            self.assertGreater(bottom, top)

    def _pattern(self, value: int) -> bool:
        return 1 <= value <= 0x80 or value in (0xFD, 0xFE, 0xFF)


if __name__ == "__main__":
    unittest.main()
