"""Field text is word 1 of the block at record +0x24.

Word 0 of that block is a run list when it is a trailer handle.
"""

import os
import struct
import unittest
from pathlib import Path

from opentoolbook.field import field_style_runs, field_text, page_ids, style_run_names

# The copyright field on page P0 of 9e954d01.tbk.
COPYRIGHT = 'Copyright ©  Nida Corporation 1997 - 2002  \r\nThis software and its supporting programs are protected by federal copyright law and all            rights are reserved by Nida Corporation.  No part or section of this software or its supporting    programs may be copied, distributed, transmitted in any form or medium electronic or           otherwise, disclosed to third parties, or used in any manner not specified in the  License            Agreement furnished by Nida Corporation.  This courseware was created with Asymetrix ToolBook I I .'


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


if __name__ == "__main__":
    unittest.main()
