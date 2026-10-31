"""What a click's run returns, and the scripts a click reads.

A click runs on the OpenScript interpreter (``clickrun.send_click``).
``Follow`` is its result: the page and book it goes to, the requests
and beeps, the inverts, and the properties the script set.
"""

from __future__ import annotations

import struct
from dataclasses import dataclass

from opentoolbook.field import _book, _chars, _page_handles, _segments, _u16
from opentoolbook.script import _script

_PAGE = 5
_BACKGROUND = 4
# The record class of an object whose inline script can hold a mouse message.
_CLASS = {"button": 0x9, "field": 0xA}


@dataclass(frozen=True)
class Follow:
    """The page a handler opens. ``book`` is None when it stays in this book."""

    page_id: str
    book: str | None
    requests: tuple[str, ...] = ()
    beeps: int = 0
    inverts: tuple[tuple[str, bool], ...] = ()
    # Properties a script set: (owner, kind, lower-case name or id, property, value), in order.
    # The owner is a page id or a background key.
    writes: tuple[tuple[str, str, object, str, object], ...] = ()


def object_handler(data: bytes, page_id: str, kind: str, name: str, message: str) -> str | None:
    """The ``to handle message`` handler in the inline script of one object on a page."""
    from opentoolbook.script import named_handler, object_scripts

    wanted = _CLASS.get(kind.lower())
    folded = name.lower()
    for item in object_scripts(data):
        if item.owner != page_id or item.kind != wanted or item.name.lower() != folded:
            continue
        text = item.source.replace("\r\n", "\n").replace("\n", "\r\n")
        found = named_handler(text, message)
        if found is not None:
            return found.replace("\r\n", "\n")
    return None


def quiz_background(data: bytes, page_id: str) -> bool:
    """True when the page's background ``buttonClick`` calls ``handleQuizClick``."""
    return "handlequizclick" in background_script(data, page_id).lower()


def background_script(data: bytes, page_id: str) -> str:
    """The inline script of the background a page names."""
    segments = _segments(data)
    by_key = {segment.key: segment for segment in segments}
    book_segment, book_record = _book(data, segments)
    for handle in _page_handles(data, by_key, book_segment, book_record):
        segment = by_key.get(handle >> 16)
        if segment is None:
            continue
        record = segment.base + (handle & 0xFFFF)
        if record < 2 or record + 0x4B > len(data) or _u16(data, record - 2) != _PAGE:
            continue
        if _chars(data, record + 6, 32) != page_id:
            continue
        far = struct.unpack_from("<I", data, record + 0x47)[0]
        owner = by_key.get(far >> 16)
        if owner is None:
            return ""
        found = owner.base + (far & 0xFFFF)
        if found < 2 or _u16(data, found - 2) != _BACKGROUND:
            return ""
        heap = b"\x00" * 6 + data[owner.file_at:owner.file_at + owner.size]
        kind = _u16(data, found - 2)
        size = _u16(data, found - 4) - (found - owner.base)
        return _script(data, heap, found, kind, size)
    return ""
