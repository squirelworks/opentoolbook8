"""Item 48: a quiz click runs shared script 103's ``buttonClick``, then ``handleQuizClick``."""

import unittest
from pathlib import Path

from opentoolbook.navigate import Navigator
from opentoolbook.props import UserProperties
from opentoolbook.script import shared_scripts
from lesson import logic_families_path


def _lesson():
    return logic_families_path()


@unittest.skipIf(_lesson() is None, "set OPENTOOLBOOK_TBK to the lesson book")
class SharedScriptClickTests(unittest.TestCase):
    def setUp(self):
        self.path = _lesson()
        self.data = self.path.read_bytes()

    def _nav(self, props):
        from opentoolbook.entry import opening_page

        sysbooks = opening_page(self.path).sysbooks
        return Navigator(self.data, "P10210", self.path, props=props, sysbooks=sysbooks)

    def test_script_103_button_click_is_one_get_line(self):
        source = next(item.source for item in shared_scripts(self.data) if item.resource_id == 103)
        start = source.lower().index("to handle buttonclick")
        body = source[start:].split("\n", 1)[1]
        end = body.lower().index("\nend")
        self.assertEqual([line.strip() for line in body[:end].splitlines() if line.strip()], ["get handleQuizClick(target)"])

    def test_the_click_reads_handle_quiz_click_from_the_test_book(self):
        nav = self._nav(UserProperties())
        self.assertIn('__quizPass is in "1,2"', nav.handlers()["handlequizclick"])


if __name__ == "__main__":
    unittest.main()
