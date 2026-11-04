"""Class 0x12 pies share arc geometry slots. A pie with both radii is painted as a wedge;
the degenerate pies of otb-pie.tbk are not."""

import unittest
from pathlib import Path

from opentoolbook.field import _segments
from opentoolbook.page import page_records
from opentoolbook.pie import PIE, pie_bounds, pie_pairs, pie_record
from opentoolbook.arc import arc_angles
from opentoolbook.show import _draw_item, show_page
from lesson import logic_families_path

PIE_BOOK = Path(__file__).parent / "fixtures" / "otb-pie.tbk"
# Authored in ToolBook II Instructor 8 (Bochs, Win98) from the Command window:
#   draw pie ..., then set bounds of pie id 0 to 1500,1500,4500,5500
#   set vertices of pie id 0 to 4000,2000,2000,5000      (stored as 3996,2006,2004,4994)
#   set bounds of pie id 1 to 6000,1500,9000,4500
#   set vertices of pie id 1 to 8500,2000,6500,2500      (stored as 8560,1940,6159,2330)
#   set fillColor of pie id 0 to 0,50,100; set fillColor of pie id 1 to 0,50,100   (HLS red)
OFF_AXIS_BOOK = Path(__file__).parent / "fixtures" / "otb-pie2.tbk"


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


class PieGeometryTests(unittest.TestCase):
    """The eight words are the same five fields TB80BAS reads for an arc."""

    EXPECTED = {
        0: (
            (600, 600, 3000, 3000),
            ((1500, 3500), (1500, 1500)),
            (1500, 3500),
            (0, 2000),
        ),
        2: (
            (-1400, 500, 2400, 500),
            ((500, 500), (2400, 500)),
            (500, 500),
            (1900, 0),
        ),
    }

    def test_the_words_are_the_arc_geometry_slots(self):
        data = PIE_BOOK.read_bytes()
        page = page_records(data, "")
        segment = next(s for s in _segments(data) if s.key == 0x9000)
        for obj in page.objects:
            if obj.kind != PIE:
                continue
            pie = pie_record(data, segment.base + obj.near)
            bounds, points, center, radii = self.EXPECTED[obj.object_id]
            self.assertEqual(pie.object_id, obj.object_id)
            self.assertEqual(pie.bounds, bounds)
            self.assertEqual(pie.points, points)
            self.assertEqual(pie.center, center)
            self.assertEqual(pie.radii, radii)
            self.assertIn(0, pie.radii)


class LastObjectTests(unittest.TestCase):
    def test_the_last_field_of_p10410_is_on_the_walk(self):
        path = logic_families_path()
        if path is None:
            self.skipTest("set OPENTOOLBOOK_TBK to 9e954d01.tbk")
        shown = show_page(Path(path).read_bytes(), "P10410", 400, 300)
        review = next(item for item in shown.items if item.name == "Review 2")
        self.assertEqual((review.kind, review.object_id), ("field", 11))
        self.assertEqual(review.bounds, (2986, 3018, 6535, 3303))
        self.assertEqual(review.text, "2.  Other Integrated Circuits")


class PieWedgeTests(unittest.TestCase):
    """Both pies agree on the draw-pie coincidence, and neither names a wedge."""

    DRAWN = {
        0: ((1500, 1500), (3500, 3500), (1500, 3500)),
        2: ((2400, 500), (1500, 2200), (500, 500)),
    }

    def test_the_words_are_the_third_point_the_first_point_and_the_reach(self):
        page = page_records(PIE_BOOK.read_bytes(), "")
        for obj in page.objects:
            if obj.kind != PIE:
                continue
            first, second, third = self.DRAWN[obj.object_id]
            pairs = pie_pairs(obj.words)
            self.assertEqual(pairs.third, third)
            self.assertEqual(pairs.first, first)
            self.assertEqual(pairs.third_again, third)
            self.assertEqual(pairs.reach, (abs(first[0] - third[0]), abs(first[1] - third[1])))
            self.assertNotIn(second, (pairs.third, pairs.first, pairs.third_again, pairs.reach))
            self.assertIn(0, pairs.reach)

    def test_pie_id_0_words_did_not_follow_its_bounds(self):
        data = PIE_BOOK.read_bytes()
        segment = next(s for s in _segments(data) if s.key == 0x9000)
        page = page_records(data, "")
        for obj in page.objects:
            if obj.kind != PIE:
                continue
            pairs = pie_pairs(obj.words)
            box = (
                pairs.third[0] - pairs.reach[0],
                pairs.third[1] - pairs.reach[1],
                pairs.third[0] + pairs.reach[0],
                pairs.third[1] + pairs.reach[1],
            )
            stored = pie_bounds(data, segment.base + obj.near)
            if obj.object_id == 2:
                self.assertEqual(box, stored)
            else:
                self.assertNotEqual(box, stored)


class Canvas:
    def __init__(self):
        self.arcs = []

    def create_arc(self, *args, **kwargs):
        self.arcs.append((args, kwargs))

    def __getattr__(self, name):
        if name.startswith("create_"):
            return lambda *a, **k: None
        raise AttributeError(name)


class OffAxisPieTests(unittest.TestCase):
    """otb-pie2.tbk: two pies whose points are off the axes, as ToolBook 8 stored them.

    ToolBook's reader drew pie id 0 as the half of its ellipse over the top and left, and
    pie id 1 as the wedge over the top from its upper-right point to its upper-left point:
    counter-clockwise from the first vertex to the second, filled red with a black edge.
    """

    def _pies(self):
        shown = show_page(OFF_AXIS_BOOK.read_bytes(), "", 200, 100)
        return [item for item in shown.items if item.kind == "pie"]

    def test_the_points_are_the_vertices_and_the_center_is_the_bounds_center(self):
        data = OFF_AXIS_BOOK.read_bytes()
        segment = next(s for s in _segments(data) if s.key == 0x9000)
        got = []
        for obj in page_records(data, "").objects:
            if obj.kind == PIE:
                got.append(pie_record(data, segment.base + obj.near))
        self.assertEqual([(p.bounds, p.points, p.center, p.radii) for p in got], [
            ((1500, 1500, 4500, 5500), ((3996, 2006), (2004, 4994)), (3000, 3500), (1500, 2000)),
            ((6000, 1500, 9000, 4500), ((8560, 1940), (6159, 2330)), (7500, 3000), (1500, 1500)),
        ])

    def test_both_pies_are_painted_red_with_a_black_edge(self):
        pies = self._pies()
        self.assertEqual([(p.object_id, p.fill, p.stroke, p.width) for p in pies],
                         [(0, (255, 0, 0), (0, 0, 0), 1), (1, (255, 0, 0), (0, 0, 0), 1)])
        self.assertEqual(pies[0].points, ((3996, 2006), (2004, 4994)))
        self.assertEqual(pies[1].points, ((8560, 1940), (6159, 2330)))

    def test_the_wedge_runs_counter_clockwise_from_the_first_point(self):
        start, extent = arc_angles(*(lambda p: (p.bounds, *p.points))(self._pies()[1]))
        self.assertAlmostEqual(start, 45.0, places=3)
        self.assertAlmostEqual(extent, 108.452, places=3)
        start, extent = arc_angles(*(lambda p: (p.bounds, *p.points))(self._pies()[0]))
        self.assertAlmostEqual(start, 48.366, places=3)
        self.assertAlmostEqual(extent, 180.0, places=3)

    def test_the_window_draws_a_filled_pieslice(self):
        canvas = Canvas()
        _draw_item(canvas, 1.0, self._pies()[1], [])
        (box, options), = canvas.arcs
        self.assertEqual(options["style"], "pieslice")
        self.assertEqual(options["fill"], "#ff0000")
        self.assertEqual(options["outline"], "#000000")
        self.assertAlmostEqual(options["start"], 45.0, places=3)
        self.assertAlmostEqual(options["extent"], 108.452, places=3)


if __name__ == "__main__":
    unittest.main()
