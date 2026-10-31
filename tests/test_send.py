"""``send name`` goes to the open book, then each book in ``sysBooks``."""

import os
import tempfile
import unittest
from pathlib import Path

from opentoolbook.entry import choose_opening
from opentoolbook.send import Chain, calls_dll, handler_chain, send_message

from test_entry import LOGO

LINKED = """to get openSession
    linkDLL "nc81rec.dll"
        INT openSession32()
    end linkDLL
    return openSession32()
end
"""


class SendTests(unittest.TestCase):
    def test_the_order(self):
        chain = Chain((
            ("lesson.tbk", {"pick": "to get pick\nreturn 1\nend\n"}),
            ("nc81base.sbk", {"pick": "to get pick\nreturn 2\nend\n", "other": "to get other\nreturn 3\nend\n"}),
        ))
        self.assertEqual(send_message(chain, "pick").value, 1)
        self.assertEqual(send_message(chain, "pick").book, "lesson.tbk")
        self.assertEqual(send_message(chain, "Other").value, 3)
        self.assertEqual(send_message(chain, "Other").book, "nc81base.sbk")
        self.assertEqual(send_message(chain, "missing").book, None)

    def test_send_get_logo_book_returns_nida81(self):
        chain = Chain((("lesson.tbk", {}), ("nc81base.sbk", {"getlogobook": LOGO})))
        sent = send_message(chain, "getLogoBook")
        self.assertEqual((sent.value, sent.book, sent.skipped), ("nida81.tbk", "nc81base.sbk", False))
        with tempfile.TemporaryDirectory() as tmp:
            Path(tmp, "MRJ81.TBK").write_bytes(b"")
            sent = send_message(chain, "getLogoBook", roots=(Path(tmp),))
        self.assertEqual(sent.value, "mrj81.tbk")

    def test_a_handler_that_links_a_dll_returns_without_running(self):
        self.assertTrue(calls_dll(LINKED))
        self.assertFalse(calls_dll(LOGO))
        chain = Chain((("nc81recs.sbk", {"opensession": LINKED}),))
        sent = send_message(chain, "openSession")
        self.assertTrue(sent.skipped)
        self.assertIsNone(sent.value)

    def test_send_in_a_startup_handler(self):
        handlers = {
            "entersystem": "to handle enterSystem\n  send goThere\n  send linked\nend\n",
            "gothere": 'to handle goThere\n  go to page "P2"\nend\n',
            "linked": 'to handle linked\n  linkDLL32 "kernel32.dll"\n  end linkDLL32\n  go to page "P1"\nend\n',
        }
        # linkDLL only declares functions. The rest of the handler runs, so the last go wins.
        self.assertEqual(choose_opening(("P0", "P1", "P2"), handlers), ("P1", None))

    def test_the_real_system_book(self):
        path = os.environ.get("OPENTOOLBOOK_TBK")
        if not path or not os.path.isfile(path):
            self.skipTest("set OPENTOOLBOOK_TBK to 9e954d01.tbk")
        from opentoolbook.entry import opening_page
        from opentoolbook.shelf import search_roots

        lesson = Path(path)
        roots = search_roots(lesson, None)
        sysbooks = opening_page(lesson).sysbooks
        self.assertEqual(sysbooks, ("nc81trnr.sbk", "nc81recs.sbk", "nc81test.sbk", "nc81base.sbk", "tb80anm.sbk", "tb80r.sbk"))
        chain = handler_chain(lesson.read_bytes(), lesson.name, roots, sysbooks)
        self.assertEqual([book.lower() for book, _ in chain.books[1:]], list(sysbooks))
        sent = send_message(chain, "getLogoBook", roots=roots, book_name=lesson.name)
        self.assertEqual(sent.book.lower(), "nc81base.sbk")
        self.assertFalse(sent.skipped)
        self.assertEqual(sent.value, opening_page(lesson).book.name)
        self.assertTrue(send_message(chain, "initializeBase").skipped)
        self.assertTrue(send_message(chain, "openSession").skipped)


class SysBooksTests(unittest.TestCase):
    """``push "x" onto sysBooks`` and ``"x" is not in sysBooks`` in startup."""

    def test_a_pushed_book_answers_the_next_get(self):
        with tempfile.TemporaryDirectory() as tmp:
            from opentoolbook.entry import _State, _statement, _condition, _call

            state = _State(("P0",), {}, (Path(tmp),), "lesson.tbk")
            self.assertTrue(_condition('"base.sbk" is not in sysBooks', state))
            _statement('push "BASE.sbk" onto sysBooks', 'push "base.sbk" onto sysbooks', state)
            self.assertEqual(state.sysbooks, ["base.sbk"])
            self.assertFalse(_condition('"base.sbk" is not in sysBooks', state))
            self.assertTrue(_condition('"Base.sbk" is in sysBooks', state))
            _statement('push "other.sbk" onto sysBooks', 'push "other.sbk" onto sysbooks', state)
            self.assertEqual(state.sysbooks, ["other.sbk", "base.sbk"])

    def test_startup_without_a_push_has_no_system_book(self):
        handlers = {
            "entersystem": 'to handle enterSystem\n  get pick()\n  if it is 2\n    go to page "P1"\n  end\nend\n',
        }
        self.assertEqual(choose_opening(("P0", "P1"), handlers), ("P0", None))

    def test_the_book_handler_wins_over_a_sysbooks_handler(self):
        from opentoolbook.entry import _State, _merge_sysbooks

        state = _State(("P0",), {"pick": "own"}, (), "lesson.tbk")
        state.loaded["base.sbk"] = {"pick": "base", "other": "base other"}
        state.sysbooks = ["base.sbk"]
        _merge_sysbooks(state)
        self.assertEqual(state.handlers["pick"], "own")
        self.assertEqual(state.handlers["other"], "base other")


if __name__ == "__main__":
    unittest.main()
