"""``send exit`` closes the reader when no handler takes the message."""

from __future__ import annotations

import unittest
from pathlib import Path
from unittest.mock import patch

from engine_run import run
from lesson import SKIP, logic_families_path
from opentoolbook.navigate import Navigator

FIXTURE = Path(__file__).parent / "fixtures" / "otb-line-rect.tbk"


class SendExitTests(unittest.TestCase):
    def test_send_exit_marks_follow_exited_without_moving(self):
        acted = run("send exit\n", ("P1", "P2"), "P1")
        self.assertEqual(acted.page_id, "P1")
        self.assertTrue(acted.exited)

    def test_navigator_click_that_sends_exit_is_exited(self):
        nav = Navigator(FIXTURE.read_bytes(), "", FIXTURE)
        source = "to handle buttonClick\n  send exit\nend\n"

        class Fake:
            books = (("book.tbk", {"buttonclick": source}),)

            def merged(self):
                return {"buttonclick": source}

        with patch.object(Navigator, "chain", return_value=Fake()):
            acted = nav.click(None)
        self.assertFalse(acted.moved)
        self.assertTrue(acted.exited)
        self.assertEqual(nav.page_id, "")


@unittest.skipIf(logic_families_path() is None, SKIP)
class LessonExitTests(unittest.TestCase):
    def test_exit_on_p900_closes_when_the_ask_is_yes(self):
        from opentoolbook.entry import opening_page

        path = logic_families_path()
        entry = opening_page(path)
        yes = Navigator(
            path.read_bytes(),
            "P900",
            path,
            props=entry.props,
            sysbooks=entry.sysbooks,
            variables=dict(entry.variables),
        )
        yes.ask = lambda prompt, buttons: "Yes"
        acted = yes.click("exit")
        self.assertFalse(acted.moved)
        self.assertTrue(acted.exited)
        self.assertEqual(yes.page_id, "P900")

        no = Navigator(
            path.read_bytes(),
            "P900",
            path,
            props=entry.props,
            sysbooks=entry.sysbooks,
            variables=dict(entry.variables),
        )
        no.ask = lambda prompt, buttons: "No"
        stayed = no.click("exit")
        self.assertFalse(stayed.moved)
        self.assertFalse(stayed.exited)
        self.assertEqual(no.page_id, "P900")

    def test_keyup_f2_exits_when_the_ask_is_yes(self):
        from opentoolbook.entry import opening_page

        path = logic_families_path()
        entry = opening_page(path)
        nav = Navigator(
            path.read_bytes(),
            "P900",
            path,
            props=entry.props,
            sysbooks=entry.sysbooks,
            variables=dict(entry.variables),
        )
        nav.ask = lambda prompt, buttons: "Yes"
        acted = nav.key_up("F2")
        self.assertIsNotNone(acted)
        self.assertTrue(acted.exited)
        self.assertEqual(nav.page_id, "P900")


if __name__ == "__main__":
    unittest.main()
