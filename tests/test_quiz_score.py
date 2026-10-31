"""``storeQuestionSkipped`` and ``getQuizScore`` over the stored arrays."""

import unittest

from opentoolbook.props import UserProperties
from opentoolbook.quizscore import get_quiz_score, record_answer, store_question_response


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


if __name__ == "__main__":
    unittest.main()
