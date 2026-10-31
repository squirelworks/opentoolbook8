"""``target is button "name" of …`` matches the click target by kind and name."""

from __future__ import annotations

import unittest
from unittest.mock import patch

from engine_run import run
from lesson import SKIP, logic_families_path
from opentoolbook.navigate import Navigator
from opentoolbook.openscript import interp


class ObjectIsTests(unittest.TestCase):
    def test_unqualified_button_matches_qualified_button_of_the_same_name(self):
        source = (
            "to handle buttonClick\n"
            '  if button "Go" is button "Go" of this page then\n'
            '    go to page "P2"\n'
            "  end if\n"
            "end\n"
        )
        acted = run(source, ("P1", "P2"), "P1")
        self.assertEqual(acted.page_id, "P2")

    def test_different_button_names_do_not_match(self):
        source = (
            "to handle buttonClick\n"
            '  if button "Go" is button "Other" of this page then\n'
            '    go to page "P2"\n'
            "  end if\n"
            "end\n"
        )
        acted = run(source, ("P1", "P2"), "P1")
        self.assertEqual(acted.page_id, "P1")


@unittest.skipIf(logic_families_path() is None, SKIP)
class SkippedCountPageTests(unittest.TestCase):
    def test_p10301_shows_the_skipped_count_and_ok_opens_the_score(self):
        from opentoolbook.entry import opening_page

        path = logic_families_path()
        entry = opening_page(path)
        props = type(entry.props)(dict(entry.props.items()))
        props.set("__quizMode", 1)
        nav = Navigator(path.read_bytes(), "P10002", path, props=props, sysbooks=entry.sysbooks)
        with patch.object(interp._random, "randint", lambda low, high: low):
            self.assertTrue(nav.click("selection1").moved)
            for index in range(15):
                if nav.page_id.startswith("P103"):
                    break
                if index % 3 == 0:
                    nav.ask = lambda prompt, buttons: "Yes"
                    self.assertTrue(nav.click("Skip").moved)
                else:
                    nav.click("A")
                    self.assertTrue(nav.click("OK").moved)
        self.assertEqual(nav.page_id, "P10301")
        stem = next(
            item.text
            for item in nav.display(800, 600).items
            if item.kind == "field" and item.name.lower() == "stem"
        )
        self.assertEqual(stem, "You skipped 4 questions.  Do you want to _________")
        self.assertNotIn("X", stem)
        nav.click("B")
        self.assertTrue(nav.click("OK").moved)
        self.assertEqual(nav.page_id, "P10303")
        score = next(
            item.text
            for item in nav.display(800, 600).items
            if item.kind == "field" and item.name.lower() == "stem"
        )
        self.assertIn("score is", score.lower())


if __name__ == "__main__":
    unittest.main()
