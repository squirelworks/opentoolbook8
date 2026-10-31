"""A ``buttonClick`` the reader already expanded.

A quoted ``go to page`` opens that page. ``of book`` names the other
file when the line quotes one. ``go to page (name) of book(name)`` and
``go to page name of book name`` read those two system variables when a
handler this runner executed assigned them a string; otherwise the page
stays. A handler line ``name = "text"``, ``name = name of this book``, or
``name = name of this page`` assigns that system variable. ``send next`` and
``send previous`` are the next and previous pages in the stored page
list. ``if``, ``break``, and ``return`` are the shared walker in
``walk.py``. ``text of field "x" = ...`` and ``set text of field "x" to
...`` write a field's text, and a later condition reads that text.
``hide`` and ``show`` of a field, button, rectangle, ellipse, line, or
polygon, by name or by ``id``, and ``set visible of ... to``, change
whether it is painted. ``get gotoMenuPage()`` opens the page that
system-book handler names. A line that is not one of those is not a
page change.
``beep`` does nothing and returns. ``request "..."`` records its text and
does not change the page.
"""

from __future__ import annotations

import re
import struct
from collections.abc import Callable
from dataclasses import dataclass

from opentoolbook.field import _book, _chars, _page_handles, _segments, _u16
from opentoolbook.script import _button_click, _script, button_clicks, quoted_go_to
from opentoolbook.walk import Flow, is_beep, reader_condition, request_text, walk

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
_GET = re.compile(r"^get\s+([a-z_][a-z0-9_]*)\s*\(\s*\)$")


@dataclass(frozen=True)
class Follow:
    """The page a handler opens. ``book`` is None when it stays in this book."""

    page_id: str
    book: str | None
    requests: tuple[str, ...] = ()
    beeps: int = 0
    fields: tuple[tuple[str, str], ...] = ()
    visible: tuple[tuple[tuple[str, str | int], bool], ...] = ()
    inverts: tuple[tuple[str, bool], ...] = ()
    # Properties a script set: (owner, kind, lower-case name, property, value), in order.
    # The owner is a page id or a background key.
    writes: tuple[tuple[str, str, str, str, object], ...] = ()


def follow_click(
    data: bytes,
    page_id: str,
    button: str,
    pages: tuple[str, ...],
    variables: dict[str, object] | None = None,
    book: str = "",
    fields: dict[str, str] | None = None,
    *,
    call: Callable[[str], str | None] | None = None,
) -> Follow | None:
    """The page this button's handler opens, or None when it has no handler.

    ``variables`` is the window's system variables. The handler's
    assignments are written into it. ``book`` is ``name of this book``.
    ``fields`` maps a field name to the text the page shows now.
    """
    source = _handler(data, page_id, button)
    if source is None:
        return None
    return run_handler(source, pages, page_id, variables, book, fields, call=call)


def page_click(
    data: bytes,
    page_id: str,
    pages: tuple[str, ...],
    variables=None,
    book: str = "",
    fields: dict[str, str] | None = None,
) -> Follow | None:
    """The page's own ``buttonClick``, or None when the page script has none."""
    from opentoolbook.enter import page_source

    text = page_source(data, page_id)
    source = _button_click(text.replace("\r\n", "\n").replace("\n", "\r\n")) if text else None
    if source is None:
        return None
    return run_handler(source, pages, page_id, variables, book, fields)


def run_handler(
    source: str,
    pages: tuple[str, ...],
    page_id: str,
    variables: dict[str, object] | None = None,
    book_name: str = "",
    fields: dict[str, str] | None = None,
    *,
    call: Callable[[str], str | None] | None = None,
    objects: Callable[[str, str | int], bool] | None = None,
) -> Follow:
    """Run the assignment, ``go to page``, ``send next``, ``send previous``, and field text lines.

    ``set invert of button "x" to true`` or ``false`` is recorded in
    ``inverts``. ``objects(kind, name or id)`` answers ``isObject``; without
    it that condition is unknown and neither branch runs.

    ``variables`` maps a lower-case system variable name to the value a
    handler this runner executed assigned it. This handler's assignments
    are written into it. ``book_name`` is ``name of this book``. ``fields``
    maps a field name to its text before the click. A write changes that
    text for the lines after it. ``call`` runs a ``get name()`` line and
    returns the page that handler goes to, or None when it does not
    change the page.
    """
    known = variables if variables is not None else {}
    landed = {"page": page_id, "book": None}
    asked: list[str] = []
    beeps = [0]
    texts = {name.lower(): text for name, text in (fields or {}).items()}
    written: list[tuple[str, str]] = []
    shown: list[tuple[tuple[str, str | int], bool]] = []
    inverted: list[tuple[str, bool]] = []

    def statement(raw: str, low: str) -> None:
        invert = _SET_INVERT.match(raw.strip())
        if invert is not None:
            inverted.append((invert.group(1), invert.group(2).lower() == "true"))
            return
        changed = visibility(raw)
        if changed is not None:
            shown.append(changed)
            return
        if is_beep(raw):
            beeps[0] += 1
            return
        asked_text = request_text(raw)
        if asked_text is not None:
            asked.append(asked_text)
            return
        text = raw.strip()
        found = quoted_go_to(raw)
        if found is not None:
            landed["page"], landed["book"] = found
            return
        write = field_write(raw)
        if write is not None:
            name, expression = write
            value = text_value(expression, texts)
            if value is not None:
                texts[name.lower()] = value
                written.append((name, value))
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
        called = _GET.match(low)
        if called is not None and call is not None:
            moved = call(called.group(1))
            if moved is not None:
                landed["page"], landed["book"] = moved, None
            return
        if low in {"send next", "send previous"}:
            landed["page"] = _step(pages, page_id, 1 if low == "send next" else -1)
            landed["book"] = None

    def condition(text: str) -> bool | None:
        settled = reader_condition(text)
        if settled is not None:
            return settled
        found = _IS_OBJECT.match(text.strip())
        if found is not None:
            if objects is None:
                return None
            kind, name, number = found.group(1), found.group(2), found.group(3)
            return objects(kind.lower(), int(number) if number is not None else name.lower())
        return text_condition(text, texts)

    walk(source.splitlines(), Flow(), condition=condition, statement=statement)
    return Follow(
        landed["page"], landed["book"], tuple(asked), beeps[0], tuple(written), tuple(shown), tuple(inverted)
    )


_FIELD = re.compile(r'^text\s+of\s+field\s+"([^"]*)"\s*', re.IGNORECASE)
_SET_FIELD = re.compile(r'^set\s+text\s+of\s+field\s+"([^"]*)"\s+to\s+(.+)$', re.IGNORECASE)
_PUT_FIELD = re.compile(r'^text\s+of\s+field\s+"([^"]*)"\s*=\s*(.+)$', re.IGNORECASE)
_COMPARE = re.compile(r"^(.+?)\s*(<>|=|\bis not\b|\bis\b)\s*(.+)$", re.IGNORECASE)


_KINDS = ("field", "button", "rectangle", "ellipse", "line", "polygon")
_TARGET = rf'({"|".join(_KINDS)})\s+(?:"([^"]*)"|id\s+(\d+))'
_HIDE = re.compile(rf"^(hide|show)\s+{_TARGET}$", re.IGNORECASE)
_SET_VISIBLE = re.compile(rf"^set\s+visible\s+of\s+{_TARGET}\s+to\s+(true|false)$", re.IGNORECASE)


_SET_INVERT = re.compile(r'^set\s+invert\s+of\s+button\s+"([^"]*)"\s+to\s+(true|false)$', re.IGNORECASE)
_IS_OBJECT = re.compile(rf"^isobject\s*\(\s*{_TARGET}\s*\)$", re.IGNORECASE)
# The record class of an object whose inline script can hold a mouse message.
_CLASS = {"button": 0x9, "field": 0xA}


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
