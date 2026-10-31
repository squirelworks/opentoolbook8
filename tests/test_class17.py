"""A class 0x17 word at +0x04 names a class 0xA field called Text."""

import unittest
from pathlib import Path

from opentoolbook.class17 import class_17_fields

from lesson import companion, logic_families_path


class Class17Tests(unittest.TestCase):
    def test_the_pointer_names_a_text_field(self):
        path = logic_families_path()
        if path is None:
            self.skipTest("set OPENTOOLBOOK_TBK to 9e954d01.tbk")
        logic = Path(path).read_bytes()
        nida = companion(path, "nida81.tbk")
        self.assertTrue(nida.is_file())
        found = class_17_fields(logic)
        self.assertEqual(len(found), 5)
        self.assertTrue(all(item.name == "Text" for item in found))
        pairs = {(item.page_id, item.near) for item in found}
        self.assertIn(("P1080", 0x240), pairs)
        self.assertIn(("P1082", 0x9C), pairs)
        self.assertEqual(class_17_fields(nida.read_bytes()), ())


if __name__ == "__main__":
    unittest.main()
