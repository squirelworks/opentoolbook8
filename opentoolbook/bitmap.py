"""A button bitmap in the huge table.

The type-1 directory entry's fourth word is the resource id. A button
stores that id plus one. When the resource marks itself as huge, the
word at ``+9`` is a 1-based row of the table at header ``+0x104``. The
row's third dword is the file offset of an 8-byte prefix, and the ``BM``
file begins on the next byte. Width, height, and depth come from that
file's info header.
"""

from __future__ import annotations

import struct
from dataclasses import dataclass

from opentoolbook.record import Book

BITMAP_TYPE = 1


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
