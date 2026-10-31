"""A disabled button draws its disabled picture when the block names one."""

import os
import struct
import unittest
from pathlib import Path

from opentoolbook.field import _Segment, page_ids
from opentoolbook.show import _button, show_page

LESSON = os.environ.get("OPENTOOLBOOK_TBK")


def _synthetic(flags: int, up: int, disabled: int):
    """A 43-byte button and a graphics block in one segment at base 0."""
    data = bytearray(0x100)
    at = 0x20
    block = 0x80
    data[at + 0x26] = flags
    struct.pack_into("<H", data, at + 0x28, block)
    struct.pack_into("<H", data, block, 0x0202)
    struct.pack_into("<H", data, block + 0x15, up)
    struct.pack_into("<H", data, block + 0x39, disabled)
    return bytes(data), _Segment(1, 6, len(data) - 6, 0), at


class SyntheticDisabledTests(unittest.TestCase):
    def test_enabled_bit_0_with_a_disabled_picture_draws_it(self):
        data, segment, at = _synthetic(0x00, 116, 128)
        painted = _button(data, segment, at, 6, "A", (0, 0, 1, 1))
        self.assertEqual((painted.picture_id, painted.picture_role), (128, "disabled"))

    def test_enabled_bit_0_without_one_keeps_the_up_picture(self):
        data, segment, at = _synthetic(0x00, 116, 0)
        painted = _button(data, segment, at, 6, "A", (0, 0, 1, 1))
        self.assertEqual((painted.picture_id, painted.picture_role), (116, "up"))

    def test_an_enabled_button_keeps_the_up_picture(self):
        data, segment, at = _synthetic(0x01, 116, 128)
        painted = _button(data, segment, at, 6, "A", (0, 0, 1, 1))
        self.assertEqual((painted.picture_id, painted.picture_role), (116, "up"))


class LessonDisabledTests(unittest.TestCase):
    def test_p10302_a_draws_bitmap_127(self):
        if not LESSON or not os.path.isfile(LESSON):
            self.skipTest("set OPENTOOLBOOK_TBK to 9e954d01.tbk")
        data = Path(LESSON).read_bytes()
        letter = next(
            item for item in show_page(data, "P10302", 400, 300).items
            if item.kind == "button" and item.name == "A"
        )
        self.assertEqual((letter.picture_id, letter.picture_role), (128, "disabled"))
        self.assertEqual(letter.picture_id - 1, 127)
        self.assertIsNotNone(letter.picture)
        enabled = next(
            item for item in show_page(data, "P10301", 400, 300).items
            if item.kind == "button" and item.name == "A"
        )
        self.assertEqual((enabled.picture_id, enabled.picture_role), (116, "up"))

    def test_nida_buttons_have_no_disabled_picture(self):
        if not LESSON or not os.path.isfile(LESSON):
            self.skipTest("set OPENTOOLBOOK_TBK to 9e954d01.tbk")
        data = Path(LESSON).with_name("nida81.tbk").read_bytes()
        for page_id in page_ids(data):
            for item in show_page(data, page_id, 400, 300).items:
                self.assertNotEqual(item.picture_role, "disabled")


if __name__ == "__main__":
    unittest.main()
