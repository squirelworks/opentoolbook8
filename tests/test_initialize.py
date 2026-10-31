"""The literal assignments of ``initializeBase``. Every DLL line is skipped by name."""

import os
import unittest
from pathlib import Path

from opentoolbook.initialize import initialize, run_literals
from opentoolbook.props import UserProperties
from opentoolbook.send import Chain

BASE = """to get initializeBase  cmdLine
\tsystem int __pageIndex
\tlocal int error
\tif  "tbfile32.dll" is not in sysLinkedDLLs  then
\t\tlinkDLL "tbfile32.dll"
\t\t\tINT fileExists32(STRING)
\t\tend linkDLL
\tend if
\terror = clearMenuFlags()
\t__pageIndex = 0
\tlinkDLL32 "kernel32.dll"
\t\tINT GetPrivateProfileIntA(STRING, STRING, INT, STRING)
\tend linkDLL32
\tnidarec = "NIDAREC.INI"
\t__lessonMode = GetPrivateProfileIntA("Lesson", "Lesson Mode", 2, nidarec)
\tif  __lessonMode = 5  then
\t\t__menuOption = "five"
\tend if
\t__quizDisableMenuKey = 0
\tif  sysLevel = reader  then
\t\tget placeLesson()
\t    set saveOnClose of this book to no
\t\tset sysChangesDB to false
\telse
\t\t__quizDisableMenuKey = 1
\tend if
\t__cmdLine = cmdLine
\tif  __pageIndex = 0  then
\t\t__copy = nidarec
\tend if
\tconditions
\t\twhen  __pageIndex = 0
\t\t\t__quizPass = 8
\tend conditions
\treturn 0
end
"""


class InitializeTests(unittest.TestCase):
    def test_literals_run_and_dll_lines_are_named(self):
        props = UserProperties()
        done = run_literals(BASE, props, ("/x",))
        self.assertEqual(
            dict(props.items()),
            {
                "__pageindex": 0,
                "__quizdisablemenukey": 0,
                "__cmdline": "/x",
                "__copy": "NIDAREC.INI",
            },
        )
        self.assertEqual(
            done.skipped,
            [
                "linkDLL tbfile32.dll",
                "linkDLL32 kernel32.dll",
                'if "tbfile32.dll" is not in syslinkeddlls',
                "clearMenuFlags",
                "GetPrivateProfileIntA",
                "if __lessonmode = 5",
                "placeLesson",
                "saveOnClose of this book",
                "sysChangesDB",
                "conditions",
            ],
        )
        self.assertNotIn("__quizpass", props)
        self.assertNotIn("__menuoption", props)

    def test_the_chain_names_a_missing_handler(self):
        with self.assertRaises(ValueError) as caught:
            initialize(Chain((("nc81base.sbk", {}),)), "initializeBase", UserProperties())
        self.assertIn("nc81base.sbk", str(caught.exception))

    def test_the_real_initialize_base(self):
        path = os.environ.get("OPENTOOLBOOK_TBK")
        if not path or not os.path.isfile(path):
            self.skipTest("set OPENTOOLBOOK_TBK to 9e954d01.tbk")
        from opentoolbook.send import handler_chain
        from opentoolbook.shelf import search_roots

        lesson = Path(path)
        chain = handler_chain(lesson.read_bytes(), lesson.name, search_roots(lesson, None))
        if chain.find("initializeBase") is None:
            self.skipTest("nc81base.sbk is not beside the lesson")
        props = UserProperties()
        done = initialize(chain, "initializeBase", props, ("",))
        self.assertEqual(
            dict(props.items()),
            {"__cmdline": "", "__pageindex": 0, "__pagelistcleared": 0, "__quizdisablemenukey": 0},
        )
        for name in (
            "linkDLL tbfile32.dll",
            "linkDLL32 kernel32.dll",
            "linkDLL32 user32.dll",
            "WritePrivateProfileStringA",
            "GetPrivateProfileIntA",
            "placeLesson",
            "if wordcount(__cmdline) >= 2",
        ):
            self.assertIn(name, done.skipped)
        self.assertNotIn("__lessonmode", props)


if __name__ == "__main__":
    unittest.main()
