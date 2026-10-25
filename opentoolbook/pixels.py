"""The pixels of a button picture.

A stored picture id is a type-1 resource id plus one. A huge-table
resource keeps its ``BM`` file after the 8-byte prefix. Any other
type-1 resource keeps a ``BM`` file eight bytes after ``01 02 01 00``.
The pixels returned are top-down RGB, one byte each for red, green,
and blue.
"""

from __future__ import annotations

import struct

from opentoolbook.bitmap import BITMAP_TYPE, _huge_offset, _resolve, _u16, _u32
from opentoolbook.record import Book

_MARKER = b"\x01\x02\x01\x00"


def picture_rgb(data: bytes, stored_id: int) -> tuple[int, int, bytes]:
    """Width, height, and top-down RGB for one stored picture id."""
    if stored_id <= 0:
        raise ValueError("picture id is empty")
    blob = _bm_file(data, stored_id - 1)
    return _decode_bmp(blob)


def _bm_file(data: bytes, resource_id: int) -> bytes:
    book = Book(data)
    records = {item.key: item for item in book.records}
    directory = _u32(data, book.header + 8 + (BITMAP_TYPE + 5) * 4)
    body = _resolve(records, directory)
    count = _u16(data, body + 2)
    table = _resolve(records, (directory & 0xFFFF0000) | _u16(data, body + 0x0E))
    for index in range(count):
        entry = table + index * 8
        if entry + 8 > len(data):
            break
        _first, near, segment, ident = struct.unpack_from("<HHHH", data, entry)
        if ident != resource_id:
            continue
        resource = _resolve(records, (segment << 16) | near)
        if data[resource + 8] & 1:
            origin = _huge_offset(data, book.header, _u16(data, resource + 9)) + 8
        else:
            origin = _inline_bm(data, resource)
        size = struct.unpack_from("<I", data, origin + 2)[0]
        if data[origin:origin + 2] != b"BM" or origin + size > len(data):
            raise ValueError(f"bitmap {resource_id} has no BM file")
        return data[origin:origin + size]
    raise ValueError(f"no bitmap resource {resource_id}")


def _inline_bm(data: bytes, resource: int) -> int:
    window = data[resource:resource + 64]
    at = window.find(_MARKER)
    if at < 0 or resource + at + 10 > len(data) or data[resource + at + 8:resource + at + 10] != b"BM":
        raise ValueError("bitmap resource has no BM file")
    return resource + at + 8


def _decode_bmp(blob: bytes) -> tuple[int, int, bytes]:
    if len(blob) < 54 or blob[:2] != b"BM":
        raise ValueError("bitmap is not a BM file")
    pixel_at = struct.unpack_from("<I", blob, 10)[0]
    header = struct.unpack_from("<I", blob, 14)[0]
    if header < 40 or 14 + header > len(blob):
        raise ValueError("bitmap info header is short")
    width, height = struct.unpack_from("<ii", blob, 18)
    bpp = struct.unpack_from("<H", blob, 28)[0]
    if struct.unpack_from("<I", blob, 30)[0] != 0:
        raise ValueError("bitmap is compressed")
    top_down = height < 0
    height = abs(height)
    if width <= 0 or height <= 0:
        raise ValueError("bitmap size is empty")
    if bpp == 24:
        colors = 0
        palette = b""
        row_bytes = width * 3
    elif bpp == 8:
        colors = struct.unpack_from("<I", blob, 46)[0] or 256
        palette_at = 14 + header
        palette = blob[palette_at:palette_at + colors * 4]
        if len(palette) < colors * 4:
            raise ValueError("bitmap palette is short")
        row_bytes = width
    else:
        raise ValueError("bitmap depth is not 8 or 24")
    stride = (row_bytes + 3) & ~3
    if pixel_at + stride * height > len(blob):
        raise ValueError("bitmap pixels are past the file")
    rgb = bytearray(width * height * 3)
    for y in range(height):
        source = y if top_down else height - 1 - y
        row = pixel_at + source * stride
        dest = y * width * 3
        if bpp == 24:
            for x in range(width):
                blue, green, red = blob[row + x * 3:row + x * 3 + 3]
                rgb[dest + x * 3:dest + x * 3 + 3] = bytes((red, green, blue))
        else:
            for x in range(width):
                index = blob[row + x]
                if index >= colors:
                    continue
                blue, green, red = palette[index * 4:index * 4 + 3]
                rgb[dest + x * 3:dest + x * 3 + 3] = bytes((red, green, blue))
    return width, height, bytes(rgb)
