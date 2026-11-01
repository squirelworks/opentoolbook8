"""Class 0x11 maps prototype pairs onto bounds and the window paints the stroke."""

import math
import struct
import unittest
from pathlib import Path

from opentoolbook.arc import (
    ARC_BYTES,
    Arc,
    _arc_record,
    arc_angles,
    arc_points,
    page_vertices,
    stored_arcs,
)
from opentoolbook.show import show_page

from lesson import companion, logic_families_path


def _lesson():
    return logic_families_path()


class SyntheticArcTests(unittest.TestCase):
    def test_the_record_is_bounds_three_pairs_and_radii(self):
        data = bytearray(ARC_BYTES)
        struct.pack_into("<H", data, 0, 80)
        struct.pack_into("<hhhh", data, 0x0F, 5010, 3675, 5550, 4230)
        struct.pack_into("<hhhhhh", data, 0x25, 1866, 5065, 1815, 4620, 1815, 4845)
        struct.pack_into("<hh", data, 0x31, 270, 225)
        self.assertEqual(
            _arc_record(bytes(data), 0),
            Arc(
                80,
                (5010, 3675, 5550, 4230),
                ((1866, 5065), (1815, 4620), (1815, 4845)),
                (270, 225),
            ),
        )
        self.assertEqual(page_vertices(_arc_record(bytes(data), 0)), ((5331, 4224), (5280, 3675)))


class ArcTests(unittest.TestCase):
    def test_p1140_object_80_points(self):
        path = _lesson()
        if path is None:
            self.skipTest("set OPENTOOLBOOK_TBK to 9e954d01.tbk")
        data = path.read_bytes()
        self.assertEqual(arc_points(data, "P1140", 80), ((1866, 5065), (1815, 4620)))

    def test_the_three_pairs_and_radii_repeat_on_arcs_with_other_bounds(self):
        path = _lesson()
        if path is None:
            self.skipTest("set OPENTOOLBOOK_TBK to 9e954d01.tbk")
        arcs = stored_arcs(path.read_bytes())
        self.assertEqual(len(arcs), 62)
        by_proto: dict = {}
        for arc in arcs:
            by_proto.setdefault((arc.points, arc.radii), set()).add(arc.bounds)
        self.assertEqual(
            {
                proto: len([arc for arc in arcs if (arc.points, arc.radii) == proto])
                for proto in by_proto
            },
            {
                (((5433, 3955), (5428, 3544), (5385, 3750)), (255, 210)): 43,
                (((1866, 5065), (1815, 4620), (1815, 4845)), (270, 225)): 19,
            },
        )
        for bounds in by_proto.values():
            self.assertGreater(len(bounds), 1)

        object_80 = next(
            arc for arc in arcs if arc.object_id == 80 and arc.bounds == (5010, 3675, 5550, 4230)
        )
        self.assertEqual(page_vertices(object_80), ((5331, 4224), (5280, 3675)))
        left, top, right, bottom = object_80.bounds
        for x, y in object_80.points:
            self.assertFalse(left <= x <= right and top <= y <= bottom)

        nida = stored_arcs(companion(path, "nida81.tbk").read_bytes())
        self.assertEqual(len(nida), 2)
        self.assertEqual(
            {(arc.points, arc.radii) for arc in nida},
            {(((3465, 4126), (3316, 4320), (3465, 4320)), (150, 195))},
        )

    def test_mapped_endpoints_lie_on_the_bounds_ellipse(self):
        path = _lesson()
        if path is None:
            self.skipTest("set OPENTOOLBOOK_TBK to 9e954d01.tbk")
        arcs = list(stored_arcs(path.read_bytes()))
        arcs.extend(stored_arcs(companion(path, "nida81.tbk").read_bytes()))
        for arc in arcs:
            left, top, right, bottom = arc.bounds
            center_x = (left + right) / 2
            center_y = (top + bottom) / 2
            radius_x = (right - left) / 2
            radius_y = (bottom - top) / 2
            for x, y in page_vertices(arc):
                value = ((x - center_x) / radius_x) ** 2 + ((y - center_y) / radius_y) ** 2
                self.assertAlmostEqual(value, 1.0, delta=0.02)

    def test_p1140_paints_the_three_arcs(self):
        path = _lesson()
        if path is None:
            self.skipTest("set OPENTOOLBOOK_TBK to 9e954d01.tbk")
        shown = show_page(path.read_bytes(), "P1140", 400, 300)
        arcs = [item for item in shown.items if item.kind == "arc"]
        self.assertEqual(
            {(item.object_id, item.bounds, item.points, item.stroke, item.fill) for item in arcs},
            {
                (
                    17,
                    (5010, 3015, 5550, 3570),
                    ((5331, 3564), (5280, 3015)),
                    (255, 255, 255),
                    None,
                ),
                (
                    65,
                    (2985, 3030, 3525, 3585),
                    ((3306, 3579), (3255, 3030)),
                    (255, 255, 255),
                    None,
                ),
                (
                    80,
                    (5010, 3675, 5550, 4230),
                    ((5331, 4224), (5280, 3675)),
                    (255, 255, 255),
                    None,
                ),
            },
        )
        for item in arcs:
            self.assertEqual(item.width, 1)
            start, extent = arc_angles(item.bounds, item.points[0], item.points[1])
            self.assertGreater(extent, 0)
            self.assertLess(extent, 360)


class ArcAngleTests(unittest.TestCase):
    def test_counter_clockwise_extent_from_first_endpoint_to_second(self):
        start, extent = arc_angles((5010, 3675, 5550, 4230), (5331, 4224), (5280, 3675))
        self.assertAlmostEqual(start, math.degrees(math.atan2(-0.978378, 0.188889)), places=3)
        self.assertAlmostEqual(extent, (90.0 - start) % 360.0, places=3)


if __name__ == "__main__":
    unittest.main()
