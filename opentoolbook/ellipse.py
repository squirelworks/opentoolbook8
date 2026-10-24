"""A class ``0xC`` record's colors and pattern.

The bytes at ``+0x17``, ``+0x18``, and ``+0x19`` are a color. The byte at
``+0x1A`` is 0. The bytes at ``+0x1B``, ``+0x1C``, and ``+0x1D`` are a
color. The byte at ``+0x1E`` is 0. The byte at ``+0x25`` is the pattern.
The bounds are four signed words at ``+0x0F``.
"""

from __future__ import annotations

import struct
from dataclasses import dataclass

from opentoolbook.field import _book, _chars, _page_handles, _segments, _u16

ELLIPSE = 0xC
# Length shared by the class 0xC records in 9e954d01.tbk.
ELLIPSE_BYTES = 41
PAGE = 5


@dataclass(frozen=True)
class Ellipse:
    bounds: tuple[int, int, int, int]
    pattern: int
    first_color: tuple[int, int, int]
    second_color: tuple[int, int, int]


def stored_ellipses(data: bytes) -> tuple[Ellipse, ...]:
    """Every class ``0xC`` record of the shared length."""
    found: list[Ellipse] = []
    for segment in _segments(data):
        found.extend(_in_segment(data, segment))
    return tuple(found)


def ellipses_on_page(data: bytes, page_id: str) -> tuple[Ellipse, ...]:
    """Class ``0xC`` records of the shared length on one page."""
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
        return tuple(_in_segment(data, segment))
    raise ValueError(f"no page {page_id}")


def _in_segment(data: bytes, segment) -> list[Ellipse]:
    found: list[Ellipse] = []
    end = segment.file_at + segment.size
    at = segment.base + 0x10
    while at + ELLIPSE_BYTES <= end and at >= 4:
        kind = _u16(data, at - 2)
        size = _u16(data, at - 4) - (at - segment.base)
        if kind == ELLIPSE and size == ELLIPSE_BYTES:
            found.append(_read(data, at))
        at += 2
    return found


def _read(data: bytes, record: int) -> Ellipse:
    left, top, right, bottom = struct.unpack_from("<hhhh", data, record + 0x0F)
    return Ellipse(
        (left, top, right, bottom),
        data[record + 0x25],
        (data[record + 0x17], data[record + 0x18], data[record + 0x19]),
        (data[record + 0x1B], data[record + 0x1C], data[record + 0x1D]),
    )
