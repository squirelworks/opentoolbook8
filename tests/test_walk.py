"""One statement walker for opening, enterPage, and buttonClick."""

import unittest

from opentoolbook.click import run_handler
from opentoolbook.walk import Flow, block_if, reader_condition, split_if, walk


def _run(source, condition=reader_condition):
    seen = []
    flow = Flow()
    value = walk(
        source.splitlines(),
        flow,
        condition=condition,
        statement=lambda raw, low: seen.append(low),
        returns=lambda expr: expr,
    )
    return seen, flow, value


class WalkTests(unittest.TestCase):
    def test_end_and_end_if_both_close_an_if(self):
        lines = ["  a", "end", "b", "end if", "c"]
        self.assertEqual(split_if(lines, 0), (["  a"], [], 2))
        self.assertEqual(split_if(lines, 2), (["b"], [], 4))

    def test_an_if_without_then_is_a_block(self):
        self.assertEqual(block_if("if syslevel = reader"), "syslevel = reader")
        self.assertEqual(block_if("if x = 1 then"), "x = 1")
        self.assertIsNone(block_if("if x = 1 then beep 1"))

    def test_taken_branch_and_else(self):
        seen, _flow, _value = _run(
            "to handle buttonClick\nif sysLevel = reader\n a\nelse\n b\nend if\nc\nend"
        )
        self.assertEqual(seen, ["a", "c"])
        seen, _flow, _value = _run("if sysLevel <> reader then\n a\nelse\n b\nend\nc")
        self.assertEqual(seen, ["b", "c"])

    def test_unknown_condition_runs_neither_branch(self):
        seen, _flow, _value = _run("if __quizHelp = 1 then\n a\n break\nelse\n b\nend if\nc")
        self.assertEqual(seen, ["c"])

    def test_break_stops_the_handler(self):
        seen, flow, _value = _run("a\nbreak\nb")
        self.assertEqual(seen, ["a"])
        self.assertTrue(flow.breaking)

    def test_return_inside_an_if_stops_and_gives_the_value(self):
        seen, flow, value = _run("if sysLevel = reader then\n return 0\nend if\nb")
        self.assertEqual(seen, [])
        self.assertTrue(flow.returning)
        self.assertEqual(value, "0")

    def test_linkdll_forward_and_comments_are_not_statements(self):
        seen, _flow, _value = _run(
            "-- note\nlinkDLL \"x.dll\"\n int f(int)\nend linkDLL\nforward\na"
        )
        self.assertEqual(seen, ["a"])

    def test_top_level_end_ends_the_handler(self):
        seen, _flow, _value = _run("a\nend buttonClick\nb")
        self.assertEqual(seen, ["a"])


class ClickWalkTests(unittest.TestCase):
    def test_click_break_in_an_unknown_branch_does_not_stop(self):
        source = (
            "to handle buttonClick\n"
            "  if __quizHelp = 1 then\n    break\n  end if\n"
            '  go to page "P20"\nend'
        )
        follow = run_handler(source, ("P10", "P20"), "P10")
        self.assertEqual((follow.page_id, follow.book), ("P20", None))

    def test_click_reader_branch_runs(self):
        source = 'if sysLevel = reader\n  forward\nend if\ngo to page("P1280")\nend'
        follow = run_handler(source, (), "P1270")
        self.assertEqual(follow.page_id, "P1280")


if __name__ == "__main__":
    unittest.main()
