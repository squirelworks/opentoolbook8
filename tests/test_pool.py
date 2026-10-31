"""``clearpool``, ``addObjectiveToPool``, ``setuppool``, and ``getNextRandomX``."""

import os
import random
import unittest
from pathlib import Path

from opentoolbook.pool import (
    add_objective_to_pool,
    clear_pool,
    get_next_question,
    pool_from_click,
    setup_pool,
)
from opentoolbook.props import UserProperties


def _numbers(props):
    table = props.get("__quizNumbers")
    return [table[index] for index in range(1, props.get("__quizCount") + 1)]


class PoolTests(unittest.TestCase):
    def test_one_objective_gives_six_numbers_inside_its_range(self):
        props = UserProperties()
        self.assertEqual(clear_pool(props), 0)
        self.assertEqual(props.get("__poolCount"), {index: 0 for index in range(1, 11)})
        add_objective_to_pool(props, 1, 110, 119, 6)
        self.assertEqual(props.get("__poolQuestions")[1], "110,111,112,113,114,115,116,117,118,119")
        self.assertEqual(props.get("__poolCount")[1], 6)
        self.assertEqual(setup_pool(props, random.Random(7)), 0)
        found = _numbers(props)
        self.assertEqual(len(found), 6)
        self.assertEqual(len(set(found)), 6)
        self.assertTrue(all(110 <= number <= 119 for number in found))
        self.assertEqual(props.get("__quizIndex"), 0)

    def test_a_seed_gives_the_same_pool(self):
        runs = []
        for _ in range(2):
            props = UserProperties()
            clear_pool(props)
            add_objective_to_pool(props, 1, 110, 119, 6)
            setup_pool(props, random.Random(42))
            runs.append(_numbers(props))
        self.assertEqual(runs[0], runs[1])

    def test_next_question_is_a_number_then_minus_one(self):
        props = UserProperties()
        clear_pool(props)
        add_objective_to_pool(props, 1, 110, 119, 2)
        setup_pool(props, random.Random(1))
        stored = _numbers(props)
        first = get_next_question(props)
        second = get_next_question(props)
        self.assertEqual([first, second], stored)
        self.assertIsInstance(first, int)
        self.assertEqual(get_next_question(props), -1)
        self.assertEqual(props.get("__quizIndex"), 2)

    def test_the_menu_group_lines_in_order(self):
        source = (
            "to handle buttonClick\n"
            "\tget clearpool()\n"
            "\terror = addObjectiveToPool(1, 110, 119, 6)    \n"
            "\terror = addObjectiveToPool(2, 120, 129, 4)\n"
            "\tif setuppool() = -1 then\n\t\tbreak\n\tend if\n"
            "\tget gotoNextQuestionEx()\nend buttonClick\n"
        )
        props = UserProperties()
        self.assertEqual(pool_from_click(source, props, random.Random(3)), 0)
        found = _numbers(props)
        self.assertEqual(len(found), 10)
        self.assertTrue(all(110 <= number <= 119 for number in found[:6]))
        self.assertTrue(all(120 <= number <= 129 for number in found[6:]))
        self.assertIsNone(pool_from_click("to handle buttonClick\n  send next\nend", UserProperties(), random.Random(3)))

    def test_the_lesson_menu_group(self):
        path = os.environ.get("OPENTOOLBOOK_TBK")
        if not path or not os.path.isfile(path):
            self.skipTest("set OPENTOOLBOOK_TBK to 9e954d01.tbk")
        from opentoolbook.script import button_clicks

        data = Path(path).read_bytes()
        source = next(
            item.source for item in button_clicks(data)
            if item.owner == "P10001" and item.name.lower() == "selection1"
        )
        props = UserProperties()
        self.assertEqual(pool_from_click(source, props, random.Random(11)), 0)
        found = _numbers(props)
        self.assertEqual(len(found), 10)
        self.assertEqual(sorted(found[:6]), sorted(set(found[:6])))
        self.assertTrue(all(110 <= number <= 119 for number in found[:6]))
        self.assertTrue(all(120 <= number <= 129 for number in found[6:]))


if __name__ == "__main__":
    unittest.main()
