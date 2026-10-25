"""A class ``0x17`` pointer.

The record is 17 bytes. The word at ``+0x04`` is a near pointer to a
class ``0xA`` field in the same segment. That field is named ``Text``.
The page window does not paint this record.
"""

from __future__ import annotations

from dataclasses import dataclass

from opentoolbook.field import (
    FIELD,
    FIELD_BYTES,
    _chars,
    _name,
    _segments,
    _trailer,
    _u16,
)

CLASS = 0x17
# Measured length of a class 0x17 record.
CLASS_BYTES = 17


@dataclass(frozen=True)
class Class17Field:
    """The page, the near pointer at ``+0x04``, and the field's name."""

    page_id: str
    near: int
    name: str


def class_17_fields(data: bytes) -> tuple[Class17Field, ...]:
    """Each class ``0x17`` record whose ``+0x04`` names a ``Text`` field.

    A book with no such record returns an empty tuple.
    """
    found: list[Class17Field] = []
    for segment in _segments(data):
        end = segment.file_at + segment.size
        page = segment.base + 0x14
        page_id = ""
        if page >= 2 and _u16(data, page - 2) == 5:
            page_id = _chars(data, page + 6, 32)
        trailer = _trailer(data, segment)
        at = segment.base + 0x18
        while at + CLASS_BYTES <= end and at >= 4:
            kind = _u16(data, at - 2)
            size = _u16(data, at - 4) - (at - segment.base)
            if kind == CLASS and size == CLASS_BYTES:
                near = _u16(data, at + 4)
                target = segment.base + near
                if (
                    trailer is not None
                    and target >= 4
                    and target + FIELD_BYTES <= end
                    and _u16(data, target - 2) == FIELD
                    and _u16(data, target - 4) - near == FIELD_BYTES
                ):
                    found.append(Class17Field(page_id, near, _name(trailer, _u16(data, target + 6))))
                at += size
                continue
            at += 1
    return tuple(found)
