"""``name of this page`` is the page id. ``name of this book`` is the file name."""

import os
import unittest
from pathlib import Path

from opentoolbook.entry import choose_opening
from opentoolbook.walk import this_name


class ThisNameTests(unittest.TestCase):
    def test_the_two_expressions(self):
        self.assertEqual(this_name("name of this page", "P300", "9e954d01.tbk"), "P300")
        self.assertEqual(this_name("Name  of This Book", "P300", "9e954d01.tbk"), "9e954d01.tbk")
        self.assertIsNone(this_name("name of this background", "P300", "9e954d01.tbk"))

    def test_a_startup_handler_returns_them(self):
        handlers = {
            "thisbook": "to get thisBook\n  return name of this book\nend\n",
            "thispage": "to get thisPage\n  return name of this page\nend\n",
        }
        scripts = {"P0": 'to handle enterPage\n  go to page "P1" of book thisBook()\nend\n'}
        self.assertEqual(
            choose_opening(("P0", "P1"), handlers, scripts, book_name="lesson.tbk"),
            ("P1", None),
        )
        scripts = {"P0": 'to handle enterPage\n  go to page "P1" of book thisPage()\nend\n'}
        self.assertEqual(
            choose_opening(("P0", "P1"), handlers, scripts, book_name="lesson.tbk"),
            ("P1", "P0"),
        )

    def test_page_number_on_p300_is_still_p300(self):
        path = os.environ.get("OPENTOOLBOOK_TBK")
        if not path or not os.path.isfile(path):
            self.skipTest("set OPENTOOLBOOK_TBK to 9e954d01.tbk")
        from opentoolbook.enter import _book_enter
        from opentoolbook.navigate import Navigator

        data = Path(path).read_bytes()
        self.assertIn("to name of this page", _book_enter(data))
        nav = Navigator(data, "P300", Path(path))
        nav.enter()
        listed = nav.display(800, 600)
        texts = {item.name.lower(): item.text for item in listed.items if item.kind == "field"}
        self.assertEqual(texts["page#"], "P300")


if __name__ == "__main__":
    unittest.main()
