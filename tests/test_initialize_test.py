"""``initializeTest`` runs its literals. Each skipped call is named."""

import os
import unittest
from pathlib import Path

from opentoolbook.initialize import run_literals
from opentoolbook.props import UserProperties

TEST = """to get initializeTest
\tsystem int __quizMode
\tlocal int error
\tseedNum = sysTime
\tformat time seedNum as "seconds"
\tget seedNum mod 32768
\tseed It
\terror = 0
\tlinkDLL32 "kernel32.dll"
\t\tINT GetPrivateProfileIntA(STRING, STRING, INT, STRING)
\tend linkDLL32
\tnidarec = "NIDAREC.INI"
\t__quizMode = GetPrivateProfileIntA("Quiz", "Quiz Mode", 0, nidarec)
\t__quizObjectiveCount = 5
\t__quizMaxResponse = 5
\t__quizHelp = 0
\treturn error
end
"""


class InitializeTestTests(unittest.TestCase):
    def test_literals_and_each_skipped_call(self):
        props = UserProperties()
        done = run_literals(TEST, props)
        self.assertEqual(
            done.skipped,
            [
                "linkDLL32 kernel32.dll",
                "sysTime",
                'format time seedNum as "seconds"',
                "get seedNum mod 32768",
                "seed It",
                "GetPrivateProfileIntA",
            ],
        )
        self.assertEqual(done.unset, ["__quizMode"])
        self.assertEqual(
            dict(props.items()),
            {"__quizobjectivecount": 5, "__quizmaxresponse": 5, "__quizhelp": 0},
        )

    def test_the_real_system_book(self):
        path = os.environ.get("OPENTOOLBOOK_TBK")
        if not path or not os.path.isfile(path):
            self.skipTest("set OPENTOOLBOOK_TBK to 9e954d01.tbk")
        from opentoolbook.initialize import initialize
        from opentoolbook.send import handler_chain
        from opentoolbook.shelf import search_roots

        lesson = Path(path)
        chain = handler_chain(lesson.read_bytes(), lesson.name, search_roots(lesson, None))
        if chain.find("initializeTest") is None:
            self.skipTest("nc81test.sbk is not beside the lesson")
        props = UserProperties()
        done = initialize(chain, "initializeTest", props)
        self.assertEqual(
            dict(props.items()),
            {
                "__embeddedtries": 0,
                "__experimentnumber": 0,
                "__quizassessment": 0,
                "__quizattempts": 0,
                "__quizchecktestandquestion": 0,
                "__quizhelp": 0,
                "__quizmaxresponse": 5,
                "__quizobjectivecount": 5,
                "__quizpretest": 0,
                "__quiztimerid": 0,
            },
        )
        self.assertEqual(done.skipped[:5], [
            "linkDLL32 kernel32.dll",
            "sysTime",
            'format time seedNum as "seconds"',
            "get seedNum mod 32768",
            "seed It",
        ])
        self.assertEqual(done.skipped[5:], ["GetPrivateProfileIntA"] * 11)
        self.assertEqual(done.unset, [
            "__quizMode", "__quizMaxAttempts", "__quizReview", "__quizCritique",
            "__quizObjectiveLevel", "__quizTimed", "__quizTimeType", "__quizTimeLimit",
            "__quizShowPageNumbers", "__quizMarkers", "__showSpecial",
        ])
        for owned in ("timerNotify", "clearRandomSetX", "clearpool", "setuppool"):
            self.assertNotIn(owned, done.skipped)


if __name__ == "__main__":
    unittest.main()
