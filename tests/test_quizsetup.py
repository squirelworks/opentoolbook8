"""The quiz menu groups call setupQuizEx, and its assignments land in the store."""

import os
import unittest
from pathlib import Path

from opentoolbook.props import UserProperties
from opentoolbook.quizsetup import selection_setup, setup_quiz_ex

LESSON = os.environ.get("OPENTOOLBOOK_TBK")

SETUP = """to get setupQuizEx string qType, int objectiveCount, string page1, string page2, string page3
	system int __quizType
	system int __quizPass
	local int error
	error = 0
	__quizStartPage = pageNumber of this page
	__quizPages[1] = page1
	__quizPages[2] = page2
	__quizPages[3] = page3
	qType = uppercase(qType)
	__quizType = 3
	conditions
		when qType = "ASSESSMENT"
			__quizType = 0
		when qType = "PRE-TEST"
			__quizType = 1
	end conditions
	__quizObjectiveCount = objectiveCount
	step i from 1 to 100
		__quizNumbers[i] = 0
	end step
	__quizIndex = 1
	__quizPass = 1
	increment(__quizAttempts)
	if  __quizMaxAttempts <> 0  then
		if  __quizAttempts > __quizMaxAttempts  then
			error = 1
			return error
		end if
	end if
	if  __quizTimed = 1  then
		linkDLL32 "kernel32.dll"
			LONG GetTickCount()
		end linkDLL32
		__quizStart = GetTickCount()
	end if
	return error
end setupQuizEx
"""

CLICK = """to handle buttonClick
	local int error
	system int __quizHelp
	if  __quizHelp = 1  then
		request "You are already in the quiz review!"
		break
	end if
	error = setupQuizEx("Pre-Test", 2, "P10301", "P10302", "P10303")
	get clearpool()
end buttonClick
"""


class SetupTests(unittest.TestCase):
    def test_the_arguments_and_the_pass_land_in_the_store(self):
        props = UserProperties()
        self.assertEqual(selection_setup(CLICK, SETUP, props, 101), 0)
        self.assertEqual(props.get("__quizPages"), {1: "P10301", 2: "P10302", 3: "P10303"})
        self.assertEqual(props.get("__quizPass"), 1)
        self.assertEqual(props.get("__quizType"), 1)
        self.assertEqual(props.get("__quizObjectiveCount"), 2)
        self.assertEqual(props.get("__quizStartPage"), 101)
        self.assertEqual(props.get("__quizAttempts"), 1)
        self.assertIsNone(props.get("__quizNumbers"))
        self.assertIsNone(props.get("__quizStart"))

    def test_too_many_attempts_is_error_1_and_quiz_help_breaks_first(self):
        props = UserProperties({"__quizMaxAttempts": 1, "__quizAttempts": 1})
        self.assertEqual(setup_quiz_ex(SETUP, ["Quiz", 2, "A", "B", "C"], props, 1), 1)
        self.assertEqual(props.get("__quizAttempts"), 2)
        self.assertEqual(props.get("__quizType"), 3)
        helped = UserProperties({"__quizHelp": 1})
        self.assertIsNone(selection_setup(CLICK, SETUP, helped, 101))
        self.assertIsNone(helped.get("__quizPass"))
        self.assertIsNone(selection_setup("get clearpool()\n", SETUP, UserProperties(), 1))


class LessonTests(unittest.TestCase):
    def test_each_selection1_group_stores_its_type_pages_and_pass(self):
        if not LESSON or not os.path.isfile(LESSON):
            self.skipTest("set OPENTOOLBOOK_TBK to 9e954d01.tbk")
        from opentoolbook.click import follow_click, quiz_setup_click
        from opentoolbook.entry import _handler_map
        from opentoolbook.field import page_ids

        path = Path(LESSON)
        data = path.read_bytes()
        handlers = _handler_map(path.with_name("nc81test.sbk").read_bytes())
        pages = page_ids(data)
        for page, kind in (("P10001", 0), ("P10002", 1), ("P10003", 2), ("P10004", 3)):
            props = UserProperties()
            self.assertEqual(quiz_setup_click(data, page, "selection1", pages, handlers, props), 0)
            self.assertEqual(props.get("__quizPages"), {1: "P10301", 2: "P10302", 3: "P10303"})
            self.assertEqual(props.get("__quizPass"), 1)
            self.assertEqual(props.get("__quizType"), kind)
            self.assertEqual(props.get("__quizObjectiveCount"), 2)
            self.assertEqual(follow_click(data, page, "selection1", pages).page_id, page)

    def test_the_window_navigator_runs_the_setup_on_click(self):
        if not LESSON or not os.path.isfile(LESSON):
            self.skipTest("set OPENTOOLBOOK_TBK to 9e954d01.tbk")
        from opentoolbook.navigate import Navigator

        path = Path(LESSON)
        from opentoolbook.entry import opening_page

        nav = Navigator(path.read_bytes(), "P10002", path, sysbooks=opening_page(path).sysbooks)
        self.assertFalse(nav.click("selection1").moved)
        self.assertEqual(nav.page_id, "P10002")
        self.assertEqual(nav.props.get("__quizPages"), {1: "P10301", 2: "P10302", 3: "P10303"})
        self.assertEqual(nav.props.get("__quizPass"), 1)
        self.assertEqual(nav.props.get("__quizType"), 1)


if __name__ == "__main__":
    unittest.main()
