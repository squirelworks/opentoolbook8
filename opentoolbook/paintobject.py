"""A class ``0x15`` paint object: a bitmap with bounds.

The record is 89 bytes. The four signed words at ``+0x0F`` are the bounds.
The byte at ``+0x26`` is the pattern, 254 on every record. The dword at
``+0x29`` is the pixel byte count. The dword at ``+0x2D`` is the stored
byte count when the pixels are packed, and 0 when they are stored as is.
The word at ``+0x4D`` is a 1-based row of the huge table at header
``+0x104``, and that row's third dword is the file offset of the stored
bytes. The word at ``+0x4F`` is the palette color count. The word at
``+0x51`` is a near pointer to a 40-byte bitmap info header, and the
palette follows it.

Packed pixels start with a word that counts the codes. A code byte below
``0xF6`` repeats the next byte that many times plus three. A code byte
of ``0xF6`` or more copies the next ``code - 0xF5`` bytes. The unpacked
bytes are the bottom-up rows of the info header.
"""

from __future__ import annotations

import struct

from opentoolbook.bitmap import _huge_offset, _u16, _u32
from opentoolbook.pixels import _decode_bmp
from opentoolbook.record import Book

PAINT_OBJECT = 0x15
PAINT_OBJECT_BYTES = 89
_INFO_BYTES = 40
_LITERAL = 0xF6


def paint_object_bounds(data: bytes, at: int) -> tuple[int, int, int, int]:
    """The rectangle at ``+0x0F``."""
    left, top, right, bottom = struct.unpack_from("<hhhh", data, at + 0x0F)
    return left, top, right, bottom


def paint_object_bmp(data: bytes, segment, at: int) -> bytes:
    """A ``BM`` file built from the stored info header, palette, and pixels."""
    pixel_bytes = _u32(data, at + 0x29)
    packed_bytes = _u32(data, at + 0x2D)
    row = _u16(data, at + 0x4D)
    colors = _u16(data, at + 0x4F)
    info = segment.base + _u16(data, at + 0x51)
    if info < 0 or info + _INFO_BYTES + 4 * colors > len(data):
        raise ValueError("paint object header is past the file")
    if _u32(data, info) != _INFO_BYTES:
        raise ValueError("paint object has no bitmap info header")
    head = data[info:info + _INFO_BYTES + 4 * colors]
    origin = _huge_offset(data, Book(data).header, row)
    if packed_bytes:
        if origin + packed_bytes > len(data):
            raise ValueError("paint object pixels are past the file")
        pixels = unpack(data[origin:origin + packed_bytes])
    else:
        if origin + pixel_bytes > len(data):
            raise ValueError("paint object pixels are past the file")
        pixels = data[origin:origin + pixel_bytes]
    if len(pixels) != pixel_bytes:
        raise ValueError("paint object pixels are not the stored count")
    offset = 14 + len(head)
    return b"BM" + struct.pack("<IHHI", offset + len(pixels), 0, 0, offset) + head + pixels


def paint_object_rgb(data: bytes, segment, at: int) -> tuple[int, int, bytes]:
    """Width, height, and top-down RGB."""
    return _decode_bmp(paint_object_bmp(data, segment, at))


def unpack(stored: bytes) -> bytes:
    """Expand packed paint-object pixels."""
    if len(stored) < 2:
        raise ValueError("packed pixels are empty")
    codes = _u16(stored, 0)
    out = bytearray()
    at = 2
    for _ in range(codes):
        if at >= len(stored):
            raise ValueError("packed pixels end early")
        code = stored[at]
        at += 1
        if code >= _LITERAL:
            count = code - (_LITERAL - 1)
            if at + count > len(stored):
                raise ValueError("packed pixels end early")
            out += stored[at:at + count]
            at += count
        else:
            if at >= len(stored):
                raise ValueError("packed pixels end early")
            out += bytes((stored[at],)) * (code + 3)
            at += 1
    if at != len(stored):
        raise ValueError("packed pixels have bytes past the last code")
    return bytes(out)
