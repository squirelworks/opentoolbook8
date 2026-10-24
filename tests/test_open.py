"""Opening a book reports a missing file and still returns the book."""

import os
import struct
import tempfile
import unittest
from pathlib import Path

from opentoolbook.record import FOLLOW_UP
from opentoolbook.shelf import open_book


def _book_naming(extra: bytes) -> bytes:
    """One real leaf, with ``extra`` stored in the body so a name scan can see it."""
    key = 0x1000
    body = b"\x00\x10xx" + extra
    length = len(body)
    stored = struct.pack("<HH", key, length - 2) + body[4:]
    level0, level1, level2, leaf, body_at = 0x200, 0x400, 0x600, 0x800, 0xA00
    data = bytearray(body_at + length + FOLLOW_UP)
    data[0:4] = b"\x03JBO"
    struct.pack_into("<I", data, 0x10E, level0)
    struct.pack_into("<I", data, level0, level1)
    struct.pack_into("<I", data, level1, level2)
    struct.pack_into("<I", data, level2, leaf)
    slot = leaf + 0x18
    struct.pack_into("<I", data, slot, body_at)
    struct.pack_into("<H", data, slot + 8, 0x4001)
    struct.pack_into("<H", data, slot + 0x0C, length)
    data[slot + 0x16] = 0x11
    data[body_at:body_at + length] = stored
    return bytes(data)


class OpenTests(unittest.TestCase):
    def test_missing_minstb32_does_not_stop_the_open(self):
        settled = Path("SETTLED.md").read_text(encoding="utf-8")
        self.assertIn("minstb32.dll", settled)
        self.assertIn("not fatal", settled)
        raw = _book_naming(b"minstb32.dll\x00nc81base.sbk\x00")
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            book = root / "9e954d01.tbk"
            book.write_bytes(raw)
            home = root / "home"
            home.mkdir()
            (home / "toolbook.lst").write_text("NC81BASE.SBK\nTB80R.SBK\n", encoding="latin1")
            opened = open_book(book, home)
            self.assertGreater(len(opened.book.records), 0)
            notes = {item.name: item.note for item in opened.files}
            self.assertEqual(notes["minstb32.dll"], "named, not shipped")
            self.assertEqual(notes["nc81base.sbk"], "not found")
            import contextlib
            import io

            from opentoolbook.__main__ import main

            buf = io.StringIO()
            with contextlib.redirect_stdout(buf):
                code = main(["opentoolbook", "--home", str(home), str(book)])
            self.assertEqual(code, 0)
            self.assertIn("records ", buf.getvalue())
            self.assertIn("minstb32.dll  named, not shipped", buf.getvalue())
            lesson = os.environ.get("OPENTOOLBOOK_TBK")
            if lesson and os.path.isfile(lesson):
                real = open_book(Path(lesson), home)
                real_notes = {item.name: item.note for item in real.files}
                self.assertEqual(real_notes["minstb32.dll"], "named, not shipped")
                self.assertGreater(len(real.book.records), 0)


if __name__ == "__main__":
    unittest.main()
