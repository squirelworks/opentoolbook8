"""``send name`` goes to the open book, then nc81base, nc81recs, nc81test, nc81trnr."""

import os
import tempfile
import unittest
from pathlib import Path

from opentoolbook.entry import choose_opening
from opentoolbook.send import SYSTEM_BOOKS, Chain, calls_dll, handler_chain, send_message

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
        self.assertEqual(SYSTEM_BOOKS, ("nc81base.sbk", "nc81recs.sbk", "nc81test.sbk", "nc81trnr.sbk"))
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
        self.assertEqual(choose_opening(("P0", "P1", "P2"), handlers), ("P2", None))

    def test_the_real_system_book(self):
        path = os.environ.get("OPENTOOLBOOK_TBK")
        if not path or not os.path.isfile(path):
            self.skipTest("set OPENTOOLBOOK_TBK to 9e954d01.tbk")
        from opentoolbook.entry import opening_page
        from opentoolbook.shelf import search_roots

        lesson = Path(path)
        roots = search_roots(lesson, None)
        chain = handler_chain(lesson.read_bytes(), lesson.name, roots)
        self.assertEqual([book.lower() for book, _ in chain.books[1:]], list(SYSTEM_BOOKS))
        sent = send_message(chain, "getLogoBook", roots=roots, book_name=lesson.name)
        self.assertEqual(sent.book.lower(), "nc81base.sbk")
        self.assertFalse(sent.skipped)
        self.assertEqual(sent.value, opening_page(lesson).book.name)
        self.assertTrue(send_message(chain, "initializeBase").skipped)
        self.assertTrue(send_message(chain, "openSession").skipped)


if __name__ == "__main__":
    unittest.main()
