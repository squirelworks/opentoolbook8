"""The background's enterPage writes the fields it names."""

import os
import unittest
from pathlib import Path

from opentoolbook.click import background_script
from opentoolbook.enter import _branch, _handler, enter_fields
from opentoolbook.show import show_page

LESSON = os.environ.get("OPENTOOLBOOK_TBK")

SCRIPT = """to handle enterBackground
    set text of field "A" to "one"
end

to handle enterPage
    set text of field "B" to name of this page
    forward
end
"""


class HandlerTests(unittest.TestCase):
    def test_each_message_is_its_own_block(self):
        self.assertIn('field "A"', _handler(SCRIPT, "enterbackground"))
        self.assertNotIn('field "B"', _handler(SCRIPT, "enterbackground"))
        self.assertIn('field "B"', _handler(SCRIPT, "enterpage"))
        self.assertEqual(_handler(SCRIPT, "leavepage"), "")

    def test_author_is_the_branch_a_reader_skips(self):
        self.assertEqual(_branch("syslevel = author", True, (), ["t"], ["s"]), ["s"])
        self.assertEqual(_branch("syslevel = author", False, (), ["t"], ["s"]), ["t"])
        self.assertEqual(_branch('syslevel = "reader"', True, (), ["t"], ["s"]), ["t"])


class LessonTests(unittest.TestCase):
    def test_the_test_background_names_the_page_in_pagetext_for_an_author(self):
        if not LESSON or not os.path.isfile(LESSON):
            self.skipTest("set OPENTOOLBOOK_TBK to 9e954d01.tbk")
        data = Path(LESSON).read_bytes()
        script = background_script(data, "P10210")
        self.assertIn('set text of field "PageText" to name of this page', script)
        self.assertNotIn("enterbackground", script.lower())
        for page in ("P10210", "P10211"):
            listed = show_page(data, page, 400, 300)
            fields = tuple((item.name, item.text or "", item.runs) for item in listed.items if item.kind == "field")
            stored = dict((name, text) for name, text, _runs in fields)
            self.assertEqual(stored["PageText"], "Testing")
            author = dict((name, text) for name, text, _runs in enter_fields(data, page, fields, sys_level="author"))
            self.assertEqual(author["PageText"], page)
            self.assertEqual(author["Stem"], stored["Stem"])
            shown = show_page(data, page, 400, 300, sys_level="author")
            page_text = [item.text for item in shown.items if item.kind == "field" and item.name == "PageText"]
            self.assertEqual(page_text, [page])


if __name__ == "__main__":
    unittest.main()
