"""A class ``0x10`` polygon as the points stored in its record.

The count is the word at ``+0x30``. The near pointer at ``+0x32`` names
the points, four bytes each. Those points lie in the source rectangle,
four words at ``+0x28``. The bounds are four words at ``+0x0F``. The
points returned are the stored pairs.
"""

from __future__ import annotations

import struct
from dataclasses import dataclass

from opentoolbook.field import _book, _chars, _page_handles, _segments, _u16

POLYGON = 0x10
# Length shared by the class 0x10 records in 9e954d01.tbk.
POLYGON_BYTES = 53
# `draw polygon` in Instructor 8.1. Same point list, different class.
DRAW_POLYGON = 0x0F
PAGE = 5


@dataclass(frozen=True)
class Polygon:
    points: tuple[tuple[int, int], ...]
    source: tuple[int, int, int, int]
    bounds: tuple[int, int, int, int]


def stored_polygons(data: bytes) -> tuple[Polygon, ...]:
    """Every class ``0x10`` record whose point list sits in its segment."""
    return tuple(_of_class(data, POLYGON))


def stored_draw_polygons(data: bytes) -> tuple[Polygon, ...]:
    """Every class ``0x0F`` record of this length. The point list matches class ``0x10``."""
    return tuple(_of_class(data, DRAW_POLYGON))


def _of_class(data: bytes, kind_wanted: int) -> list[Polygon]:
    found: list[Polygon] = []
    for segment in _segments(data):
        end = segment.file_at + segment.size
        at = segment.base + 0x10
        while at + POLYGON_BYTES <= end and at >= 4:
            kind = _u16(data, at - 2)
            size = _u16(data, at - 4) - (at - segment.base)
            if kind == kind_wanted and size == POLYGON_BYTES:
                found.append(_read(data, segment, at))
            at += 2
    return found


def polygon_points(data: bytes, page_id: str, object_id: int) -> tuple[tuple[int, int], ...]:
    """Stored points of one polygon. The word at the start of the record is its id."""
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
        return _read(data, segment, found).points
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


def _read(data: bytes, segment, record: int) -> Polygon:
    count = _u16(data, record + 0x30)
    pointer = _u16(data, record + 0x32)
    source = _rect(data, record + 0x28)
    bounds = _rect(data, record + 0x0F)
    origin = segment.base + pointer
    if count == 0 or origin < 0 or origin + 4 * count > segment.file_at + segment.size:
        raise ValueError("polygon points are past the segment")
    points = tuple(
        struct.unpack_from("<hh", data, origin + 4 * index) for index in range(count)
    )
    return Polygon(points, source, bounds)


def _rect(data: bytes, offset: int) -> tuple[int, int, int, int]:
    left, top, right, bottom = struct.unpack_from("<hhhh", data, offset)
    return left, top, right, bottom


@dataclass(frozen=True)
class PolygonColor:
    """Colors stored beside the points.

    The bytes at ``+0x17`` are a color and the byte at ``+0x1A`` is 0.
    The bytes at ``+0x1B`` are a color and the byte at ``+0x1E`` is 0.
    The byte at ``+0x25`` is the pattern. The bounds are four signed
    words at ``+0x0F``.
    """

    bounds: tuple[int, int, int, int]
    pattern: int
    first_color: tuple[int, int, int]
    second_color: tuple[int, int, int]


def stored_polygon_colors(data: bytes) -> tuple[PolygonColor, ...]:
    """Every class ``0x10`` record of the shared length."""
    found: list[PolygonColor] = []
    for segment in _segments(data):
        end = segment.file_at + segment.size
        at = segment.base + 0x10
        while at + POLYGON_BYTES <= end and at >= 4:
            kind = _u16(data, at - 2)
            size = _u16(data, at - 4) - (at - segment.base)
            if kind == POLYGON and size == POLYGON_BYTES:
                found.append(_color(data, at))
            at += 2
    return tuple(found)


def _color(data: bytes, record: int) -> PolygonColor:
    return PolygonColor(
        _rect(data, record + 0x0F),
        data[record + 0x25],
        (data[record + 0x17], data[record + 0x18], data[record + 0x19]),
        (data[record + 0x1B], data[record + 0x1C], data[record + 0x1D]),
    )

