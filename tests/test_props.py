"""The ``__`` names live in memory for the process."""

import unittest
from pathlib import Path

from opentoolbook.entry import choose_opening
from opentoolbook.props import UserProperties
from lesson import logic_families_path

ENTER_APPLICATION = """
to handle enterApplication
    system __import, __studentFirst
    __import = false
    __studentFirst = "Ada"
    forward
end
"""

GET_FIRST = """
to get getFirst
    system string __studentFirst
    return __studentFirst
end
"""

PAGE = """
to handle enterPage
    system __import
    if __import = false then
        go to page "P2"
    end if
end
"""


class StoreTests(unittest.TestCase):
    def test_names_fold_case_and_only_double_underscore_names_are_kept(self):
        props = UserProperties()
        self.assertIsNone(props.get("__studentFirst"))
        props.set("__StudentFirst", "Ada")
        self.assertEqual(props.get("__studentfirst"), "Ada")
        self.assertIn("__STUDENTFIRST", props)
        with self.assertRaises(ValueError):
            props.set("nextpage", "P1")
        with self.assertRaises(ValueError):
            props.set("__", 1)

    def test_startup_writes_and_reads_the_store(self):
        props = UserProperties()
        handlers = {"enterApplication": ENTER_APPLICATION, "getFirst": GET_FIRST}
        page, book = choose_opening(("P1", "P2"), handlers, {"P1": PAGE}, props=props)
        self.assertEqual((page, book), ("P2", None))
        self.assertIs(props.get("__import"), False)
        self.assertEqual(props.get("__studentFirst"), "Ada")

    def test_an_unset_name_is_null_and_not_false(self):
        # A system name nobody assigned is null. Null is not false, so the branch does not run.
        props = UserProperties()
        page, _book = choose_opening(("P1", "P2"), {}, {"P1": PAGE}, props=props)
        self.assertEqual(page, "P1")
        props.set("__import", False)
        page, _book = choose_opening(("P1", "P2"), {}, {"P1": PAGE}, props=props)
        self.assertEqual(page, "P2")
        props.set("__import", True)
        page, _book = choose_opening(("P1", "P2"), {}, {"P1": PAGE}, props=props)
        self.assertEqual(page, "P1")


class GreetingTests(unittest.TestCase):
    def test_p10_greets_the_student_the_store_names(self):
        if logic_families_path() is None:
            self.skipTest("set OPENTOOLBOOK_TBK to 9e954d01.tbk")
        from opentoolbook.entry import opening_page
        from opentoolbook.navigate import Navigator

        path = logic_families_path()
        opened = opening_page(path)

        def first(name):
            props = type(opened.props)(dict(opened.props.items()))
            if name is not None:
                props.set("__studentFirst", name)
            nav = Navigator(path.read_bytes(), "P10", path, props=props, sysbooks=opened.sysbooks)
            nav.enter()
            shown = nav.display(400, 300)
            return next(item for item in shown.items if item.kind == "field" and item.name.lower() == "first")

        # With no NIDAREC.INI, startup leaves __studentFirst "Student".
        self.assertEqual(first(None).text, "Hello Student, this lesson is about:")
        named = first("Ada")
        self.assertEqual(named.text, "Hello Ada, this lesson is about:")
        self.assertEqual(named.runs, ((0, "Arial"),))


if __name__ == "__main__":
    unittest.main()
