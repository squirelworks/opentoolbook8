"""The points stored on a class ``0x11`` arc.

They are the signed pairs at ``+0x25`` and ``+0x29``, and a third pair at
``+0x2D``. The words at ``+0x31`` and ``+0x33`` are the half-width and
half-height of the ellipse those pairs sit on. The third pair is that
ellipse's center. Arcs with different bounds reuse the same three pairs
and the same two radii, so the pairs are not page positions.

The page vertices are the first two pairs mapped through the bounds at
``+0x0F``: the bounds center is the image of the third pair, and each
axis scales by the bounds half-size over the stored radius. The window
strokes the open arc of that ellipse from the first mapped point to the
second, counter-clockwise. The arc is not filled.
"""

from __future__ import annotations

import math
import struct
from dataclasses import dataclass

from opentoolbook.field import _book, _chars, _page_handles, _segments, _u16

ARC = 0x11
# Measured length of a class 0x11 record. P1140 object 80 is one.
ARC_BYTES = 61
PAGE = 5


@dataclass(frozen=True)
class Arc:
    """One class ``0x11`` record: bounds, three prototype pairs, and two radii."""

    object_id: int
    bounds: tuple[int, int, int, int]
    points: tuple[tuple[int, int], tuple[int, int], tuple[int, int]]
    radii: tuple[int, int]


def stored_arcs(data: bytes) -> tuple[Arc, ...]:
    """Every class ``0x11`` record of the measured length, in stored order."""
    found: list[Arc] = []
    for segment in _segments(data):
        end = segment.file_at + segment.size
        at = segment.base + 0x18
        while at + ARC_BYTES <= end and at >= 4:
            kind = _u16(data, at - 2)
            size = _u16(data, at - 4) - (at - segment.base)
            if kind == ARC and size == ARC_BYTES:
                found.append(_arc_record(data, at))
                at += size
                continue
            at += 1
    return tuple(found)


def _arc_record(data: bytes, at: int) -> Arc:
    return Arc(
        _u16(data, at),
        struct.unpack_from("<hhhh", data, at + 0x0F),
        (
            struct.unpack_from("<hh", data, at + 0x25),
            struct.unpack_from("<hh", data, at + 0x29),
            struct.unpack_from("<hh", data, at + 0x2D),
        ),
        struct.unpack_from("<hh", data, at + 0x31),
    )


def page_vertices(arc: Arc) -> tuple[tuple[int, int], tuple[int, int]]:
    """The two page endpoints: prototype pairs mapped onto ``bounds``."""
    left, top, right, bottom = arc.bounds
    center_x = (left + right) / 2
    center_y = (top + bottom) / 2
    radius_x = (right - left) / 2
    radius_y = (bottom - top) / 2
    proto_x, proto_y = arc.radii
    origin_x, origin_y = arc.points[2]
    scale_x = radius_x / proto_x
    scale_y = radius_y / proto_y

    def mapped(point: tuple[int, int]) -> tuple[int, int]:
        x = center_x + (point[0] - origin_x) * scale_x
        y = center_y + (point[1] - origin_y) * scale_y
        return round(x), round(y)

    return mapped(arc.points[0]), mapped(arc.points[1])


def arc_angles(
    bounds: tuple[int, int, int, int],
    start: tuple[int, int],
    end: tuple[int, int],
) -> tuple[float, float]:
    """Tk ``start`` and counter-clockwise ``extent`` for the mapped endpoints.

    Angles are measured as if the oval were a circle, then stretched to the
    bounds — the same rule Tk's ``create_arc`` uses.
    """
    left, top, right, bottom = bounds
    center_x = (left + right) / 2
    center_y = (top + bottom) / 2
    radius_x = (right - left) / 2
    radius_y = (bottom - top) / 2
    if radius_x == 0 or radius_y == 0:
        return 0.0, 0.0

    def theta(point: tuple[int, int]) -> float:
        return math.degrees(
            math.atan2((center_y - point[1]) / radius_y, (point[0] - center_x) / radius_x)
        )

    start_angle = theta(start)
    extent = (theta(end) - start_angle) % 360.0
    return start_angle, extent


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
