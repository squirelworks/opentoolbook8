"""``storeQuestionSkipped`` and ``getQuizScore`` over the stored arrays."""

import os
import unittest
from pathlib import Path

from opentoolbook.navigate import Navigator
from opentoolbook.props import UserProperties
from opentoolbook.quizscore import get_quiz_score, record_answer, store_question_response

LESSON = os.environ.get("OPENTOOLBOOK_TBK")


def _lesson():
    if not LESSON or not os.path.isfile(LESSON):
        return None
    return Path(LESSON)


class QuizScoreTests(unittest.TestCase):
    def test_two_stored_responses_average_with_div(self):
        props = UserProperties({"__quizPass": 1, "__quizCount": 2})
        props.set("__quizIndex", 1)
        store_question_response(props, 1, 110, "c", 100)
        props.set("__quizIndex", 2)
        store_question_response(props, 1, 111, "a", 0)
        self.assertEqual(props.get("__quizScore"), {1: 100, 2: 0})
        self.assertEqual(get_quiz_score(props), 50)

    def test_an_unstored_question_counts_as_0(self):
        props = UserProperties({"__quizCount": 3, "__quizScore": {1: 100, 2: 100}})
        # 200 div 3 is 66.
        self.assertEqual(get_quiz_score(props), 66)

    def test_no_questions_is_0(self):
        self.assertEqual(get_quiz_score(UserProperties()), 0)

    def test_no_letter_stores_the_question_as_skipped(self):
        props = UserProperties({"__quizPass": 1, "__quizIndex": 3})
        self.assertIsNone(record_answer(props, {}, "C", "1", "112"))
        self.assertEqual(props.get("__quizTestNo"), {3: 1})
        self.assertEqual(props.get("__quizQuestionNo"), {3: 112})
        self.assertIsNone(props.get("__quizResponse"))
        self.assertIsNone(props.get("__quizAttempted"))


@unittest.skipUnless(_lesson(), "set OPENTOOLBOOK_TBK to Logic Families")
class LessonQuizScoreTests(unittest.TestCase):
    def test_two_pages_answered_score_50(self):
        data = _lesson().read_bytes()
        props = UserProperties({"__quizPass": 1, "__quizIndex": 1, "__quizCount": 2})
        nav = Navigator(data, "P10210", props=props)
        nav.click("C")
        nav.click("Next")
        self.assertEqual(nav.page_id, "P10211")
        props.set("__quizIndex", 2)
        nav.click("A")
        nav.click("Next")
        self.assertEqual(props.get("__quizResponse"), {1: "c", 2: "a"})
        self.assertEqual(get_quiz_score(props), 50)

    def test_ok_with_no_letter_stores_nothing(self):
        # handleQuizClick: OK with __quizPass in 1,2 and no response beeps and returns 0.
        data = _lesson().read_bytes()
        props = UserProperties({"__quizPass": 1, "__quizIndex": 1})
        nav = Navigator(data, "P10210", props=props)
        nav.click("OK")
        self.assertIsNone(props.get("__quizQuestionNo"))

    def test_next_with_no_letter_stores_the_question_as_skipped(self):
        data = _lesson().read_bytes()
        props = UserProperties({"__quizPass": 1, "__quizIndex": 1})
        nav = Navigator(data, "P10210", props=props)
        nav.click("Next")
        self.assertEqual(props.get("__quizQuestionNo"), {1: 110})
        self.assertIsNone(props.get("__quizResponse"))


if __name__ == "__main__":
    unittest.main()
