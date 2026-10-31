"""Item 48: a quiz click runs shared script 103's ``buttonClick``, then ``handleQuizClick``."""

import os
import unittest
from pathlib import Path

from opentoolbook.navigate import Navigator
from opentoolbook.props import UserProperties
from opentoolbook.script import shared_scripts

LESSON = os.environ.get("OPENTOOLBOOK_TBK")


def _lesson():
    if not LESSON or not os.path.isfile(LESSON):
        return None
    return Path(LESSON)


@unittest.skipIf(_lesson() is None, "set OPENTOOLBOOK_TBK to the lesson book")
class SharedScriptClickTests(unittest.TestCase):
    def setUp(self):
        self.path = _lesson()
        self.data = self.path.read_bytes()

    def _nav(self, props):
        return Navigator(self.data, "P10210", self.path, props=props)

    def test_script_103_button_click_is_one_get_line(self):
        source = next(item.source for item in shared_scripts(self.data) if item.resource_id == 103)
        start = source.lower().index("to handle buttonclick")
        body = source[start:].split("\n", 1)[1]
        end = body.lower().index("\nend")
        self.assertEqual([line.strip() for line in body[:end].splitlines() if line.strip()], ["get handleQuizClick(target)"])

    def test_the_click_reads_handle_quiz_click_from_the_test_book(self):
        nav = self._nav(UserProperties())
        self.assertIn('__quizPass is in "1,2"', nav.handlers()["handlequizclick"])

    def test_empty_ok_on_pass_1_and_2_stays_and_beeps(self):
        for quiz_pass in (1, 2):
            props = UserProperties({"__quizPass": quiz_pass, "__quizIndex": 1})
            nav = self._nav(props)
            clicked = nav.click("OK")
            self.assertFalse(clicked.moved)
            self.assertTrue(clicked.beep)
            self.assertEqual(nav.page_id, "P10210")

    def test_ok_with_no_quiz_running_still_moves(self):
        nav = self._nav(UserProperties())
        clicked = nav.click("OK")
        self.assertTrue(clicked.moved)
        self.assertFalse(clicked.beep)

    def test_next_on_pass_1_opens_the_next_pooled_question(self):
        # __quizNumbers holds 110 then 111. __quizIndex 1 is P10210 (110).
        props = UserProperties(
            {
                "__quizPass": 1,
                "__quizIndex": 1,
                "__quizCount": 2,
                "__quizNumbers": {1: 110, 2: 111},
                "__quizStartPage": 1,
            }
        )
        nav = self._nav(props)
        nav.click("C")
        clicked = nav.click("Next")
        self.assertTrue(clicked.moved)
        self.assertEqual(nav.page_id, "P10211")
        self.assertEqual(props.get("__quizResponse"), {1: "c"})


if __name__ == "__main__":
    unittest.main()
