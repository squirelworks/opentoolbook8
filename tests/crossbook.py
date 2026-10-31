"""Build the two cross-book fixtures from ``otb-line-rect.tbk``'s bytes.

``otb_cross_b.tbk`` is the line-rect book with its one page id set to
``P0``. ``otb_cross_a.tbk`` is the line-rect book with an inline
``enterPage`` on its one page that quotes ``go to page "P0" of book
"otb_cross_b.tbk"``. Nothing else changes. The checked-in files are the
output of ``build()``; ``test_crossbook`` keeps them equal.

These books are for this reader. ToolBook has not opened them.

Run ``python3 tests/crossbook.py`` to rewrite the two files.
"""

from __future__ import annotations

import struct
from pathlib import Path

from opentoolbook.field import PAGE, _book, _page_handles, _segments
from opentoolbook.record import Book

FIXTURES = Path(__file__).parent / "fixtures"
SOURCE = FIXTURES / "otb-line-rect.tbk"
BOOK_A = "otb_cross_a.tbk"
BOOK_B = "otb_cross_b.tbk"
PAGE_B = "P0"
ENTER_A = (
    "to handle enterPage\r\n"
    f'  go to page "{PAGE_B}" of book "{BOOK_B}"\r\n'
    "end enterPage\r\n"
)
# The page id is the C string at page +6, 32 bytes on the line-rect page.
_ID_AT = 6
_ID_BYTES = 32
# Page script mode is the byte at +0x30; low bits 0 is an inline script at +0x2A.
_MODE_AT = 0x30
_SCRIPT_AT = 0x2A
# A follow-up read is two bytes after the record (record.FOLLOW_UP).
_FOLLOW_UP = 2


def _page(data: bytes) -> tuple[int, int]:
    """``(segment key, file offset)`` of the one stored page."""
    segments = _segments(data)
    by_key = {segment.key: segment for segment in segments}
    book_segment, book_record = _book(data, segments)
    handles = _page_handles(data, by_key, book_segment, book_record)
    if len(handles) != 1:
        raise ValueError(f"{SOURCE.name} stores {len(handles)} pages, not one")
    segment = by_key[handles[0] >> 16]
    record = segment.base + (handles[0] & 0xFFFF)
    if struct.unpack_from("<H", data, record - 2)[0] != PAGE:
        raise ValueError("the page handle does not name a page")
    return segment.key, record


def with_page_id(data: bytes, page_id: str) -> bytes:
    """Write ``page_id`` into the empty C string at page ``+6``."""
    _key, record = _page(data)
    out = bytearray(data)
    stored = out[record + _ID_AT:record + _ID_AT + _ID_BYTES]
    if any(stored):
        raise ValueError("the page id is not empty")
    encoded = page_id.encode("latin-1")
    if len(encoded) >= _ID_BYTES:
        raise ValueError("page id is too long")
    out[record + _ID_AT:record + _ID_AT + len(encoded)] = encoded
    return bytes(out)


def with_inline_script(data: bytes, source: str) -> bytes:
    """Store ``source`` as the page's inline script.

    The page's segment record is copied to the end of the file with one
    more heap block: the end word, class 0, then the script the reader
    expands: a skip word of 0, a count, the characters, a 0 byte, and two
    0 bytes of pad. The leaf entry names the new position and length, the
    record's own length word follows, and the two follow-up bytes come
    after it. The page word at ``+0x2A`` is the near pointer to the skip word.
    """
    key, record = _page(data)
    book = Book(data)
    leaf = next(item for item in book.records if item.key == key)
    if data[record + _MODE_AT] & 3 != 0 or struct.unpack_from("<H", data, record + _SCRIPT_AT)[0]:
        raise ValueError("the page already stores a script")
    text = source.encode("latin-1")
    if any(byte >= 0x80 for byte in text):
        raise ValueError("the script is stored as plain characters below 0x80")
    count = len(text) + 1
    script = struct.pack("<HH", 0, count) + text + b"\x00" + b"\x00\x00"
    old = data[leaf.position:leaf.position + leaf.length]
    follow = data[leaf.position + leaf.length:leaf.position + leaf.length + _FOLLOW_UP]
    pad = b"\x00" * (len(old) % 2)
    header_near = len(old) + len(pad) + 6
    near = header_near + 4
    block = struct.pack("<HH", near + len(script), 0) + script
    body = bytearray(old + pad + block)
    struct.pack_into("<H", body, 2, len(body) - 2)
    page_near = record - (leaf.position - 6)
    struct.pack_into("<H", body, page_near + _SCRIPT_AT - 6, near)
    out = bytearray(data)
    out.extend(b"\x00" * (len(out) % 2))
    position = len(out)
    out.extend(body)
    if leaf.wants_follow_up:
        out.extend(follow)
    struct.pack_into("<I", out, leaf.slot, position)
    struct.pack_into("<H", out, leaf.slot + 0x0C, len(body))
    return bytes(out)


def build() -> dict[str, bytes]:
    data = SOURCE.read_bytes()
    return {
        BOOK_A: with_inline_script(data, ENTER_A),
        BOOK_B: with_page_id(data, PAGE_B),
    }


if __name__ == "__main__":
    for name, blob in build().items():
        (FIXTURES / name).write_bytes(blob)
        print(f"{name}  {len(blob)} bytes")
