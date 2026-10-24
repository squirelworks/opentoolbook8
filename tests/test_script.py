"""buttonClick is source text. The handler is not called."""

import os
import unittest
from pathlib import Path

from opentoolbook.keywords import KEYWORDS
from opentoolbook.script import button_clicks

GO_P310 = 'go to page "P310" of book "nida81.tbk"'
GO_NEXT = "go to page nextpage of book lastbook"


class ButtonClickTests(unittest.TestCase):
    def test_button_click_is_source_text(self):
        path = os.environ.get("OPENTOOLBOOK_TBK")
        if not path or not os.path.isfile(path):
            self.skipTest("set OPENTOOLBOOK_TBK to 9e954d01.tbk")
        logic = Path(path).read_bytes()
        nida_path = Path(path).with_name("nida81.tbk")
        self.assertTrue(nida_path.is_file())
        nida = nida_path.read_bytes()

        self.assertEqual(len(KEYWORDS), 994)
        self.assertEqual(KEYWORDS[0], "to")
        self.assertEqual(KEYWORDS[1], "handle")
        self.assertEqual(KEYWORDS[0x0AF], "go")
        self.assertEqual(KEYWORDS[0x183], "page")
        self.assertEqual(KEYWORDS[8], "of")
        self.assertEqual(KEYWORDS[0x38], "book")
        self.assertIn(b'\x90\xaf\x80\x91\x83"P310"', logic)

        found = button_clicks(logic)
        self.assertGreater(len(found), 1)
        selection = [
            item for item in found
            if item.owner == "P300" and item.name.lower() == "selection1"
        ]
        self.assertTrue(selection)
        self.assertTrue(any(GO_P310 in item.source for item in selection))
        self.assertTrue(any("send next" in item.source for item in selection))
        self.assertNotIn("?", selection[0].source)

        other = button_clicks(nida)
        self.assertGreater(len(other), 1)
        jumps = [item for item in other if GO_NEXT in item.source]
        self.assertTrue(any(item.owner == "P340" and item.name == "Next" for item in jumps))
        self.assertTrue(any(item.owner == "P340" and item.name == "Back" for item in jumps))


if __name__ == "__main__":
    unittest.main()
