"""How TB80BAS loads one object record, and how it finds the procedure to call.

The directory is a four-level radix tree. Its root is the dword at the
``03 4A 42 4F`` header plus ``0x10E``. Three internal levels hold sixteen
children of ``0x14`` bytes. The leaves hold sixteen entries of ``0x18``
bytes. A leaf is real when the body it names starts with the tree key and
the following word is the stored length minus two.

The entry's first dword is the file position and the word at ``+0x0C`` is
the length. Bit 6 of the high byte at ``+0x08`` asks for a second read.
On the lesson open traced in October 2026 that second read was two bytes,
beginning at ``position + length``. The low bit of the same word is set
on disk and clear once the entry is in memory.

Sending a message does not index the method table by the message number.
The lookup loads the far pointer at the start of the class's ``0x76``-byte
slot and calls that procedure with the message. A class word of zero has
no procedure. The lesson-open path in ``TB80BAS`` sends message ``0xE``
this way, after the body bytes are already in memory. This module returns
that pointer and that message. It does not call a DLL.
"""

from __future__ import annotations

import struct
from dataclasses import dataclass

HEADER = b"\x03JBO"
ENTRY_SIZE = 0x18
CLASS_SLOT = 0x76
# The flag-0x40 callback read two bytes on the traced lesson open.
FOLLOW_UP = 2
MESSAGE_AFTER_LOAD = 0xE


@dataclass(frozen=True)
class Record:
    key: int
    position: int
    length: int
    flags: int
    type_byte: int
    slot: int

    @property
    def on_disk_status(self) -> bool:
        return bool(self.flags & 1)

    @property
    def wants_follow_up(self) -> bool:
        return bool(self.flags & 0x4000)


@dataclass(frozen=True)
class Loaded:
    record: Record
    body: bytes
    follow_up: bytes


class Book:
    def __init__(self, data: bytes):
        self.data = data
        self.header = data.find(HEADER)
        if self.header < 0:
            raise ValueError("not a ToolBook object store")
        self.root = self._u32(self.header + 0x10E)
        self.records = self._walk(self.root, 0, 0)

    def load(self, record: Record) -> Loaded:
        end = record.position + record.length
        if end > len(self.data):
            raise ValueError(f"record {record.key:#x} runs past the file")
        body = self.data[record.position:end]
        follow = b""
        if record.wants_follow_up:
            if end + FOLLOW_UP > len(self.data):
                raise ValueError(f"record {record.key:#x} follow-up runs past the file")
            follow = self.data[end:end + FOLLOW_UP]
        return Loaded(record, body, follow)

    def _walk(self, pos: int, level: int, prefix: int) -> list[Record]:
        found: list[Record] = []
        if level < 3:
            for n in range(16):
                child = self._u32(pos + n * 0x14)
                if child:
                    found.extend(self._walk(child, level + 1, prefix | (n << (4 * level))))
            return found
        for n in range(16):
            slot = pos + n * ENTRY_SIZE
            record = self._leaf(slot, prefix | (n << 12))
            if record is not None:
                found.append(record)
        return found

    def _leaf(self, slot: int, key: int) -> Record | None:
        if slot + ENTRY_SIZE > len(self.data):
            return None
        position = self._u32(slot)
        flags = self._u16(slot + 8)
        length = self._u16(slot + 0x0C)
        if position == 0 or length < 4 or position + length > len(self.data):
            return None
        if self._u16(position) != key or self._u16(position + 2) != length - 2:
            return None
        return Record(
            key=key,
            position=position,
            length=length,
            flags=flags,
            type_byte=self.data[slot + 0x16],
            slot=slot,
        )

    def _u16(self, off: int) -> int:
        return struct.unpack_from("<H", self.data, off)[0]

    def _u32(self, off: int) -> int:
        return struct.unpack_from("<I", self.data, off)[0]


def handler_at(class_word: int, slots: bytes, index: int = 0) -> tuple[int, int] | None:
    """Far pointer of one class procedure, as ``(segment, offset)``.

    ``slots`` is the array the class record points at. Class ``n`` owns
    ``0x76`` bytes, and procedure ``index`` is the far pointer
    ``index * 4`` bytes into that class. The send on lesson open uses
    index 0.
    """
    if class_word == 0:
        return None
    at = class_word * CLASS_SLOT + index * 4
    if at + 4 > len(slots):
        raise ValueError("class slot is past the method table")
    offset, segment = struct.unpack_from("<HH", slots, at)
    return segment, offset


def procedure_for_message(class_word: int, slots: bytes, message: int) -> tuple[tuple[int, int] | None, int]:
    """The procedure a lesson-open send calls, and the message it receives."""
    return handler_at(class_word, slots, 0), message
