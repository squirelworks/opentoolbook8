"""A book stores its user properties as a table of name and value blocks."""

import os
import unittest
from pathlib import Path

from opentoolbook.enter import blocks_write, concatenate, enter_fields
from opentoolbook.show import show_page
from opentoolbook.userprops import book_properties

FIXTURES = Path(__file__).parent / "fixtures"
LESSON = os.environ.get("OPENTOOLBOOK_TBK")


class StoredPropertyTests(unittest.TestCase):
    def test_the_instructor_fixtures_store_the_same_three_properties(self):
        for name in ("otb-line-rect.tbk", "otb-pie.tbk"):
            stored = book_properties((FIXTURES / name).read_bytes())
            self.assertEqual(stored[":hdmediapath"], "<BookPath>")
            self.assertEqual(stored["_asym_ea_version"], "8.0")
            self.assertEqual(stored["asym_deploymentmethod"], "Native")
            self.assertNotIn("__nidaversion", stored)

    def test_a_file_without_the_table_has_no_properties(self):
        self.assertEqual(book_properties(b""), {})
        self.assertEqual(book_properties(b"\x00" * 64 + b":HDMEDIAPATH\x00"), {})

    def test_of_this_book_reads_a_stored_property(self):
        expression = '"Version: " & __nidaVersion of this book'
        stored = {"__nidaversion": "2.003.0001"}
        self.assertEqual(concatenate(expression, book=stored), "Version: 2.003.0001")
        missing = concatenate(expression, book={})
        self.assertTrue(blocks_write(missing))


class LessonTests(unittest.TestCase):
    def test_pinfo_and_pqinfo_show_the_version_the_book_stores(self):
        if not LESSON or not os.path.isfile(LESSON):
            self.skipTest("set OPENTOOLBOOK_TBK to 9e954d01.tbk")
        data = Path(LESSON).read_bytes()
        stored = book_properties(data)
        self.assertEqual(stored["__nidaversion"], "2.003.0001")
        self.assertEqual(stored["__beentop1"], "true")
        self.assertEqual(stored["_asym_ea_version"], "8.0")
        self.assertNotIn("__nidaversion", book_properties(Path(LESSON).with_name("nida81.tbk").read_bytes()))
        for page in ("PINFO", "PQINFO"):
            written = enter_fields(data, page, (("version", "", ()),))
            self.assertEqual(written, (("version", "Version: 2.003.0001", ()),))
            listed = show_page(data, page, 400, 300)
            version = [item.text for item in listed.items if item.kind == "field" and item.name.lower() == "version"]
            self.assertEqual(version, ["Version: 2.003.0001"])


if __name__ == "__main__":
    unittest.main()
