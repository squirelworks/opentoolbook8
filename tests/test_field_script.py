"""``text of field "name"`` in a click: a write, then a read in a later condition."""

import unittest
from pathlib import Path

from engine_run import run
from lesson import logic_families_path

HANDLER = """to handle buttonClick
    text of field "Stem" = "Pick" && "one" & ":"
    if text of field "Stem" = "pick one:" then
        set text of field "A" to text of field "Stem" & " A"
    end if
    if text of field "Stem" <> "Pick one:" then
        go to page "P2"
    end if
end"""


def _texts(follow):
    return tuple((name, value) for _owner, kind, name, prop, value in follow.writes if kind == "field" and prop == "text")


class FieldScriptTests(unittest.TestCase):
    def test_a_write_then_a_read_in_a_later_condition(self):
        follow = run(HANDLER, ("P1", "P2"), "P1", fields={"Stem": "old", "A": "a"})
        self.assertEqual(follow.page_id, "P1")
        self.assertEqual(_texts(follow), (("stem", "Pick one:"), ("a", "Pick one: A")))

    def test_the_read_uses_the_text_the_page_shows(self):
        source = 'if text of field "Stem" = "Ready" then\n  go to page "P2"\nend if'
        self.assertEqual(run(source, ("P1", "P2"), "P1", fields={"stem": "ready"}).page_id, "P2")
        self.assertEqual(run(source, ("P1", "P2"), "P1", fields={"stem": "other"}).page_id, "P1")


class FieldDisplayTests(unittest.TestCase):
    def test_the_display_list_shows_the_written_text(self):
        path = logic_families_path()
        if path is None:
            self.skipTest("set OPENTOOLBOOK_TBK to 9e954d01.tbk")
        from opentoolbook.field import page_ids
        from opentoolbook.show import field_texts, show_page

        data = Path(path).read_bytes()
        before = show_page(data, "P10", 800, 600)
        texts = field_texts(before)
        self.assertEqual(texts["Text"], "LOGIC FAMILIES")
        source = (
            'to handle buttonClick\n'
            '  if text of field "Text" = "logic families" then\n'
            '    text of field "Text" = "Changed by a click"\n'
            '  end if\nend'
        )
        follow = run(source, page_ids(data), "P10", data=data, fields=texts)
        self.assertEqual(follow.page_id, "P10")
        self.assertEqual(_texts(follow), (("text", "Changed by a click"),))
        after = show_page(data, "P10", 800, 600, fields={"Text": "Changed by a click"})
        changed = field_texts(after)
        self.assertEqual(changed["Text"], "Changed by a click")
        self.assertEqual(changed["first"], texts["first"])
        runs = [item.runs for item in after.items if item.kind == "field" and item.name == "Text"][0]
        self.assertEqual(runs[0][0], 0)


class NavigatorFieldTests(unittest.TestCase):
    def test_the_window_keeps_the_written_text_with_its_page(self):
        from unittest.mock import patch

        from opentoolbook import navigate
        from opentoolbook.click import Follow

        fixture = Path(__file__).parent / "fixtures" / "otb-line-rect.tbk"
        nav = navigate.Navigator(fixture.read_bytes(), "")
        wrote = Follow("", None, writes=(("", "field", "stem", "text", "new"),))
        with patch.object(navigate.Navigator, "_send", return_value=wrote) as called:
            clicked = nav.click("Check", {"Stem": "old"})
        self.assertEqual(called.call_args.args[2], {"Stem": "old"})
        self.assertEqual((clicked.moved, clicked.changed), (False, True))
        self.assertEqual(nav._overlay()[("field", "stem")], {"text": "new"})


if __name__ == "__main__":
    unittest.main()
