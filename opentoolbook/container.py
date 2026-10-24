"""A class ``0x0B`` rectangle as the union of the objects that name it.

The rectangle is the four signed words at ``+0x0F``. Another object in
the same segment names the record with the word at ``+0x04``. The
rectangle equals the union of those objects' own rectangles at ``+0x0F``.
"""

from __future__ import annotations

import struct
from dataclasses import dataclass

from opentoolbook.field import _segments, _u16

CONTAINER = 0x0B
# Measured length of a class 0x0B record.
CONTAINER_BYTES = 49
# Class and length of an object whose rectangle participates in the union.
_CHILD_BYTES = {
    0x08: 41,
    0x09: 43,
    0x0A: 61,
    0x0B: CONTAINER_BYTES,
    0x0C: 41,
    0x0D: 45,
    0x0E: 53,
    0x10: 53,
    0x11: 61,
    0x13: 55,
    0x19: 89,
}


@dataclass(frozen=True)
class Container:
    bounds: tuple[int, int, int, int]
    children: tuple[tuple[int, int, int, int], ...]


def stored_containers(data: bytes) -> tuple[Container, ...]:
    """Every 49-byte class ``0x0B`` record, with the rectangles of the objects that name it."""
    found: list[Container] = []
    for segment in _segments(data):
        end = segment.file_at + segment.size
        records: list[tuple[int, int]] = []
        at = segment.base + 0x10
        while at + 0x17 <= end and at >= 4:
            kind = _u16(data, at - 2)
            size = _u16(data, at - 4) - (at - segment.base)
            if kind in _CHILD_BYTES and size == _CHILD_BYTES[kind] and at + size <= end:
                records.append((at, kind))
            at += 2
        owners = {
            record - segment.base: record
            for record, kind in records
            if kind == CONTAINER
        }
        named: dict[int, list[tuple[int, int, int, int]]] = {near: [] for near in owners}
        for record, _kind in records:
            parent = _u16(data, record + 4)
            near = record - segment.base
            if parent in named and near != parent:
                named[parent].append(_rect(data, record + 0x0F))
        for near, record in owners.items():
            found.append(Container(_rect(data, record + 0x0F), tuple(named[near])))
    return tuple(found)


def _rect(data: bytes, offset: int) -> tuple[int, int, int, int]:
    left, top, right, bottom = struct.unpack_from("<hhhh", data, offset)
    return left, top, right, bottom
