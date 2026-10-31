"""Class 0xC stores two colors and a pattern byte beside its rectangle."""

import os
import unittest
from collections import defaultdict
from pathlib import Path

from opentoolbook.background import background
from opentoolbook.ellipse import ellipses_on_page, stored_ellipses

from lesson import companion


class EllipseTests(unittest.TestCase):
    def test_colors_match_a_second_page(self):
        path = os.environ.get("OPENTOOLBOOK_TBK")
        if not path or not os.path.isfile(path):
            self.skipTest("set OPENTOOLBOOK_TBK to 9e954d01.tbk")
        logic = Path(path).read_bytes()
        nida_path = companion(path, "nida81.tbk")
        self.assertTrue(nida_path.is_file())
        nida = nida_path.read_bytes()
        first = self._background_pair(logic, "P410")
        second = self._background_pair(nida, "P310")
        self.assertNotEqual(first, second)
        self._colors(logic, two_patterns=True)
        self._colors(nida, two_patterns=False)

    def _background_pair(self, data: bytes, page_id: str) -> tuple[int, int, int]:
        page = background(data, page_id)
        found = ellipses_on_page(data, page_id)
        ink = (page.red, page.green, page.blue)
        matched = [
            item
            for item in found
            if item.pattern == page.pattern and item.first_color == ink
        ]
        self.assertGreaterEqual(len(matched), 2)
        self.assertGreaterEqual(len({item.bounds for item in matched}), 2)
        self.assertEqual(len({item.second_color for item in matched}), 1)
        second = matched[0].second_color
        self.assertNotEqual(second, ink)
        self.assertEqual(second[0], second[1])
        self.assertEqual(second[1], second[2])
        if page_id == "P310":
            self.assertGreater(len(found), len(matched))
        return second

    def _colors(self, data: bytes, *, two_patterns: bool):
        found = stored_ellipses(data)
        self.assertGreaterEqual(len(found), 2)
        if two_patterns:
            self.assertGreaterEqual(len({item.pattern for item in found}), 2)
        self.assertGreaterEqual(len({item.first_color for item in found}), 2)
        self.assertGreaterEqual(len({item.second_color for item in found}), 2)
        self.assertTrue(any(item.first_color != item.second_color for item in found))
        self.assertTrue(any(item.first_color == item.second_color for item in found))
        groups = defaultdict(list)
        for item in found:
            groups[item.pattern].append(item)
        largest = max(groups.values(), key=len)
        self.assertGreater(len({item.first_color for item in largest}), 1)
        self.assertGreater(len({item.second_color for item in largest}), 1)
        for item in found:
            left, top, right, bottom = item.bounds
            self.assertGreater(right, left)
            self.assertGreater(bottom, top)


if __name__ == "__main__":
    unittest.main()
