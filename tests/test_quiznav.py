"""A quiz click beeps or turns the page. The display list does not need a screen."""

import os
import unittest
from pathlib import Path

from opentoolbook.field import page_ids
from opentoolbook.quiznav import quiz_click
from opentoolbook.script import book_handlers, resource_scripts, shared_scripts
from opentoolbook.show import DisplayList, Paint, button_at, show_page, unit_to_px

from lesson import companion

LESSON = os.environ.get("OPENTOOLBOOK_TBK")
PAGES = ("P10004", "P10210", "P10211", "P10212")


def _lesson():
    if not LESSON or not os.path.isfile(LESSON):
        return None
    return Path(LESSON)


class QuizClickTests(unittest.TestCase):
    def test_a_list_opened_page_turns_into_the_next_or_previous_page(self):
        for name in ("OK", "Next", "Skip", "ok"):
            moved = quiz_click(PAGES, "P10210", name)
            self.assertEqual(moved.page_id, "P10211")
            self.assertFalse(moved.beep)
        back = quiz_click(PAGES, "P10210", "Back")
        self.assertEqual(back.page_id, "P10004")
        self.assertFalse(back.beep)
        self.assertEqual(quiz_click(PAGES, "P10210", "A").page_id, "P10210")
        self.assertEqual(quiz_click(("P10210",), "P10210", "OK").page_id, "P10210")
        self.assertEqual(quiz_click(PAGES, "P10004", "Back").page_id, "P10004")

    def test_ok_with_no_choice_on_pass_1_or_2_beeps_and_stays(self):
        for quiz_pass in (1, 2):
            for checked in (None, "", "  "):
                stayed = quiz_click(PAGES, "P10210", "OK", quiz_pass=quiz_pass, checked=checked)
                self.assertEqual(stayed.page_id, "P10210")
                self.assertTrue(stayed.beep)
        chosen = quiz_click(PAGES, "P10210", "OK", quiz_pass=1, checked="C")
        self.assertEqual(chosen.page_id, "P10210")
        self.assertFalse(chosen.beep)
        self.assertEqual(quiz_click(PAGES, "P10210", "Next", quiz_pass=1).page_id, "P10210")

    def test_pass_8_sends_next_and_a_chosen_skip_beeps(self):
        self.assertEqual(quiz_click(PAGES, "P10210", "OK", quiz_pass=8).page_id, "P10211")
        self.assertEqual(quiz_click(PAGES, "P10210", "Back", quiz_pass=8).page_id, "P10004")
        skipped = quiz_click(PAGES, "P10210", "Skip", quiz_pass=8, checked="A")
        self.assertEqual(skipped.page_id, "P10210")
        self.assertTrue(skipped.beep)
        empty = quiz_click(PAGES, "P10210", "Skip", quiz_pass=8, checked="")
        self.assertEqual(empty.page_id, "P10211")
        self.assertFalse(empty.beep)

    def test_the_top_button_is_the_one_under_the_point(self):
        listed = DisplayList(
            "P10210",
            100,
            100,
            100,
            100,
            1,
            (
                Paint("button", 1, "Back", bounds=(0, 0, 30, 30)),
                Paint("button", 2, "OK", bounds=(30, 0, 60, 30)),
                Paint("field", 3, "A", bounds=(30, 0, 60, 30), text="A"),
            ),
        )
        ok_x = (unit_to_px(30, 1) + unit_to_px(60, 1)) / 2
        ok_y = unit_to_px(15, 1)
        self.assertEqual(button_at(listed, ok_x, ok_y), "OK")
        self.assertEqual(button_at(listed, unit_to_px(10, 1), ok_y), "Back")
        self.assertIsNone(button_at(listed, 100, 100))


class QuizPageTests(unittest.TestCase):
    def test_p10210_keeps_the_up_face_and_the_script_names_the_beep(self):
        path = _lesson()
        if path is None:
            self.skipTest("set OPENTOOLBOOK_TBK to 9e954d01.tbk")
        data = path.read_bytes()
        ids = page_ids(data)
        opened = quiz_click(ids, "P10210", "OK")
        self.assertEqual(opened.page_id, "P10211")
        self.assertFalse(opened.beep)
        self.assertEqual(quiz_click(ids, "P10210", "Back").page_id, "P10004")
        stayed = quiz_click(ids, "P10210", "OK", quiz_pass=1)
        self.assertTrue(stayed.beep)
        self.assertEqual(stayed.page_id, "P10210")
        stayed_again = quiz_click(ids, "P10210", "OK", quiz_pass=2)
        self.assertTrue(stayed_again.beep)
        shown = show_page(data, "P10210", 400, 300)
        for letter in ("A", "B", "C", "D"):
            button = next(item for item in shown.items if item.kind == "button" and item.name == letter)
            self.assertEqual(button.picture_role, "up")
            self.assertNotEqual(button.picture_id, 118)
        self.assertFalse(any(item.kind == "rectangle" and item.name.lower() == "correct" for item in shown.items))
        ok = next(item for item in shown.items if item.kind == "button" and item.name == "OK")
        point_x = (unit_to_px(ok.bounds[0], shown.scale) + unit_to_px(ok.bounds[2], shown.scale)) / 2
        point_y = (unit_to_px(ok.bounds[1], shown.scale) + unit_to_px(ok.bounds[3], shown.scale)) / 2
        self.assertEqual(button_at(shown, point_x, point_y), "OK")
        shared = next(item.source for item in shared_scripts(data) if item.resource_id == 103)
        self.assertIn("get handleQuizClick(target)", shared)
        quiz = resource_scripts(companion(path, "nc81test.sbk").read_bytes())[0].source
        click = _body(quiz, "handleQuizClick")
        self.assertIn('__quizPass is in "1,2"', click)
        self.assertIn("beep(1)", click)
        self.assertIn("return 0", click)
        self.assertIn("send next", _body(quiz, "gotoNextQuestionEx"))
        self.assertIn("send previous", _body(quiz, "gotoPreviousQuestionEx"))


def _body(source: str, name: str) -> str:
    found = next(item for item in book_handlers("book", source) if item.name.lower() == name.lower())
    lines = []
    for line in source[found.body_start:].splitlines():
        if lines and line and not line[0].isspace() and line.lower().startswith("to "):
            break
        lines.append(line)
    return "\n".join(lines)


if __name__ == "__main__":
    unittest.main()
