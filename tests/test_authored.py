"""A blank native book saved by ToolBook II Instructor 8.1.

The page id is empty. The page stores one rectangle and one angled line.
The angled line is a class 0x13 point list, and its bounds are the extrema
of those points. The rectangle uses the class 0x8 color and pattern bytes.
"""

import unittest
from pathlib import Path

from opentoolbook.bitmap import stored_button_bounds
from opentoolbook.ellipse import stored_ellipses
from opentoolbook.field import field_text, page_ids, stored_field_bounds
from opentoolbook.line import stored_lines
from opentoolbook.page import page_records
from opentoolbook.polygon import stored_polygons
from opentoolbook.polyline import Polyline, stored_polylines
from opentoolbook.record import Book
from opentoolbook.rectangle import Rectangle, stored_rectangles
from opentoolbook.shelf import lesson_names

FIXTURE = Path(__file__).parent / "fixtures" / "otb-line-rect.tbk"


class AuthoredLineRectTests(unittest.TestCase):
    def test_blank_native_page_stores_a_rectangle_and_an_angled_line(self):
        data = FIXTURE.read_bytes()
        book = Book(data)
        self.assertEqual(book.header, 0xC00)
        self.assertEqual(len(book.records), 11)
        self.assertEqual(sum(record.wants_follow_up for record in book.records), 3)
        self.assertEqual(page_ids(data), ("",))
        self.assertEqual(lesson_names(data), ("MINSTB32.dll",))

        page = page_records(data, "")
        self.assertEqual(page.background.pattern, 254)
        self.assertEqual((page.background.red, page.background.green, page.background.blue), (255, 255, 255))
        self.assertEqual(
            (page.background.second_red, page.background.second_green, page.background.second_blue),
            (0, 0, 0),
        )
        self.assertEqual(
            [(item.kind, item.object_id, item.name) for item in page.objects],
            [(0x8, 0, ""), (0x13, 1, "")],
        )
        self.assertEqual(
            stored_rectangles(data),
            (
                Rectangle(
                    bounds=(1350, 3675, 2700, 4275),
                    pattern=254,
                    first_color=(0, 0, 0),
                    second_color=(255, 255, 255),
                ),
            ),
        )
        self.assertEqual(
            stored_polylines(data),
            (
                Polyline(
                    points=((2040, 2955), (240, 5295)),
                    bounds=(240, 2955, 2040, 5295),
                ),
            ),
        )
        self.assertEqual(stored_lines(data), ())
        self.assertEqual(stored_ellipses(data), ())
        self.assertEqual(stored_polygons(data), ())


FIELD_BOOK = Path(__file__).parent / "fixtures" / "otb-fld.tbk"


class AuthoredFieldTests(unittest.TestCase):
    def test_blank_native_page_stores_a_field(self):
        data = FIELD_BOOK.read_bytes()
        self.assertEqual(page_ids(data), ("",))
        self.assertEqual(stored_field_bounds(data), ((500, 500, 2500, 1400),))
        self.assertEqual(field_text(data, "", "otb"), "otb field")
        page = page_records(data, "")
        self.assertEqual(
            [(item.kind, item.object_id, item.name) for item in page.objects],
            [(0xA, 0, "otb")],
        )


BUTTON_BOOK = Path(__file__).parent / "fixtures" / "otb-btn.tbk"


class AuthoredButtonTests(unittest.TestCase):
    def test_blank_native_page_stores_two_buttons(self):
        data = BUTTON_BOOK.read_bytes()
        self.assertEqual(
            stored_button_bounds(data),
            ((600, 600, 2200, 1100), (600, 1400, 2200, 1900)),
        )
        page = page_records(data, "")
        self.assertEqual(
            [(item.kind, item.object_id, item.name) for item in page.objects],
            [(0x9, 0, ""), (0x9, 1, "")],
        )


if __name__ == "__main__":
    unittest.main()
