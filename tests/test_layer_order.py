"""A page's objects paint in the order of its stored layer list."""

import unittest
from pathlib import Path

from opentoolbook.field import _Trailer, _trailer, _u16
from opentoolbook.page import _handle_words, _objects, layer_nears
from opentoolbook.show import button_at, show_page, unit_to_px

from lesson import companion, logic_families_path


def _lesson():
    return logic_families_path()


def _page_segments(data):
    """(page id, segment, page near) for each page."""
    from opentoolbook.field import _book, _chars, _page_handles, _segments

    segments = _segments(data)
    by_key = {segment.key: segment for segment in segments}
    book_segment, book_record = _book(data, segments)
    for handle in _page_handles(data, by_key, book_segment, book_record):
        segment = by_key.get(handle >> 16)
        if segment is None:
            continue
        record = segment.base + (handle & 0xFFFF)
        if _u16(data, record - 2) != 5:
            continue
        yield _chars(data, record + 6, 32), segment, handle & 0xFFFF


class HandleWordsTests(unittest.TestCase):
    def test_the_handle_item_is_count_near_words(self):
        heap = b"\0" * 10 + bytes.fromhex("5a02da029c00e400f603f603")
        trailer = _Trailer({1: heap}, ((0, 0, 0, 0), (1, 10, 0, 0)))
        self.assertEqual(_handle_words(trailer, 1, 5), (0x25A, 0x2DA, 0x9C, 0xE4, 0x3F6))
        self.assertEqual(_handle_words(trailer, 2, 5), ())
        self.assertEqual(_handle_words(trailer, 1, 99), ())


@unittest.skipUnless(_lesson(), "set OPENTOOLBOOK_TBK to Logic Families")
class LessonLayerTests(unittest.TestCase):
    def setUp(self):
        self.data = _lesson().read_bytes()

    def _check_book(self, data, pages):
        for page_id, segment, near in _page_segments(data):
            trailer = _trailer(data, segment)
            top = {at - segment.base for at, _kind in _objects(data, segment) if _u16(data, at + 4) == near}
            layers = layer_nears(data, segment, trailer, near)
            self.assertEqual(sorted(layers), sorted(top), page_id)
            pages.append(page_id)

    def test_every_page_lists_its_objects_once(self):
        pages = []
        self._check_book(self.data, pages)
        self.assertEqual(len(pages), 131)
        nida = companion(_lesson(), "nida81.tbk")
        if nida.is_file():
            more = []
            self._check_book(nida.read_bytes(), more)
            self.assertEqual(len(more), 44)

    def test_p300_layer_list(self):
        found = {page_id: (segment, near) for page_id, segment, near in _page_segments(self.data)}
        segment, near = found["P300"]
        layers = layer_nears(self.data, segment, _trailer(self.data, segment), near)
        self.assertEqual(layers, (0x25A, 0x2DA, 0x9C, 0xE4, 0x3F6))

    def test_p300_menu_frame_is_behind_the_selection(self):
        shown = show_page(self.data, "P300", 800, 600)
        names = [(item.kind, item.object_id) for item in shown.items]
        self.assertLess(names.index(("button", 19)), names.index(("button", 16)))
        x = unit_to_px(3000, shown.scale)
        y = unit_to_px(1450, shown.scale)
        self.assertEqual(button_at(shown, x, y), "selection1")


if __name__ == "__main__":
    unittest.main()
