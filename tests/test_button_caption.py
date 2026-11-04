"""A button's caption is the C string its word at +0x22 names, drawn in the font +0x24 names."""

import struct
import unittest

from opentoolbook.bitmap import button_caption, stored_button_captions
from opentoolbook.field import _Segment, page_ids
from opentoolbook.show import Paint, _button, _draw_item, show_page

from lesson import companion, logic_families_path


def _synthetic(caption: bytes | None):
    """A 43-byte button, its caption block, and a font-table entry, in one segment at base 0.

    The caption block is the shape the lesson stores: an end word, class 0,
    then the characters and a 0 byte. The font entry is a face name with
    minus the character height at +0x20.
    """
    data = bytearray(0x200)
    at = 0x20
    block = 0x80
    font = 0x100
    data[at + 0x26] = 1
    struct.pack_into("<H", data, at + 0x24, font)
    if caption is not None:
        struct.pack_into("<HH", data, block - 4, block + len(caption) + 1, 0)
        data[block:block + len(caption)] = caption
        struct.pack_into("<H", data, at + 0x22, block)
    data[font:font + 5] = b"Arial"
    struct.pack_into("<h", data, font + 0x20, -195)
    return bytes(data), _Segment(1, 6, len(data) - 6, 0), at, font


class Canvas:
    def __init__(self):
        self.texts = []

    def create_text(self, *args, **kwargs):
        self.texts.append((args, kwargs))

    def __getattr__(self, name):
        if name.startswith("create_"):
            return lambda *a, **k: None
        raise AttributeError(name)


class SyntheticCaptionTests(unittest.TestCase):
    def test_the_word_at_0x22_names_the_caption(self):
        data, segment, at, font = _synthetic(b"OK")
        painted = _button(data, segment, at, 6, "", (0, 0, 300, 150), base=0, known={font})
        self.assertEqual(painted.caption, "OK")
        self.assertEqual(painted.caption_font, ("Arial", 195))

    def test_a_zero_word_is_no_caption(self):
        data, segment, at, font = _synthetic(None)
        painted = _button(data, segment, at, 6, "", (0, 0, 300, 150), base=0, known={font})
        self.assertIsNone(painted.caption)

    def test_a_font_word_not_in_the_list_is_no_font(self):
        data, segment, at, _font = _synthetic(b"OK")
        painted = _button(data, segment, at, 6, "", (0, 0, 300, 150), base=0, known=set())
        self.assertEqual(painted.caption, "OK")
        self.assertIsNone(painted.caption_font)

    def test_the_window_draws_the_caption_centered_in_the_font(self):
        button = Paint(
            "button", 6, "", (0, 0, 300, 150), stroke=(0, 0, 128),
            frame=(0, 0, 300, 150), caption="OK", caption_font=("Arial", 195),
        )
        canvas = Canvas()
        _draw_item(canvas, 1.0, button, [])
        self.assertEqual(len(canvas.texts), 1)
        args, kwargs = canvas.texts[0]
        self.assertEqual(args, (10.0, 5.0))
        self.assertEqual(kwargs["text"], "OK")
        self.assertEqual(kwargs["anchor"], "center")
        self.assertEqual(kwargs["font"], ("Arial", -13))
        self.assertEqual(kwargs["fill"], "#000080")

    def test_a_button_with_no_caption_draws_no_text(self):
        canvas = Canvas()
        _draw_item(canvas, 1.0, Paint("button", 6, "", (0, 0, 300, 150), frame=(0, 0, 300, 150)), [])
        self.assertEqual(canvas.texts, [])


@unittest.skipUnless(logic_families_path(), "set OPENTOOLBOOK_TBK to 9e954d01.tbk")
class LessonCaptionTests(unittest.TestCase):
    def setUp(self):
        self.data = logic_families_path().read_bytes()

    def test_the_ok_button_on_p30000_is_ok_in_arial_10(self):
        listed = show_page(self.data, "P30000", 800, 600)
        captioned = [item for item in listed.items if item.kind == "button" and item.caption]
        self.assertEqual([(item.bounds, item.caption, item.caption_font) for item in captioned],
                         [((4111, 3945, 5323, 4245), "OK", ("Arial", 195))])
        self.assertEqual(button_caption(self.data, "P30000", ""), "OK")

    def test_only_the_two_ok_buttons_have_a_caption(self):
        captions = stored_button_captions(self.data)
        self.assertEqual(len(captions), 398)
        self.assertEqual(sorted(caption for caption in captions if caption), ["OK", "OK"])

    def test_next_on_p300_has_no_caption(self):
        self.assertIsNone(button_caption(self.data, "P300", "Next"))

    def test_nida_retry_and_check_voltages(self):
        nida = companion(logic_families_path(), "nida81.tbk")
        if not nida.is_file():
            self.skipTest("nida81.tbk is not beside the lesson")
        data = nida.read_bytes()
        self.assertEqual(button_caption(data, "P12000", "Retry"), "Recheck")
        retry = next(item for item in show_page(data, "P12000", 800, 600).items
                     if item.kind == "button" and item.name == "Retry")
        self.assertEqual((retry.caption, retry.caption_font), ("Recheck", ("Arial", 240)))
        captions = stored_button_captions(data)
        self.assertEqual(len(captions), 156)
        self.assertEqual(sorted(caption for caption in captions if caption),
                         ["Check Voltages"] * 3 + ["Recheck"] * 4)
        self.assertIn("P12000", page_ids(data))


if __name__ == "__main__":
    unittest.main()
