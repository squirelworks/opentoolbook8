"""setupQuizEx from the selection1 groups on P10001 to P10004, run on the interpreter."""

import unittest
from functools import lru_cache
from unittest.mock import patch

from lesson import SKIP, lesson_path
from opentoolbook.navigate import Navigator
from opentoolbook.openscript import interp


@lru_cache(maxsize=1)
def _opened():
    from opentoolbook.entry import opening_page

    return opening_page(lesson_path())


@unittest.skipIf(lesson_path() is None, SKIP)
class LessonTests(unittest.TestCase):
    def setUp(self):
        fixed = patch.object(interp._random, "randint", lambda low, high: low)
        fixed.start()
        self.addCleanup(fixed.stop)

    def _nav(self, page):
        opened = _opened()
        props = type(opened.props)(dict(opened.props.items()))
        path = lesson_path()
        return Navigator(path.read_bytes(), page, path, props=props, sysbooks=opened.sysbooks)

    def test_each_selection1_group_stores_its_type_pages_and_pass(self):
        for page, kind in (("P10001", 0), ("P10002", 1), ("P10003", 2), ("P10004", 3)):
            with self.subTest(page=page):
                nav = self._nav(page)
                nav.click("selection1")
                self.assertEqual(nav.props.get("__quizPages").cells, {(1,): "P10301", (2,): "P10302", (3,): "P10303"})
                self.assertEqual(nav.props.get("__quizPass"), 1)
                self.assertEqual(nav.props.get("__quizType"), kind)
                self.assertEqual(nav.props.get("__quizObjectiveCount"), 2)
                self.assertEqual(nav.page_id, "P10210")

    def test_quiz_help_1_asks_and_breaks_first(self):
        nav = self._nav("P10002")
        nav.props.set("__quizHelp", 1)
        clicked = nav.click("selection1")
        self.assertEqual((clicked.moved, clicked.requests), (False, ("You are already in the quiz review!",)))
        self.assertIsNone(nav.props.get("__quizPass"))

    def test_too_many_attempts_is_error_1(self):
        nav = self._nav("P10002")
        nav.props.set("__quizMaxAttempts", 1)
        nav.props.set("__quizAttempts", 1)
        clicked = nav.click("selection1")
        self.assertEqual(
            clicked.requests,
            ("You have already attempted the quiz the maximum number of times!  Contact your instructor.",),
        )
        self.assertEqual(nav.page_id, "P10002")


if __name__ == "__main__":
    unittest.main()
