"""A lesson Menu button calls gotoMenuPage, and that names a quoted page."""

import unittest
from pathlib import Path
from lesson import logic_families_path


class LessonTests(unittest.TestCase):
    def test_the_window_navigator_follows_menu_on_p450(self):
        if logic_families_path() is None:
            self.skipTest("set OPENTOOLBOOK_TBK to 9e954d01.tbk")
        from opentoolbook.navigate import Navigator

        path = logic_families_path()
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
