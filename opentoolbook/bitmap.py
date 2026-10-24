"""A button bitmap in the huge table.

The type-1 directory entry's fourth word is the resource id. A class
``0x09`` button names a picture by the stored id, which is that resource
id plus one. The word at record ``+0x28`` is a near pointer to a graphics
block that starts with ``0x0202``, and the stored id is the unaligned
word at byte ``0x15`` of the block. When the resource marks itself as
huge, the word at ``+9`` is a 1-based row of the table at header ``+0x104``. The
row's third dword is the file offset of an 8-byte prefix, and the ``BM``
file begins on the next byte. Width, height, and depth come from that
file's info header.
"""

from __future__ import annotations

import struct
from dataclasses import dataclass

from opentoolbook.field import (
    _book,
    _chars,
    _name,
    _page_handles,
    _segments,
    _trailer,
)
from opentoolbook.record import Book

BITMAP_TYPE = 1
BUTTON = 0x09
BUTTON_BYTES = 43
PAGE = 5


@dataclass(frozen=True)
class Bitmap:
    resource_id: int
    stored_id: int
    offset: int
    width: int
    height: int
    bpp: int


def button_bitmap(data: bytes, resource_id: int) -> Bitmap:
    """The huge-table bitmap for one resource id."""
    book = Book(data)
    records = {item.key: item for item in book.records}
    directory = _u32(data, book.header + 8 + (BITMAP_TYPE + 5) * 4)
    body = _resolve(records, directory)
    count = _u16(data, body + 2)
    table = _resolve(records, (directory & 0xFFFF0000) | _u16(data, body + 0x0E))
    resource = None
    for index in range(count):
        entry = table + index * 8
        if entry + 8 > len(data):
            break
        _first, near, segment, ident = struct.unpack_from("<HHHH", data, entry)
        if ident == resource_id:
            resource = _resolve(records, (segment << 16) | near)
            break
    if resource is None:
        raise ValueError(f"no bitmap resource {resource_id}")
    if data[resource + 8] & 1 == 0:
        raise ValueError(f"bitmap {resource_id} is not in the huge table")
    row_number = _u16(data, resource + 9)
    offset = _huge_offset(data, book.header, row_number)
    if data[offset + 8:offset + 10] != b"BM":
        raise ValueError(f"bitmap {resource_id} has no BM file")
    info = offset + 0x16
    if _u32(data, info) < 40:
        raise ValueError(f"bitmap {resource_id} info header is short")
    width, height = struct.unpack_from("<ii", data, info + 4)
    bpp = _u16(data, info + 14)
    return Bitmap(resource_id, resource_id + 1, offset, width, height, bpp)


def button_picture_ids(data: bytes) -> tuple[int, ...]:
    """Stored picture id of every button whose graphics block starts ``0x0202``.

    A zero pointer at ``+0x28`` is a button with no picture. The id is a
    type-1 resource id plus one.
    """
    found: list[int] = []
    for segment in _segments(data):
        end = segment.file_at + segment.size
        at = segment.base + 0x10
        while at + BUTTON_BYTES <= end and at >= 4:
            kind = _u16(data, at - 2)
            size = _u16(data, at - 4) - (at - segment.base)
            if kind == BUTTON and size == BUTTON_BYTES:
                pointer = _u16(data, at + 0x28)
                origin = segment.base + pointer
                if pointer and origin + 0x17 <= end and _u16(data, origin) == 0x0202:
                    found.append(_u16(data, origin + 0x15))
            at += 2
    return tuple(found)


def button_checked_picture(data: bytes, page_id: str, button_name: str) -> int:
    """The unaligned word at byte ``0x4b`` of the named button's graphics block.

    It is a type-1 resource id plus one, or 0 when that button has no
    checked picture. The picture id at byte ``0x15`` is not this word.
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
        parent = record - segment.base
        for button in _buttons(data, segment):
            if _u16(data, button + 4) != parent:
                continue
            if trailer is None or _name(trailer, _u16(data, button + 6)) != button_name:
                continue
            word = _graphic_word(data, segment, button, 0x4B)
            if word is None:
                raise ValueError(f"{button_name} on {page_id} has no graphics block")
            return word
    raise ValueError(f"no {button_name} button on {page_id}")


def button_checked_ids(data: bytes) -> tuple[int, ...]:
    """Checked picture id of every button whose graphics block starts ``0x0202``.

    The id is the unaligned word at byte ``0x4b``. Zero is no checked
    picture. A nonzero id is a type-1 resource id plus one.
    """
    found: list[int] = []
    for segment in _segments(data):
        for button in _buttons(data, segment):
            word = _graphic_word(data, segment, button, 0x4B)
            if word is not None:
                found.append(word)
    return tuple(found)


def button_invert_picture(data: bytes, page_id: str, button_name: str) -> int:
    """The unaligned word at byte ``0x27`` of the named button's graphics block.

    It is a type-1 resource id plus one, or 0 when that button has no
    invert picture. The border byte at the button record's ``+0x27`` is
    not this word.
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
        parent = record - segment.base
        for button in _buttons(data, segment):
            if _u16(data, button + 4) != parent:
                continue
            if trailer is None or _name(trailer, _u16(data, button + 6)) != button_name:
                continue
            word = _graphic_word(data, segment, button, 0x27)
            if word is None:
                raise ValueError(f"{button_name} on {page_id} has no graphics block")
            return word
    raise ValueError(f"no {button_name} button on {page_id}")


def button_invert_ids(data: bytes) -> tuple[int, ...]:
    """Invert picture id of every button whose graphics block starts ``0x0202``.

    The id is the unaligned word at byte ``0x27`` of the block. Zero is no
    invert picture. A nonzero id is a type-1 resource id plus one.
    """
    found: list[int] = []
    for segment in _segments(data):
        for button in _buttons(data, segment):
            word = _graphic_word(data, segment, button, 0x27)
            if word is not None:
                found.append(word)
    return tuple(found)


def button_disabled_picture(data: bytes, page_id: str, button_name: str) -> int:
    """The unaligned word at byte ``0x39`` of the named button's graphics block.

    It is a type-1 resource id plus one, or 0 when that button has no
    disabled picture. The checked picture at byte ``0x4b`` is not this word.
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
        parent = record - segment.base
        for button in _buttons(data, segment):
            if _u16(data, button + 4) != parent:
                continue
            if trailer is None or _name(trailer, _u16(data, button + 6)) != button_name:
                continue
            word = _graphic_word(data, segment, button, 0x39)
            if word is None:
                raise ValueError(f"{button_name} on {page_id} has no graphics block")
            return word
    raise ValueError(f"no {button_name} button on {page_id}")


def button_disabled_ids(data: bytes) -> tuple[int, ...]:
    """Disabled picture id of every button whose graphics block starts ``0x0202``.

    The id is the unaligned word at byte ``0x39`` of the block. Zero is no
    disabled picture. A nonzero id is a type-1 resource id plus one.
    """
    found: list[int] = []
    for segment in _segments(data):
        for button in _buttons(data, segment):
            word = _graphic_word(data, segment, button, 0x39)
            if word is not None:
                found.append(word)
    return tuple(found)


def _graphic_word(data: bytes, segment, button: int, offset: int) -> int | None:
    end = segment.file_at + segment.size
    pointer = _u16(data, button + 0x28)
    origin = segment.base + pointer
    if pointer and origin + offset + 2 <= end and _u16(data, origin) == 0x0202:
        return _u16(data, origin + offset)
    return None


def button_bounds(data: bytes, page_id: str, button_name: str) -> tuple[int, int, int, int]:
    """The four signed words at ``+0x0F`` of the named button.

    They are a rectangle. The picture id in the graphics block is not
    this rectangle.
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
        parent = record - segment.base
        for button in _buttons(data, segment):
            if _u16(data, button + 4) != parent:
                continue
            if trailer is None or _name(trailer, _u16(data, button + 6)) != button_name:
                continue
            return _bounds(data, button)
    raise ValueError(f"no {button_name} button on {page_id}")


def button_border(data: bytes, page_id: str, button_name: str) -> int:
    """The byte at ``+0x27`` of the named button.

    It is the border. The rectangle at ``+0x0F`` is not this byte.
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
        parent = record - segment.base
        for button in _buttons(data, segment):
            if _u16(data, button + 4) != parent:
                continue
            if trailer is None or _name(trailer, _u16(data, button + 6)) != button_name:
                continue
            return data[button + 0x27]
    raise ValueError(f"no {button_name} button on {page_id}")


def stored_button_borders(data: bytes) -> tuple[int, ...]:
    """The border byte at ``+0x27`` of every class ``0x09`` button of this length."""
    return tuple(data[button + 0x27] for _segment, button in _button_records(data))


def button_enabled(data: bytes, page_id: str, button_name: str) -> int:
    """Bit 0 of the byte at ``+0x26`` of the named button.

    1 is enabled and 0 is not. The other bits of that byte are not this field.
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
        parent = record - segment.base
        for button in _buttons(data, segment):
            if _u16(data, button + 4) != parent:
                continue
            if trailer is None or _name(trailer, _u16(data, button + 6)) != button_name:
                continue
            return data[button + 0x26] & 1
    raise ValueError(f"no {button_name} button on {page_id}")


def stored_button_enabled(data: bytes) -> tuple[int, ...]:
    """Bit 0 of ``+0x26`` on every class ``0x09`` button of this length."""
    return tuple(data[button + 0x26] & 1 for _segment, button in _button_records(data))


def button_checked(data: bytes, page_id: str, button_name: str) -> int:
    """Bit 4 of the byte at ``+0x26`` of the named button.

    1 is checked and 0 is not. The checked picture in the graphics block
    is not this bit, and bit 0 of this byte is enabled.
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
        parent = record - segment.base
        for button in _buttons(data, segment):
            if _u16(data, button + 4) != parent:
                continue
            if trailer is None or _name(trailer, _u16(data, button + 6)) != button_name:
                continue
            return (data[button + 0x26] >> 4) & 1
    raise ValueError(f"no {button_name} button on {page_id}")


def stored_button_checked(data: bytes) -> tuple[int, ...]:
    """Bit 4 of ``+0x26`` on every class ``0x09`` button of this length."""
    return tuple((data[button + 0x26] >> 4) & 1 for _segment, button in _button_records(data))


def stored_button_bounds(data: bytes) -> tuple[tuple[int, int, int, int], ...]:
    """The rectangle at ``+0x0F`` of every class ``0x09`` button of this length."""
    return tuple(_bounds(data, button) for _segment, button in _button_records(data))


def _button_records(data: bytes) -> tuple[tuple, ...]:
    found = []
    for segment in _segments(data):
        for button in _buttons(data, segment):
            found.append((segment, button))
    return tuple(found)


def _buttons(data: bytes, segment) -> tuple[int, ...]:
    end = segment.file_at + segment.size
    at = segment.base + 0x10
    found: list[int] = []
    while at + BUTTON_BYTES <= end and at >= 4:
        kind = _u16(data, at - 2)
        size = _u16(data, at - 4) - (at - segment.base)
        if kind == BUTTON and size == BUTTON_BYTES:
            found.append(at)
        at += 2
    return tuple(found)


def _bounds(data: bytes, record: int) -> tuple[int, int, int, int]:
    left, top, right, bottom = struct.unpack_from("<hhhh", data, record + 0x0F)
    return left, top, right, bottom


def huge_bitmaps(data: bytes) -> tuple[Bitmap, ...]:
    """Every type-1 resource whose huge-table row is a ``BM`` file.

    The count is however many of those rows the directory names. It is
    not written down here.
    """
    book = Book(data)
    records = {item.key: item for item in book.records}
    directory = _u32(data, book.header + 8 + (BITMAP_TYPE + 5) * 4)
    body = _resolve(records, directory)
    count = _u16(data, body + 2)
    table = _resolve(records, (directory & 0xFFFF0000) | _u16(data, body + 0x0E))
    found: list[Bitmap] = []
    for index in range(count):
        entry = table + index * 8
        if entry + 8 > len(data):
            break
        _first, near, segment, ident = struct.unpack_from("<HHHH", data, entry)
        resource = _resolve(records, (segment << 16) | near)
        if resource + 9 >= len(data) or data[resource + 8] & 1 == 0:
            continue
        found.append(button_bitmap(data, ident))
    return tuple(found)


def _huge_offset(data: bytes, header: int, row_number: int) -> int:
    if row_number < 1:
        raise ValueError("huge-table row is empty")
    table = _u32(data, header + 0x104)
    if table + 12 > len(data):
        raise ValueError("huge table is past the file")
    count = _u16(data, table + 10)
    if row_number > count:
        raise ValueError("huge-table row is past the table")
    row = table + 12 + (row_number - 1) * 12
    if row + 12 > len(data):
        raise ValueError("huge-table row is past the file")
    _size, _unused, offset = struct.unpack_from("<III", data, row)
    if offset < 0 or offset + 0x16 > len(data):
        raise ValueError("bitmap prefix is past the file")
    return offset


def _resolve(records: dict, handle: int) -> int:
    record = records.get(handle >> 16)
    if record is None:
        raise ValueError("resource segment is missing")
    return record.position - 6 + (handle & 0xFFFF)


def _u16(data: bytes, offset: int) -> int:
    return struct.unpack_from("<H", data, offset)[0]


def _u32(data: bytes, offset: int) -> int:
    return struct.unpack_from("<I", data, offset)[0]
