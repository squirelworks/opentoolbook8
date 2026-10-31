"""``enterSystemBook`` / ``leaveSystemBook`` when ``sysBooks`` gains or loses a book."""

from __future__ import annotations

import unittest

from opentoolbook.entry import _State
from opentoolbook.run import BookHost, engine_for


def _engine(own: dict[str, str], loaded: dict[str, dict[str, str]], variables: dict):
    state = _State(("P0",), {}, (), "lesson.tbk", variables=variables)
    state.own = dict(own)
    state.handlers = dict(own)
    state.loaded.update(loaded)
    host = BookHost(state.pages, state.book_file, state.roots)
    return engine_for(state, host), state


class SysBooksMessages(unittest.TestCase):
    def test_push_sends_enter_and_pop_sends_leave(self):
        variables = {"log": ""}
        engine, state = _engine(
            {
                "entersystem": (
                    "to handle enterSystem\n"
                    "  system log\n"
                    '  push "helper.sbk" onto sysBooks\n'
                    "  pop sysBooks\n"
                    "end\n"
                ),
            },
            {
                "helper.sbk": {
                    "entersystembook": (
                        "to handle enterSystemBook\n"
                        "  system log\n"
                        '  put "enter " after log\n'
                        "end\n"
                    ),
                    "leavesystembook": (
                        "to handle leaveSystemBook\n"
                        "  system log\n"
                        '  put "leave " after log\n'
                        "end\n"
                    ),
                },
            },
            variables,
        )
        engine.send("entersystem")
        self.assertEqual(variables["log"], "enter leave ")
        self.assertEqual(state.sysbooks, [])

    def test_set_sysbooks_enters_each_new_book(self):
        variables = {"log": ""}
        loaded = {
            name: {
                "entersystembook": (
                    "to handle enterSystemBook\n"
                    "  system log\n"
                    f'  put "{name} " after log\n'
                    "end\n"
                ),
            }
            for name in ("one.sbk", "two.sbk")
        }
        engine, state = _engine(
            {
                "entersystem": (
                    "to handle enterSystem\n"
                    "  system log\n"
                    '  sysBooks = "one.sbk,two.sbk"\n'
                    "end\n"
                ),
            },
            loaded,
            variables,
        )
        engine.send("entersystem")
        self.assertEqual(variables["log"], "one.sbk two.sbk ")
        self.assertEqual(state.sysbooks, ["one.sbk", "two.sbk"])

    def test_clear_sends_leave_for_each_book(self):
        variables = {"log": ""}
        engine, state = _engine(
            {
                "entersystem": (
                    "to handle enterSystem\n"
                    "  system log\n"
                    '  push "helper.sbk" onto sysBooks\n'
                    "  clear sysBooks\n"
                    "end\n"
                ),
            },
            {
                "helper.sbk": {
                    "entersystembook": (
                        "to handle enterSystemBook\n"
                        "  system log\n"
                        '  put "enter " after log\n'
                        "end\n"
                    ),
                    "leavesystembook": (
                        "to handle leaveSystemBook\n"
                        "  system log\n"
                        '  put "leave " after log\n'
                        "end\n"
                    ),
                },
            },
            variables,
        )
        engine.send("entersystem")
        self.assertEqual(variables["log"], "enter leave ")
        self.assertEqual(state.sysbooks, [])


if __name__ == "__main__":
    unittest.main()
