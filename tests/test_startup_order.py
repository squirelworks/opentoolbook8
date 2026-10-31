"""Opening messages run in the TB80RTM order on a synthetic book."""

from __future__ import annotations

import unittest
from pathlib import Path

from opentoolbook.entry import _State, _open_on_page, opening_page
from opentoolbook.field import page_ids

FIXTURE = Path(__file__).parent / "fixtures" / "otb-line-rect.tbk"

_LOG = (
    "to handle {name}\n"
    "  system log\n"
    '  put "{name} " after log\n'
    "  forward\n"
    "end\n"
)


def _logging_handlers(*names: str) -> dict[str, str]:
    return {name.lower(): _LOG.format(name=name) for name in names}


class StartupOrder(unittest.TestCase):
    def test_opening_messages_log_in_tb80rtm_order(self):
        data = FIXTURE.read_bytes()
        pages = page_ids(data)
        variables = {"log": ""}
        names = (
            "enterSystem",
            "enterApplication",
            "enterBook",
            "enterWindow",
            "enterBackground",
            "enterPage",
            "firstIdle",
        )
        handlers = _logging_handlers(*names)
        state = _State(pages, handlers, (), FIXTURE.name, variables=variables, data=data)
        state.own = dict(handlers)
        page, other = _open_on_page(state, startup=True)
        self.assertIsNone(other)
        self.assertEqual(page, pages[0])
        self.assertEqual(
            variables["log"],
            "enterSystem enterApplication enterBook enterWindow enterBackground enterPage firstIdle ",
        )

    def test_fixture_without_system_script_has_no_tb80r_handlers(self):
        entry = opening_page(FIXTURE)
        self.assertEqual(entry.sysbooks, ())
        self.assertNotIn("tb80r.sbk", entry.sysbooks)


if __name__ == "__main__":
    unittest.main()
