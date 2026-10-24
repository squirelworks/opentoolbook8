"""The two points stored on a class ``0x11`` arc.

They are the signed pairs at ``+0x25`` and ``+0x29``. The record is not
filled, and the points are not moved onto the bounds.
"""

from __future__ import annotations

import struct

from opentoolbook.field import _book, _chars, _page_handles, _segments, _u16

ARC = 0x11
# Measured length of a class 0x11 record. P1140 object 80 is one.
ARC_BYTES = 61
PAGE = 5


def arc_points(data: bytes, page_id: str, object_id: int) -> tuple[tuple[int, int], tuple[int, int]]:
    """The point pair stored on one arc. The word at the start of the record is its id."""
    segments = _segments(data)
    by_key = {segment.key: segment for segment in segments}
    book_segment, book_record = _book(data, segments)
    for handle in _page_handles(data, by_key, book_segment, book_record):
        segment = by_key.get(handle >> 16)
        if segment is None:
            continue
        record = segment.base + (handle & 0xFFFF)
        if record < 2 or record + 8 > len(data) or _u16(data, record - 2) != PAGE:
            continue
        if _chars(data, record + 6, 32) != page_id:
            continue
        found = _arc(data, segment, object_id)
        if found is None:
            break
        if found + 0x2D > len(data):
            break
        return (
            struct.unpack_from("<hh", data, found + 0x25),
            struct.unpack_from("<hh", data, found + 0x29),
        )
    raise ValueError(f"no arc {object_id} on {page_id}")


def _arc(data: bytes, segment, object_id: int) -> int | None:
    end = segment.file_at + segment.size
    at = segment.base + 0x18
    while at + ARC_BYTES <= end and at >= 4:
        kind = _u16(data, at - 2)
        size = _u16(data, at - 4) - (at - segment.base)
        if kind == ARC and size == ARC_BYTES:
            if _u16(data, at) == object_id:
                return at
            at += size
            continue
        at += 1
    return None
