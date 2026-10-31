"""A ``buttonClick`` the reader already expanded.

A quoted ``go to page`` opens that page. ``of book`` names the other
file when the line quotes one. ``go to page (name) of book(name)`` and
``go to page name of book name`` read those two system variables when a
handler this runner executed assigned them a string; otherwise the page
stays. A handler line ``name = "text"``, ``name = name of this book``, or
``name = name of this page`` assigns that system variable. ``send next`` and
``send previous`` are the next and previous pages in the stored page
list. ``if``, ``break``, and ``return`` are the shared walker in
``walk.py``. A line that is not one of those is not a page change.
"""

from __future__ import annotations

import re
import struct
from dataclasses import dataclass

from opentoolbook.field import _book, _chars, _page_handles, _segments, _u16
from opentoolbook.script import _button_click, _script, button_clicks, quoted_go_to
from opentoolbook.walk import Flow, reader_condition, walk

_PAGE = 5
_BACKGROUND = 4
# go to page (nextpage) of book(lastbook): two names in parentheses.
_NAMED_GO_TO = re.compile(
    r"^go\s+to\s+page\s*\(\s*([a-z_][a-z0-9_]*)\s*\)"
    r"(?:\s*of\s+book\s*\(\s*([a-z_][a-z0-9_]*)\s*\))?\s*$",
    re.IGNORECASE,
)
# go to page nextpage of book lastbook: the same two names without parentheses.
_BARE_GO_TO = re.compile(
    r"^go\s+to\s+page\s+([a-z_][a-z0-9_]*)(?:\s+of\s+book\s+([a-z_][a-z0-9_]*))?\s*$",
    re.IGNORECASE,
)
_ASSIGN = re.compile(r"^([a-z_][a-z0-9_]*)\s*=\s*(.+?)\s*$", re.IGNORECASE)


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
    variables: dict[str, object] | None = None,
    book: str = "",
) -> Follow | None:
    """The page this button's handler opens, or None when it has no handler.

    ``variables`` is the window's system variables. The handler's
    assignments are written into it. ``book`` is ``name of this book``.
    """
    source = _handler(data, page_id, button)
    if source is None:
        return None
    return run_handler(source, pages, page_id, variables, book)


def page_click(
    data: bytes,
    page_id: str,
    pages: tuple[str, ...],
    variables=None,
    book: str = "",
) -> Follow | None:
    """The page's own ``buttonClick``, or None when the page script has none."""
    from opentoolbook.enter import page_source

    text = page_source(data, page_id)
    source = _button_click(text.replace("\r\n", "\n").replace("\n", "\r\n")) if text else None
    if source is None:
        return None
    return run_handler(source, pages, page_id, variables, book)


def run_handler(
    source: str,
    pages: tuple[str, ...],
    page_id: str,
    variables: dict[str, object] | None = None,
    book_name: str = "",
) -> Follow:
    """Run the assignment, ``go to page``, ``send next``, and ``send previous`` lines.

    ``variables`` maps a lower-case system variable name to the value a
    handler this runner executed assigned it. This handler's assignments
    are written into it. ``book_name`` is ``name of this book``.
    """
    known = variables if variables is not None else {}
    landed = {"page": page_id, "book": None}

    def statement(raw: str, low: str) -> None:
        text = raw.strip()
        found = quoted_go_to(raw)
        if found is not None:
            landed["page"], landed["book"] = found
            return
        assigned = _ASSIGN.match(text)
        if assigned is not None and not assigned.group(1).startswith("__"):
            value = _assigned(assigned.group(2), page_id, book_name)
            if value is not None:
                known[assigned.group(1).lower()] = value
            return
        named = _NAMED_GO_TO.match(text) or _BARE_GO_TO.match(text)
        if named is not None:
            page_value = known.get(named.group(1).lower())
            book_value = known.get(named.group(2).lower()) if named.group(2) else None
            if not isinstance(page_value, str) or not page_value:
                return
            if named.group(2) and (not isinstance(book_value, str) or not book_value):
                return
            landed["page"], landed["book"] = page_value, book_value
            return
        if low in {"send next", "send previous"}:
            landed["page"] = _step(pages, page_id, 1 if low == "send next" else -1)
            landed["book"] = None

    walk(source.splitlines(), Flow(), condition=reader_condition, statement=statement)
    return Follow(landed["page"], landed["book"])


def _assigned(expression: str, page_id: str, book_name: str) -> str | None:
    low = " ".join(expression.lower().split())
    if low == "name of this page":
        return page_id
    if low == "name of this book":
        return book_name or None
    if len(expression) >= 2 and expression[0] == '"' and expression[-1] == '"':
        return expression[1:-1]
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
