"""The characters stored in a field.

A field is class ``0xA``. The word at the record's ``+0x24`` is a near
pointer to a short block in that segment. Word 1 of the block is the
trailer handle of the text. The text is a capacity word, a length word,
and then the characters. The word at ``+0x42`` is not the text.
"""

from __future__ import annotations

import struct
from dataclasses import dataclass

from opentoolbook.record import Book

FIELD = 0xA
# Measured length of a class 0xA field. The copyright field on page P0 is one.
FIELD_BYTES = 61
PAGE = 5
BOOK = 1


@dataclass(frozen=True)
class _Segment:
    key: int
    file_at: int
    size: int
    flags: int

    @property
    def base(self) -> int:
        return self.file_at - 6


@dataclass(frozen=True)
class _Trailer:
    heaps: dict[int, bytes]
    slots: tuple[tuple[int, int, int, int], ...]


def page_ids(data: bytes) -> tuple[str, ...]:
    """Page ids from the same walk that finds P0. The id is the C string at record ``+6``."""
    segments = _segments(data)
    by_key = {segment.key: segment for segment in segments}
    book_segment, book_record = _book(data, segments)
    found: list[str] = []
    for handle in _page_handles(data, by_key, book_segment, book_record):
        segment = by_key.get(handle >> 16)
        if segment is None:
            continue
        record = segment.base + (handle & 0xFFFF)
        if record < 2 or record + 8 > len(data) or _u16(data, record - 2) != PAGE:
            continue
        found.append(_chars(data, record + 6, 32))
    return tuple(found)


def field_text(data: bytes, page_id: str, field_name: str) -> str:
    """Text of the named field on one page, from word 1 of the ``+0x24`` block."""
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
        trailer = _trailer(data, segment)
        for field in _fields(data, segment, record):
            if trailer is None or _name(trailer, _u16(data, field + 6)) != field_name:
                continue
            return _field_text(trailer, _u16(data, field + 0x24))
    raise ValueError(f"no {field_name} field on {page_id}")


def _segments(data: bytes) -> tuple[_Segment, ...]:
    book = Book(data)
    return tuple(
        _Segment(item.key, item.position, item.length, item.flags) for item in book.records
    )


def _book(data: bytes, segments: tuple[_Segment, ...]) -> tuple[_Segment, int]:
    for segment in segments:
        record = segment.base + 0x14
        if record >= 2 and record + 0x12 <= len(data) and _u16(data, record - 2) == BOOK:
            return segment, record
    raise ValueError("book record was not found")


def _page_handles(
    data: bytes,
    by_key: dict[int, _Segment],
    book_segment: _Segment,
    book_record: int,
) -> tuple[int, ...]:
    """Page references off book ``+0x10``. Each stored row is 13 bytes."""
    head = book_segment.base + _u16(data, book_record + 0x10)
    if head + 4 > len(data):
        raise ValueError("page list is past the file")
    children = _u16(data, head + 2)
    found: list[int] = []
    for child in range(children):
        at = head + 4 + 8 * child
        if at + 8 > len(data):
            break
        _flags, count, ref = struct.unpack_from("<HHI", data, at)
        segment = by_key.get(ref >> 16)
        if segment is None:
            continue
        record = segment.base + (ref & 0xFFFF)
        if record + 5 > len(data):
            continue
        total = _u16(data, record + 3)
        rows = min(count or total, total)
        for index in range(rows):
            row = record + 5 + 13 * index
            if row + 13 > len(data):
                break
            _background, _page_id, page, _zero = struct.unpack_from("<IIIB", data, row)
            found.append(page)
    return tuple(found)


def _fields(data: bytes, segment: _Segment, page_record: int) -> tuple[int, ...]:
    parent = page_record - segment.base
    end = segment.file_at + segment.size
    at = segment.base + 0x18
    found: list[int] = []
    while at + FIELD_BYTES <= end and at >= 4:
        kind = _u16(data, at - 2)
        size = _u16(data, at - 4) - (at - segment.base)
        if kind == FIELD and size == FIELD_BYTES and _u16(data, at + 4) == parent:
            found.append(at)
            at += size
            continue
        at += 1
    return tuple(found)


def _trailer(data: bytes, segment: _Segment) -> _Trailer | None:
    if not segment.flags & 0x4000:
        return None
    off = segment.file_at + segment.size
    if off + 4 > len(data) or _u16(data, off) != 1:
        return None
    count = _u16(data, off + 2)
    pos = off + 4
    headers: list[tuple[int, int, int, int, int]] = []
    for _index in range(count):
        if pos + 12 > len(data):
            return None
        headers.append(struct.unpack_from("<HHIHH", data, pos))
        pos += 12
    heaps = {0: b"\x00" * 6 + data[segment.file_at:segment.file_at + segment.size]}
    for index, (_mark, prefix, length, _rest, _tail) in enumerate(headers):
        if pos + length > len(data):
            return None
        blob = data[pos:pos + length]
        pos += length
        if length:
            heaps[index + 1] = b"\x00" * prefix + blob
    if pos + 4 > len(data) or _u16(data, pos) != 1:
        return None
    first = _u16(data, pos + 2)
    pos += 4 + 4 * first
    if pos + 2 > len(data):
        return None
    slots_n = _u16(data, pos)
    pos += 2
    if pos + 8 * slots_n > len(data):
        return None
    slots = tuple(struct.unpack_from("<HHHH", data, pos + 8 * index) for index in range(slots_n))
    return _Trailer(heaps, slots)


def _field_text(trailer: _Trailer, pointer: int) -> str:
    heap = trailer.heaps.get(0)
    if heap is None or pointer + 4 > len(heap):
        return ""
    _runs, handle = struct.unpack_from("<HH", heap, pointer)
    raw = _item(trailer, handle)
    if len(raw) < 4:
        return ""
    _capacity, length = struct.unpack_from("<HH", raw, 0)
    if length > len(raw) - 4:
        return ""
    return raw[4:4 + length].decode("latin-1")


def _name(trailer: _Trailer, handle: int) -> str:
    raw = _item(trailer, handle)
    return raw.split(b"\x00", 1)[0].decode("latin-1")


def _item(trailer: _Trailer, handle: int) -> bytes:
    if handle in (0, 0xFFFF) or handle >= len(trailer.slots):
        return b""
    heap_id, offset, _one, _two = trailer.slots[handle]
    blob = trailer.heaps.get(heap_id)
    if blob is None or offset >= len(blob):
        return b""
    end = _u16(blob, offset - 6) if offset >= 6 else offset + 64
    if end <= offset or end > len(blob):
        end = min(len(blob), offset + 64)
    return blob[offset:end]


def _chars(data: bytes, offset: int, limit: int) -> str:
    raw = data[offset:offset + limit]
    end = raw.find(b"\x00")
    if end >= 0:
        raw = raw[:end]
    return raw.decode("latin-1")


def _u16(data: bytes, offset: int) -> int:
    return struct.unpack_from("<H", data, offset)[0]
