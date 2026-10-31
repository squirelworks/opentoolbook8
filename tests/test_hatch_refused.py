"""No class 0x8 pattern other than 254 and 253 occurs in both books, so no hatch is drawn."""

import unittest
from collections import Counter
from pathlib import Path

from opentoolbook.field import _segments
from opentoolbook.page import _objects
from opentoolbook.show import show_page

from lesson import companion, logic_families_path

RECTANGLE = 0x8


def _lesson():
    return logic_families_path()


def _patterns(data: bytes) -> Counter:
    found = Counter()
    for segment in _segments(data):
        for at, kind in _objects(data, segment):
            if kind == RECTANGLE:
                found[data[at + 0x25]] += 1
    return found


@unittest.skipUnless(_lesson(), "set OPENTOOLBOOK_TBK to Logic Families")
class HatchTests(unittest.TestCase):
    def setUp(self):
        self.data = _lesson().read_bytes()

    def test_lesson_class_8_pattern_counts(self):
        self.assertEqual(_patterns(self.data), Counter({254: 143, 33: 56, 253: 41, 4: 3}))

    def test_no_pattern_past_254_and_253_is_in_both_books(self):
        nida = companion(_lesson(), "nida81.tbk")
        if not nida.is_file():
            self.skipTest("nida81.tbk is not beside the lesson")
        theirs = _patterns(nida.read_bytes())
        self.assertEqual(theirs, Counter({254: 75, 253: 9, 81: 2}))
        shared = set(_patterns(self.data)) & set(theirs)
        self.assertEqual(shared, {254, 253})

    def test_pattern_33_is_drawn_as_its_fill_color(self):
        listed = show_page(self.data, "P440", 800, 600)
        bars = [item for item in listed.items if item.kind == "rectangle" and item.pattern == 33]
        self.assertTrue(bars)
        first = bars[0]
        self.assertEqual(first.bounds, (750, 4830, 825, 5130))
        self.assertEqual(first.fill, (192, 192, 192))
        self.assertEqual(first.stroke, (0, 0, 0))


if __name__ == "__main__":
    unittest.main()
