"""A class 4 background.

A page names it with the far reference at ``+0x47``. The class word
immediately before that record is 4. The pattern byte is at ``+0x4B``.
Red, green, and blue are the bytes at ``+0x5B``, ``+0x5C``, and ``+0x5D``.
"""

from __future__ import annotations

import struct
from dataclasses import dataclass

from opentoolbook.field import _book, _chars, _page_handles, _segments, _u16

BACKGROUND = 4
PAGE = 5


@dataclass(frozen=True)
class Background:
    pattern: int
    red: int
    green: int
    blue: int


def background(data: bytes, page_id: str) -> Background:
    """Pattern and color of the class 4 background a page names."""
    segments = _segments(data)
    by_key = {segment.key: segment for segment in segments}
    book_segment, book_record = _book(data, segments)
    for handle in _page_handles(data, by_key, book_segment, book_record):
        segment = by_key.get(handle >> 16)
        if segment is None:
            continue
        record = segment.base + (handle & 0xFFFF)
        if record < 2 or record + 0x4B > len(data) or _u16(data, record - 2) != PAGE:
            continue
        if _chars(data, record + 6, 32) != page_id:
            continue
        far = struct.unpack_from("<I", data, record + 0x47)[0]
        owner = by_key.get(far >> 16)
        if owner is None:
            break
        found = owner.base + (far & 0xFFFF)
        if found < 2 or _u16(data, found - 2) != BACKGROUND:
            break
        if found + 0x5E > len(data):
            break
        return Background(
            data[found + 0x4B],
            data[found + 0x5B],
            data[found + 0x5C],
            data[found + 0x5D],
        )
    raise ValueError(f"no class 4 background on {page_id}")
