"""``keyDown`` carries the OpenScript key constant for PageUp, PageDown, and F-keys."""

from __future__ import annotations

import unittest

from engine_run import run
from opentoolbook.keys import KEYSYMS
from opentoolbook.navigate import Navigator
from pathlib import Path
from unittest.mock import patch

FIXTURE = Path(__file__).parent / "fixtures" / "otb-line-rect.tbk"


class KeyDownTests(unittest.TestCase):
    def test_keysyms_map_prior_next_and_f_keys(self):
        self.assertEqual(KEYSYMS["Prior"], "keyprior")
        self.assertEqual(KEYSYMS["Next"], "keynext")
        self.assertEqual(KEYSYMS["F2"], "keyf2")
        self.assertEqual(KEYSYMS["Up"], "keyuparrow")

    def test_keydown_handler_reads_the_key_constant(self):
        source = (
            "to handle keyDown key\n"
            "  if key = keyNext then\n"
            '    go to page "P2"\n'
            "  end if\n"
            "end\n"
        )
        acted = run(source, ("P1", "P2"), "P1", args=("keynext",))
        self.assertEqual(acted.page_id, "P2")
        stayed = run(source, ("P1", "P2"), "P1", args=("keyprior",))
        self.assertEqual(stayed.page_id, "P1")

    def test_navigator_key_down_sends_keynext(self):
        nav = Navigator(FIXTURE.read_bytes(), "", FIXTURE)
        source = (
            "to handle keyDown key\n"
            "  if key = keyNext then\n"
            '    go to page "P2"\n'
            "  end if\n"
            "end\n"
        )

        class Fake:
            books = (("book.tbk", {"keydown": source}),)

            def merged(self):
                return {"keydown": source}

        with patch.object(Navigator, "chain", return_value=Fake()):
            nav.pages = ("", "P2")
            acted = nav.key_down("Next")
        self.assertIsNotNone(acted)
        self.assertEqual(nav.page_id, "P2")
        self.assertTrue(acted.moved)


if __name__ == "__main__":
    unittest.main()
