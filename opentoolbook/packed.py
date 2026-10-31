"""Packed bytes in the huge table.

A class ``0x15`` paint object and a class ``0x19`` picture name a
huge-table row whose bytes are packed when the record's dword at
``+0x2D`` is not 0. The packed bytes are blocks. Each block is a word
that counts its codes, then those codes. A code below ``0xF6`` repeats
the next byte the code plus three times. A code of ``0xF6`` or more
copies the next ``code - 0xF5`` bytes. A block does not start on the
last byte of a 64 KB span of the packed bytes: that byte is skipped and
the block starts on the next span.
"""

from __future__ import annotations

import struct

_LITERAL = 0xF6
_SPAN = 0x10000


def unpack(stored: bytes) -> bytes:
    """Expand packed bytes."""
    out = bytearray()
    at = 0
    if not stored:
        raise ValueError("packed bytes are empty")
    while at < len(stored):
        if at % _SPAN == _SPAN - 1:
            at += 1
            continue
        if at + 2 > len(stored):
            raise ValueError("packed block count is past the end")
        codes = struct.unpack_from("<H", stored, at)[0]
        at += 2
        for _ in range(codes):
            if at >= len(stored):
                raise ValueError("packed bytes end early")
            code = stored[at]
            at += 1
            if code >= _LITERAL:
                count = code - (_LITERAL - 1)
                if at + count > len(stored):
                    raise ValueError("packed bytes end early")
                out += stored[at:at + count]
                at += count
            else:
                if at >= len(stored):
                    raise ValueError("packed bytes end early")
                out += bytes((stored[at],)) * (code + 3)
                at += 1
    return bytes(out)
