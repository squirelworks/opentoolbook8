"""``beep`` returns. ``request`` records its text, and the page stays."""

import os
import unittest
from pathlib import Path

from opentoolbook.click import run_handler
from opentoolbook.quiznav import quiz_click, skip_request
from opentoolbook.walk import is_beep, request_text

SKIP = """to get handleQuizClick vTarget
    if  name of vTarget is "Skip"  then
        response = getQuizResponse()
        if  response <> ""  then
            beep(1)
            request "Do you want to discard your answer?" with "Yes" or "No"
            conditions
                when it is "No"
                    return 0
            end conditions
            set checked of button response to false
        end if
        get gotoNextQuestionEx()
    end if
    return 0
end
"""


class RequestTests(unittest.TestCase):
    def test_the_two_statements(self):
        self.assertTrue(is_beep("beep(1)"))
        self.assertTrue(is_beep("beep 2"))
        self.assertTrue(is_beep("beep"))
        self.assertFalse(is_beep("beeper"))
        self.assertEqual(request_text('request "Say ""hi"""'), 'Say "hi"')
        self.assertEqual(request_text('request "Q?" with "Yes" or "No"'), "Q?")
        self.assertIsNone(request_text("request x"))

    def test_a_click_records_the_request_and_stays(self):
        source = (
            "to handle buttonClick\n"
            "  beep(1)\n"
            '  request "You are already in the quiz review!"\n'
            "  break\n"
            '  go to page "P2"\nend'
        )
        follow = run_handler(source, ("P1", "P2"), "P1")
        self.assertEqual(follow.page_id, "P1")
        self.assertEqual(follow.requests, ("You are already in the quiz review!",))
        self.assertEqual(follow.beeps, 1)

    def test_skip_with_a_checked_letter(self):
        pages = ("P10004", "P10210", "P10211")
        self.assertEqual(skip_request(SKIP), "Do you want to discard your answer?")
        result = quiz_click(pages, "P10210", "Skip", quiz_pass=8, checked="a", script=SKIP)
        self.assertEqual(
            (result.page_id, result.beep, result.request),
            ("P10210", True, "Do you want to discard your answer?"),
        )
        moved = quiz_click(pages, "P10210", "Skip", quiz_pass=8, script=SKIP)
        self.assertEqual((moved.page_id, moved.request), ("P10211", None))

    def test_the_system_book_skip_branch(self):
        path = os.environ.get("OPENTOOLBOOK_TBK")
        if not path or not os.path.isfile(path):
            self.skipTest("set OPENTOOLBOOK_TBK to 9e954d01.tbk")
        from opentoolbook.entry import _handler_map
        from opentoolbook.shelf import find_file, search_roots

        found = find_file(search_roots(Path(path), None), "nc81test.sbk")
        if found is None:
            self.skipTest("nc81test.sbk is not beside the lesson")
        script = _handler_map(found.read_bytes())["handlequizclick"]
        result = quiz_click(("P10004", "P10210", "P10211"), "P10210", "Skip", quiz_pass=8, checked="a", script=script)
        self.assertEqual(result.page_id, "P10210")
        self.assertEqual(result.request, "Do you want to discard your answer?")


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
