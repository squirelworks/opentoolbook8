"""``hide`` and ``show`` of a named object change the display list."""

import unittest
from pathlib import Path

from engine_run import run
from opentoolbook.show import show_page
from lesson import logic_families_path

FIXTURE = Path(__file__).parent / "fixtures" / "otb-line-rect.tbk"


def _visible(follow):
    return {(kind, name): value for _owner, kind, name, prop, value in follow.writes if prop == "visible"}


class HideShowTests(unittest.TestCase):
    def test_a_handler_hides_a_rectangle(self):
        data = FIXTURE.read_bytes()
        before = show_page(data, "", 800, 600)
        self.assertIn("rectangle", [item.kind for item in before.items])
        follow = run("to handle buttonClick\n  hide rectangle id 0\nend", ("",), "", data=data)
        hidden = show_page(data, "", 800, 600, visible=_visible(follow))
        self.assertEqual(hidden.items, tuple(item for item in before.items if item.kind != "rectangle"))
        follow = run("hide rectangle id 0\nshow rectangle id 0", ("",), "", data=data)
        self.assertEqual([write[4] for write in follow.writes], [False, True])
        shown = show_page(data, "", 800, 600, visible=_visible(follow))
        self.assertEqual(shown.items, before.items)

    def test_hiding_by_name_on_the_lesson(self):
        path = logic_families_path()
        if path is None:
            self.skipTest("set OPENTOOLBOOK_TBK to 9e954d01.tbk")
        data = path.read_bytes()
        before = show_page(data, "P300", 800, 600)
        self.assertIn("MenuFrame", [item.name for item in before.items])
        follow = run('hide button "menuframe"', ("P300",), "P300", data=data)
        after = show_page(data, "P300", 800, 600, visible=_visible(follow))
        self.assertNotIn("MenuFrame", [item.name for item in after.items])
        self.assertEqual(len(after.items), len(before.items) - 1)


class NavigatorHideTests(unittest.TestCase):
    def test_the_window_keeps_a_hidden_object_hidden_until_the_page_changes(self):
        from unittest.mock import patch

        from opentoolbook import navigate
        from opentoolbook.click import Follow

        nav = navigate.Navigator(FIXTURE.read_bytes(), "")
        hid = Follow("", None, writes=(("", "rectangle", 0, "visible", False),))
        with patch.object(navigate.Navigator, "_send", return_value=hid):
            clicked = nav.click("Hide")
        self.assertEqual((clicked.moved, clicked.changed), (False, True))
        listed = nav.display(800, 600)
        self.assertNotIn("rectangle", [item.kind for item in listed.items])


if __name__ == "__main__":
    unittest.main()
