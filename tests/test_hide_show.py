"""``hide`` and ``show`` of a named object change the display list."""

import os
import unittest
from pathlib import Path

from opentoolbook.click import run_handler, visibility
from opentoolbook.show import show_page

FIXTURE = Path(__file__).parent / "fixtures" / "otb-line-rect.tbk"


class HideShowTests(unittest.TestCase):
    def test_the_statements(self):
        self.assertEqual(visibility('hide field "Correct"'), (("field", "correct"), False))
        self.assertEqual(visibility("show rectangle id 0"), (("rectangle", 0), True))
        self.assertEqual(visibility('set visible of button "OK" to false'), (("button", "ok"), False))
        self.assertIsNone(visibility('hide menubar'))

    def test_a_handler_hides_a_rectangle(self):
        data = FIXTURE.read_bytes()
        before = show_page(data, "", 800, 600)
        self.assertEqual([item.kind for item in before.items], ["background", "rectangle"])
        follow = run_handler("to handle buttonClick\n  hide rectangle id 0\nend", (), "")
        hidden = show_page(data, "", 800, 600, visible=dict(follow.visible))
        self.assertEqual([item.kind for item in hidden.items], ["background"])
        follow = run_handler("hide rectangle id 0\nshow rectangle id 0", (), "")
        self.assertEqual(follow.visible, ((("rectangle", 0), False), (("rectangle", 0), True)))
        shown = show_page(data, "", 800, 600, visible=dict(follow.visible))
        self.assertEqual(shown.items, before.items)

    def test_hiding_by_name_on_the_lesson(self):
        path = os.environ.get("OPENTOOLBOOK_TBK")
        if not path or not os.path.isfile(path):
            self.skipTest("set OPENTOOLBOOK_TBK to 9e954d01.tbk")
        data = Path(path).read_bytes()
        before = show_page(data, "P300", 800, 600)
        self.assertIn("MenuFrame", [item.name for item in before.items])
        follow = run_handler('hide button "menuframe"', (), "P300")
        after = show_page(data, "P300", 800, 600, visible=dict(follow.visible))
        self.assertNotIn("MenuFrame", [item.name for item in after.items])
        self.assertEqual(len(after.items), len(before.items) - 1)
        unfilled = [item for item in before.items if item.pattern == 253]
        follow = run_handler(
            "\n".join(f"show {item.kind} id {item.object_id}" for item in unfilled), (), "P300"
        )
        again = show_page(data, "P300", 800, 600, visible=dict(follow.visible))
        self.assertEqual([item for item in again.items if item.pattern == 253], unfilled)


if __name__ == "__main__":
    unittest.main()
