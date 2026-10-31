"""A page's inline script, its ``enterPage`` block, and how a field's style runs follow new text.

``enterPage`` itself runs on the OpenScript interpreter.
"""

from __future__ import annotations

from opentoolbook.field import _book, _chars, _page_handles, _segments, _u16
from opentoolbook.script import _script, resource_scripts

_PAGE = 5


def cover_style(
    old: str,
    new: str,
    runs: tuple[tuple[int, str | None], ...],
) -> tuple[tuple[int, str | None], ...]:
    """A run that covered all of ``old`` covers all of ``new``.

    A run that starts later stays where it is. A run that started at the
    end of ``old`` moves to the end of ``new``.
    """
    if not runs:
        return runs
    ordered = tuple(sorted(runs))
    for index, (offset, _face) in enumerate(ordered):
        end = ordered[index + 1][0] if index + 1 < len(ordered) else len(old)
        if offset != 0 or end < len(old):
            continue
        delta = len(new) - len(old)
        moved = []
        for place, (run_offset, face) in enumerate(ordered):
            if place == index:
                moved.append((0, face))
            elif run_offset >= len(old):
                moved.append((run_offset + delta, face))
            else:
                moved.append((run_offset, face))
        return tuple(moved)
    return runs


def page_source(data: bytes, page_id: str) -> str:
    """The inline script of one page. Empty when that page stores none."""
    segments = _segments(data)
    by_key = {segment.key: segment for segment in segments}
    book_segment, book_record = _book(data, segments)
    for handle in _page_handles(data, by_key, book_segment, book_record):
        segment = by_key.get(handle >> 16)
        if segment is None:
            continue
        record = segment.base + (handle & 0xFFFF)
        if record < 2 or record + 8 > len(data) or _u16(data, record - 2) != _PAGE:
            continue
        if _chars(data, record + 6, 32) != page_id:
            continue
        heap = b"\x00" * 6 + data[segment.file_at:segment.file_at + segment.size]
        kind = _u16(data, record - 2)
        size = _u16(data, record - 4) - (record - segment.base)
        return _script(data, heap, record, kind, size)
    return ""


def _enter_page(source: str) -> str:
    return _handler(source, "enterpage")


def _handler(source: str, message: str) -> str:
    """The ``to handle`` block for ``message`` in ``source``, or empty."""
    lines = source.splitlines()
    start = None
    for index, line in enumerate(lines):
        parts = line.strip().split()
        if (
            len(parts) >= 3
            and parts[0].lower() == "to"
            and parts[1].lower() == "handle"
            and parts[2].lower() == message
        ):
            start = index
            break
    if start is None:
        return ""
    stop = len(lines)
    for index in range(start + 1, len(lines)):
        parts = lines[index].strip().split()
        if len(parts) >= 3 and parts[0].lower() == "to" and parts[1].lower() == "handle":
            stop = index
            break
    return "\n".join(lines[start:stop])


def _book_enter(data: bytes) -> str:
    """The book ``enterPage`` that names field ``page#``. Empty when there is none."""
    try:
        scripts = resource_scripts(data)
    except (ValueError, IndexError):
        return ""
    for item in scripts:
        handler = _enter_page(item.source)
        if "page#" in handler.lower():
            return handler
    return ""
