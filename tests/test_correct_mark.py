"""The rectangle ``Correct`` is painted only after ``setupQuizPage`` shows it."""

import os
import unittest
from pathlib import Path

from opentoolbook.props import UserProperties
from opentoolbook.quiznav import quiz_click, setup_quiz_page_correct

PAGES = ("P10004", "P10210", "P10211", "P10303")


class CorrectMarkTests(unittest.TestCase):
    def test_the_line_by_pass(self):
        self.assertIs(setup_quiz_page_correct(1), False)
        self.assertIs(setup_quiz_page_correct(3), False)
        self.assertIs(setup_quiz_page_correct(5), True)
        self.assertIs(setup_quiz_page_correct(8), True)
        self.assertIsNone(setup_quiz_page_correct(None))
        self.assertIs(setup_quiz_page_correct(1, reader=False), True)

    def test_clicks_carry_it(self):
        self.assertIsNone(quiz_click(PAGES, "P10210", "Next").correct)
        moved = quiz_click(PAGES, "P10210", "Next", quiz_pass=8)
        self.assertEqual((moved.page_id, moved.correct), ("P10211", True))
        back = quiz_click(PAGES, "P10211", "Back", quiz_pass=8)
        self.assertEqual((back.page_id, back.correct), ("P10210", True))
        props = UserProperties()
        props.set("__quizPass", 1)
        props.set("__quizStartPage", 1)
        props.set("__quizCount", 1)
        props.set("__quizIndex", 0)
        props.set("__quizNumbers", {1: 111})
        running = quiz_click(PAGES, "P10210", "Next", quiz_pass=1, props=props,
                             question_numbers={"P10210": 110, "P10211": 111})
        self.assertEqual((running.page_id, running.correct), ("P10211", False))

    def test_painted_only_after_the_line(self):
        path = os.environ.get("OPENTOOLBOOK_TBK")
        if not path or not os.path.isfile(path):
            self.skipTest("set OPENTOOLBOOK_TBK to 9e954d01.tbk")
        from opentoolbook.field import page_ids
        from opentoolbook.show import show_page

        data = Path(path).read_bytes()
        pages = page_ids(data)
        before = show_page(data, "P10211", 800, 600)
        self.assertNotIn("correct", [item.name.lower() for item in before.items])
        moved = quiz_click(pages, "P10210", "Next", quiz_pass=8)
        self.assertEqual(moved.page_id, "P10211")
        after = show_page(data, moved.page_id, 800, 600, correct=bool(moved.correct))
        marks = [item for item in after.items if item.name.lower() == "correct"]
        self.assertEqual(len(marks), 1)
        self.assertEqual((marks[0].kind, marks[0].pattern), ("rectangle", 253))
        self.assertEqual(len(after.items), len(before.items) + 1)


if __name__ == "__main__":
    unittest.main()
