"""A type 10 resource stores a handler. The reader returns the text and does not call it."""

import os
import unittest
from pathlib import Path

from opentoolbook.script import resource_scripts


class ResourceScriptTests(unittest.TestCase):
    def test_type_10_bytes_are_a_handler(self):
        path = os.environ.get("OPENTOOLBOOK_TBK")
        if not path or not os.path.isfile(path):
            self.skipTest("set OPENTOOLBOOK_TBK to 9e954d01.tbk")
        self._handlers(
            Path(path).read_bytes(),
            "to handle enterPage",
            "to handle enterSystem",
        )
        nida = Path(path).with_name("nida81.tbk")
        self.assertTrue(nida.is_file())
        self._handlers(
            nida.read_bytes(),
            "To handle enterpage",
            "to handle enterApplication",
        )

    def _handlers(self, data: bytes, first: str, second: str):
        found = resource_scripts(data)
        self.assertGreaterEqual(len(found), 2)
        sources = [item.source for item in found]
        self.assertGreaterEqual(len(set(sources)), 2)
        self.assertTrue(any(item.source.startswith(first) for item in found))
        self.assertTrue(any(item.source.startswith(second) for item in found))
        self.assertEqual(len({item.resource_id for item in found}), len(found))
        for item in found:
            self.assertTrue(item.source.lower().startswith("to handle "))
            self.assertNotIn("\x00", item.source)
            lines = [line.strip() for line in item.source.splitlines() if line.strip()]
            self.assertEqual(lines[-1].lower(), "end")
            self.assertNotEqual(lines[0].lower(), "end")

    def test_system_book_script_is_the_whole_count(self):
        path = os.environ.get("OPENTOOLBOOK_TBK")
        if not path or not os.path.isfile(path):
            self.skipTest("set OPENTOOLBOOK_TBK to 9e954d01.tbk")
        folder = Path(path).parent
        books = {
            "nc81base.sbk": (129, "-- NC81BASE.SBK"),
            "nc81recs.sbk": (268, "-- NC81RECS.SBK"),
            "nc81test.sbk": (741, "-- NC81TEST.SBK"),
            "nc81trnr.sbk": (428, "-- NC82TRNR.SBK"),
        }
        for name, (ident, head) in books.items():
            found = resource_scripts((folder / name).read_bytes())
            self.assertEqual(len(found), 1)
            item = found[0]
            self.assertEqual(item.resource_id, ident)
            self.assertTrue(item.source.startswith(head))
            self.assertGreater(len(item.source), 8000)
            self.assertNotIn("\x00", item.source)
            self.assertIn("to get ", item.source)
            lines = [line.strip() for line in item.source.splitlines() if line.strip()]
            self.assertEqual(lines[-1].lower(), "end")
        quiz = resource_scripts((folder / "nc81test.sbk").read_bytes())[0].source
        self.assertIn("to get handleQuizClick", quiz)
        self.assertIn("to get getQuizScore\r", quiz)
        self.assertIn("to get getQuizScorePM", quiz)
        self.assertIn("to get gotoNextQuestionEx", quiz)
        self.assertIn("to get gotoPreviousQuestionEx", quiz)
        self.assertEqual(quiz.count("response = answer of this page"), 2)
        self.assertEqual(
            quiz.count("get storeQuestionResponse(testNo of this page, questionNo of this page, response, score)"),
            2,
        )
        self.assertGreaterEqual(quiz.count("score = score + __quizScore[i]"), 2)
        self.assertEqual(quiz.count("error = score div count"), 2)
        self.assertEqual(quiz.count("get gotoNextQuestionEx()"), 6)


if __name__ == "__main__":
    unittest.main()
