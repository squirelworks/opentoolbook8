"""The records stored on one page.

The background is the class 4 record named by the far reference at
``+0x47``. An object is on the page when the word at ``+0x04`` is that
page's near offset. Those objects are returned in the order the records
are stored. A class ``0x0B`` group's children are the objects whose word
at ``+0x04`` names the group, in the order of the 10-byte entries at
``+0x2E``.

A class ``0x17`` hotword is 17 bytes, and its word at ``+0x04`` names a
class ``0xA`` field. The walk returns a field's hotwords as that field's
children, in stored order. A hotword is not on the page by itself.

Class ``0x12`` pies are on the walk. A record whose end word is 1 is the
last object in its directory record and runs to the end of that record;
the pie fixture's second pie is one. A pie carries its stored words.
"""

from __future__ import annotations

from dataclasses import dataclass

from opentoolbook.background import Background, background
from opentoolbook.field import (
    _book,
    _chars,
    _name,
    _page_handles,
    _segments,
    _trailer,
    _u16,
)
from opentoolbook.pie import PIE, PIE_BYTES, pie_words

PAGE = 5
FIELD = 0x0A
GROUP = 0x0B
HOTWORD = 0x17
# Class and length of a record the walk can name. Each length repeats.
LAYER = 0x06
LAYER_BYTES = 15

_BYTES = {
    0x08: 41,
    0x09: 43,
    0x0A: 61,
    0x0B: 49,
    0x0C: 41,
    0x0D: 45,
    0x0E: 53,
    0x10: 53,
    0x11: 61,
    PIE: PIE_BYTES,
    0x13: 55,
    0x15: 89,
    HOTWORD: 17,
    0x19: 89,
}


@dataclass(frozen=True)
class PageObject:
    """One stored object. ``near`` is the offset the child list records."""

    kind: int
    object_id: int
    name: str
    near: int
    children: tuple[PageObject, ...] = ()
    words: tuple[int, ...] = ()


@dataclass(frozen=True)
class PageRecords:
    """The background a page names, then the objects stored on that page."""

    background: Background
    objects: tuple[PageObject, ...]


def page_records(data: bytes, page_id: str) -> PageRecords:
    """Background, page objects, and each group's stored children."""
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
        return PageRecords(
            background(data, page_id),
            _stored(data, segment, record - segment.base),
        )
    raise ValueError(f"no page {page_id}")


def _stored(data: bytes, segment, page_near: int) -> tuple[PageObject, ...]:
    found = _objects(data, segment)
    by_near = {at - segment.base: (at, kind) for at, kind in found}
    trailer = _trailer(data, segment)
    return tuple(
        _object(data, segment, trailer, by_near, at, kind)
        for at, kind in found
        if _u16(data, at + 4) == page_near
    )


def _objects(data: bytes, segment) -> list[tuple[int, int]]:
    end = segment.file_at + segment.size
    at = segment.base + 0x18
    found: list[tuple[int, int]] = []
    while at + 6 <= end and at >= 4:
        kind = _u16(data, at - 2)
        size = _u16(data, at - 4) - (at - segment.base)
        if kind in _BYTES and size == _BYTES[kind] and at + size <= end:
            found.append((at, kind))
            at += size
            continue
        # The last object stores 1 as its end word and runs to the end of the record.
        if kind in _BYTES and _u16(data, at - 4) == 1 and end + 1 - at == _BYTES[kind]:
            found.append((at, kind))
            break
        at += 1
    return found


def _object(data, segment, trailer, by_near, at: int, kind: int) -> PageObject:
    near = at - segment.base
    children: tuple[PageObject, ...] = ()
    if kind == GROUP:
        nested: list[PageObject] = []
        for child_near in _child_nears(data, segment, at):
            child = by_near.get(child_near)
            if child is None or _u16(data, child[0] + 4) != near:
                continue
            nested.append(_object(data, segment, trailer, by_near, child[0], child[1]))
        children = tuple(nested)
    elif kind == FIELD:
        children = tuple(
            _object(data, segment, trailer, by_near, hot_at, hot_kind)
            for hot_at, hot_kind in by_near.values()
            if hot_kind == HOTWORD and _u16(data, hot_at + 4) == near
        )
    words = pie_words(data, at) if kind == PIE else ()
    return PageObject(kind, _u16(data, at), _object_name(data, trailer, at), near, children, words)


def layer_nears(data: bytes, segment, trailer, parent: int) -> tuple[int, ...]:
    """The nears of a page's or background's objects, back to front.

    A class ``0x06`` record of 15 bytes whose word at ``+0x08`` is the
    parent near holds the count at ``+0x02`` and, at ``+0x0C``, a trailer
    handle. The handle's item is that many near words. Empty when no such
    record or item is stored.
    """
    if trailer is None:
        return ()
    end = segment.file_at + segment.size
    at = segment.base + 0x18
    while at + LAYER_BYTES <= end and at >= 4:
        if (
            _u16(data, at - 2) == LAYER
            and _u16(data, at - 4) - (at - segment.base) == LAYER_BYTES
            and _u16(data, at + 0x08) == parent
        ):
            return _handle_words(trailer, _u16(data, at + 0x0C), _u16(data, at + 0x02))
        at += 1
    return ()


def _handle_words(trailer, handle: int, count: int) -> tuple[int, ...]:
    if handle >= len(trailer.slots):
        return ()
    heap_id, offset, _one, _two = trailer.slots[handle]
    blob = trailer.heaps.get(heap_id)
    if blob is None or offset + 2 * count > len(blob):
        return ()
    return tuple(_u16(blob, offset + 2 * index) for index in range(count))


def _child_nears(data: bytes, segment, record: int) -> tuple[int, ...]:
    count = _u16(data, record + 0x24)
    pointer = _u16(data, record + 0x2E)
    end = segment.file_at + segment.size
    found: list[int] = []
    for index in range(count):
        at = segment.base + pointer + 10 * index
        if at + 2 > end:
            break
        found.append(_u16(data, at))
    return tuple(found)


def _object_name(data: bytes, trailer, at: int) -> str:
    if trailer is None:
        return ""
    handle = _u16(data, at + 6)
    if handle in (0, 0xFFFF):
        return ""
    return _name(trailer, handle)
