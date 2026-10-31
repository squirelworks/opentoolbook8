"""``enterButton`` and ``leaveButton`` are not in the lesson or the system books."""

import os
import unittest
from pathlib import Path

from opentoolbook.script import button_clicks, handler_sites, object_scripts

FIXTURE = Path(__file__).parent / "fixtures" / "otb-line-rect.tbk"
BOOKS = ("9e954d01.tbk", "nida81.tbk", "nc81base.sbk", "nc81recs.sbk", "nc81test.sbk", "nc81trnr.sbk")


def _lesson():
    path = os.environ.get("OPENTOOLBOOK_TBK")
    if not path or not os.path.isfile(path):
        return None
    return Path(path)


class HandlerSiteTests(unittest.TestCase):
    def test_the_fixture_has_no_script(self):
        data = FIXTURE.read_bytes()
        self.assertEqual(object_scripts(data), ())
        self.assertEqual(handler_sites(data, "enterButton"), ())

    def test_no_book_handles_enter_or_leave_button(self):
        path = _lesson()
        if path is None:
            self.skipTest("set OPENTOOLBOOK_TBK to 9e954d01.tbk")
        counts = {}
        for name in BOOKS:
            data = path.with_name(name).read_bytes()
            self.assertEqual(handler_sites(data, "enterButton"), (), name)
            self.assertEqual(handler_sites(data, "leaveButton"), (), name)
            counts[name] = (len(handler_sites(data, "mouseEnter")), len(handler_sites(data, "mouseLeave")))
        self.assertEqual(counts["9e954d01.tbk"], (19, 19))
        self.assertEqual(counts["nida81.tbk"], (3, 3))
        for name in BOOKS[2:]:
            self.assertEqual(counts[name], (0, 0), name)
        lesson = path.read_bytes()
        places = {site[:2] for site in handler_sites(lesson, "mouseEnter")}
        self.assertIn(("inline", "P300"), places)
        self.assertTrue(all(site[0] == "inline" for site in handler_sites(lesson, "mouseEnter")))

    def test_button_clicks_still_come_from_the_same_walk(self):
        path = _lesson()
        if path is None:
            self.skipTest("set OPENTOOLBOOK_TBK to 9e954d01.tbk")
        # 249 inline scripts, and 3 more in the type 10 page scripts of P10301 to P10303.
        self.assertEqual(len(button_clicks(path.read_bytes())), 252)
        self.assertEqual(len(button_clicks(path.with_name("nida81.tbk").read_bytes())), 119)


if __name__ == "__main__":
    unittest.main()
