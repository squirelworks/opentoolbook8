"""A class ``0x8`` record's colors and pattern.

The bytes at ``+0x17``, ``+0x18``, and ``+0x19`` are a color. The byte at
``+0x1A`` is 0. The bytes at ``+0x1B``, ``+0x1C``, and ``+0x1D`` are a
color. The byte at ``+0x1E`` is 0. The byte at ``+0x25`` is the pattern.
The bounds are four signed words at ``+0x0F``.
"""

from __future__ import annotations

import struct
from dataclasses import dataclass

from opentoolbook.field import _segments, _u16

RECTANGLE = 0x8
# Length shared by the class 0x8 records in 9e954d01.tbk.
RECTANGLE_BYTES = 41


@dataclass(frozen=True)
class Rectangle:
    bounds: tuple[int, int, int, int]
    pattern: int
    first_color: tuple[int, int, int]
    second_color: tuple[int, int, int]


def stored_rectangles(data: bytes) -> tuple[Rectangle, ...]:
    """Every class ``0x8`` record of the shared length."""
    found: list[Rectangle] = []
    for segment in _segments(data):
        end = segment.file_at + segment.size
        at = segment.base + 0x10
        while at + RECTANGLE_BYTES <= end and at >= 4:
            kind = _u16(data, at - 2)
            size = _u16(data, at - 4) - (at - segment.base)
            if kind == RECTANGLE and size == RECTANGLE_BYTES:
                found.append(_read(data, at))
            at += 2
    return tuple(found)


def _read(data: bytes, record: int) -> Rectangle:
    left, top, right, bottom = struct.unpack_from("<hhhh", data, record + 0x0F)
    return Rectangle(
        (left, top, right, bottom),
        data[record + 0x25],
        (data[record + 0x17], data[record + 0x18], data[record + 0x19]),
        (data[record + 0x1B], data[record + 0x1C], data[record + 0x1D]),
    )
