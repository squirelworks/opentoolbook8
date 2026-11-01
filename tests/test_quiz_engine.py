"""A Logic Families quiz, run by nc81test.sbk on the interpreter.

The pre-test starts from ``selection1`` on ``P10002``. ``random`` is fixed
to its lowest value, so ``addToRandomSetX`` picks questions in order:
110 to 115, then 120 to 123.
"""

import unittest
from functools import lru_cache
from unittest.mock import patch

from lesson import SKIP, logic_families_path
from opentoolbook.navigate import Navigator
from opentoolbook.openscript import interp
from opentoolbook.show import show_page


@lru_cache(maxsize=1)
def _opened():
    from opentoolbook.entry import opening_page

    return opening_page(logic_families_path())


def _cells(props, name):
    found = props.get(name)
    return {index[0]: value for index, value in found.cells.items() if value not in ("", 0)}


def _letters(nav):
    listed = show_page(nav.data, nav.page_id, 800, 600, checked=nav.checked_buttons())
    return {item.name: item.picture_role for item in listed.items if item.kind == "button" and item.name in "ABCD"}


@unittest.skipIf(logic_families_path() is None, SKIP)
class QuizOnTheEngineTests(unittest.TestCase):
    def setUp(self):
        fixed = patch.object(interp._random, "randint", lambda low, high: low)
        fixed.start()
        self.addCleanup(fixed.stop)
        opened = _opened()
        props = type(opened.props)(dict(opened.props.items()))
        path = logic_families_path()
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

    def test_skip_with_a_letter_asks_and_no_keeps_the_answer(self):
        # Skip is enabled when __quizMode is not 0.
        nav = self.nav
        nav.props.set("__quizMode", 1)
        nav.click("selection1")
        nav.click("A")
        asked = []
        nav.ask = lambda prompt, buttons: asked.append((prompt, buttons)) or "No"
        clicked = nav.click("Skip")
        self.assertEqual(asked, [("Do you want to discard your answer?", ("Yes", "No"))])
        self.assertEqual((clicked.moved, clicked.beep, nav.page_id), (False, True, "P10210"))
        self.assertTrue(nav.checked_buttons()["a"])
        nav.ask = lambda prompt, buttons: "Yes"
        self.assertTrue(nav.click("Skip").moved)
        self.assertEqual(nav.page_id, "P10211")
        self.assertEqual(_cells(nav.props, "__quizResponse"), {})

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

    def test_menu_selection_t_then_begin_opens_the_first_question(self):
        opened = _opened()
        path = logic_families_path()
        props = type(opened.props)(dict(opened.props.items()))
        nav = Navigator(path.read_bytes(), "P450", path, props=props, sysbooks=opened.sysbooks)
        self.assertEqual(opened.props.get("__lessonMode"), 2)
        self.assertTrue(nav.click("Menu").moved)
        self.assertEqual(nav.page_id, "P900")
        self.assertEqual(nav.title(), "9e954d01.tbk - P900")
        self.assertTrue(nav.click("selectiont").moved)
        self.assertEqual(nav.page_id, "P10004")
        self.assertTrue(nav.click("selection1").moved)
        self.assertEqual(nav.page_id, "P10210")
        self.assertEqual(nav.props.get("__quizPass"), 1)
        self.assertEqual(nav.props.get("__quizType"), 3)
        self.assertEqual(nav.props.get("__quizIndex"), 1)
        self.assertEqual(nav.title(), "9e954d01.tbk - P10210")

    def test_menu_with_lesson_mode_0_opens_assessment_and_begin_starts_it(self):
        opened = _opened()
        path = logic_families_path()
        props = type(opened.props)(dict(opened.props.items()))
        props.set("__lessonMode", 0)
        props.set("__quizAssessment", 0)
        nav = Navigator(path.read_bytes(), "P450", path, props=props, sysbooks=opened.sysbooks)
        self.assertTrue(nav.click("Menu").moved)
        self.assertEqual(nav.page_id, "P10001")
        self.assertEqual(nav.props.get("__quizDisableMenuKey"), 1)
        self.assertEqual(nav.title(), "9e954d01.tbk - P10001")
        self.assertTrue(nav.click("selection1").moved)
        self.assertEqual(nav.page_id, "P10210")
        self.assertEqual(nav.props.get("__quizPass"), 1)
        self.assertEqual(nav.props.get("__quizType"), 0)
        self.assertEqual(nav.props.get("__quizIndex"), 1)
        self.assertEqual(nav.title(), "9e954d01.tbk - P10210")

    def test_answering_every_question_opens_the_score_page(self):
        from opentoolbook.quiz import questions

        nav = self.nav
        by_page = {item.page_id: item for item in questions(nav.data)}
        self.assertTrue(nav.click("selection1").moved)
        self.assertEqual(nav.props.get("__quizMode"), 0)
        for _ in range(15):
            if nav.page_id.startswith("P103"):
                break
            answer = (by_page[nav.page_id].answer or "A").upper()
            nav.click(answer)
            self.assertTrue(nav.click("OK").moved)
        self.assertEqual(nav.page_id, "P10303")
        self.assertEqual(nav.title(), "9e954d01.tbk - P10303")
        stem = next(
            item.text
            for item in nav.display(800, 600).items
            if item.kind == "field" and item.name.lower() == "stem"
        )
        self.assertEqual(stem, "The test is complete and your score is 100%.  Do you want to _________")

    def test_score_page_ok_returns_to_the_menu(self):
        from opentoolbook.quiz import questions

        nav = self.nav
        by_page = {item.page_id: item for item in questions(nav.data)}
        self.assertTrue(nav.click("selection1").moved)
        for _ in range(15):
            if nav.page_id.startswith("P103"):
                break
            answer = (by_page[nav.page_id].answer or "A").upper()
            nav.click(answer)
            self.assertTrue(nav.click("OK").moved)
        self.assertEqual(nav.page_id, "P10303")
        self.assertEqual(nav.checked_buttons().get("b"), True)
        self.assertTrue(nav.click("OK").moved)
        self.assertEqual(nav.page_id, "P900")
        self.assertEqual(nav.title(), "9e954d01.tbk - P900")

    def test_one_wrong_answer_shows_ninety_percent_on_the_score_page(self):
        from opentoolbook.quiz import questions

        nav = self.nav
        by_page = {item.page_id: item for item in questions(nav.data)}
        self.assertTrue(nav.click("selection1").moved)
        for index in range(15):
            if nav.page_id.startswith("P103"):
                break
            answer = (by_page[nav.page_id].answer or "A").upper()
            if index == 0:
                pick = "A" if answer != "A" else "B"
            else:
                pick = answer
            nav.click(pick)
            self.assertTrue(nav.click("OK").moved)
        self.assertEqual(nav.page_id, "P10303")
        stem = next(
            item.text
            for item in nav.display(800, 600).items
            if item.kind == "field" and item.name.lower() == "stem"
        )
        self.assertEqual(stem, "The test is complete and your score is 90%.  Do you want to _________")

    def test_selection2_opens_directions_then_next_returns(self):
        nav = self.nav
        self.assertEqual(nav.book_name, "9e954d01.tbk")
        self.assertTrue(nav.click("selection2").moved)
        self.assertEqual(nav.page_id, "P10020")
        self.assertEqual(nav.book_name, "nida81.tbk")
        self.assertEqual(nav.title(), "nida81.tbk - P10020")
        texts = {
            item.name: item.text
            for item in nav.display(800, 600).items
            if item.kind == "field"
        }
        self.assertEqual(texts.get(""), "Directions")
        self.assertEqual(texts.get("Page#"), "P10020")
        self.assertTrue(nav.click("Next").moved)
        self.assertEqual(nav.page_id, "P10002")
        self.assertEqual(nav.book_name, "9e954d01.tbk")
        self.assertEqual(nav.title(), "9e954d01.tbk - P10002")


if __name__ == "__main__":
    unittest.main()
