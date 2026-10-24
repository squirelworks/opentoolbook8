"""buttonClick is source text. The handler is not called."""

import os
import unittest
from pathlib import Path

from opentoolbook.keywords import KEYWORDS
from opentoolbook.script import button_clicks, quoted_go_to

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


class QuotedGoToTests(unittest.TestCase):
    def test_quotes_only(self):
        path = os.environ.get("OPENTOOLBOOK_TBK")
        if not path or not os.path.isfile(path):
            self.skipTest("set OPENTOOLBOOK_TBK to 9e954d01.tbk")
        logic = Path(path).read_bytes()
        nida = Path(path).with_name("nida81.tbk").read_bytes()
        self.assertIsNone(quoted_go_to("send next"))
        self.assertIsNone(quoted_go_to("go to page nextpage of book lastbook"))
        self.assertIsNone(quoted_go_to("go to page (nextpage) of book(lastbook)"))
        saw_p310 = False
        saw_p400 = False
        saw_paren = False
        for item in button_clicks(logic):
            for line in item.source.split("\r\n"):
                if line.strip().lower() == "send next":
                    self.assertIsNone(quoted_go_to(line))
                if 'go to page "P310" of book "nida81.tbk"' in line:
                    self.assertEqual(quoted_go_to(line), ("P310", "nida81.tbk"))
                    self.assertEqual(item.owner, "P300")
                    saw_p310 = True
                if line.strip() == 'go to page "P400"':
                    self.assertEqual(quoted_go_to(line), ("P400", None))
                    saw_p400 = True
                if 'go to page("P1210")' in line:
                    self.assertEqual(quoted_go_to(line), ("P1210", None))
                    saw_paren = True
        self.assertTrue(saw_p310 and saw_p400 and saw_paren)
        saw_book = False
        saw_plain = False
        saw_71 = False
        for item in button_clicks(nida):
            for line in item.source.split("\r\n"):
                if "go to page nextpage of book lastbook" in line and '"' not in line:
                    self.assertIsNone(quoted_go_to(line))
                    saw_plain = True
                if "go to page (nextpage) of book(lastbook)" in line:
                    self.assertIsNone(quoted_go_to(line))
                    saw_plain = True
                if 'go to page "P20001" of book "nida81.tbk"' in line:
                    self.assertEqual(quoted_go_to(line), ("P20001", "nida81.tbk"))
                    saw_book = True
                if 'go to page "P12060" of book "nida71.tbk"' in line:
                    self.assertEqual(quoted_go_to(line), ("P12060", "nida71.tbk"))
                    self.assertIn(item.owner, {"P12000", "P12001", "P12002", "P12003"})
                    saw_71 = True
        self.assertTrue(saw_book and saw_plain and saw_71)


if __name__ == "__main__":
    unittest.main()
