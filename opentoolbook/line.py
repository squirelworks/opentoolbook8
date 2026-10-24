"""A class ``0x0E`` line as the two endpoints stored in its record.

The endpoints are the signed pairs at ``+0x26``. The four words at
``+0x0F`` are a rectangle around those points, and they are not the
line. The reader returns the stored endpoints.
"""

from __future__ import annotations

import struct
from dataclasses import dataclass

from opentoolbook.field import _segments, _u16

LINE = 0x0E
# Length shared by the class 0x0E records. Same length as a class 0x10 polygon.
LINE_BYTES = 53


@dataclass(frozen=True)
class Line:
    endpoints: tuple[tuple[int, int], tuple[int, int]]
    bounds: tuple[int, int, int, int]


def stored_lines(data: bytes) -> tuple[Line, ...]:
    """Every class ``0x0E`` record of this length. The points are the words at ``+0x26``."""
    found: list[Line] = []
    for segment in _segments(data):
        end = segment.file_at + segment.size
        at = segment.base + 0x10
        while at + LINE_BYTES <= end and at >= 4:
            kind = _u16(data, at - 2)
            size = _u16(data, at - 4) - (at - segment.base)
            if kind == LINE and size == LINE_BYTES:
                found.append(_read(data, at))
            at += 2
    return tuple(found)


def _read(data: bytes, record: int) -> Line:
    x1, y1, x2, y2 = struct.unpack_from("<hhhh", data, record + 0x26)
    left, top, right, bottom = struct.unpack_from("<hhhh", data, record + 0x0F)
    return Line(((x1, y1), (x2, y2)), (left, top, right, bottom))
