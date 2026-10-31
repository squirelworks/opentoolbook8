"""The system books a book's class table is bound to.

A book stores one class table object, class word ``0x3A``. Its bytes start
``3a 00 02 00 3c 00 3d 00 3c 00``. The word after those ten bytes is the
count of bound books and the next word is a near pointer to an array of
that many near pointers, each to an upper-case file name and a NUL. A near
pointer is an offset into the record that holds the object, counted from
six bytes before the record's first byte.

When ToolBook opens a book it appends each bound name that ``sysBooks``
does not already hold (``CDBADDBOUNDSYSBOOKS``). The source is
``knowledge/claude/system_book_loading_2026-10-21.md``: the provider list
read from ``FUN_1278_124e`` / ``1454`` / ``1366`` and the Author's
``FUN_1108_0000``.
"""

from __future__ import annotations

import struct

from opentoolbook.record import Book

MARK = b"\x3a\x00\x02\x00\x3c\x00\x3d\x00\x3c\x00"
# The record's first byte is near pointer 6.
NEAR_BASE = 6


def bound_sysbooks(data: bytes) -> tuple[str, ...]:
    """Bound system book names in stored order, as stored. Empty when the book has none."""
    try:
        book = Book(data)
    except ValueError:
        return ()
    for record in book.records:
        end = record.position + record.length
        at = data.find(MARK, record.position, end)
        if at < 0 or at + len(MARK) + 4 > end:
            continue
        base = record.position - NEAR_BASE
        count, array = struct.unpack_from("<HH", data, at + len(MARK))
        names: list[str] = []
        for index in range(count):
            slot = base + array + 2 * index
            if not (record.position <= slot and slot + 2 <= end):
                return ()
            text = base + struct.unpack_from("<H", data, slot)[0]
            stop = data.find(b"\x00", text, end)
            if text < record.position or stop < 0:
                return ()
            names.append(data[text:stop].decode("latin1"))
        return tuple(names)
    return ()
