"""Item 49: ``buttonDown`` and ``buttonUp`` handlers run on press and release."""

import unittest

from opentoolbook.click import run_handler
from opentoolbook.navigate import Navigator
from opentoolbook.script import handler_sites
from opentoolbook.show import object_at, show_page, unit_to_px

from lesson import SKIP, companion, lesson_path

PAGES = ("P1", "P2", "P3")


class FixtureTests(unittest.TestCase):
    def test_button_up_go_to_page_navigates(self):
        up = run_handler('to handle buttonUp\n\tgo to page "P3"\nend\n', PAGES, "P1")
        self.assertEqual(up.page_id, "P3")
        self.assertEqual(up.inverts, ())

    def test_button_down_only_sets_the_invert(self):
        source = 'to handle buttonDown\n\tif isObject(button "A") then\n\t\tset invert of button "A" to true\n\tend if\nend\n'
        down = run_handler(source, PAGES, "P1", objects=lambda kind, key: (kind, key) == ("button", "a"))
        self.assertEqual(down.page_id, "P1")
        self.assertEqual(down.inverts, (("A", True),))
        self.assertEqual((down.fields, down.visible, down.requests), ((), (), ()))

    def test_is_object_false_or_unknown_runs_nothing(self):
        source = 'to handle buttonUp\n\tif isObject(button "A") then\n\t\tset invert of button "A" to false\n\tend if\nend\n'
        self.assertEqual(run_handler(source, PAGES, "P1", objects=lambda kind, key: False).inverts, ())
        self.assertEqual(run_handler(source, PAGES, "P1").inverts, ())


@unittest.skipIf(lesson_path() is None, SKIP)
class LessonTests(unittest.TestCase):
    def setUp(self):
        self.path = lesson_path()
        self.data = self.path.read_bytes()

    def test_the_lesson_has_nineteen_of_each_and_the_system_books_none(self):
        self.assertEqual(len(handler_sites(self.data, "buttonDown")), 19)
        self.assertEqual(len(handler_sites(self.data, "buttonUp")), 19)
        self.assertTrue(all(place == "inline" for place, _owner, _name in handler_sites(self.data, "buttonUp")))
        for name in ("nc81base.sbk", "nc81recs.sbk", "nc81test.sbk", "nc81trnr.sbk"):
            book = companion(self.path, name)
            if not book.is_file():
                continue
            data = book.read_bytes()
            self.assertEqual(handler_sites(data, "buttonDown"), (), name)
            self.assertEqual(handler_sites(data, "buttonUp"), (), name)

    def _button(self, listed, name):
        return next(item for item in listed.items if item.kind == "button" and item.name == name)

    def test_press_on_the_selection_field_inverts_the_button_and_release_restores_it(self):
        nav = Navigator(self.data, "P300", self.path)
        listed = nav.display(800, 600)
        field = next(item for item in listed.items if item.kind == "field" and item.name == "Selection1")
        x = (unit_to_px(field.bounds[0], listed.scale) + unit_to_px(field.bounds[2], listed.scale)) / 2
        y = (unit_to_px(field.bounds[1], listed.scale) + unit_to_px(field.bounds[3], listed.scale)) / 2
        self.assertEqual(object_at(listed, x, y), ("field", "Selection1"))
        self.assertEqual(self._button(listed, "selection1").picture_role, "up")

        down = nav.message("field", "Selection1", "buttonDown")
        self.assertFalse(down.moved)
        self.assertTrue(down.changed)
        self.assertEqual(nav.page_id, "P300")
        held = nav.display(800, 600)
        self.assertEqual(self._button(held, "selection1").picture_role, "invert")
        self.assertEqual(self._button(held, "selection1").picture_id, 153)

        up = nav.message("field", "Selection1", "buttonUp")
        self.assertFalse(up.moved)
        self.assertEqual(self._button(nav.display(800, 600), "selection1").picture_role, "up")

    def test_an_object_with_no_handler_gets_none(self):
        nav = Navigator(self.data, "P300", self.path)
        self.assertIsNone(nav.message("button", "Next", "buttonDown"))
        self.assertIsNone(nav.message("field", "Selection1", "buttonDoubleClick"))

    def test_a_page_change_drops_the_invert(self):
        nav = Navigator(self.data, "P300", self.path)
        nav.message("field", "Selection1", "buttonDown")
        nav.click("Next")
        self.assertEqual(nav.inverted, {})


if __name__ == "__main__":
    unittest.main()
