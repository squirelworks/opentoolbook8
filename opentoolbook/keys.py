"""Keys the book's own ``keyUp`` handler quotes.

The book script is the type 10 script that holds ``enterSystem`` or
``enterApplication``. Its ``keyUp`` handler is a ``conditions`` block of
``when key = keyX`` branches. A page whose record names its own type 10
script (mode byte ``+0x30`` low bits 2, resource id in the word at
``+0x2A``) and whose script has its own ``keyUp`` handles the key there,
and the book handler does not see it.

The runner performs one statement from a branch: ``send buttonClick to
button "name"``. A branch made of ``request``, ``open viewer``, ``get``
calls, or ``send exit`` is not run.
"""

from __future__ import annotations

import re
from dataclasses import dataclass

from opentoolbook.field import _book, _chars, _page_handles, _segments, _u16
from opentoolbook.script import resource_scripts

_PAGE = 5
# Tk key names to the OpenScript key constant the handler compares against.
KEYSYMS = {"Return": "keyenter", "KP_Enter": "keyenter"}
KEYSYMS.update({f"F{index}": f"keyf{index}" for index in range(1, 13)})

_HANDLER = re.compile(r"^\s*to\s+handle\s+keyup\b", re.IGNORECASE)
_WHEN = re.compile(r"^when\s+key\s+(?:=|is)\s+(key[a-z0-9]+)$")
_SEND_CLICK = re.compile(r'^send\s+buttonclick\s+to\s+button\s+"([^"]+)"$')
_STARTUP = re.compile(r"^\s*to\s+handle\s+(?:entersystem|enterapplication)\b", re.IGNORECASE | re.MULTILINE)


@dataclass(frozen=True)
class KeyHandler:
    """Where a key's ``keyUp`` handler is, and the branch it quotes for one key."""

    owner: str
    resource_id: int
    key: str
    branch: tuple[str, ...]
    button: str | None


def page_script_id(data: bytes, page_id: str) -> int | None:
    """The type 10 resource id a page record names for its script, or None."""
    segments = _segments(data)
    by_key = {segment.key: segment for segment in segments}
    book_segment, book_record = _book(data, segments)
    for handle in _page_handles(data, by_key, book_segment, book_record):
        segment = by_key.get(handle >> 16)
        if segment is None:
            continue
        record = segment.base + (handle & 0xFFFF)
        if record < 2 or record + 0x31 > len(data) or _u16(data, record - 2) != _PAGE:
            continue
        if _chars(data, record + 6, 32).lower() != page_id.lower():
            continue
        if data[record + 0x30] & 3 != 2:
            return None
        return _u16(data, record + 0x2A) or None
    return None


def key_up(source: str) -> list[str] | None:
    """The lines of the ``to handle keyUp`` handler in ``source``, or None."""
    lines = source.splitlines()
    for index, line in enumerate(lines):
        if not _HANDLER.match(line):
            continue
        body: list[str] = []
        for text in lines[index + 1:]:
            low = " ".join(text.lower().split())
            if low == "end" or low.startswith("end keyup") or re.match(r"^\s*to\s+(handle|get|set)\b", text, re.I):
                return body
            body.append(text)
        return body
    return None


def branch_for(body: list[str], key: str) -> tuple[str, ...] | None:
    """The first ``when key = KEY`` branch, in source order, or None when no branch quotes it."""
    wanted = key.lower()
    depth = 0
    taking = False
    found: list[str] = []
    for text in body:
        low = " ".join(text.split()).lower()
        if not low or low.startswith("--"):
            continue
        if low == "conditions":
            depth += 1
            if taking:
                found.append(low)
            continue
        if low == "end conditions":
            if taking and depth == 1:
                return tuple(found)
            depth -= 1
            if taking:
                found.append(low)
            continue
        if depth == 1 and (low.startswith("when ") or low == "else"):
            if taking:
                return tuple(found)
            match = _WHEN.match(low)
            taking = match is not None and match.group(1) == wanted
            continue
        if taking:
            found.append(low)
    return tuple(found) if taking else None


def key_handler(data: bytes, page_id: str, keysym: str) -> KeyHandler | None:
    """The handler and branch a key reaches on a page, or None when no handler quotes it."""
    key = KEYSYMS.get(keysym)
    if key is None:
        return None
    scripts = {item.resource_id: item.source for item in resource_scripts(data)}
    own = page_script_id(data, page_id)
    if own is not None and own in scripts:
        body = key_up(scripts[own])
        if body is not None:
            return _handler(page_id, own, key, body)
    for resource_id, source in scripts.items():
        if _STARTUP.search(source) is None:
            continue
        body = key_up(source)
        if body is not None:
            return _handler("book", resource_id, key, body)
    return None


def _handler(owner: str, resource_id: int, key: str, body: list[str]) -> KeyHandler | None:
    branch = branch_for(body, key)
    if branch is None:
        return KeyHandler(owner, resource_id, key, (), None) if owner != "book" else None
    button = None
    for low in branch:
        match = _SEND_CLICK.match(low)
        if match is not None:
            button = match.group(1)
            break
    return KeyHandler(owner, resource_id, key, branch, button)
