"""A lesson Menu button calls gotoMenuPage, and that names a quoted page."""

import os
import unittest
from pathlib import Path

from opentoolbook.click import follow_click, run_handler
from opentoolbook.menu import get_menu_page, goto_menu_page
from opentoolbook.props import UserProperties

LESSON = os.environ.get("OPENTOOLBOOK_TBK")

GET_MENU = """to get getMenuPage
	system int __lessonMode
	system int __quizAssessment
	local string menupage
	--menupage = "P901"
	menupage = "P900"
	__quizDisableMenuKey = 0
	conditions
		when __lessonMode = 0
			if  __quizAssessment = 0  then
				__quizDisableMenuKey = 1
				menupage = "P10001"
			end if
		when __lessonMode = 1
			menupage = "P10002"
	end
	if  not isObject(page menupage)  then
		menupage = "P900"
	end if
	return menupage
end
"""

GOTO_MENU = """to get gotoMenuPage
	system int __lessonMode
	menupage = getMenuPage()
	get setupMenuPage(menupage, __lessonMode)
	go to page(menupage)
	return 0
end
"""

PAGES = ("P450", "P900", "P10001", "P10002")


class MenuTests(unittest.TestCase):
    def test_only_the_branch_for_the_stored_lesson_mode_runs(self):
        props = UserProperties()
        self.assertEqual(get_menu_page(GET_MENU, PAGES, props), "P10001")
        self.assertEqual(props.get("__quizDisableMenuKey"), 1)
        props = UserProperties({"__lessonMode": 1})
        self.assertEqual(get_menu_page(GET_MENU, PAGES, props), "P10002")
        self.assertEqual(props.get("__quizDisableMenuKey"), 0)
        props = UserProperties({"__quizAssessment": 1})
        self.assertEqual(get_menu_page(GET_MENU, PAGES, props), "P900")
        self.assertEqual(get_menu_page(GET_MENU, ("P450", "P900"), UserProperties()), "P900")

    def test_a_menu_click_opens_the_page_go_to_menu_page_names(self):
        handlers = {"gotomenupage": GOTO_MENU, "getmenupage": GET_MENU}
        props = UserProperties()

        def call(name):
            return goto_menu_page(handlers, PAGES, props) if name == "gotomenupage" else None

        followed = run_handler("to handle buttonClick\n\tget gotoMenuPage()\nend\n", PAGES, "P450", call=call)
        self.assertEqual((followed.page_id, followed.book), ("P10001", None))
        stayed = run_handler("get gotoMenuPage()\n", PAGES, "P450")
        self.assertEqual(stayed.page_id, "P450")
        self.assertIsNone(goto_menu_page({"getmenupage": GET_MENU}, PAGES, props))


class LessonTests(unittest.TestCase):
    def test_menu_on_p450_opens_p10001_with_the_mode_startup_left(self):
        if not LESSON or not os.path.isfile(LESSON):
            self.skipTest("set OPENTOOLBOOK_TBK to 9e954d01.tbk")
        from opentoolbook.entry import _handler_map
        from opentoolbook.field import page_ids

        path = Path(LESSON)
        data = path.read_bytes()
        handlers = _handler_map(path.with_name("nc81base.sbk").read_bytes())
        self.assertIn("go to page(menupage)", handlers["gotomenupage"])
        pages = page_ids(data)
        props = UserProperties()
        self.assertIsNone(props.get("__lessonMode"))

        def call(name):
            return goto_menu_page(handlers, pages, props) if name == "gotomenupage" else None

        followed = follow_click(data, "P450", "Menu", pages, call=call)
        self.assertEqual((followed.page_id, followed.book), ("P10001", None))
        self.assertEqual(props.get("__quizDisableMenuKey"), 1)

    def test_the_window_navigator_follows_menu_on_p450(self):
        if not LESSON or not os.path.isfile(LESSON):
            self.skipTest("set OPENTOOLBOOK_TBK to 9e954d01.tbk")
        from opentoolbook.navigate import Navigator

        path = Path(LESSON)
        nav = Navigator(path.read_bytes(), "P450", path)
        self.assertTrue(nav.click("Menu").moved)
        self.assertEqual(nav.page_id, "P10001")
        self.assertEqual(nav.props.get("__quizDisableMenuKey"), 1)


if __name__ == "__main__":
    unittest.main()
