"""An 8-bit picture is palette indexes. The window draws the palette colors, not the index bytes."""

import hashlib
import os
import struct
import unittest
from pathlib import Path

from opentoolbook.pixels import _bm_file, _decode_bmp, picture_rgb
from opentoolbook.show import show_page

LESSON = os.environ.get("OPENTOOLBOOK_TBK")


def _bm8(width, height, palette, rows, used=None):
    colors = b"".join(bytes((blue, green, red, 0)) for red, green, blue in palette)
    stride = (width + 3) & ~3
    pixels = b"".join(bytes(row) + b"\0" * (stride - width) for row in reversed(rows))
    offset = 14 + 40 + len(colors)
    info = struct.pack(
        "<IiiHHIIiiII", 40, width, height, 1, 8, 0, len(pixels), 0, 0,
        len(palette) if used is None else used, 0,
    )
    return b"BM" + struct.pack("<IHHI", offset + len(pixels), 0, 0, offset) + info + colors + pixels


class SyntheticPaletteTests(unittest.TestCase):
    def test_indexes_are_looked_up_and_rows_turn_top_down(self):
        blob = _bm8(2, 2, [(192, 192, 192), (255, 0, 0), (0, 0, 255)], [[0, 1], [2, 0]])
        width, height, rgb = _decode_bmp(blob)
        self.assertEqual((width, height), (2, 2))
        self.assertEqual(rgb, bytes((192, 192, 192, 255, 0, 0, 0, 0, 255, 192, 192, 192)))
        self.assertNotEqual(rgb[:3], b"\0\0\0")

    def test_a_short_palette_is_refused(self):
        blob = _bm8(1, 1, [(1, 2, 3)], [[0]], used=4)
        with self.assertRaises(ValueError):
            _decode_bmp(blob)


class LessonPaletteTests(unittest.TestCase):
    EXPECTED = {
        148: (581, 157, "bbca0feec49117f4"),
        150: (580, 387, "66d6f86f2b5e3293"),
        155: (580, 158, "66d6f86f2b5e3293"),
        164: (580, 158, "7765430cc25cd1c1"),
    }

    def test_the_four_huge_table_bitmaps_use_their_color_tables(self):
        if not LESSON or not os.path.isfile(LESSON):
            self.skipTest("set OPENTOOLBOOK_TBK to 9e954d01.tbk")
        data = Path(LESSON).read_bytes()
        for resource_id, (width, height, first_row) in self.EXPECTED.items():
            blob = _bm_file(data, resource_id)
            self.assertEqual(struct.unpack_from("<H", blob, 28)[0], 8)
            pixel_at = struct.unpack_from("<I", blob, 10)[0]
            got_w, got_h, rgb = picture_rgb(data, resource_id + 1)
            self.assertEqual((got_w, got_h), (width, height))
            self.assertEqual(hashlib.sha256(rgb[:width * 3]).hexdigest()[:16], first_row)
            bottom = rgb[(height - 1) * width * 3:(height - 1) * width * 3 + 3]
            index = blob[pixel_at]
            palette_at = 14 + struct.unpack_from("<I", blob, 14)[0]
            self.assertEqual(bottom, blob[palette_at + 4 * index:palette_at + 4 * index + 3][::-1])
        _w, _h, rgb = picture_rgb(data, 156)
        self.assertEqual(rgb[:3], bytes((192, 192, 192)))

    def test_the_p450_textbox_draws_resource_155(self):
        if not LESSON or not os.path.isfile(LESSON):
            self.skipTest("set OPENTOOLBOOK_TBK to 9e954d01.tbk")
        shown = show_page(Path(LESSON).read_bytes(), "P450", 400, 300)
        box = next(item for item in shown.items if item.kind == "button" and item.picture_id == 156)
        self.assertEqual(box.picture[:2], (580, 158))
        self.assertEqual(hashlib.sha256(box.picture[2][:580 * 3]).hexdigest()[:16], "66d6f86f2b5e3293")


if __name__ == "__main__":
    unittest.main()
