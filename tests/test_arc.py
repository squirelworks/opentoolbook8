"""Class 0x11 stores three pairs that are not page positions. The window does not paint it."""

import os
import struct
import unittest
from pathlib import Path

from opentoolbook.arc import ARC_BYTES, Arc, _arc_record, arc_points, stored_arcs
from opentoolbook.show import show_page

LESSON = os.environ.get("OPENTOOLBOOK_TBK")


def _lesson():
    if not LESSON or not os.path.isfile(LESSON):
        return None
    return Path(LESSON)


class SyntheticArcTests(unittest.TestCase):
    def test_the_record_is_bounds_and_three_pairs(self):
        data = bytearray(ARC_BYTES)
        struct.pack_into("<H", data, 0, 80)
        struct.pack_into("<hhhh", data, 0x0F, 5010, 3675, 5550, 4230)
        struct.pack_into("<hhhhhh", data, 0x25, 1866, 5065, 1815, 4620, 1815, 4845)
        self.assertEqual(
            _arc_record(bytes(data), 0),
            Arc(80, (5010, 3675, 5550, 4230), ((1866, 5065), (1815, 4620), (1815, 4845))),
        )


class ArcTests(unittest.TestCase):
    def test_p1140_object_80_points(self):
        path = _lesson()
        if path is None:
            self.skipTest("set OPENTOOLBOOK_TBK to 9e954d01.tbk")
        data = path.read_bytes()
        self.assertEqual(arc_points(data, "P1140", 80), ((1866, 5065), (1815, 4620)))

    def test_the_three_pairs_repeat_on_arcs_with_other_bounds(self):
        path = _lesson()
        if path is None:
            self.skipTest("set OPENTOOLBOOK_TBK to 9e954d01.tbk")
        arcs = stored_arcs(path.read_bytes())
        self.assertEqual(len(arcs), 62)
        by_points: dict = {}
        for arc in arcs:
            by_points.setdefault(arc.points, set()).add(arc.bounds)
        self.assertEqual(
            {points: len([arc for arc in arcs if arc.points == points]) for points in by_points},
            {
                ((5433, 3955), (5428, 3544), (5385, 3750)): 43,
                ((1866, 5065), (1815, 4620), (1815, 4845)): 19,
            },
        )
        for bounds in by_points.values():
            self.assertGreater(len(bounds), 1)
        object_80 = next(
            arc for arc in arcs if arc.object_id == 80 and arc.bounds == (5010, 3675, 5550, 4230)
        )
        left, top, right, bottom = object_80.bounds
        for x, y in object_80.points:
            self.assertFalse(left <= x <= right and top <= y <= bottom)

        nida = stored_arcs(path.with_name("nida81.tbk").read_bytes())
        self.assertEqual(len(nida), 2)
        self.assertEqual({arc.points for arc in nida}, {((3465, 4126), (3316, 4320), (3465, 4320))})

    def test_p1140_does_not_paint_an_arc(self):
        path = _lesson()
        if path is None:
            self.skipTest("set OPENTOOLBOOK_TBK to 9e954d01.tbk")
        shown = show_page(path.read_bytes(), "P1140", 400, 300)
        self.assertFalse([item for item in shown.items if item.kind == "arc"])


if __name__ == "__main__":
    unittest.main()
