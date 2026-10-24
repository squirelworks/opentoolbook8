"""The characters stored in a field, and the runs stored beside them.

A field is class ``0xA``. The word at the record's ``+0x24`` is a near
pointer to a short block in that segment. Word 1 of the block is the
trailer handle of the text. The text is a capacity word, a length word,
and then the characters. The word at ``+0x42`` is not the text. Word 0
is a trailer handle to a run list: the second word there is a count,
then that many 11-byte runs.
"""

from __future__ import annotations

import struct
from dataclasses import dataclass

from opentoolbook.record import Book

FIELD = 0xA
# Measured length of a class 0xA field. The copyright field on page P0 is one.
FIELD_BYTES = 61
# One style run. The count word is at byte 2 of the run block; the runs follow it.
RUN_BYTES = 11
PAGE = 5
BOOK = 1


@dataclass(frozen=True)
class FieldStyle:
    """Text from word 1 of the ``+0x24`` block, and the runs from word 0."""

    text: str
    runs: tuple[bytes, ...]


@dataclass(frozen=True)
class StyleNames:
    """C strings named by the word at byte 2 of each style run.

    ``base`` is the book segment base. ``table`` is the file offset of the
    pointer list at the book record's ``+0x28``. ``names`` lines up with
    ``field_style_runs``: ``None`` where that word is 1.
    """

    base: int
    table: int
    names: tuple[tuple[str | None, ...], ...]


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


@dataclass(frozen=True)
class FieldTextPlace:
    """The file bytes of one field's text, and the directory body beside them.

    ``body`` is the directory body. ``gap`` is the first byte after it.
    ``at`` is the capacity word of the text record. ``text`` is the characters
    that follow the length word.
    """

    page_id: str
    name: str
    body: int
    gap: int
    at: int
    text: str


def field_text_places(data: bytes) -> tuple[FieldTextPlace, ...]:
    """Where each field's text record sits.

    Word 1 of the block at ``+0x24`` names the record. The record is a
    capacity word, a length word, and the characters. On a page that record
    is in the gap after the directory body.
    """
    found: list[FieldTextPlace] = []
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
        trailer = _trailer(data, segment)
        blobs = _gap_blobs(data, segment)
        if trailer is None or not blobs:
            continue
        page_id = _chars(data, record + 6, 32)
        gap = segment.file_at + segment.size
        end = gap
        at = segment.base + 0x18
        while at + FIELD_BYTES <= end and at >= 4:
            kind = _u16(data, at - 2)
            size = _u16(data, at - 4) - (at - segment.base)
            if kind == FIELD and size == FIELD_BYTES:
                place = _text_place(data, segment, trailer, blobs, page_id, at)
                if place is not None:
                    found.append(place)
                at += size
                continue
            at += 1
    return tuple(found)


def field_bounds(data: bytes, page_id: str, field_name: str) -> tuple[int, int, int, int]:
    """The four signed words at ``+0x0F`` of the named field.

    They are a rectangle. The text at ``+0x24`` is not this rectangle.
    """
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
            return _bounds(data, field)
    raise ValueError(f"no {field_name} field on {page_id}")


def stored_field_bounds(data: bytes) -> tuple[tuple[int, int, int, int], ...]:
    """The rectangle at ``+0x0F`` of every class ``0xA`` field of this length."""
    found: list[tuple[int, int, int, int]] = []
    for segment in _segments(data):
        end = segment.file_at + segment.size
        at = segment.base + 0x18
        while at + FIELD_BYTES <= end and at >= 4:
            kind = _u16(data, at - 2)
            size = _u16(data, at - 4) - (at - segment.base)
            if kind == FIELD and size == FIELD_BYTES:
                found.append(_bounds(data, at))
                at += size
                continue
            at += 1
    return tuple(found)


def _bounds(data: bytes, record: int) -> tuple[int, int, int, int]:
    left, top, right, bottom = struct.unpack_from("<hhhh", data, record + 0x0F)
    return left, top, right, bottom


def field_words(data: bytes) -> tuple[tuple[int, int, int, int, int], ...]:
    """The words at ``+0x28``, ``+0x2A``, ``+0x2C``, and ``+0x32``, and the byte at ``+0x36``.

    One tuple per class ``0xA`` field of the shared length, in the order
    the records are stored.
    """
    found: list[tuple[int, int, int, int, int]] = []
    for segment in _segments(data):
        end = segment.file_at + segment.size
        at = segment.base + 0x18
        while at + FIELD_BYTES <= end and at >= 4:
            kind = _u16(data, at - 2)
            size = _u16(data, at - 4) - (at - segment.base)
            if kind == FIELD and size == FIELD_BYTES:
                found.append((
                    _u16(data, at + 0x28),
                    _u16(data, at + 0x2A),
                    _u16(data, at + 0x2C),
                    _u16(data, at + 0x32),
                    data[at + 0x36],
                ))
                at += size
                continue
            at += 1
    return tuple(found)


def field_style_runs(data: bytes) -> tuple[FieldStyle, ...]:
    """Runs named by word 0 of the block at record ``+0x24``.

    That word is a trailer handle. The second word of the run list is a
    count, and each run is the next 11 bytes, read from the heap for the
    whole count. The first word of a run is an offset into the field text.
    """
    found: list[FieldStyle] = []
    for segment in _segments(data):
        trailer = _trailer(data, segment)
        if trailer is None:
            continue
        end = segment.file_at + segment.size
        at = segment.base + 0x18
        while at + FIELD_BYTES <= end and at >= 4:
            kind = _u16(data, at - 2)
            size = _u16(data, at - 4) - (at - segment.base)
            if kind == FIELD and size == FIELD_BYTES:
                pointer = _u16(data, at + 0x24)
                runs = _style_runs(trailer, pointer)
                if runs:
                    found.append(FieldStyle(_field_text(trailer, pointer), runs))
                at += size
                continue
            at += 1
    return tuple(found)


def style_run_names(data: bytes) -> StyleNames:
    """The C string named by the word at byte 2 of each style run.

    The word 1 is not an entry. Any other word is a near pointer in the
    list at the book record's ``+0x28``, and the bytes at that pointer
    are a C string.
    """
    base, table, pointers = _name_table(data)
    known = set(pointers)
    rows: list[tuple[str | None, ...]] = []
    for item in field_style_runs(data):
        row: list[str | None] = []
        for run in item.runs:
            word = _u16(run, 2)
            if word == 1 or word not in known:
                row.append(None)
                continue
            row.append(_cstring(data, base + word))
        rows.append(tuple(row))
    return StyleNames(base, table, tuple(rows))


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


def _gap_blobs(data: bytes, segment: _Segment) -> tuple[tuple[int, int, int], ...]:
    """Heap id, file offset, and prefix of each blob after the directory body."""
    off = segment.file_at + segment.size
    if off + 4 > len(data) or _u16(data, off) != 1:
        return ()
    count = _u16(data, off + 2)
    pos = off + 4
    headers: list[tuple[int, int, int, int, int]] = []
    for _index in range(count):
        if pos + 12 > len(data):
            return ()
        headers.append(struct.unpack_from("<HHIHH", data, pos))
        pos += 12
    blobs: list[tuple[int, int, int]] = []
    for index, (_mark, prefix, length, _rest, _tail) in enumerate(headers):
        blobs.append((index + 1, pos, prefix))
        if pos + length > len(data):
            return ()
        pos += length
    return tuple(blobs)


def _text_place(
    data: bytes,
    segment: _Segment,
    trailer: _Trailer,
    blobs: tuple[tuple[int, int, int], ...],
    page_id: str,
    field: int,
) -> FieldTextPlace | None:
    heap = trailer.heaps.get(0)
    pointer = _u16(data, field + 0x24)
    if heap is None or pointer + 4 > len(heap):
        return None
    _runs, handle = struct.unpack_from("<HH", heap, pointer)
    if handle in (0, 0xFFFF) or handle >= len(trailer.slots):
        return None
    heap_id, offset, _one, _two = trailer.slots[handle]
    if heap_id == 0:
        at = segment.file_at + (offset - 6)
    else:
        at = None
        for blob_id, start, prefix in blobs:
            if blob_id == heap_id:
                at = start + (offset - prefix)
                break
        if at is None:
            return None
    if at < 0 or at + 4 > len(data):
        return None
    _capacity, length = struct.unpack_from("<HH", data, at)
    if length == 0 or at + 4 + length > len(data):
        return None
    text = data[at + 4:at + 4 + length].decode("latin-1")
    return FieldTextPlace(
        page_id,
        _name(trailer, _u16(data, field + 6)),
        segment.file_at,
        segment.file_at + segment.size,
        at,
        text,
    )


def _name_table(data: bytes) -> tuple[int, int, tuple[int, ...]]:
    """Book segment base, file offset of the ``+0x28`` list, and its pointers."""
    segments = _segments(data)
    segment, record = _book(data, segments)
    table = segment.base + _u16(data, record + 0x28)
    if table + 2 > len(data):
        return segment.base, table, ()
    count = _u16(data, table)
    if table + 4 + 2 * count > len(data):
        return segment.base, table, ()
    pointers = tuple(_u16(data, table + 4 + 2 * index) for index in range(count))
    return segment.base, table, pointers


def _cstring(data: bytes, offset: int) -> str | None:
    if offset < 0 or offset >= len(data):
        return None
    end = data.find(b"\x00", offset, offset + 64)
    if end <= offset:
        return None
    raw = data[offset:end]
    if any(byte < 32 or byte > 126 for byte in raw):
        return None
    return raw.decode("latin-1")


def _style_runs(trailer: _Trailer, pointer: int) -> tuple[bytes, ...]:
    """The runs named by word 0 of the field block.

    ``_item`` takes its end from the word at ``offset - 6`` and otherwise
    keeps 64 bytes. That cut a run list short of its count, so the bytes
    here are ``count * 11`` from the heap.
    """
    heap = trailer.heaps.get(0)
    if heap is None or pointer + 4 > len(heap):
        return ()
    handle = _u16(heap, pointer)
    if handle in (0, 0xFFFF) or handle >= len(trailer.slots):
        return ()
    heap_id, offset, _one, _two = trailer.slots[handle]
    blob = trailer.heaps.get(heap_id)
    if blob is None or offset + 4 > len(blob):
        return ()
    count = _u16(blob, offset + 2)
    start = offset + 4
    need = count * RUN_BYTES
    if count == 0 or start + need > len(blob):
        return ()
    raw = blob[start:start + need]
    return tuple(raw[index:index + RUN_BYTES] for index in range(0, need, RUN_BYTES))


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
