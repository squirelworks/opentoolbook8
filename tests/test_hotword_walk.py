"""Class 0x17 hotwords are on the walk under the field they name, and are not painted."""

import unittest
from pathlib import Path

from opentoolbook.field import page_ids
from opentoolbook.page import HOTWORD, page_records
from opentoolbook.show import show_page

from lesson import companion, logic_families_path

FIXTURE = Path(__file__).parent / "fixtures" / "otb-line-rect.tbk"


def _walk(objects, owner=None):
    """Every object with the object that holds it."""
    for obj in objects:
        yield obj, owner
        yield from _walk(obj.children, obj)


class HotwordWalkTests(unittest.TestCase):
    def test_the_five_hotwords_are_under_their_text_fields(self):
        if logic_families_path() is None:
            self.skipTest("set OPENTOOLBOOK_TBK to 9e954d01.tbk")
        path = logic_families_path()
        data = path.read_bytes()
        found = []
        for page_id in page_ids(data):
            for obj, owner in _walk(page_records(data, page_id).objects):
                if obj.kind == HOTWORD:
                    found.append((page_id, obj.object_id, obj.name, owner.kind, owner.name, owner.near))
        self.assertEqual(
            found,
            [
                ("P1080", 4, "tolerance", 0x0A, "Text", 0x240),
                ("P1082", 6, "tolerance", 0x0A, "Text", 0x9C),
                ("P1200", 4, "propagation delay", 0x0A, "Text", 0x240),
                ("P1207", 6, "propagation delay", 0x0A, "Text", 0x9C),
                ("P2070", 6, "impedance", 0x0A, "Text", 0x9C),
            ],
        )
        nida_path = companion(path, "nida81.tbk")
        if not nida_path.is_file():
            self.skipTest("nida81.tbk is not beside the lesson")
        nida = nida_path.read_bytes()
        for page_id in page_ids(nida):
            self.assertFalse([obj for obj, _owner in _walk(page_records(nida, page_id).objects) if obj.kind == HOTWORD])

    def test_the_text_is_painted_once(self):
        if logic_families_path() is None:
            self.skipTest("set OPENTOOLBOOK_TBK to 9e954d01.tbk")
        path = logic_families_path()
        shown = show_page(path.read_bytes(), "P1080", 400, 300)
        texts = [item.text for item in shown.items if item.kind == "field" and item.text and "tolerance" in item.text]
        self.assertEqual(len(texts), 1)
        self.assertNotIn("hotword", [item.kind for item in shown.items])

    def test_a_page_with_no_hotword_is_unchanged(self):
        page = page_records(FIXTURE.read_bytes(), "")
        self.assertEqual([(obj.kind, obj.children) for obj in page.objects], [(0x08, ()), (0x13, ())])


if __name__ == "__main__":
    unittest.main()
