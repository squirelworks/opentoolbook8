"""The PE header in front of the ToolBook object store."""

import os
import unittest
from pathlib import Path

from opentoolbook.header import export_module_name

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
        path = os.environ.get("OPENTOOLBOOK_TBK")
        if not path or not os.path.isfile(path):
            self.skipTest("set OPENTOOLBOOK_TBK to 9e954d01.tbk")
        self.assertEqual(export_module_name(Path(path).read_bytes()), "MINSTB32.dll")
        nida = Path(path).with_name("nida81.tbk")
        if not nida.is_file():
            self.skipTest("nida81.tbk is not beside the lesson")
        self.assertEqual(export_module_name(nida.read_bytes()), "MINSTB32.dll")


if __name__ == "__main__":
    unittest.main()
