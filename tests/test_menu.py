"""A lesson Menu button calls gotoMenuPage, and that names a quoted page."""

import os
import unittest
from pathlib import Path

LESSON = os.environ.get("OPENTOOLBOOK_TBK")


class LessonTests(unittest.TestCase):
    def test_the_window_navigator_follows_menu_on_p450(self):
        if not LESSON or not os.path.isfile(LESSON):
            self.skipTest("set OPENTOOLBOOK_TBK to 9e954d01.tbk")
        from opentoolbook.navigate import Navigator

        path = Path(LESSON)
        from opentoolbook.entry import opening_page

        opened = opening_page(path)
        # Startup leaves __lessonMode 2, so getMenuPage keeps "P900".
        nav = Navigator(path.read_bytes(), "P450", path, props=opened.props, sysbooks=opened.sysbooks)
        self.assertTrue(nav.click("Menu").moved)
        self.assertEqual(nav.page_id, "P900")
        self.assertEqual(nav.props.get("__quizDisableMenuKey"), 0)
        # In mode 0 with no assessment, the quiz menu page opens and the menu key is off.
        nav = Navigator(path.read_bytes(), "P450", path, props=opened.props, sysbooks=opened.sysbooks)
        nav.props.set("__lessonMode", 0)
        self.assertTrue(nav.click("Menu").moved)
        self.assertEqual(nav.page_id, "P10001")
        self.assertEqual(nav.props.get("__quizDisableMenuKey"), 1)

if __name__ == "__main__":
    unittest.main()
