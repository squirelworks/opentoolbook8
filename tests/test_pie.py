"""Class 0x12 pies are on the page walk with their stored words. They are not painted."""

import os
import unittest
from pathlib import Path

from opentoolbook.field import _segments
from opentoolbook.page import page_records
from opentoolbook.pie import PIE, pie_bounds
from opentoolbook.show import show_page

PIE_BOOK = Path(__file__).parent / "fixtures" / "otb-pie.tbk"


class PieWalkTests(unittest.TestCase):
    def test_both_pies_are_on_the_walk(self):
        page = page_records(PIE_BOOK.read_bytes(), "")
        self.assertEqual([(obj.kind, obj.object_id) for obj in page.objects], [(PIE, 0), (0x0C, 1), (PIE, 2)])
        pies = [obj for obj in page.objects if obj.kind == PIE]
        self.assertEqual(pies[0].words, (1500, 3500, 1500, 1500, 1500, 3500, 0, 2000))
        self.assertEqual(pies[1].words, (500, 500, 2400, 500, 500, 500, 1900, 0))
        self.assertEqual(page.objects[1].words, ())

    def test_the_bounds_are_the_rectangle_at_0x0f(self):
        data = PIE_BOOK.read_bytes()
        bounds = []
        page = page_records(data, "")
        segment = next(s for s in _segments(data) if s.key == 0x9000)
        for obj in page.objects:
            if obj.kind == PIE:
                bounds.append(pie_bounds(data, segment.base + obj.near))
        self.assertEqual(bounds, [(600, 600, 3000, 3000), (-1400, 500, 2400, 500)])

    def test_the_window_does_not_draw_a_wedge(self):
        shown = show_page(PIE_BOOK.read_bytes(), "", 200, 100)
        self.assertEqual([item.kind for item in shown.items], ["background", "ellipse"])


class LastObjectTests(unittest.TestCase):
    def test_the_last_field_of_p10410_is_on_the_walk(self):
        path = os.environ.get("OPENTOOLBOOK_TBK")
        if not path or not os.path.isfile(path):
            self.skipTest("set OPENTOOLBOOK_TBK to 9e954d01.tbk")
        shown = show_page(Path(path).read_bytes(), "P10410", 400, 300)
        review = next(item for item in shown.items if item.name == "Review 2")
        self.assertEqual((review.kind, review.object_id), ("field", 11))
        self.assertEqual(review.bounds, (2986, 3018, 6535, 3303))
        self.assertEqual(review.text, "2.  Other Integrated Circuits")


if __name__ == "__main__":
    unittest.main()
