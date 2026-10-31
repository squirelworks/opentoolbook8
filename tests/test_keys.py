"""Right and Left press the page's Next and Back buttons."""

import unittest
from pathlib import Path

from opentoolbook.navigate import Navigator
from opentoolbook.show import Paint, key_button, press_key, show_page

from lesson import companion, logic_families_path

FIXTURE = Path(__file__).parent / "fixtures" / "otb-line-rect.tbk"


def _lesson():
    return logic_families_path()


class KeyButtonTests(unittest.TestCase):
    def test_a_page_without_next_or_back_ignores_the_keys(self):
        data = FIXTURE.read_bytes()
        listed = show_page(data, "", 600, 400)
        nav = Navigator(data, "", FIXTURE)
        for key in ("Right", "Left", "Up", "space"):
            self.assertIsNone(key_button(listed, key))
            self.assertIsNone(press_key(nav, listed, key))
        self.assertEqual(nav.page_id, "")

    def test_the_key_names_the_button_as_the_page_spells_it(self):
        from dataclasses import replace

        listed = show_page(FIXTURE.read_bytes(), "", 600, 400)
        buttons = (Paint("button", 1, "NEXT"), Paint("field", 2, "Back"), Paint("button", 3, "back"))
        listed = replace(listed, items=listed.items + buttons)
        self.assertEqual(key_button(listed, "Right"), "NEXT")
        # A field named Back is not a button.
        self.assertEqual(key_button(listed, "Left"), "back")


class LessonKeyTests(unittest.TestCase):
    def test_right_and_left_on_p300(self):
        path = _lesson()
        if path is None:
            self.skipTest("set OPENTOOLBOOK_TBK to 9e954d01.tbk")
        data = path.read_bytes()
        right = Navigator(data, "P300", path)
        listed = right.display(624, 442)
        self.assertEqual(key_button(listed, "Right"), "Next")
        self.assertTrue(press_key(right, listed, "Right").moved)
        self.assertEqual(right.page_id, "P400")
        left = Navigator(data, "P300", path)
        self.assertEqual(key_button(listed, "Left"), "Back")
        self.assertTrue(press_key(left, left.display(624, 442), "Left").moved)
        self.assertEqual(left.page_id, "P100")
        # The key and the button are the same path.
        clicked = Navigator(data, "P300", path)
        clicked.click("Next")
        self.assertEqual(clicked.page_id, right.page_id)

    def test_right_on_a_quiz_page_is_the_background_next(self):
        path = _lesson()
        if path is None:
            self.skipTest("set OPENTOOLBOOK_TBK to 9e954d01.tbk")
        from unittest.mock import patch

        from opentoolbook.entry import opening_page
        from opentoolbook.openscript import interp

        opened = opening_page(path)
        nav = Navigator(path.read_bytes(), "P10002", path, props=opened.props, sysbooks=opened.sysbooks)
        fixed = patch.object(interp._random, "randint", lambda low, high: low)
        fixed.start()
        self.addCleanup(fixed.stop)
        # The pre-test opens question 110 on P10210. Pass 1 disables the
        # background's Next, so Right is Next and does nothing there.
        nav.click("selection1")
        self.assertEqual(nav.page_id, "P10210")
        listed = nav.display(624, 442)
        self.assertEqual(key_button(listed, "Right"), "Next")
        self.assertFalse(press_key(nav, listed, "Right").moved)
        self.assertEqual(nav.page_id, "P10210")

if __name__ == "__main__":
    unittest.main()


class BookKeyTests(unittest.TestCase):
    SCRIPT = (
        "to handle enterSystem\n"
        "end\n"
        "to handle keyup key\n"
        "\tconditions\n"
        "\t\twhen key = keyf2\n"
        '\t\t\trequest "Exit?" with "&Yes" or "&No"\n'
        "\t\twhen key = keyEnter\n"
        '\t\t\tif  isObject(button("Next"))  then\n'
        '\t\t\t\tsend buttonClick to button "next"\n'
        "\t\t\tend if\n"
        "\telse\n"
        "\t\tforward\n"
        "\tend conditions\n"
        "end\n"
    )

    def test_the_branch_names_the_button_it_sends_buttonclick(self):
        from opentoolbook.keys import branch_for, key_up

        body = key_up(self.SCRIPT)
        self.assertIsNotNone(body)
        self.assertEqual(
            branch_for(body, "keyenter"),
            ('if isobject(button("next")) then', 'send buttonclick to button "next"', "end if"),
        )
        self.assertEqual(branch_for(body, "keyf2"), ('request "exit?" with "&yes" or "&no"',))
        self.assertIsNone(branch_for(body, "keyf3"))
        self.assertIsNone(key_up("to handle enterPage\nend\n"))
        self.assertEqual(key_up("to handle keyUp\nend\n"), [])

    def test_enter_on_p300_is_the_book_keyup_next(self):
        from opentoolbook.keys import key_handler

        path = _lesson()
        if path is None:
            self.skipTest("set OPENTOOLBOOK_TBK to 9e954d01.tbk")
        data = path.read_bytes()
        handler = key_handler(data, "P300", "Return")
        self.assertEqual((handler.owner, handler.resource_id, handler.button), ("book", 376, "next"))
        nav = Navigator(data, "P300", path)
        self.assertTrue(press_key(nav, nav.display(624, 442), "Return").moved)
        self.assertEqual(nav.page_id, "P400")
        # F1, F2, F4, F5 to F9, F11, and F12 are quoted, and their branches do not send a click.
        for key in ("F1", "F2", "F4", "F5", "F6", "F7", "F8", "F9", "F11", "F12"):
            quoted = key_handler(data, "P300", key)
            self.assertIsNotNone(quoted, key)
            self.assertIsNone(quoted.button, key)
            stay = Navigator(data, "P300", path)
            self.assertIsNone(press_key(stay, stay.display(624, 442), key), key)
            self.assertEqual(stay.page_id, "P300")
        self.assertIsNone(key_handler(data, "P300", "F10"))
        self.assertIsNone(key_handler(data, "P300", "F3"))

    def test_a_page_with_its_own_empty_keyup_keeps_enter(self):
        from opentoolbook.keys import key_handler, page_script_id

        path = _lesson()
        if path is None:
            self.skipTest("set OPENTOOLBOOK_TBK to 9e954d01.tbk")
        data = path.read_bytes()
        self.assertEqual(page_script_id(data, "P10301"), 373)
        self.assertEqual(page_script_id(data, "P10302"), 374)
        self.assertIsNone(page_script_id(data, "P300"))
        handler = key_handler(data, "P10301", "Return")
        self.assertEqual((handler.owner, handler.resource_id, handler.branch, handler.button), ("P10301", 373, (), None))
        nav = Navigator(data, "P10301", path)
        self.assertIsNone(press_key(nav, nav.display(624, 442), "Return"))
        self.assertEqual(nav.page_id, "P10301")

    def test_nida81_enter_is_its_own_book_keyup(self):
        from opentoolbook.keys import key_handler

        path = _lesson()
        if path is None:
            self.skipTest("set OPENTOOLBOOK_TBK to 9e954d01.tbk")
        nida = companion(path, "nida81.tbk")
        if not nida.is_file():
            self.skipTest("nida81.tbk is not beside the lesson")
        data = nida.read_bytes()
        handler = key_handler(data, "P310", "Return")
        self.assertEqual((handler.owner, handler.resource_id, handler.button), ("book", 165, "next"))
