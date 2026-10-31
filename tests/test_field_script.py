"""``text of field "name"`` in a click: a write, then a read in a later condition."""

import os
import unittest
from pathlib import Path

from opentoolbook.click import field_write, run_handler, text_value

HANDLER = """to handle buttonClick
    text of field "Stem" = "Pick" && "one" & ":"
    if text of field "Stem" = "pick one:" then
        set text of field "A" to text of field "Stem" & " A"
    end if
    if text of field "Stem" <> "Pick one:" then
        go to page "P2"
    end if
end"""


class FieldScriptTests(unittest.TestCase):
    def test_a_write_then_a_read_in_a_later_condition(self):
        follow = run_handler(HANDLER, ("P1", "P2"), "P1", fields={"Stem": "old", "A": "a"})
        self.assertEqual(follow.page_id, "P1")
        self.assertEqual(follow.fields, (("Stem", "Pick one:"), ("A", "Pick one: A")))

    def test_the_read_uses_the_text_the_page_shows(self):
        source = 'if text of field "Stem" = "Ready" then\n  go to page "P2"\nend if'
        self.assertEqual(run_handler(source, ("P1", "P2"), "P1", fields={"stem": "ready"}).page_id, "P2")
        self.assertEqual(run_handler(source, ("P1", "P2"), "P1", fields={"stem": "other"}).page_id, "P1")

    def test_a_field_the_page_does_not_have_decides_nothing(self):
        source = 'if text of field "Nope" = "x" then\n  go to page "P2"\nelse\n  go to page "P1"\nend if'
        follow = run_handler(source, ("P1", "P2"), "P0", fields={})
        self.assertEqual(follow.page_id, "P0")

    def test_an_expression_the_reader_cannot_evaluate_is_not_written(self):
        self.assertIsNone(text_value("getFirst()", {}))
        follow = run_handler('text of field "A" = getFirst()', (), "P1", fields={"A": "a"})
        self.assertEqual(follow.fields, ())

    def test_both_spellings(self):
        self.assertEqual(field_write('set text of field "x" to "y"'), ("x", '"y"'))
        self.assertEqual(field_write('text of field "x" = "y"'), ("x", '"y"'))
        self.assertIsNone(field_write('text of field "x"'))


class FieldDisplayTests(unittest.TestCase):
    def test_the_display_list_shows_the_written_text(self):
        path = os.environ.get("OPENTOOLBOOK_TBK")
        if not path or not os.path.isfile(path):
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
        follow = run_handler(source, page_ids(data), "P10", fields=texts)
        self.assertEqual(follow.page_id, "P10")
        after = show_page(data, "P10", 800, 600, fields=dict(follow.fields))
        changed = field_texts(after)
        self.assertEqual(changed["Text"], "Changed by a click")
        self.assertEqual(changed["first"], texts["first"])
        runs = [item.runs for item in after.items if item.kind == "field" and item.name == "Text"][0]
        self.assertEqual(runs[0][0], 0)


class NavigatorFieldTests(unittest.TestCase):
    def test_the_window_keeps_the_written_text_until_the_page_changes(self):
        from unittest.mock import patch

        from opentoolbook import navigate
        from opentoolbook.click import Follow

        nav = navigate.Navigator.__new__(navigate.Navigator)
        nav.data, nav.pages, nav.page_id, nav.book, nav.home, nav.fields = b"", ("P1", "P2"), "P1", None, None, {}
        nav.lesson, nav.variables, nav._handlers, nav.sysbooks = None, {}, {}, ()
        nav.props, nav.letters = navigate.UserProperties(), {}
        nav.history = []
        wrote = Follow("P1", None, fields=(("Stem", "new"),))
        # These two clicks are on no stored page, so no quiz group runs setupQuizEx.
        quiet = patch.object(navigate, "quiz_setup_click")
        quiet.start()
        self.addCleanup(quiet.stop)
        with patch.object(navigate, "follow_click", return_value=wrote) as called:
            clicked = nav.click("Check", {"Stem": "old"})
        self.assertEqual(called.call_args.args[6], {"Stem": "old"})
        self.assertEqual((clicked.moved, clicked.changed), (False, True))
        self.assertEqual(nav.fields, {"Stem": "new"})
        with patch.object(navigate, "follow_click", return_value=Follow("P2", None)), patch.object(
            navigate.Navigator, "enter"
        ):
            clicked = nav.click("Next", {"Stem": "new"})
        self.assertTrue(clicked.moved)
        self.assertEqual(nav.fields, {})


if __name__ == "__main__":
    unittest.main()
