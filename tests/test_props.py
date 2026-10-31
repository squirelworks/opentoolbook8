"""The ``__`` names live in memory for the process."""

import os
import unittest
from pathlib import Path

from opentoolbook.entry import choose_opening
from opentoolbook.props import UserProperties
from opentoolbook.show import show_page

LESSON = os.environ.get("OPENTOOLBOOK_TBK")

ENTER_APPLICATION = """
to handle enterApplication
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

    def test_an_unset_name_is_false_in_a_condition(self):
        props = UserProperties()
        page, _book = choose_opening(("P1", "P2"), {}, {"P1": PAGE}, props=props)
        self.assertEqual(page, "P2")
        props.set("__import", True)
        page, _book = choose_opening(("P1", "P2"), {}, {"P1": PAGE}, props=props)
        self.assertEqual(page, "P1")


class GreetingTests(unittest.TestCase):
    def test_p10_greets_the_student_the_store_names(self):
        if not LESSON or not os.path.isfile(LESSON):
            self.skipTest("set OPENTOOLBOOK_TBK to 9e954d01.tbk")
        data = Path(LESSON).read_bytes()

        def first(props):
            shown = show_page(data, "P10", 400, 300, props)
            return next(item for item in shown.items if item.kind == "field" and item.name.lower() == "first")

        props = UserProperties()
        self.assertEqual(first(props).text, "Hello Student, this lesson is about:")
        props.set("__studentFirst", "")
        self.assertEqual(first(props).text, "Hello Student, this lesson is about:")
        props.set("__studentFirst", "Ada")
        named = first(props)
        self.assertEqual(named.text, "Hello Ada, this lesson is about:")
        self.assertEqual(named.runs, ((0, "Arial"),))
        self.assertEqual(first(None).text, "Hello Student, this lesson is about:")


if __name__ == "__main__":
    unittest.main()
