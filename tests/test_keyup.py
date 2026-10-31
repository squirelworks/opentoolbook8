"""``keyUp`` carries the OpenScript key constant on the live interpreter path."""

from __future__ import annotations

import unittest
from pathlib import Path
from unittest.mock import patch

from engine_run import run
from opentoolbook.navigate import Navigator

FIXTURE = Path(__file__).parent / "fixtures" / "otb-line-rect.tbk"


class KeyUpTests(unittest.TestCase):
    def test_keyup_handler_reads_the_key_constant(self):
        source = (
            "to handle keyUp key\n"
            "  if key = keyF2 then\n"
            '    go to page "P2"\n'
            "  end if\n"
            "end\n"
        )
        acted = run(source, ("P1", "P2"), "P1", args=("keyf2",))
        self.assertEqual(acted.page_id, "P2")
        stayed = run(source, ("P1", "P2"), "P1", args=("keyf1",))
        self.assertEqual(stayed.page_id, "P1")

    def test_navigator_key_up_sends_keyf2(self):
        nav = Navigator(FIXTURE.read_bytes(), "", FIXTURE)
        source = (
            "to handle keyUp key\n"
            "  if key = keyF2 then\n"
            '    go to page "P2"\n'
            "  end if\n"
            "end\n"
        )

        class Fake:
            books = (("book.tbk", {"keyup": source}),)

            def merged(self):
                return {"keyup": source}

        with patch.object(Navigator, "chain", return_value=Fake()):
            nav.pages = ("", "P2")
            acted = nav.key_up("F2")
        self.assertIsNotNone(acted)
        self.assertEqual(nav.page_id, "P2")
        self.assertTrue(acted.moved)


if __name__ == "__main__":
    unittest.main()
