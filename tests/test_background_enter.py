"""The background's enterPage writes the fields it names."""

import os
import unittest
from pathlib import Path

from opentoolbook.click import background_script
from opentoolbook.enter import _handler
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


class LessonTests(unittest.TestCase):
    def test_the_test_background_stores_testing_in_pagetext(self):
        if not LESSON or not os.path.isfile(LESSON):
            self.skipTest("set OPENTOOLBOOK_TBK to 9e954d01.tbk")
        data = Path(LESSON).read_bytes()
        script = background_script(data, "P10210")
        self.assertIn('set text of field "PageText" to name of this page', script)
        self.assertNotIn("enterbackground", script.lower())
        for page in ("P10210", "P10211"):
            listed = show_page(data, page, 400, 300)
            stored = {item.name: item.text or "" for item in listed.items if item.kind == "field"}
            self.assertEqual(stored["PageText"], "Testing")


if __name__ == "__main__":
    unittest.main()
