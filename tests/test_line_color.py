"""Class 0x0E stores two colors beside the endpoints. The byte at +0x25 is not one of them."""

import unittest
from pathlib import Path

from opentoolbook.line import stored_line_colors

from lesson import companion, logic_families_path


class LineColorTests(unittest.TestCase):
    def test_colors_are_not_the_endpoints(self):
        path = logic_families_path()
        if path is None:
            self.skipTest("set OPENTOOLBOOK_TBK to 9e954d01.tbk")
        self._logic(Path(path).read_bytes())
        nida = companion(path, "nida81.tbk")
        self.assertTrue(nida.is_file())
        self._nida(nida.read_bytes())

    def _logic(self, data: bytes):
        found = stored_line_colors(data)
        self.assertGreaterEqual(len(found), 2)
        self._known(found, ((2145, 4065), (1530, 4065)), (255, 252, 240), (128, 128, 128))
        self._known(found, ((4425, 4065), (3735, 4065)), (255, 252, 240), (128, 128, 128))
        self.assertGreaterEqual(len({item.first_color for item in found}), 2)
        self.assertGreaterEqual(len({item.second_color for item in found}), 2)
        by_ends: dict = {}
        for item in found:
            by_ends.setdefault(item.endpoints, set()).add((item.first_color, item.second_color))
        self.assertTrue(any(len(colors) > 1 for colors in by_ends.values()))
        self.assertTrue(any(len(ends) > 1 for ends in self._by_color(found).values()))

    def _nida(self, data: bytes):
        found = stored_line_colors(data)
        self.assertGreaterEqual(len(found), 2)
        self._known(found, ((840, 4545), (6960, 4545)), (64, 64, 64), (255, 255, 255))
        self._known(found, ((840, 4530), (6960, 4530)), (96, 96, 96), (255, 255, 255))
        self.assertGreaterEqual(len({item.first_color for item in found}), 2)
        self.assertGreaterEqual(len({item.second_color for item in found}), 2)
        self.assertTrue(any(len(ends) > 1 for ends in self._by_color(found).values()))

    def _known(self, found, endpoints, first, second):
        hits = [item for item in found if item.endpoints == endpoints]
        self.assertEqual(len(hits), 1)
        self.assertEqual(hits[0].first_color, first)
        self.assertEqual(hits[0].second_color, second)
        self.assertNotEqual(hits[0].first_color, hits[0].second_color)

    def _by_color(self, found):
        grouped: dict = {}
        for item in found:
            grouped.setdefault((item.first_color, item.second_color), set()).add(item.endpoints)
        return grouped


if __name__ == "__main__":
    unittest.main()
