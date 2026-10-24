"""Quiz pages store a stem, four choices, and an answer property."""

import os
import unittest
from pathlib import Path

from opentoolbook.field import field_text
from opentoolbook.quiz import questions
from opentoolbook.script import button_clicks


class QuizTests(unittest.TestCase):
    def test_question_numbers_match_the_info_field(self):
        path = os.environ.get("OPENTOOLBOOK_TBK")
        if not path or not os.path.isfile(path):
            self.skipTest("set OPENTOOLBOOK_TBK to 9e954d01.tbk")
        data = Path(path).read_bytes()
        found = questions(data)
        self.assertGreaterEqual(len(found), 2)
        self.assertGreaterEqual(len({item.answer for item in found}), 2)
        info = {}
        for line in field_text(data, "PQINFO", "InfoText").splitlines():
            parts = line.split()
            if len(parts) >= 3 and parts[0].isdigit():
                info[parts[0]] = (parts[1], parts[2])
        matched = 0
        for item in found:
            number = item.page_id[1:] if item.page_id.startswith("P") else ""
            if number not in info:
                continue
            test_no, question_no = info[number]
            self.assertEqual((item.test_no, item.question_no), (test_no, question_no))
            self.assertEqual(item.source_question_no, item.question_no)
            self.assertEqual(item.source_test_no, item.test_no)
            self.assertEqual(item.source_page, item.page_id)
            letters = {letter for letter, _text in item.choices}
            self.assertIn(item.answer, letters)
            self.assertTrue(item.stem.strip())
            for _letter, text in item.choices:
                self.assertTrue(text.strip())
            matched += 1
        self.assertGreaterEqual(matched, 2)

    def test_quiz_start_ends_at_end_buttonclick(self):
        path = os.environ.get("OPENTOOLBOOK_TBK")
        if not path or not os.path.isfile(path):
            self.skipTest("set OPENTOOLBOOK_TBK to 9e954d01.tbk")
        found = {
            item.owner: item.source
            for item in button_clicks(Path(path).read_bytes())
            if item.name.lower() == "selection1" and item.owner in {"P10001", "P10002", "P10003", "P10004"}
        }
        self.assertEqual(set(found), {"P10001", "P10002", "P10003", "P10004"})
        names = {
            "P10001": "Assessment",
            "P10002": "Pre-Test",
            "P10003": "Post-Test",
            "P10004": "Quiz",
        }
        for owner, source in found.items():
            lines = [line.strip() for line in source.split("\r\n") if line.strip()]
            self.assertEqual(lines[-1], "end buttonClick")
            self.assertIn(
                f'setupQuizEx("{names[owner]}", 2, "P10301", "P10302", "P10303")',
                source,
            )
            self.assertIn("get clearpool()", source)
            self.assertIn("addObjectiveToPool(1, 110, 119, 6)", source)
            self.assertIn("addObjectiveToPool(2, 120, 129, 4)", source)
            self.assertIn("setuppool()", source)
            self.assertIn("get gotoNextQuestionEx()", source)


if __name__ == "__main__":
    unittest.main()
