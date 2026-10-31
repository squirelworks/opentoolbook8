"""Field text is word 1 of the block at record +0x24.

Word 0 of that block is a run list when it is a trailer handle.
"""

import os
import struct
import unittest
from pathlib import Path

from opentoolbook.field import (
    field_bounds,
    field_style_runs,
    field_text,
    field_text_places,
    field_words,
    page_ids,
    stored_field_bounds,
    style_run_names,
)

from lesson import companion

# The copyright field on page P0 of 9e954d01.tbk.
COPYRIGHT = 'Copyright ©  Nida Corporation 1997 - 2002  \r\nThis software and its supporting programs are protected by federal copyright law and all            rights are reserved by Nida Corporation.  No part or section of this software or its supporting    programs may be copied, distributed, transmitted in any form or medium electronic or           otherwise, disclosed to third parties, or used in any manner not specified in the  License            Agreement furnished by Nida Corporation.  This courseware was created with Asymetrix ToolBook I I .'

# The character record in the gap after P440, already quoted in FINDINGS.md.
P440_BODY = (
    "\r\n\r\nICs are classified into logic families based on voltage requirements, "
    "speed and the number of circuits they can drive."
)


class FieldTextTests(unittest.TestCase):
    def test_p0_copyright_field(self):
        path = os.environ.get("OPENTOOLBOOK_TBK")
        if not path or not os.path.isfile(path):
            self.skipTest("set OPENTOOLBOOK_TBK to 9e954d01.tbk")
        data = Path(path).read_bytes()
        self.assertEqual(field_text(data, "P0", "Copyright"), COPYRIGHT)

    def test_page_ids_include_p0_and_p430(self):
        path = os.environ.get("OPENTOOLBOOK_TBK")
        if not path or not os.path.isfile(path):
            self.skipTest("set OPENTOOLBOOK_TBK to 9e954d01.tbk")
        data = Path(path).read_bytes()
        found = page_ids(data)
        self.assertIn("P0", found)
        self.assertIn("P430", found)


class FieldStyleRunTests(unittest.TestCase):
    def test_runs_follow_the_field_text(self):
        path = os.environ.get("OPENTOOLBOOK_TBK")
        if not path or not os.path.isfile(path):
            self.skipTest("set OPENTOOLBOOK_TBK to 9e954d01.tbk")
        data = Path(path).read_bytes()
        found = field_style_runs(data)
        self.assertGreaterEqual(len(found), 2)
        for item in found:
            offsets = []
            for run in item.runs:
                self.assertEqual(len(run), 11)
                self.assertIn(run[6], (0, 4))
                self.assertEqual(run[10], 0)
                offsets.append(struct.unpack_from("<H", run, 0)[0])
            self.assertGreaterEqual(len(offsets), 1)
            self.assertEqual(len(offsets), len(set(offsets)))
            self.assertEqual(offsets, sorted(offsets))
            for offset in offsets:
                self.assertLessEqual(offset, len(item.text))


class StyleRunNameTests(unittest.TestCase):
    def test_run_word_names_a_c_string_or_is_one(self):
        path = os.environ.get("OPENTOOLBOOK_TBK")
        if not path or not os.path.isfile(path):
            self.skipTest("set OPENTOOLBOOK_TBK to 9e954d01.tbk")
        data = Path(path).read_bytes()
        runs = field_style_runs(data)
        named = style_run_names(data)
        self.assertEqual(len(named.names), len(runs))
        self.assertGreaterEqual(len(runs), 2)
        count = struct.unpack_from("<H", data, named.table)[0]
        pointers = struct.unpack_from("<" + "H" * count, data, named.table + 4)
        self.assertNotIn(1, pointers)
        seen = []
        sentinels = 0
        by_word = {}
        for item, names in zip(runs, named.names):
            self.assertEqual(len(item.runs), len(names))
            for run, name in zip(item.runs, names):
                word = struct.unpack_from("<H", run, 2)[0]
                if word == 1:
                    self.assertIsNone(name)
                    sentinels += 1
                    continue
                self.assertIn(word, pointers)
                raw = data[named.base + word:]
                end = raw.find(b"\x00")
                self.assertGreater(end, 0)
                self.assertEqual(name, raw[:end].decode("latin-1"))
                seen.append(name)
                by_word.setdefault(word, set()).add(name)
        self.assertGreaterEqual(sentinels, 2)
        self.assertGreaterEqual(len(set(seen)), 2)
        self.assertGreaterEqual(max(seen.count(name) for name in set(seen)), 2)
        for names in by_word.values():
            self.assertEqual(len(names), 1)


class FieldWordTests(unittest.TestCase):
    def test_the_five_numbers_repeat(self):
        path = os.environ.get("OPENTOOLBOOK_TBK")
        if not path or not os.path.isfile(path):
            self.skipTest("set OPENTOOLBOOK_TBK to 9e954d01.tbk")
        logic = Path(path).read_bytes()
        nida = companion(path, "nida81.tbk")
        self.assertTrue(nida.is_file())
        self._words(logic, 518, (360, 360, 310, 50, 5), 85, (0, 0, 0, 50, 1), 258)
        self._words(nida.read_bytes(), 246, (360, 360, 310, 50, 5), 19, (0, 0, 0, 50, 1), 100)

    def _words(self, data: bytes, total: int, body, body_count: int, common, common_count: int):
        found = field_words(data)
        self.assertEqual(len(found), total)
        self.assertGreaterEqual(len(set(found)), 2)
        self.assertEqual(found.count(body), body_count)
        self.assertEqual(found.count(common), common_count)
        for row in found:
            self.assertEqual(len(row), 5)


class FieldTextPlaceTests(unittest.TestCase):
    def test_the_gap_record_is_the_field(self):
        path = os.environ.get("OPENTOOLBOOK_TBK")
        if not path or not os.path.isfile(path):
            self.skipTest("set OPENTOOLBOOK_TBK to 9e954d01.tbk")
        logic = Path(path).read_bytes()
        nida = companion(path, "nida81.tbk")
        self.assertTrue(nida.is_file())
        self._same_bytes(logic, expect_p440=True)
        self._same_bytes(nida.read_bytes(), expect_p440=False)

    def _same_bytes(self, data: bytes, expect_p440: bool):
        places = field_text_places(data)
        self.assertEqual({place.page_id for place in places}, set(page_ids(data)))
        self.assertGreater(len(places), len(page_ids(data)))
        saw_p440 = False
        for place in places:
            self.assertLess(place.body, place.gap)
            self.assertGreaterEqual(place.at, place.gap)
            capacity, length = struct.unpack_from("<HH", data, place.at)
            raw = data[place.at + 4:place.at + 4 + length]
            self.assertEqual(raw.decode("latin-1"), place.text)
            self.assertGreater(length, 0)
            self.assertLessEqual(length, capacity)
            needle = struct.pack("<HH", capacity, length) + raw[:min(12, length)]
            self.assertNotIn(needle, data[place.body:place.gap])
            if place.page_id == "P440" and place.name == "Text":
                saw_p440 = True
                self.assertEqual(place.at, 0xCBAD7)
                self.assertEqual(place.text, P440_BODY)
        self.assertEqual(saw_p440, expect_p440)


class FieldBoundsTests(unittest.TestCase):
    def test_bounds_are_the_rectangle_at_0x0f(self):
        path = os.environ.get("OPENTOOLBOOK_TBK")
        if not path or not os.path.isfile(path):
            self.skipTest("set OPENTOOLBOOK_TBK to 9e954d01.tbk")
        data = Path(path).read_bytes()
        copyright_bounds = field_bounds(data, "P0", "Copyright")
        stem_bounds = field_bounds(data, "P10210", "Stem")
        self.assertEqual(copyright_bounds, (248, 4500, 9638, 6300))
        self.assertEqual(stem_bounds, (2430, 690, 7050, 1545))
        self.assertNotEqual(copyright_bounds, stem_bounds)
        self._ordered(data)
        nida = companion(path, "nida81.tbk")
        self.assertTrue(nida.is_file())
        self._ordered(nida.read_bytes())

    def _ordered(self, data: bytes):
        found = stored_field_bounds(data)
        self.assertGreaterEqual(len(found), 2)
        self.assertGreaterEqual(len(set(found)), 2)
        for left, top, right, bottom in found:
            self.assertLessEqual(left, right)
            self.assertLessEqual(top, bottom)


if __name__ == "__main__":
    unittest.main()
