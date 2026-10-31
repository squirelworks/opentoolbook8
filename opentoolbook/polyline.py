"""A class ``0x13`` point list as the points stored in its record.

The count is the word at ``+0x2D``. The near pointer at ``+0x2F`` names
the points, four bytes each. The four signed words at ``+0x25`` are the
minimum x, the minimum y, the maximum x, and the maximum y of those
points. The points returned are the stored pairs. The page window
strokes them as an angled line.
"""

from __future__ import annotations

import struct
from dataclasses import dataclass

from opentoolbook.field import _segments, _u16

POLYLINE = 0x13
# Length shared by the class 0x13 records in 9e954d01.tbk.
POLYLINE_BYTES = 55


@dataclass(frozen=True)
class Polyline:
    points: tuple[tuple[int, int], ...]
    bounds: tuple[int, int, int, int]


def stored_polylines(data: bytes) -> tuple[Polyline, ...]:
    """Every class ``0x13`` record whose point list sits in its segment."""
    found: list[Polyline] = []
    for segment in _segments(data):
        end = segment.file_at + segment.size
        at = segment.base + 0x10
        while at + POLYLINE_BYTES <= end and at >= 4:
            kind = _u16(data, at - 2)
            size = _u16(data, at - 4) - (at - segment.base)
            if kind == POLYLINE and size == POLYLINE_BYTES:
                found.append(_read(data, segment, at))
            at += 2
    return tuple(found)


def _read(data: bytes, segment, record: int) -> Polyline:
    count = _u16(data, record + 0x2D)
    pointer = _u16(data, record + 0x2F)
    bounds = _rect(data, record + 0x25)
    origin = segment.base + pointer
    if count == 0 or origin < 0 or origin + 4 * count > segment.file_at + segment.size:
        raise ValueError("polyline points are past the segment")
    points = tuple(
        struct.unpack_from("<hh", data, origin + 4 * index) for index in range(count)
    )
    return Polyline(points, bounds)


def _rect(data: bytes, offset: int) -> tuple[int, int, int, int]:
    left, top, right, bottom = struct.unpack_from("<hhhh", data, offset)
    return left, top, right, bottom
