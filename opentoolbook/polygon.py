"""A class ``0x10`` polygon, placed on its bounds.

The count is the word at ``+0x30``. The near pointer at ``+0x32`` names
the points, four bytes each. The source rectangle is four words at
``+0x28`` and the bounds are four words at ``+0x0F``. A point moves by

``x' = (x - src.left) * dstW / srcW + dst.left``

and the same for y. The result is those points. It is not the bounds
rectangle.
"""

from __future__ import annotations

import struct

from opentoolbook.field import _book, _chars, _page_handles, _segments, _u16

POLYGON = 0x10
# Measured length of a class 0x10 record. P430 object 136 is one.
POLYGON_BYTES = 53
PAGE = 5


def polygon_points(data: bytes, page_id: str, object_id: int) -> tuple[tuple[int, int], ...]:
    """Mapped points of one polygon. The word at the start of the record is its id."""
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
        found = _polygon(data, segment, object_id)
        if found is None:
            break
        return _place(data, segment, found)
    raise ValueError(f"no polygon {object_id} on {page_id}")


def _polygon(data: bytes, segment, object_id: int) -> int | None:
    end = segment.file_at + segment.size
    at = segment.base + 0x18
    while at + POLYGON_BYTES <= end and at >= 4:
        kind = _u16(data, at - 2)
        size = _u16(data, at - 4) - (at - segment.base)
        if kind == POLYGON and size == POLYGON_BYTES:
            if _u16(data, at) == object_id:
                return at
            at += size
            continue
        at += 1
    return None


def _place(data: bytes, segment, record: int) -> tuple[tuple[int, int], ...]:
    count = _u16(data, record + 0x30)
    pointer = _u16(data, record + 0x32)
    source = _rect(data, record + 0x28)
    bounds = _rect(data, record + 0x0F)
    src_w = source[2] - source[0]
    src_h = source[3] - source[1]
    dst_w = bounds[2] - bounds[0]
    dst_h = bounds[3] - bounds[1]
    if src_w == 0 or src_h == 0:
        raise ValueError("polygon source rectangle has no area")
    origin = segment.base + pointer
    if count == 0 or origin < 0 or origin + 4 * count > segment.file_at + segment.size:
        raise ValueError("polygon points are past the segment")
    points: list[tuple[int, int]] = []
    for index in range(count):
        x, y = struct.unpack_from("<hh", data, origin + 4 * index)
        points.append((
            _muldiv(x - source[0], dst_w, src_w) + bounds[0],
            _muldiv(y - source[1], dst_h, src_h) + bounds[1],
        ))
    return tuple(points)


def _rect(data: bytes, offset: int) -> tuple[int, int, int, int]:
    left, top, right, bottom = struct.unpack_from("<hhhh", data, offset)
    return left, top, right, bottom


def _muldiv(delta: int, dst_span: int, src_span: int) -> int:
    """Truncating ``delta * dst_span / src_span``."""
    numerator = delta * dst_span
    negative = (numerator < 0) != (src_span < 0)
    value = abs(numerator) // abs(src_span)
    return -value if negative else value
