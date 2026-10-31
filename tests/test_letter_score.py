"""A checked letter and its score go to ``__quizResponse`` and ``__quizScore``."""

import os
import unittest
from pathlib import Path

from opentoolbook.navigate import Navigator
from opentoolbook.props import UserProperties
from opentoolbook.quizscore import answer_score, get_quiz_response, record_answer

LESSON = os.environ.get("OPENTOOLBOOK_TBK")


def _lesson():
    if not LESSON or not os.path.isfile(LESSON):
        return None
    return Path(LESSON)


def _running(index=1, quiz_pass=1):
    return UserProperties({"__quizPass": quiz_pass, "__quizIndex": index})


class ResponseTests(unittest.TestCase):
    def test_the_last_checked_letter_is_the_response(self):
        self.assertEqual(get_quiz_response({"a": True, "c": True}), "c")
        self.assertEqual(get_quiz_response({"A": False, "b": True}), "b")
        self.assertEqual(get_quiz_response({}), "")
        # ``__quizMaxResponse`` is 5, so ``f`` is never read.
        self.assertEqual(get_quiz_response({"f": True}), "")

    def test_the_score_compares_without_case(self):
        self.assertEqual(answer_score("c", "C"), 100)
        self.assertEqual(answer_score("a", "C"), 0)

    def test_the_pair_is_stored_at_the_quiz_index(self):
        props = _running(index=2)
        self.assertEqual(record_answer(props, {"c": True}, "C", "1", "110"), 100)
        self.assertEqual(props.get("__quizResponse"), {2: "c"})
        self.assertEqual(props.get("__quizScore"), {2: 100})
        self.assertEqual(props.get("__quizAttempted"), {2: 1})
        self.assertEqual(props.get("__quizTestNo"), {2: 1})
        self.assertEqual(props.get("__quizQuestionNo"), {2: 110})

    def test_nothing_is_stored_outside_the_first_block(self):
        for props, checked in (
            (_running(index=0), {"a": True}),
            (_running(quiz_pass=4), {"a": True}),
            (_running(), {}),
        ):
            self.assertIsNone(record_answer(props, checked, "A", "1", "110"))
            self.assertIsNone(props.get("__quizScore"))


@unittest.skipUnless(_lesson(), "set OPENTOOLBOOK_TBK to Logic Families")
class LessonScoreTests(unittest.TestCase):
    def setUp(self):
        self.data = _lesson().read_bytes()

    def test_the_answer_letter_on_p10210_stores_100(self):
        props = _running()
        nav = Navigator(self.data, "P10210", props=props)
        nav.click("C")
        nav.click("Next")
        self.assertEqual(props.get("__quizResponse"), {1: "c"})
        self.assertEqual(props.get("__quizScore"), {1: 100})
        self.assertEqual(props.get("__quizQuestionNo"), {1: 110})

    def test_another_letter_on_p10210_stores_0(self):
        props = _running()
        nav = Navigator(self.data, "P10210", props=props)
        nav.click("A")
        nav.click("Next")
        self.assertEqual(props.get("__quizResponse"), {1: "a"})
        self.assertEqual(props.get("__quizScore"), {1: 0})

    def test_the_stored_checked_letter_counts_without_a_click(self):
        # P10211 stores B checked, and its Answer is B.
        props = _running()
        nav = Navigator(self.data, "P10211", props=props)
        self.assertEqual(nav.record_answer(), 100)
        self.assertEqual(props.get("__quizResponse"), {1: "b"})

    def test_no_props_store_writes_nothing(self):
        nav = Navigator(self.data, "P10210")
        nav.click("C")
        clicked = nav.click("Next")
        self.assertTrue(clicked.moved)
        self.assertIsNone(nav.props)


if __name__ == "__main__":
    unittest.main()
