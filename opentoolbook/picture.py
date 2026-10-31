"""A class ``0x19`` picture: a packed Windows metafile with bounds.

The record is 89 bytes. The four signed words at ``+0x0F`` are the
bounds. The byte at ``+0x26`` is 254. The words at ``+0x41`` and
``+0x43`` are the picture's width and height in pixels, and the word at
``+0x45`` is its bits per pixel. The dword at ``+0x29`` is the metafile
byte count. The dword at ``+0x2D`` is the stored byte count when the
metafile is packed, and 0 when it is stored as is. The word at ``+0x4D``
is a 1-based row of the huge table at header ``+0x104``, and that row's
third dword is the file offset of the stored bytes.

Every metafile in ``nida81.tbk`` is the same list of records around one
or two ``StretchDIB`` records. The window extent is about the picture's own size. The window draws that extent, from its
origin, into the record's bounds. One record with ``SRCCOPY`` is the
picture. Two records are ``SRCPAINT`` then ``SRCAND``. Where the first
picture is black and the second is white, the page shows through. Every
other pixel is the first picture AND the second.
"""

from __future__ import annotations

import struct
from dataclasses import dataclass

from opentoolbook.bitmap import _huge_offset, _u16, _u32
from opentoolbook.packed import unpack
from opentoolbook.record import Book

PICTURE = 0x19
PICTURE_BYTES = 89
_STRETCH_DIB = 0x0F43
_EOF = 0x0000
SRCCOPY = 0x00CC0020
SRCPAINT = 0x00EE0086
SRCAND = 0x008800C6
# The records each metafile in nida81.tbk plays before and after its DIBs.
_FRAME = (0x001E, 0x0102, 0x020B, 0x020C, 0x0107, 0x0416, 0x0106, 0x0104)
_CLOSE = (0x0104, 0x0127, _EOF)


@dataclass(frozen=True)
class Picture:
    """Window width and height, top-down RGB, and a mask: 1 where the picture covers the page."""

    width: int
    height: int
    rgb: bytes
    mask: bytes | None


def picture_metafile(data: bytes, at: int) -> bytes:
    """The metafile bytes the record names, unpacked."""
    size = _u32(data, at + 0x29)
    packed = _u32(data, at + 0x2D)
    row = _u16(data, at + 0x4D)
    origin = _huge_offset(data, Book(data).header, row)
    stored = packed or size
    if origin + stored > len(data):
        raise ValueError("picture bytes are past the file")
    metafile = unpack(data[origin:origin + stored]) if packed else data[origin:origin + stored]
    if len(metafile) != size:
        raise ValueError("picture bytes are not the stored count")
    return metafile


def metafile_records(metafile: bytes) -> tuple[tuple[int, int, int], ...]:
    """``(function, offset, size in words)`` for each metafile record."""
    if len(metafile) < 18 or _u16(metafile, 0) != 1 or _u16(metafile, 2) != 9:
        raise ValueError("picture is not a metafile")
    at = _u16(metafile, 2) * 2
    found = []
    while at + 6 <= len(metafile):
        words, function = struct.unpack_from("<IH", metafile, at)
        found.append((function, at, words))
        if function == _EOF:
            break
        if words < 3:
            raise ValueError("metafile record is short")
        at += words * 2
    if not found or found[-1][0] != _EOF:
        raise ValueError("metafile has no end record")
    return tuple(found)


def picture_pixels(data: bytes, at: int) -> Picture:
    """The picture the record's metafile draws."""
    return metafile_picture(picture_metafile(data, at))


def metafile_picture(metafile: bytes) -> Picture:
    """The picture a metafile draws, one pixel per unit of its window extent."""
    records = metafile_records(metafile)
    functions = tuple(function for function, _at, _words in records)
    dibs = [offset for function, offset, _words in records if function == _STRETCH_DIB]
    if functions != _FRAME + (_STRETCH_DIB,) * len(dibs) + _CLOSE or len(dibs) not in (1, 2):
        raise ValueError("picture metafile is not the stored frame")
    params = {function: offset + 6 for function, offset, _words in records}
    origin_y, origin_x = struct.unpack_from("<hh", metafile, params[0x020B])
    extent_h, extent_w = struct.unpack_from("<hh", metafile, params[0x020C])
    clip = struct.unpack_from("<hhhh", metafile, params[0x0416])
    if extent_w <= 0 or extent_h <= 0:
        raise ValueError("picture window is empty")
    bottom, right, top, left = clip
    window = (origin_x, origin_y, extent_w, extent_h)
    drawn = [_place(metafile, offset, window, (left, top, right, bottom)) for offset in dibs]
    if len(drawn) == 1:
        rop, rgb, covered = drawn[0]
        if rop != SRCCOPY:
            raise ValueError("one picture record is not SRCCOPY")
        return Picture(extent_w, extent_h, rgb, covered)
    (first_rop, first, first_covered), (second_rop, second, second_covered) = drawn
    if (first_rop, second_rop) != (SRCPAINT, SRCAND) or first_covered != second_covered:
        raise ValueError("picture records are not SRCPAINT then SRCAND over one rectangle")
    rgb = bytearray(len(first))
    mask = bytearray(extent_w * extent_h)
    for pixel in range(extent_w * extent_h):
        if not first_covered[pixel]:
            continue
        a = first[pixel * 3:pixel * 3 + 3]
        b = second[pixel * 3:pixel * 3 + 3]
        if a == b"\x00\x00\x00" and b == b"\xff\xff\xff":
            continue
        if any((x | (~y & 0xFF)) != 0xFF for x, y in zip(a, b)):
            raise ValueError("picture pixel depends on the page under it")
        mask[pixel] = 1
        rgb[pixel * 3:pixel * 3 + 3] = bytes(x & y for x, y in zip(a, b))
    return Picture(extent_w, extent_h, bytes(rgb), bytes(mask))


def _place(metafile: bytes, at: int, window, clip) -> tuple[int, bytes, bytes]:
    """One StretchDIB drawn into the window, clipped. Returns the rop, RGB, and covered pixels."""
    origin_x, origin_y, width, height = window
    params = at + 6
    src_h, src_w, src_y, src_x, dest_h, dest_w, dest_y, dest_x = struct.unpack_from(
        "<hhhhhhhh", metafile, params + 6
    )
    rop, dib_w, dib_h, dib = _stretch_dib(metafile, at)
    if dest_w <= 0 or dest_h <= 0 or src_w <= 0 or src_h <= 0:
        raise ValueError("picture record is empty")
    if src_x < 0 or src_y < 0 or src_x + src_w > dib_w or src_y + src_h > dib_h:
        raise ValueError("picture source is outside its DIB")
    left, top, right, bottom = (
        clip[0] - origin_x, clip[1] - origin_y, clip[2] - origin_x, clip[3] - origin_y
    )
    dest_x -= origin_x
    dest_y -= origin_y
    rgb = bytearray(width * height * 3)
    covered = bytearray(width * height)
    for y in range(max(0, top, dest_y), min(height, bottom, dest_y + dest_h)):
        # DIB rows were turned top-down, so the source row counts from the top.
        source_y = src_y + (y - dest_y) * src_h // dest_h
        for x in range(max(0, left, dest_x), min(width, right, dest_x + dest_w)):
            source_x = src_x + (x - dest_x) * src_w // dest_w
            start = (source_y * dib_w + source_x) * 3
            rgb[(y * width + x) * 3:(y * width + x) * 3 + 3] = dib[start:start + 3]
            covered[y * width + x] = 1
    return rop, bytes(rgb), bytes(covered)


def _stretch_dib(metafile: bytes, at: int) -> tuple[int, int, int, bytes]:
    params = at + 6
    rop = _u32(metafile, params)
    info = params + 22
    header, width, height, _planes, bpp, compression = struct.unpack_from("<IiiHHI", metafile, info)
    used = _u32(metafile, info + 32)
    if header != 40 or compression != 0 or bpp != 8 or width <= 0 or height == 0:
        raise ValueError("picture DIB is not 8 bits, uncompressed")
    colors = used or 256
    palette_at = info + header
    pixel_at = palette_at + 4 * colors
    stride = (width + 3) & ~3
    rows = abs(height)
    if pixel_at + stride * rows > len(metafile):
        raise ValueError("picture DIB is past the metafile")
    palette = [metafile[palette_at + 4 * index:palette_at + 4 * index + 3][::-1] for index in range(colors)]
    rgb = bytearray(width * rows * 3)
    for y in range(rows):
        source = pixel_at + (y if height < 0 else rows - 1 - y) * stride
        for x in range(width):
            index = metafile[source + x]
            if index < colors:
                rgb[(y * width + x) * 3:(y * width + x) * 3 + 3] = palette[index]
    return rop, width, rows, bytes(rgb)

