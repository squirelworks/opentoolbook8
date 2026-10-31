"""A checked letter and its score go to ``__quizResponse`` and ``__quizScore``."""

import unittest

from opentoolbook.props import UserProperties
from opentoolbook.quizscore import answer_score, get_quiz_response, record_answer


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


if __name__ == "__main__":
    unittest.main()
