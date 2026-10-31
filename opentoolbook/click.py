"""A ``buttonClick`` the reader already expanded.

A quoted ``go to page`` opens that page. ``of book`` names the other
file when the line quotes one. ``send next`` and ``send previous`` are
the next and previous pages in the stored page list. ``if``, ``break``,
and ``return`` are the shared walker in ``walk.py``. ``text of field
"x" = ...`` and ``set text of field "x" to ...`` write a field's text,
and a later condition reads that text. ``hide`` and ``show`` of a
field, button, rectangle, ellipse, line, or polygon, by name or by
``id``, and ``set visible of ... to``, change whether it is painted. A line that is not
one of those is not a page change.
"""

from __future__ import annotations

import re
import struct
from dataclasses import dataclass

from opentoolbook.field import _book, _chars, _page_handles, _segments, _u16
from opentoolbook.script import _script, button_clicks, quoted_go_to
from opentoolbook.walk import Flow, reader_condition, walk

_PAGE = 5
_BACKGROUND = 4


@dataclass(frozen=True)
class Follow:
    """The page a handler opens. ``book`` is None when it stays in this book.

    ``fields`` is each ``(field name, text)`` the handler wrote, in order.
    ``visible`` is each ``((kind, name or id), shown)`` from ``hide`` and
    ``show``, in order.
    """

    page_id: str
    book: str | None
    fields: tuple[tuple[str, str], ...] = ()
    visible: tuple[tuple[tuple[str, str | int], bool], ...] = ()


def follow_click(
    data: bytes,
    page_id: str,
    button: str,
    pages: tuple[str, ...],
    fields: dict[str, str] | None = None,
) -> Follow | None:
    """The quoted page this button's handler opens, or None when it has no handler.

    ``fields`` maps a field name to the text the page shows now.
    """
    source = _handler(data, page_id, button)
    if source is None:
        return None
    return run_handler(source, pages, page_id, fields)


def run_handler(
    source: str,
    pages: tuple[str, ...],
    page_id: str,
    fields: dict[str, str] | None = None,
) -> Follow:
    """Run the ``go to page``, ``send next``, ``send previous``, and field text lines.

    ``fields`` maps a field name to its text before the click. A write
    changes that text for the lines after it.
    """
    landed = {"page": page_id, "book": None}
    texts = {name.lower(): text for name, text in (fields or {}).items()}
    written: list[tuple[str, str]] = []
    shown: list[tuple[tuple[str, str | int], bool]] = []

    def statement(raw: str, low: str) -> None:
        changed = visibility(raw)
        if changed is not None:
            shown.append(changed)
            return
        found = quoted_go_to(raw)
        if found is not None:
            landed["page"], landed["book"] = found
            return
        if low in {"send next", "send previous"}:
            landed["page"] = _step(pages, page_id, 1 if low == "send next" else -1)
            landed["book"] = None
            return
        write = field_write(raw)
        if write is not None:
            name, expression = write
            value = text_value(expression, texts)
            if value is not None:
                texts[name.lower()] = value
                written.append((name, value))

    def condition(text: str) -> bool | None:
        known = reader_condition(text)
        if known is not None:
            return known
        return text_condition(text, texts)

    walk(source.splitlines(), Flow(), condition=condition, statement=statement)
    return Follow(landed["page"], landed["book"], tuple(written), tuple(shown))


_FIELD = re.compile(r'^text\s+of\s+field\s+"([^"]*)"\s*', re.IGNORECASE)
_SET_FIELD = re.compile(r'^set\s+text\s+of\s+field\s+"([^"]*)"\s+to\s+(.+)$', re.IGNORECASE)
_PUT_FIELD = re.compile(r'^text\s+of\s+field\s+"([^"]*)"\s*=\s*(.+)$', re.IGNORECASE)
_COMPARE = re.compile(r"^(.+?)\s*(<>|=|\bis not\b|\bis\b)\s*(.+)$", re.IGNORECASE)


_KINDS = ("field", "button", "rectangle", "ellipse", "line", "polygon")
_TARGET = rf'({"|".join(_KINDS)})\s+(?:"([^"]*)"|id\s+(\d+))'
_HIDE = re.compile(rf"^(hide|show)\s+{_TARGET}$", re.IGNORECASE)
_SET_VISIBLE = re.compile(rf"^set\s+visible\s+of\s+{_TARGET}\s+to\s+(true|false)$", re.IGNORECASE)


def visibility(line: str) -> tuple[tuple[str, str | int], bool] | None:
    """``((kind, name or id), shown)`` for ``hide``, ``show``, or ``set visible of``."""
    text = line.strip()
    found = _HIDE.match(text)
    if found is not None:
        shown = found.group(1).lower() == "show"
        kind, name, number = found.group(2), found.group(3), found.group(4)
    else:
        found = _SET_VISIBLE.match(text)
        if found is None:
            return None
        kind, name, number = found.group(1), found.group(2), found.group(3)
        shown = found.group(4).lower() == "true"
    key: str | int = int(number) if number is not None else name.lower()
    return (kind.lower(), key), shown


def field_write(line: str) -> tuple[str, str] | None:
    """``(field name, expression)`` for ``text of field "x" = ...`` or ``set text of field "x" to ...``."""
    text = line.strip()
    found = _SET_FIELD.match(text) or _PUT_FIELD.match(text)
    if found is None:
        return None
    return found.group(1), found.group(2).strip()


def text_value(expression: str, texts: dict[str, str]) -> str | None:
    """A quoted string, a number, or ``text of field "x"``, joined by ``&`` and ``&&``.

    None when any part is something else.
    """
    parts: list[str] = []
    joins: list[str] = []
    rest = expression.strip()
    while True:
        value, rest = _operand(rest, texts)
        if value is None:
            return None
        parts.append(value)
        rest = rest.lstrip()
        if not rest:
            break
        if rest.startswith("&&"):
            joins.append(" ")
            rest = rest[2:].lstrip()
        elif rest.startswith("&"):
            joins.append("")
            rest = rest[1:].lstrip()
        else:
            return None
    out = parts[0]
    for join, part in zip(joins, parts[1:]):
        out = out + join + part
    return out


def text_condition(text: str, texts: dict[str, str]) -> bool | None:
    """``text of field "x" = "y"``, ``<>``, ``is``, and ``is not``. Strings compare without case."""
    found = _COMPARE.match(text.strip())
    if found is None or "text of field" not in text.lower():
        return None
    left = text_value(found.group(1), texts)
    right = text_value(found.group(3), texts)
    if left is None or right is None:
        return None
    same = left.lower() == right.lower()
    operator = " ".join(found.group(2).lower().split())
    return same if operator in {"=", "is"} else not same


def _operand(text: str, texts: dict[str, str]) -> tuple[str | None, str]:
    if text.startswith('"'):
        chars: list[str] = []
        index = 1
        while index < len(text):
            if text[index] == '"':
                if text.startswith('""', index):
                    chars.append('"')
                    index += 2
                    continue
                return "".join(chars), text[index + 1:]
            chars.append(text[index])
            index += 1
        return None, ""
    found = _FIELD.match(text)
    if found is not None:
        name = found.group(1).lower()
        if name not in texts:
            return None, ""
        return texts[name], text[found.end():]
    number = re.match(r"-?\d+", text)
    if number is not None:
        return number.group(0), text[number.end():]
    return None, ""


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
