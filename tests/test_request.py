"""``beep`` returns. ``request`` records its text, and the page stays."""

import unittest
from pathlib import Path

from engine_run import run

class RequestTests(unittest.TestCase):
    def test_a_click_records_the_request_and_stays(self):
        source = (
            "to handle buttonClick\n"
            "  beep(1)\n"
            '  request "You are already in the quiz review!"\n'
            "  break\n"
            '  go to page "P2"\nend'
        )
        follow = run(source, ("P1", "P2"), "P1")
        self.assertEqual(follow.page_id, "P1")
        self.assertEqual(follow.requests, ("You are already in the quiz review!",))
        self.assertEqual(follow.beeps, 1)


class NavigatorRequestTests(unittest.TestCase):
    def test_the_window_gets_the_request_and_stays(self):
        from unittest.mock import patch

        from opentoolbook import navigate
        from opentoolbook.click import Follow

        fixture = Path(__file__).parent / "fixtures" / "otb-line-rect.tbk"
        nav = navigate.Navigator(fixture.read_bytes(), "")
        asked = Follow("", None, requests=("You are already in the quiz review!",), beeps=1)
        with patch.object(navigate.Navigator, "_send", return_value=asked):
            clicked = nav.click("selection1")
        self.assertEqual(
            (clicked.moved, clicked.beep, clicked.requests),
            (False, True, ("You are already in the quiz review!",)),
        )


if __name__ == "__main__":
    unittest.main()
