"""A Logic Families quiz, run by nc81test.sbk on the interpreter.

The pre-test starts from ``selection1`` on ``P10002``. ``random`` is fixed
to its lowest value, so ``addToRandomSetX`` picks questions in order:
110 to 115, then 120 to 123.
"""

import unittest
from functools import lru_cache
from unittest.mock import patch

from lesson import SKIP, lesson_path
from opentoolbook.navigate import Navigator
from opentoolbook.openscript import interp
from opentoolbook.show import show_page


@lru_cache(maxsize=1)
def _opened():
    from opentoolbook.entry import opening_page

    return opening_page(lesson_path())


def _cells(props, name):
    found = props.get(name)
    return {index[0]: value for index, value in found.cells.items() if value not in ("", 0)}


def _letters(nav):
    listed = show_page(nav.data, nav.page_id, 800, 600, checked=nav.checked_buttons())
    return {item.name: item.picture_role for item in listed.items if item.kind == "button" and item.name in "ABCD"}


@unittest.skipIf(lesson_path() is None, SKIP)
class QuizOnTheEngineTests(unittest.TestCase):
    def setUp(self):
        fixed = patch.object(interp._random, "randint", lambda low, high: low)
        fixed.start()
        self.addCleanup(fixed.stop)
        opened = _opened()
        props = type(opened.props)(dict(opened.props.items()))
        path = lesson_path()
        self.nav = Navigator(path.read_bytes(), "P10002", path, props=props, sysbooks=opened.sysbooks)

    def test_selection1_sets_up_the_pool_and_opens_the_first_question(self):
        nav = self.nav
        self.assertTrue(nav.click("selection1").moved)
        self.assertEqual(nav.page_id, "P10210")
        self.assertEqual(nav.props.get("__quizPass"), 1)
        self.assertEqual(nav.props.get("__quizIndex"), 1)
        self.assertEqual(_cells(nav.props, "__quizPages"), {1: "P10301", 2: "P10302", 3: "P10303"})
        self.assertEqual(
            _cells(nav.props, "__quizNumbers"),
            {1: "110", 2: "111", 3: "112", 4: "113", 5: "114", 6: "115", 7: "120", 8: "121", 9: "122", 10: "123"},
        )

    def test_a_letter_checks_itself_and_unchecks_the_others(self):
        nav = self.nav
        nav.click("selection1")
        clicked = nav.click("A")
        self.assertEqual((clicked.moved, clicked.checked), (False, True))
        self.assertEqual(_letters(nav)["A"], "checked")
        nav.click("b")
        self.assertEqual(_letters(nav), {"A": "up", "B": "checked", "C": "up", "D": "up"})

    def test_ok_stores_the_response_and_opens_the_next_question(self):
        nav = self.nav
        nav.click("selection1")
        nav.click("C")
        self.assertTrue(nav.click("OK").moved)
        self.assertEqual(nav.page_id, "P10211")
        self.assertEqual(_cells(nav.props, "__quizResponse"), {1: "c"})
        # P10210's Answer is C.
        self.assertEqual(_cells(nav.props, "__quizScore"), {1: 100})
        self.assertEqual(_cells(nav.props, "__quizQuestionNo"), {1: "110"})
        self.assertEqual(nav.props.get("__quizIndex"), 2)

    def test_ok_with_no_letter_beeps_and_stays(self):
        nav = self.nav
        nav.click("selection1")
        clicked = nav.click("OK")
        self.assertEqual((clicked.moved, clicked.beep), (False, True))
        self.assertEqual(nav.page_id, "P10210")

    def test_pass_1_disables_next_and_back_so_they_get_no_click(self):
        # setupQuizPage on pass 1 sets enabled of the background's Next and Back to false.
        nav = self.nav
        nav.click("selection1")
        listed = nav.display(800, 600)
        state = {item.name: item.enabled for item in listed.items if item.kind == "button" and item.name in ("OK", "Next", "Back")}
        self.assertEqual(state, {"OK": True, "Next": False, "Back": False})
        self.assertFalse(nav.click("Next").moved)
        self.assertEqual(nav.page_id, "P10210")
        self.assertEqual(_cells(nav.props, "__quizQuestionNo"), {})

    def test_background_fields_show_the_question_index(self):
        nav = self.nav
        nav.click("selection1")
        texts = {item.name: item.text for item in nav.display(800, 600).items if item.kind == "field"}
        self.assertEqual(texts.get("Index"), "Question 1.")
        nav.click("C")
        nav.click("OK")
        texts = {item.name: item.text for item in nav.display(800, 600).items if item.kind == "field"}
        self.assertEqual(texts.get("Index"), "Question 2.")

    def test_the_checked_state_stays_with_its_page(self):
        nav = self.nav
        nav.click("selection1")
        nav.click("A")
        nav.click("OK")
        self.assertEqual(nav.page_id, "P10211")
        self.assertNotIn(True, nav.checked_buttons().values())
        self.assertTrue(nav.back())
        self.assertEqual(nav.page_id, "P10210")
        self.assertTrue(nav.checked_buttons()["a"])

    def test_get_quiz_score_averages_with_div(self):
        from opentoolbook.openscript.interp import Engine
        from opentoolbook.openscript.values import Array
        from opentoolbook.run import BookHost, chain_lookup

        nav = self.nav
        books = [handlers for _book, handlers in nav.chain().books]
        for count, scores, expected in ((2, (100, 0), 50), (3, (100, 100), 66)):
            stored = Array()
            for index, score in enumerate(scores, 1):
                stored.set((index,), score)
            nav.props.set("__quizScore", stored)
            nav.props.set("__quizCount", count)
            engine = Engine(chain_lookup(lambda: books), BookHost(nav.pages, nav.book_name, nav.roots()), props=nav.props)
            self.assertEqual(engine.get("getquizscore"), expected)


if __name__ == "__main__":
    unittest.main()
