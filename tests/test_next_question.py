"""``gotoNextQuestionEx`` opens the page whose ``QuestionNo`` is the next pool number."""

import os
import random
import unittest
from pathlib import Path

from opentoolbook.pool import add_objective_to_pool, clear_pool, goto_next_question_ex, setup_pool
from opentoolbook.props import UserProperties
from opentoolbook.quiznav import quiz_click

PAGES = ("P10001", "P10004", "P10210", "P10211", "P10212", "P10303")
NUMBERS = {"P10210": 110, "P10211": 111, "P10212": 112}


def _running(numbers, start=1, mode=None):
    props = UserProperties()
    props.set("__quizPass", 1)
    props.set("__quizStartPage", start)
    props.set("__quizIndex", 0)
    props.set("__quizCount", len(numbers))
    props.set("__quizNumbers", {index + 1: number for index, number in enumerate(numbers)})
    props.set("__quizPages", {1: "P10301", 2: "P10302", 3: "P10303"})
    if mode is not None:
        props.set("__quizMode", mode)
    return props


class NextQuestionTests(unittest.TestCase):
    def test_a_pool_of_one_number_opens_that_page(self):
        props = _running([111])
        self.assertEqual(goto_next_question_ex(props, PAGES, NUMBERS), "P10211")
        self.assertEqual(props.get("__quizIndex"), 1)

    def test_after_the_last_question_pass_1_opens_quiz_page_3(self):
        props = _running([111])
        goto_next_question_ex(props, PAGES, NUMBERS)
        self.assertEqual(goto_next_question_ex(props, PAGES, NUMBERS), "P10303")
        props = _running([], mode=1)
        self.assertEqual(goto_next_question_ex(props, PAGES, NUMBERS), "P10301")

    def test_the_search_starts_at_the_start_page(self):
        props = _running([110], start=4)
        self.assertIsNone(goto_next_question_ex(props, PAGES, NUMBERS))

    def test_no_quiz_keeps_the_stored_list(self):
        self.assertEqual(quiz_click(PAGES, "P10210", "Next").page_id, "P10211")
        self.assertEqual(quiz_click(PAGES, "P10210", "Back").page_id, "P10004")

    def test_pass_8_keeps_send_next(self):
        props = _running([112])
        self.assertEqual(
            quiz_click(PAGES, "P10210", "Next", quiz_pass=8, props=props, question_numbers=NUMBERS).page_id,
            "P10211",
        )

    def test_a_running_quiz_click(self):
        props = _running([112, 110])
        moved = quiz_click(PAGES, "P10210", "Next", quiz_pass=1, props=props, question_numbers=NUMBERS)
        self.assertEqual(moved.page_id, "P10212")
        moved = quiz_click(PAGES, "P10212", "OK", quiz_pass=1, checked="a", props=props, question_numbers=NUMBERS)
        self.assertEqual(moved.page_id, "P10210")
        stay = quiz_click(PAGES, "P10210", "OK", quiz_pass=1, props=props, question_numbers=NUMBERS)
        self.assertEqual((stay.page_id, stay.beep), ("P10210", True))
        self.assertEqual(
            quiz_click(PAGES, "P10210", "Back", quiz_pass=1, props=props, question_numbers=NUMBERS).page_id,
            "P10210",
        )
        self.assertEqual(
            quiz_click(PAGES, "P10210", "Next", quiz_pass=1, props=props, question_numbers=NUMBERS).page_id,
            "P10303",
        )

    def test_the_lesson_quiz(self):
        path = os.environ.get("OPENTOOLBOOK_TBK")
        if not path or not os.path.isfile(path):
            self.skipTest("set OPENTOOLBOOK_TBK to 9e954d01.tbk")
        from opentoolbook.field import page_ids
        from opentoolbook.quiz import questions

        data = Path(path).read_bytes()
        pages = page_ids(data)
        numbers = {item.page_id: int(item.question_no) for item in questions(data)}
        props = UserProperties()
        props.set("__quizPass", 1)
        props.set("__quizStartPage", pages.index("P10001") + 1)
        clear_pool(props)
        add_objective_to_pool(props, 1, 110, 119, 1)
        setup_pool(props, random.Random(5))
        expected = props.get("__quizNumbers")[1]
        opened = goto_next_question_ex(props, pages, numbers)
        self.assertEqual(numbers[opened], expected)
        self.assertEqual(opened, f"P10{expected + 100}")


if __name__ == "__main__":
    unittest.main()
