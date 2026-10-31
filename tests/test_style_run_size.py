"""A style run's size is the height word of the font-table entry it names."""

import os
import struct
import unittest
from pathlib import Path

from opentoolbook.show import _size_at, _spans_at, font_height, show_page

LESSON = os.environ.get("OPENTOOLBOOK_TBK")


def _lesson():
    if not LESSON or not os.path.isfile(LESSON):
        return None
    return Path(LESSON)


def _entry(face: bytes, height: int) -> bytes:
    return face.ljust(0x20, b"\0") + struct.pack("<h", -height) + b"\0\0"


class FontHeightTests(unittest.TestCase):
    def test_the_word_at_0x20_is_minus_the_height(self):
        data = b"\xaa" * 4 + _entry(b"Arial", 240) + _entry(b"Arial", 285)
        self.assertEqual(font_height(data, 0, {4, 40}, 4), 240)
        self.assertEqual(font_height(data, 0, {4, 40}, 40), 285)

    def test_a_word_outside_the_list_has_no_height(self):
        data = _entry(b"Arial", 240)
        self.assertIsNone(font_height(data, 0, {0}, 1))
        self.assertIsNone(font_height(data, 0, {0, 64}, 64))

    def test_each_span_takes_the_height_of_the_run_it_starts_in(self):
        text = "Digital Logic\nFamilies"
        runs = ((0, "Arial"), (8, "MS Sans Serif"))
        sizes = ((0, 240), (8, 285))
        heights = tuple(_size_at(sizes, start, 1) for start, _text, _face in _spans_at(text, runs))
        self.assertEqual(heights, (16, 19))
        self.assertIsNone(_size_at((), 0, 1))


@unittest.skipUnless(_lesson(), "set OPENTOOLBOOK_TBK to Logic Families")
class LessonSizeTests(unittest.TestCase):
    def setUp(self):
        self.data = _lesson().read_bytes()

    def _field(self, page_id, name):
        listed = show_page(self.data, page_id, 800, 600)
        return next(item for item in listed.items if item.kind == "field" and item.name == name)

    def test_two_runs_with_different_size_words_get_different_sizes(self):
        field = self._field("P100", "Objective1Title")
        self.assertEqual(field.runs, ((0, "Arial"), (18, "MS Sans Serif")))
        self.assertEqual(field.sizes, ((0, 240), (18, 280)))
        heights = tuple(_size_at(field.sizes, start, 1) for start, _text, _face in _spans_at(field.text, field.runs))
        self.assertEqual(heights, (16, 19))

    def test_a_run_word_of_1_is_the_field_font(self):
        field = self._field("P900", "Exit")
        self.assertEqual(field.runs[1], (2, None))
        self.assertEqual(field.sizes, ((0, 160), (2, 240)))


if __name__ == "__main__":
    unittest.main()
