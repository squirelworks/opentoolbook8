"""A book stores its user properties as a table of name and value blocks."""

import unittest
from pathlib import Path

from opentoolbook.navigate import Navigator
from opentoolbook.userprops import book_properties

from lesson import companion, logic_families_path

FIXTURES = Path(__file__).parent / "fixtures"

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


class LessonTests(unittest.TestCase):
    def test_pinfo_and_pqinfo_show_the_version_the_book_stores(self):
        if logic_families_path() is None:
            self.skipTest("set OPENTOOLBOOK_TBK to 9e954d01.tbk")
        path = logic_families_path()
        data = path.read_bytes()
        stored = book_properties(data)
        self.assertEqual(stored["__nidaversion"], "2.003.0001")
        self.assertEqual(stored["__beentop1"], "true")
        self.assertEqual(stored["_asym_ea_version"], "8.0")
        nida = companion(path, "nida81.tbk")
        if not nida.is_file():
            self.skipTest("nida81.tbk is not beside the lesson")
        self.assertNotIn("__nidaversion", book_properties(nida.read_bytes()))
        for page in ("PINFO", "PQINFO"):
            nav = Navigator(data, page, path)
            nav.enter()
            listed = nav.display(400, 300)
            version = [item.text for item in listed.items if item.kind == "field" and item.name.lower() == "version"]
            self.assertEqual(version, ["Version: 2.003.0001"])


if __name__ == "__main__":
    unittest.main()
