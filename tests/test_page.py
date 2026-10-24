"""A page is the background it names and the objects whose parent word names it."""

import os
import unittest
from pathlib import Path

from opentoolbook.background import background
from opentoolbook.page import page_records

# P1140 stores this child-list three times. Object 80 is the arc in one of them.
_GATE = (0x11, 0x13, 0x0C, 0x0E, 0x0B)


class PageRecordTests(unittest.TestCase):
    def test_a_page_is_the_records_it_stores(self):
        path = os.environ.get("OPENTOOLBOOK_TBK")
        if not path or not os.path.isfile(path):
            self.skipTest("set OPENTOOLBOOK_TBK to 9e954d01.tbk")
        logic = Path(path).read_bytes()
        nida_path = Path(path).with_name("nida81.tbk")
        self.assertTrue(nida_path.is_file())
        nida = nida_path.read_bytes()
        self._logic(logic)
        self._nida(nida)

    def _logic(self, data: bytes):
        page = page_records(data, "P300")
        self.assertEqual(page.background, background(data, "P300"))
        group = next(obj for obj in page.objects if obj.kind == 0x0B and obj.name == "Selection1")
        self.assertEqual(tuple(child.kind for child in group.children), (0x09, 0x0A))

        page = page_records(data, "P1140")
        self.assertEqual(page.background, background(data, "P1140"))
        gates = [obj for obj in _groups(page.objects) if _kinds(obj) == _GATE]
        self.assertEqual(len(gates), 3)
        self.assertTrue(any(gate.children[0].object_id == 80 for gate in gates))
        for gate in gates:
            self.assertEqual(gate.children[-1].kind, 0x0B)
            self.assertGreaterEqual(len(gate.children[-1].children), 1)

        for page_id in ("P1910", "P1999", "P2910", "P2999"):
            page = page_records(data, page_id)
            earlier = [
                group
                for group in _groups(page.objects)
                if _before(group, 7, 8)
            ]
            self.assertEqual(len(earlier), 1)

        for page_id in ("P410", "P430"):
            page = page_records(data, page_id)
            found = [
                group
                for group in _groups(page.objects)
                if _kinds(group)[-2:] == (0x08, 0x11)
            ]
            self.assertGreaterEqual(len(found), 1)
            for group in found:
                self.assertEqual(group.children[0].kind, 0x10)

    def _nida(self, data: bytes):
        page = page_records(data, "P310")
        self.assertEqual(page.background, background(data, "P310"))
        pair = [
            group
            for group in _groups(page.objects)
            if tuple(child.near for child in group.children) == (0xB5C, 0xBDC)
        ]
        self.assertEqual(len(pair), 1)
        self.assertEqual(tuple(child.kind for child in pair[0].children), (0x09, 0x0A))

        page = page_records(data, "P22000")
        group = next(obj for obj in page.objects if obj.kind == 0x0B and obj.name == "Selection1")
        self.assertEqual(tuple(child.kind for child in group.children), (0x09, 0x0A))

        page = page_records(data, "P370")
        self.assertTrue(any(
            child.kind == 0x19 and child.object_id == 38
            for group in _groups(page.objects)
            for child in group.children
        ))

        page = page_records(data, "P22100")
        listed = [
            group
            for group in _groups(page.objects)
            if tuple(child.object_id for child in group.children if child.kind == 0x0C) == (301, 302, 304)
        ]
        self.assertEqual(len(listed), 1)


def _groups(objects):
    for obj in objects:
        if obj.kind == 0x0B:
            yield obj
            yield from _groups(obj.children)


def _kinds(group) -> tuple[int, ...]:
    return tuple(child.kind for child in group.children)


def _before(group, first: int, second: int) -> bool:
    ids = [child.object_id for child in group.children]
    return first in ids and second in ids and ids.index(first) < ids.index(second)


if __name__ == "__main__":
    unittest.main()
