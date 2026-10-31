"""``keyChar`` carries the typed character to the page."""

from __future__ import annotations

import unittest
from pathlib import Path
from unittest.mock import patch

from engine_run import run
from opentoolbook.navigate import Navigator

FIXTURE = Path(__file__).parent / "fixtures" / "otb-line-rect.tbk"


class KeyCharTests(unittest.TestCase):
    def test_keychar_handler_reads_the_character(self):
        source = (
            "to handle keyChar key\n"
            '  if key = "a" then\n'
            '    go to page "P2"\n'
            "  end if\n"
            "end\n"
        )
        acted = run(source, ("P1", "P2"), "P1", args=("a",))
        self.assertEqual(acted.page_id, "P2")
        stayed = run(source, ("P1", "P2"), "P1", args=("b",))
        self.assertEqual(stayed.page_id, "P1")

    def test_navigator_key_char_sends_the_character(self):
        nav = Navigator(FIXTURE.read_bytes(), "", FIXTURE)
        source = (
            "to handle keyChar key\n"
            '  if key = "x" then\n'
            '    go to page "P2"\n'
            "  end if\n"
            "end\n"
        )
        with patch.object(Navigator, "chain") as chain:
            chain.return_value.books = (("book.tbk", {"keychar": source}),)
            # chain().books is used as a list of pairs; also merged/handlers may be hit.
            class Fake:
                books = (("book.tbk", {"keychar": source}),)

                def merged(self):
                    return {"keychar": source}

            chain.return_value = Fake()
            # Page id "" is the fixture's only page; go to P2 needs that page in pages.
            nav.pages = ("", "P2")
            acted = nav.key_char("x")
        self.assertIsNotNone(acted)
        self.assertEqual(nav.page_id, "P2")
        self.assertTrue(acted.moved)


if __name__ == "__main__":
    unittest.main()
