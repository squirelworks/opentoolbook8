"""Quiz pages store a stem, four choices, and an answer property."""

import os
import unittest
from pathlib import Path

from opentoolbook.field import field_text
from opentoolbook.quiz import questions


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
            letters = {letter for letter, _text in item.choices}
            self.assertIn(item.answer, letters)
            self.assertTrue(item.stem.strip())
            for _letter, text in item.choices:
                self.assertTrue(text.strip())
            matched += 1
        self.assertGreaterEqual(matched, 2)


if __name__ == "__main__":
    unittest.main()
