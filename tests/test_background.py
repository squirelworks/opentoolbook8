"""A class 4 background stores a pattern byte and a red, green, and blue byte."""

import unittest
from collections import Counter
from pathlib import Path

from opentoolbook.background import background
from opentoolbook.field import page_ids

from lesson import companion, logic_families_path


class BackgroundTests(unittest.TestCase):
    def test_p0_pattern_and_color(self):
        path = logic_families_path()
        if path is None:
            self.skipTest("set OPENTOOLBOOK_TBK to 9e954d01.tbk")
        data = path.read_bytes()
        found = background(data, "P0")
        self.assertEqual(found.pattern, 0xFE)
        self.assertEqual((found.red, found.green, found.blue), (0, 0, 191))

    def test_second_color(self):
        path = logic_families_path()
        if path is None:
            self.skipTest("set OPENTOOLBOOK_TBK to 9e954d01.tbk")
        logic = Path(path).read_bytes()
        nida = companion(path, "nida81.tbk")
        self.assertTrue(nida.is_file())
        self._second(logic, {(0, 0, 0), (255, 255, 0)})
        self._second(nida.read_bytes(), {(0, 0, 0)})

    def _second(self, data: bytes, expected: set[tuple[int, int, int]]):
        counts: Counter[tuple[int, int, int]] = Counter()
        for page_id in page_ids(data):
            item = background(data, page_id)
            counts[(item.second_red, item.second_green, item.second_blue)] += 1
        self.assertEqual(set(counts), expected)
        for count in counts.values():
            self.assertGreaterEqual(count, 2)


if __name__ == "__main__":
    unittest.main()
