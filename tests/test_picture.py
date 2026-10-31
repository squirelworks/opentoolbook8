"""Class 0x19 is a packed metafile picture. The window draws it into its bounds."""

import os
import struct
import unittest
from pathlib import Path

from opentoolbook.field import _segments
from opentoolbook.page import _objects
from opentoolbook.picture import PICTURE, SRCAND, SRCCOPY, SRCPAINT, metafile_picture, picture_pixels
from opentoolbook.show import _png, _stretch, show_page

LESSON = os.environ.get("OPENTOOLBOOK_TBK")


def _record(function: int, params: bytes) -> bytes:
    return struct.pack("<IH", 3 + len(params) // 2, function) + params


def _stretch_dib(rop: int, width: int, height: int, palette, rows) -> bytes:
    info = struct.pack("<IiiHHIIiiII", 40, width, height, 1, 8, 0, 0, 0, 0, len(palette), 0)
    colors = b"".join(bytes((blue, green, red, 0)) for red, green, blue in palette)
    stride = (width + 3) & ~3
    pixels = b"".join(bytes(row) + b"\0" * (stride - width) for row in reversed(rows))
    params = struct.pack("<IHhhhhhhhh", rop, 0, height, width, 0, 0, height, width, 0, 0)
    body = params + info + colors + pixels
    if len(body) % 2:
        body += b"\0"
    return _record(0x0F43, body)


def _metafile(*dibs, width=2, height=1) -> bytes:
    records = [
        _record(0x001E, b""),
        _record(0x0102, struct.pack("<H", 1)),
        _record(0x020B, struct.pack("<hh", 0, 0)),
        _record(0x020C, struct.pack("<hh", height, width)),
        _record(0x0107, struct.pack("<H", 3)),
        _record(0x0416, struct.pack("<hhhh", height, width, 0, 0)),
        _record(0x0106, struct.pack("<H", 1)),
        _record(0x0104, struct.pack("<H", 15)),
        *dibs,
        _record(0x0104, struct.pack("<H", 13)),
        _record(0x0127, struct.pack("<h", -1)),
        _record(0x0000, b""),
    ]
    body = b"".join(records)
    return struct.pack("<HHHIHIH", 1, 9, 0x300, (18 + len(body)) // 2, 0, 0, 0) + body


class SyntheticPictureTests(unittest.TestCase):
    def test_srcpaint_then_srcand_is_clear_where_black_meets_white(self):
        first = _stretch_dib(SRCPAINT, 2, 1, [(0, 0, 0), (255, 255, 255)], [[0, 1]])
        second = _stretch_dib(SRCAND, 2, 1, [(255, 255, 255), (200, 10, 10)], [[0, 1]])
        drawn = metafile_picture(_metafile(first, second))
        self.assertEqual((drawn.width, drawn.height), (2, 1))
        self.assertEqual(drawn.mask, bytes((0, 1)))
        self.assertEqual(drawn.rgb[3:6], bytes((200, 10, 10)))

    def test_a_pixel_that_needs_the_page_under_it_is_refused(self):
        first = _stretch_dib(SRCPAINT, 2, 1, [(0, 0, 0), (200, 10, 10)], [[0, 1]])
        second = _stretch_dib(SRCAND, 2, 1, [(255, 255, 255), (255, 0, 0)], [[0, 1]])
        with self.assertRaises(ValueError):
            metafile_picture(_metafile(first, second))

    def test_one_srccopy_covers_its_rectangle(self):
        only = _stretch_dib(SRCCOPY, 2, 1, [(1, 2, 3), (4, 5, 6)], [[1, 0]])
        drawn = metafile_picture(_metafile(only))
        self.assertEqual(drawn.mask, bytes((1, 1)))
        self.assertEqual(drawn.rgb, bytes((4, 5, 6, 1, 2, 3)))

    def test_another_record_list_is_refused(self):
        only = _stretch_dib(SRCPAINT, 2, 1, [(1, 2, 3)], [[0, 0]])
        with self.assertRaises(ValueError):
            metafile_picture(_metafile(only))

    def test_the_stretch_fills_the_bounds_and_leaves_the_mask_clear(self):
        width, height, rgba = _stretch((2, 1, bytes((9, 9, 9, 7, 7, 7))), bytes((0, 1)), 4, 2)
        self.assertEqual((width, height), (4, 2))
        self.assertEqual(rgba[:16], bytes((0, 0, 0, 0)) * 2 + bytes((7, 7, 7, 255)) * 2)
        self.assertTrue(_png(width, height, rgba).startswith(b"\x89PNG"))


class NidaPictureTests(unittest.TestCase):
    def test_all_39_pictures_draw_and_the_pages_list_them(self):
        if not LESSON or not os.path.isfile(LESSON):
            self.skipTest("set OPENTOOLBOOK_TBK to 9e954d01.tbk")
        data = Path(LESSON).with_name("nida81.tbk").read_bytes()
        found = [
            at
            for segment in _segments(data)
            for at, kind in _objects(data, segment)
            if kind == PICTURE
        ]
        self.assertEqual(len(found), 39)
        masked = 0
        for at in found:
            self.assertEqual(data[at + 0x26], 254)
            drawn = picture_pixels(data, at)
            self.assertEqual(len(drawn.rgb), drawn.width * drawn.height * 3)
            if 0 in drawn.mask:
                masked += 1
        self.assertGreater(masked, 0)
        shown = show_page(data, "P310", 400, 300)
        computer = next(item for item in shown.items if item.kind == "picture" and item.object_id == 36)
        self.assertEqual(computer.bounds, (1080, 945, 6645, 6900))
        self.assertEqual(computer.picture[:2], (372, 397))
        nested = show_page(data, "P370", 400, 300)
        self.assertIn(38, [item.object_id for item in nested.items if item.kind == "picture"])


if __name__ == "__main__":
    unittest.main()
