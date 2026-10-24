"""The source text of a ``buttonClick`` handler.

An ordinary object's script is inline when the low two bits of the byte
at ``+0x0A`` are 0. The word at ``+0x0B`` is a near pointer. A page or a
background uses the byte at ``+0x30`` and the word at ``+0x2A``. The word
at the pointer is a count of bytes to skip. The next word is the length
of the bytecode, and those bytes follow it.

The bytecode is the encoding in the decompile record, chapter 14, from
``FUN_1040_0970``. A keyword id is an entry in ``KEYWORDS``. A
back-reference copies from this segment, not from the expanded text.
The reader returns the text. It does not call the handler.
"""

from __future__ import annotations

import struct
from dataclasses import dataclass

from opentoolbook.field import _chars, _name, _segments, _trailer, _u16
from opentoolbook.keywords import KEYWORDS

# Repeating class lengths. Page and background use the other script word.
_BYTES = {
    0x04: 103,
    0x05: 81,
    0x08: 41,
    0x09: 43,
    0x0A: 61,
    0x0B: 49,
    0x0C: 41,
    0x0D: 45,
    0x0E: 53,
    0x10: 53,
    0x11: 61,
    0x13: 55,
    0x15: 89,
    0x17: 17,
    0x19: 89,
}
_PAGE = 5
_BACKGROUND = 4


@dataclass(frozen=True)
class ButtonClick:
    """One object's ``buttonClick`` handler, as source text.

    ``owner`` is the page id, or the background name when the object is
    not on a page. ``source`` is the handler, not a call.
    """

    owner: str
    name: str
    source: str


def button_clicks(data: bytes) -> tuple[ButtonClick, ...]:
    """Every inline ``buttonClick`` in the book, in the order the records are stored."""
    found: list[ButtonClick] = []
    for segment in _segments(data):
        trailer = _trailer(data, segment)
        heap = b"\x00" * 6 + data[segment.file_at:segment.file_at + segment.size]
        end = segment.file_at + segment.size
        owner = _owner(data, segment.base)
        at = segment.base + 0x14
        while at + 8 <= end and at >= 4:
            kind = _u16(data, at - 2)
            size = _u16(data, at - 4) - (at - segment.base)
            if kind not in _BYTES or size != _BYTES[kind]:
                at += 1
                continue
            text = _script(data, heap, at, kind, size)
            handler = _button_click(text) if text else None
            if handler:
                found.append(ButtonClick(owner, _object_name(data, trailer, at, kind), handler))
            at += size
    return tuple(found)


def _owner(data: bytes, base: int) -> str:
    record = base + 0x14
    if record < 2 or record + 8 > len(data):
        return ""
    kind = _u16(data, record - 2)
    if kind == _PAGE:
        return _chars(data, record + 6, 32)
    if kind == _BACKGROUND:
        return _chars(data, record + 6, 32)
    return ""


def _object_name(data: bytes, trailer, record: int, kind: int) -> str:
    if kind in (_PAGE, _BACKGROUND):
        return _chars(data, record + 6, 32)
    if trailer is None:
        return ""
    return _name(trailer, _u16(data, record + 6))


def _script(data: bytes, heap: bytes, record: int, kind: int, size: int) -> str:
    if kind in (_PAGE, _BACKGROUND):
        if size <= 0x31:
            return ""
        mode = data[record + 0x30]
        word = _u16(data, record + 0x2A)
    else:
        if size <= 0x0C:
            return ""
        mode = data[record + 0x0A]
        word = _u16(data, record + 0x0B)
    if (mode & 3) != 0 or word == 0 or word + 4 > len(heap):
        return ""
    skip = _u16(heap, word)
    length_at = word + 2 + skip
    if length_at + 2 > len(heap):
        return ""
    length = _u16(heap, length_at)
    start = length_at + 2
    if length == 0 or length > 8000 or start + length > len(heap):
        return ""
    return _expand(heap, start, length)


def _expand(blob: bytes, origin: int, span: int) -> str:
    """Expand ``span`` bytecode bytes at ``origin`` inside ``blob``."""
    out = bytearray()
    pos = origin
    end = min(len(blob), origin + span)
    while pos < end and len(out) < 8000:
        opcode = blob[pos]
        pos += 1
        if opcode < 0x80:
            if opcode == 0:
                break
            out.append(opcode)
            continue
        if (opcode & 0xF0) == 0xF0:
            if opcode == 0xFF:
                if pos + 1 >= end:
                    break
                piece = blob[pos]
                count = blob[pos + 1] + 1
                pos += 2
                out.extend([piece] * count)
            else:
                out.extend(b" " * ((opcode & 0xF) + 2))
            continue
        if (opcode & 0xF0) == 0xE0:
            out.extend(b"\r\n" + b" " * (opcode & 0xF))
            continue
        if (opcode & 0x40) == 0:
            index = opcode & 0xF
            if opcode & 0x10:
                if pos >= end:
                    break
                index = (index << 8) | blob[pos]
                pos += 1
            if index < len(KEYWORDS):
                out.extend(KEYWORDS[index].encode("latin-1"))
            if (opcode & 0x20) == 0:
                out.append(0x20)
            continue
        if (opcode & 0x10) == 0:
            if pos >= end:
                break
            length = (opcode & 0xF) + 3
            src = pos + (-4 - blob[pos])
            pos += 1
        else:
            if pos + 1 >= end:
                break
            length = (opcode & 0xF) + 4
            src = pos + (-1 - struct.unpack_from("<H", blob, pos)[0])
            pos += 2
        for index in range(length):
            at = src + index
            out.append(blob[at] if 0 <= at < len(blob) else ord("?"))
    return out.decode("latin-1")


def _button_click(text: str) -> str | None:
    lines = text.split("\r\n")
    start = None
    for index, line in enumerate(lines):
        parts = line.strip().split()
        if (
            len(parts) >= 3
            and parts[0].lower() == "to"
            and parts[1].lower() == "handle"
            and parts[2].lower() == "buttonclick"
        ):
            start = index
            break
    if start is None:
        return None
    stop = len(lines)
    for index in range(start + 1, len(lines)):
        if lines[index].strip().lower() == "end":
            stop = index + 1
            break
    return "\r\n".join(lines[start:stop])
