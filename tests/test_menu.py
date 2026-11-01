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

    def test_p900_selection1_opens_the_ttl_section_menu(self):
        if logic_families_path() is None:
            self.skipTest("set OPENTOOLBOOK_TBK to 9e954d01.tbk")
        from opentoolbook.entry import opening_page
        from opentoolbook.navigate import Navigator

        path = logic_families_path()
        opened = opening_page(path)
        nav = Navigator(path.read_bytes(), "P900", path, props=opened.props, sysbooks=opened.sysbooks)
        self.assertTrue(nav.click("selection1").moved)
        self.assertEqual(nav.page_id, "P1001")
        self.assertEqual(nav.title(), "9e954d01.tbk - P1001")
        texts = {
            item.name: item.text
            for item in nav.display(800, 600).items
            if item.kind == "field"
        }
        self.assertEqual(texts.get("menutext"), "TTL INTEGRATED CIRCUITS")
        self.assertEqual(texts.get("Page#"), "P1001")

    def test_p900_selection2_opens_the_other_ics_section_menu(self):
        if logic_families_path() is None:
            self.skipTest("set OPENTOOLBOOK_TBK to 9e954d01.tbk")
        from opentoolbook.entry import opening_page
        from opentoolbook.navigate import Navigator

        path = logic_families_path()
        opened = opening_page(path)
        nav = Navigator(path.read_bytes(), "P900", path, props=opened.props, sysbooks=opened.sysbooks)
        self.assertTrue(nav.click("selection2").moved)
        self.assertEqual(nav.page_id, "P2001")
        self.assertEqual(nav.title(), "9e954d01.tbk - P2001")
        texts = {
            item.name: item.text
            for item in nav.display(800, 600).items
            if item.kind == "field"
        }
        self.assertEqual(texts.get("menutext"), "OTHER INTEGRATED CIRCUITS")
        self.assertEqual(texts.get("Page#"), "P2001")

    def test_ttl_discussion_next_and_back(self):
        if logic_families_path() is None:
            self.skipTest("set OPENTOOLBOOK_TBK to 9e954d01.tbk")
        from opentoolbook.entry import opening_page
        from opentoolbook.navigate import Navigator

        path = logic_families_path()
        opened = opening_page(path)
        nav = Navigator(path.read_bytes(), "P900", path, props=opened.props, sysbooks=opened.sysbooks)
        self.assertTrue(nav.click("selection1").moved)
        self.assertEqual(nav.page_id, "P1001")
        self.assertTrue(nav.click("selection1").moved)
        self.assertEqual(nav.page_id, "P1040")
        self.assertEqual(nav.title(), "9e954d01.tbk - P1040")
        texts = {
            item.name: item.text
            for item in nav.display(800, 600).items
            if item.kind == "field"
        }
        self.assertEqual(texts.get("Page#"), "P1040")
        for page_id in ("P1050", "P1060", "P1070"):
            self.assertTrue(nav.click("Next").moved)
            self.assertEqual(nav.page_id, page_id)
            self.assertEqual(nav.title(), f"9e954d01.tbk - {page_id}")
        self.assertTrue(nav.click("Back").moved)
        self.assertEqual(nav.page_id, "P1040")
        self.assertEqual(nav.title(), "9e954d01.tbk - P1040")

    def test_ttl_summary_opens_p1920_and_next_back(self):
        if logic_families_path() is None:
            self.skipTest("set OPENTOOLBOOK_TBK to 9e954d01.tbk")
        from opentoolbook.entry import opening_page
        from opentoolbook.navigate import Navigator

        path = logic_families_path()
        opened = opening_page(path)
        nav = Navigator(path.read_bytes(), "P900", path, props=opened.props, sysbooks=opened.sysbooks)
        self.assertTrue(nav.click("selection1").moved)
        self.assertEqual(nav.page_id, "P1001")
        self.assertTrue(nav.click("selection2").moved)
        self.assertEqual(nav.page_id, "P1920")
        self.assertEqual(nav.title(), "9e954d01.tbk - P1920")
        texts = {
            item.name: item.text
            for item in nav.display(800, 600).items
            if item.kind == "field"
        }
        self.assertEqual(texts.get(""), "SUMMARY")
        self.assertEqual(texts.get("Page#"), "P1920")
        self.assertTrue(nav.click("Next").moved)
        self.assertEqual(nav.page_id, "P1930")
        self.assertTrue(nav.click("Back").moved)
        self.assertEqual(nav.page_id, "P1920")

    def test_other_ics_summary_opens_p2920_and_next_back(self):
        if logic_families_path() is None:
            self.skipTest("set OPENTOOLBOOK_TBK to 9e954d01.tbk")
        from opentoolbook.entry import opening_page
        from opentoolbook.navigate import Navigator

        path = logic_families_path()
        opened = opening_page(path)
        nav = Navigator(path.read_bytes(), "P900", path, props=opened.props, sysbooks=opened.sysbooks)
        self.assertTrue(nav.click("selection2").moved)
        self.assertEqual(nav.page_id, "P2001")
        self.assertTrue(nav.click("selection2").moved)
        self.assertEqual(nav.page_id, "P2920")
        self.assertEqual(nav.title(), "9e954d01.tbk - P2920")
        texts = {
            item.name: item.text
            for item in nav.display(800, 600).items
            if item.kind == "field"
        }
        self.assertEqual(texts.get(""), "SUMMARY")
        self.assertEqual(texts.get("Page#"), "P2920")
        self.assertTrue(nav.click("Next").moved)
        self.assertEqual(nav.page_id, "P2930")
        self.assertTrue(nav.click("Back").moved)
        self.assertEqual(nav.page_id, "P2920")

    def test_section_help_opens_nida81_then_next_returns(self):
        if logic_families_path() is None:
            self.skipTest("set OPENTOOLBOOK_TBK to 9e954d01.tbk")
        from opentoolbook.entry import opening_page
        from opentoolbook.navigate import Navigator

        path = logic_families_path()
        opened = opening_page(path)
        nav = Navigator(path.read_bytes(), "P900", path, props=opened.props, sysbooks=opened.sysbooks)
        self.assertTrue(nav.click("selection1").moved)
        self.assertEqual(nav.page_id, "P1001")
        self.assertTrue(nav.click("Help").moved)
        self.assertEqual(nav.page_id, "P20001")
        self.assertEqual(nav.book_name, "nida81.tbk")
        self.assertEqual(nav.title(), "nida81.tbk - P20001")
        texts = {
            item.name: item.text
            for item in nav.display(800, 600).items
            if item.kind == "field"
        }
        self.assertEqual(texts.get(""), "HELP")
        self.assertEqual(texts.get("Page#"), "P20001")
        self.assertTrue(nav.click("Next").moved)
        self.assertEqual(nav.page_id, "P1001")
        self.assertEqual(nav.book_name, "9e954d01.tbk")
        self.assertEqual(nav.title(), "9e954d01.tbk - P1001")


if __name__ == "__main__":
    unittest.main()
