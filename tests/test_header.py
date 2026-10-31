"""The PE header in front of the ToolBook object store."""

import unittest
from pathlib import Path

from opentoolbook.header import VersionFields, export_module_name, version_fields

from lesson import companion, logic_families_path

FIXTURE = Path(__file__).parent / "fixtures" / "otb-line-rect.tbk"


class ExportModuleTests(unittest.TestCase):
    def test_authored_book_names_the_export_module(self):
        data = FIXTURE.read_bytes()
        decoy = bytearray(data)
        decoy[0x40:0x4B] = b"NOTTHIS.dll"
        self.assertLess(bytes(decoy).find(b"NOTTHIS.dll"), bytes(decoy).find(b"MINSTB32.dll"))
        self.assertEqual(export_module_name(data), "MINSTB32.dll")
        self.assertEqual(export_module_name(bytes(decoy)), "MINSTB32.dll")

    def test_nida_book_names_the_export_module(self):
        path = logic_families_path()
        if path is None:
            self.skipTest("set OPENTOOLBOOK_TBK to 9e954d01.tbk")
        self.assertEqual(export_module_name(Path(path).read_bytes()), "MINSTB32.dll")
        nida = companion(path, "nida81.tbk")
        if not nida.is_file():
            self.skipTest("nida81.tbk is not beside the lesson")
        self.assertEqual(export_module_name(nida.read_bytes()), "MINSTB32.dll")


_SHARED = VersionFields(
    file_description="Toolbook II",
    internal_name="TB80",
    original_filename="TB80.EXE",
    product_version="8.10.131",
    company_name="Click2learn, Inc.",
)


class VersionFieldTests(unittest.TestCase):
    def test_authored_book_repeats_the_version_strings(self):
        data = bytearray(FIXTURE.read_bytes())
        self.assertEqual(version_fields(bytes(data)), _SHARED)
        key = "CompanyName".encode("utf-16le")
        at = data.find(key)
        value = data.find("Click2learn, Inc.".encode("utf-16le"), at)
        data[value:value + 34] = "Example Company!!".encode("utf-16le")
        self.assertIn("Click2learn, Inc.".encode("utf-16le"), bytes(data))
        changed = version_fields(bytes(data))
        self.assertEqual(changed.company_name, "Example Company!!")
        self.assertEqual(changed.file_description, _SHARED.file_description)
        self.assertEqual(changed.product_version, _SHARED.product_version)

    def test_nida_book_repeats_the_version_strings(self):
        path = logic_families_path()
        if path is None:
            self.skipTest("set OPENTOOLBOOK_TBK to 9e954d01.tbk")
        self.assertEqual(version_fields(Path(path).read_bytes()), _SHARED)
        nida = companion(path, "nida81.tbk")
        if not nida.is_file():
            self.skipTest("nida81.tbk is not beside the lesson")
        self.assertEqual(version_fields(nida.read_bytes()), _SHARED)
        for name in ("nc81base.sbk", "nc81recs.sbk", "nc81test.sbk", "nc81trnr.sbk"):
            book = companion(path, name)
            if book.is_file():
                self.assertEqual(version_fields(book.read_bytes()), _SHARED)


if __name__ == "__main__":
    unittest.main()
