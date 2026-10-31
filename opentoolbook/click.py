"""A ``buttonClick`` the reader already expanded.

A quoted ``go to page`` opens that page. ``of book`` names the other
file when the line quotes one. ``send next`` and ``send previous`` are
the next and previous pages in the stored page list. ``break`` stops
the handler. A line that is not one of those is not a page change.
"""

from __future__ import annotations

import struct
from dataclasses import dataclass

from opentoolbook.field import _book, _chars, _page_handles, _segments, _u16
from opentoolbook.script import _script, button_clicks, quoted_go_to

_PAGE = 5
_BACKGROUND = 4


@dataclass(frozen=True)
class Follow:
    """The page a handler opens. ``book`` is None when it stays in this book."""

    page_id: str
    book: str | None


def follow_click(
    data: bytes,
    page_id: str,
    button: str,
    pages: tuple[str, ...],
) -> Follow | None:
    """The quoted page this button's handler opens, or None when it has no handler."""
    source = _handler(data, page_id, button)
    if source is None:
        return None
    return run_handler(source, pages, page_id)


def run_handler(source: str, pages: tuple[str, ...], page_id: str) -> Follow:
    """Run the ``go to page``, ``send next``, and ``send previous`` lines."""
    target = page_id
    book = None
    for line in source.splitlines():
        text = line.strip()
        if not text or text.startswith("--"):
            continue
        low = " ".join(text.lower().split())
        if low.startswith("to handle") or low.startswith("end"):
            continue
        if low == "break":
            break
        found = quoted_go_to(text)
        if found is not None:
            target, book = found
            continue
        if low == "send next":
            target = _step(pages, page_id, 1)
            book = None
            continue
        if low == "send previous":
            target = _step(pages, page_id, -1)
            book = None
            continue
    return Follow(target, book)


def quiz_setup_click(
    data: bytes,
    page_id: str,
    button: str,
    pages: tuple[str, ...],
    handlers: dict[str, str],
    props,
) -> int | None:
    """Run the ``setupQuizEx`` call in this button's handler into ``props``.

    Returns that call's ``error``, or None when the handler makes no such
    call or the system books do not define ``setupQuizEx``.
    """
    from opentoolbook.quizsetup import selection_setup

    source = _handler(data, page_id, button)
    setup = handlers.get("setupquizex")
    if source is None or not setup:
        return None
    number = pages.index(page_id) + 1 if page_id in pages else 0
    return selection_setup(source, setup, props, number)


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


def _handler(data: bytes, page_id: str, button: str) -> str | None:
    folded = button.lower()
    for item in button_clicks(data):
        if item.owner == page_id and item.name.lower() == folded:
            return item.source
    return None


def _step(pages: tuple[str, ...], page_id: str, step: int) -> str:
    try:
        index = pages.index(page_id)
    except ValueError:
        return page_id
    moved = index + step
    if moved < 0 or moved >= len(pages):
        return page_id
    return pages[moved]
