"""Class 0x15 is a paint object: bounds and a stored bitmap, packed or as is."""

import hashlib
import unittest
from pathlib import Path

from opentoolbook.field import _segments
from opentoolbook.page import _objects
from opentoolbook.paintobject import PAINT_OBJECT, paint_object_bmp
from opentoolbook.show import show_page

from lesson import companion, logic_families_path


def _lesson():
    return logic_families_path()


def _records(data):
    for segment in _segments(data):
        for at, kind in _objects(data, segment):
            if kind == PAINT_OBJECT:
                yield segment, at


class LessonPaintObjectTests(unittest.TestCase):
    def test_every_record_is_an_info_header_and_the_stored_pixel_count(self):
        path = _lesson()
        if path is None:
            self.skipTest("set OPENTOOLBOOK_TBK to 9e954d01.tbk")
        seen = []
        for name in (path, companion(path, "nida81.tbk")):
            data = name.read_bytes()
            for segment, at in _records(data):
                blob = paint_object_bmp(data, segment, at)
                width, height, bpp = (
                    int.from_bytes(blob[18:22], "little"),
                    int.from_bytes(blob[22:26], "little"),
                    int.from_bytes(blob[28:30], "little"),
                )
                seen.append((name.name.lower(), width, height, bpp, data[at + 0x26]))
        self.assertEqual(
            sorted(seen),
            sorted([
                ("9e954d01.tbk", 624, 442, 24, 254),
                ("9e954d01.tbk", 627, 24, 8, 254),
                ("9e954d01.tbk", 627, 24, 8, 254),
                ("9e954d01.tbk", 627, 28, 8, 254),
                ("9e954d01.tbk", 627, 28, 8, 254),
                ("nida81.tbk", 554, 390, 24, 254),
            ]),
        )

    def test_the_pages_draw_the_bitmaps(self):
        path = _lesson()
        if path is None:
            self.skipTest("set OPENTOOLBOOK_TBK to 9e954d01.tbk")
        data = path.read_bytes()
        expected = {
            ("P450", 2): ((0, 0, 9360, 6630), 624, 442, "0000bf0000bf", "eab3939aca6ee141"),
            ("P10210", 16): ((-22, 0, 9383, 360), 627, 24, "999999999999", "ee4b6325103353a6"),
            ("P10210", 20): ((-22, 6210, 9383, 6630), 627, 28, "ffffffffffff", "fd0a005f4315f440"),
        }
        nida = companion(path, "nida81.tbk").read_bytes()
        shown = {
            "P450": show_page(data, "P450", 400, 300),
            "P10210": show_page(data, "P10210", 400, 300),
        }
        for (page_id, object_id), (bounds, width, height, first, row) in expected.items():
            item = next(
                item for item in shown[page_id].items
                if item.kind == "paint object" and item.object_id == object_id
            )
            self.assertEqual(item.bounds, bounds)
            self.assertEqual(item.picture[:2], (width, height))
            self.assertEqual(item.picture[2][:6].hex(), first)
            self.assertEqual(hashlib.sha256(item.picture[2][:width * 3]).hexdigest()[:16], row)
        logo = [item for item in show_page(nida, "P0", 400, 300).items if item.kind == "paint object"]
        self.assertEqual([(item.object_id, item.bounds, item.picture[:2]) for item in logo], [(4, (525, 405, 8835, 6255), (554, 390))])


if __name__ == "__main__":
    unittest.main()
