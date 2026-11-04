"""The source text of a ``buttonClick`` handler.

An ordinary object's script is inline when the low two bits of the byte
at ``+0x0A`` are 0. The word at ``+0x0B`` is a near pointer. A page or a
background uses the byte at ``+0x30`` and the word at ``+0x2A``. The word
at the pointer is a count of bytes to skip. The next word is the length
of the bytecode, and those bytes follow it.

The bytecode is the encoding in the decompile record, chapter 14, from
``FUN_1040_0970``. A keyword id is an entry in ``KEYWORDS``. A
back-reference copies from this segment, not from the expanded text.
This module returns the text. It does not call the handler. The page
window runs a subset of that text: ``enterPage`` field writes, a quoted
``go to page``, ``send next``, ``send previous``, and the quiz-button
cases. Opening a book follows that same quoted ``go to page`` in the
startup handlers and in the entry page's ``enterPage``. A ``linkDLL``
line is not called. The OpenScript engine runs ``forward`` (``openscript/interp.py``).
"""

from __future__ import annotations

import re
import struct
from dataclasses import dataclass

from opentoolbook.field import _chars, _name, _segments, _trailer, _u16
from opentoolbook.keywords import KEYWORDS
from opentoolbook.record import Book

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


_QUOTED_PAGE = re.compile(r'go\s+to\s+page\s*\(?\s*"([^"]*)"', re.IGNORECASE)
_QUOTED_BOOK = re.compile(r'of\s+book\s*\(?\s*"([^"]*)"', re.IGNORECASE)


def quoted_go_to(line: str) -> tuple[str, str | None] | None:
    """The quoted page and the quoted book on one ``go to page`` line.

    A page or a book that is not in double quotes is not returned.
    ``send next`` is not a page id.
    """
    found = _QUOTED_PAGE.search(line)
    if not found:
        return None
    book = _QUOTED_BOOK.search(line, found.end())
    return found.group(1), book.group(1) if book else None


def button_clicks(data: bytes) -> tuple[ButtonClick, ...]:
    """Every inline ``buttonClick`` in the book, in the order the records are stored."""
    found: list[ButtonClick] = []
    for item in object_scripts(data):
        handler = _button_click(item.source)
        if handler:
            found.append(ButtonClick(item.owner, item.name, handler))
    return tuple(found)


@dataclass(frozen=True)
class ObjectScript:
    """One inline object script, as source text. ``kind`` is the record class."""

    owner: str
    name: str
    kind: int
    source: str


def object_scripts(data: bytes) -> tuple[ObjectScript, ...]:
    """Every inline script in the book, in stored order, whatever handlers it holds."""
    found: list[ObjectScript] = []
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
            if text:
                found.append(ObjectScript(owner, _object_name(data, trailer, at, kind), kind, text))
            at += size
    return tuple(found)


def handler_sites(data: bytes, name: str) -> tuple[tuple[str, str, str], ...]:
    """Where ``to handle NAME`` starts a handler: ``(place, owner, object)``.

    The places are inline object scripts, type 10 scripts, and type 19
    shared scripts. The match ignores case and spacing. The handler is
    not called.
    """
    header = re.compile(r"^\s*to\s+handle\s+" + re.escape(name) + r"\b", re.IGNORECASE | re.MULTILINE)
    sites: list[tuple[str, str, str]] = []
    for item in object_scripts(data):
        sites.extend(("inline", item.owner, item.name) for _ in header.finditer(item.source))
    for place, reader in (("type 10", resource_scripts), ("type 19", shared_scripts)):
        try:
            stored = reader(data)
        except ValueError:
            # A book with no resource segment stores no such script.
            stored = ()
        for item in stored:
            sites.extend((place, str(item.resource_id), "") for _ in header.finditer(item.source))
    return tuple(sites)


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
    if kind in (_PAGE, _BACKGROUND) and (mode & 3) == 2 and word:
        # The script is the type 10 resource whose id is the word minus 1.
        return _resource_source(data, word - 1)
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
    """Expand ``span`` bytecode bytes at ``origin`` inside ``blob``.

    A zero byte ends the handler. The span is the bound.
    """
    out = bytearray()
    pos = origin
    end = min(len(blob), origin + span)
    while pos < end:
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


@dataclass(frozen=True)
class ResourceScript:
    """One type 10 handler, as source text. ``source`` is not a call."""

    resource_id: int
    source: str


# Header slot (type + 5) * 4. Type 10 stores the handler bytes.
_SCRIPT_TYPE = 10
_SCRIPT_BYTES = 15
_SCRIPT_CLASS = 0x2A


_RESOURCES: dict[int, tuple[bytes, dict[int, str]]] = {}


def _resource_source(data: bytes, resource_id: int) -> str:
    """The source of one type 10 handler, or the empty string."""
    cached = _RESOURCES.get(id(data))
    if cached is None or cached[0] is not data:
        try:
            table = {item.resource_id: item.source for item in resource_scripts(data)}
        except (ValueError, IndexError, KeyError, struct.error):
            table = {}
        cached = (data, table)
        _RESOURCES[id(data)] = cached
    return cached[1].get(resource_id, "")


def book_script(data: bytes) -> str:
    """The book's own script.

    The low two bits of the byte at ``+0x26`` of the book record are 2 when
    the script is a type 10 resource; the word at ``+0x24`` is that id plus 1.
    A book whose word is 0 has no book script.
    """
    from opentoolbook.field import _book

    try:
        _segment, record = _book(data, _segments(data))
    except (ValueError, IndexError, KeyError, struct.error):
        return ""
    if record + 0x27 > len(data):
        return ""
    word = _u16(data, record + 0x24)
    if word == 0 or data[record + 0x26] & 3 != 2:
        return ""
    return _resource_source(data, word - 1)


def resource_scripts(data: bytes) -> tuple[ResourceScript, ...]:
    """Every type 10 handler. The word at ``+9`` names a length and the bytes.

    The record is 15 bytes and starts with ``0x0202``, ``0x0001``. The
    word at the pointer is a count, and the last byte of that count is
    0. The reader expands the whole count. It does not call the handler.
    """
    book = Book(data)
    records = {item.key: item for item in book.records}
    handle = _u32(data, book.header + 8 + (_SCRIPT_TYPE + 5) * 4)
    directory, _record = _at(records, handle)
    count = _u16(data, directory + 2)
    table, _table_record = _at(records, (handle & 0xFFFF0000) | _u16(data, directory + 0x0E))
    found: list[ResourceScript] = []
    for index in range(count):
        entry = table + index * 8
        _first, near, segment, ident = struct.unpack_from("<HHHH", data, entry)
        resource, record = _at(records, (segment << 16) | near)
        if _u16(data, resource - 2) != _SCRIPT_CLASS:
            raise ValueError(f"type 10 resource {ident} is not class {_SCRIPT_CLASS:#x}")
        length = _u16(data, resource - 4) - near
        if length != _SCRIPT_BYTES or _u16(data, resource) != 0x0202 or _u16(data, resource + 2) != 0x0001:
            raise ValueError(f"type 10 resource {ident} is not a 15-byte handler record")
        base = record.position - 6
        origin = base + _u16(data, resource + 9)
        if origin + 2 > record.position + record.length:
            raise ValueError(f"type 10 resource {ident} pointer is past the segment")
        span = _u16(data, origin)
        start = origin + 2
        if span == 0 or start + span > record.position + record.length:
            raise ValueError(f"type 10 resource {ident} handler is past the segment")
        found.append(ResourceScript(ident, _expand(data, start, span)))
    return tuple(found)


@dataclass(frozen=True)
class BookHandler:
    """One handler defined in an .sbk. ``name`` is not a call.

    ``arguments`` is the rest of the header line, with the spaces around
    it removed. ``body_start`` is the source offset of the next line.
    """

    book: str
    kind: str
    name: str
    arguments: str
    body_start: int


# A column-0 handler header in a system-book script.
_BOOK_HEADER = re.compile(r"^to\s+(handle|get|set)\s+(\S+)(.*)$", re.IGNORECASE)


def book_handlers(book: str, source: str) -> tuple[BookHandler, ...]:
    """Handlers in one system-book script.

    ``source`` is the type 10 text the reader already expanded. A column-0
    line ``to handle``, ``to get``, or ``to set`` names a handler whose
    body is in ``book``. The name and the argument list are on that line.
    The body starts on the next line. The reader does not call the handler.
    """
    found: list[BookHandler] = []
    offset = 0
    for line in source.splitlines(keepends=True):
        text = line.rstrip("\r\n")
        if text and not text[0].isspace():
            match = _BOOK_HEADER.match(text)
            if match is not None:
                found.append(BookHandler(
                    book,
                    match.group(1).lower(),
                    match.group(2),
                    match.group(3).strip(),
                    offset + len(line),
                ))
        offset += len(line)
    return tuple(found)


@dataclass(frozen=True)
class SharedScript:
    """One type 19 shared script, as source text. ``source`` is not a call."""

    resource_id: int
    source: str


# Header slot (type + 5) * 4. Type 19 stores a shared script.
_SHARED_TYPE = 19
_SHARED_MARK = b"\x01\x02\x13\x00"
# Opcode pair for the words ``to handle``.
_TO_HANDLE = b"\x80\x81"


def shared_scripts(data: bytes) -> tuple[SharedScript, ...]:
    """Every type 19 shared script. The word at ``+9`` names the payload.

    The record is 15 bytes and starts with ``0x0202``. The payload starts
    ``01 02 13 00``. The handler is the first ``80 81`` in that payload.
    The reader expands until opcode 0. It does not call the handler. A
    zero directory handle is no shared script.
    """
    book = Book(data)
    records = {item.key: item for item in book.records}
    handle = _u32(data, book.header + 8 + (_SHARED_TYPE + 5) * 4)
    if handle == 0:
        return ()
    directory, _record = _at(records, handle)
    count = _u16(data, directory + 2)
    table, _table_record = _at(records, (handle & 0xFFFF0000) | _u16(data, directory + 0x0E))
    pending: list[tuple[int, int, object, int]] = []
    for index in range(count):
        entry = table + index * 8
        _first, near, segment, ident = struct.unpack_from("<HHHH", data, entry)
        resource, record = _at(records, (segment << 16) | near)
        pending.append((resource, ident, record, near))
    found: list[SharedScript] = []
    for resource, ident, record, near in pending:
        if _u16(data, resource - 2) != _SCRIPT_CLASS:
            raise ValueError(f"type 19 resource {ident} is not class {_SCRIPT_CLASS:#x}")
        length = _u16(data, resource - 4) - near
        if length != _SCRIPT_BYTES or _u16(data, resource) != 0x0202:
            raise ValueError(f"type 19 resource {ident} is not a 15-byte script record")
        base = record.position - 6
        origin = base + _u16(data, resource + 9)
        later = [
            other
            for other, _other_id, other_record, _other_near in pending
            if other_record is record and other > resource
        ]
        limit = min(later) if later else record.position + record.length
        if origin < 0 or origin + len(_SHARED_MARK) > limit or data[origin:origin + 4] != _SHARED_MARK:
            raise ValueError(f"type 19 resource {ident} payload is not a shared script")
        at = data.find(_TO_HANDLE, origin, limit)
        if at < 0:
            raise ValueError(f"type 19 resource {ident} has no handler")
        found.append(SharedScript(ident, _expand(data, at, limit - at)))
    return tuple(found)


def _at(records: dict, handle: int):
    record = records.get(handle >> 16)
    if record is None:
        raise ValueError("resource segment is missing")
    return record.position - 6 + (handle & 0xFFFF), record


def _u32(data: bytes, offset: int) -> int:
    return struct.unpack_from("<I", data, offset)[0]


def _button_click(text: str) -> str | None:
    return named_handler(text, "buttonclick")


def named_handler(text: str, message: str) -> str | None:
    """The ``to handle message`` handler in ``text`` (CR LF lines), or None."""
    wanted = message.lower()
    lines = text.split("\r\n")
    start = None
    name = None
    for index, line in enumerate(lines):
        parts = line.strip().split()
        if (
            len(parts) >= 3
            and parts[0].lower() == "to"
            and parts[1].lower() == "handle"
            and parts[2].lower() == wanted
        ):
            start = index
            name = parts[2].lower()
            break
    if start is None:
        return None
    stop = len(lines)
    named = None
    bare = None
    limit = len(lines)
    for index in range(start + 1, len(lines)):
        stripped = lines[index].strip().lower()
        parts = stripped.split()
        if len(parts) >= 3 and parts[0] == "to" and parts[1] == "handle":
            limit = index
            break
        if len(parts) >= 2 and parts[0] == "end" and parts[1] == name:
            named = index
            break
        if stripped == "end" and bare is None:
            bare = index
    if named is not None:
        stop = named + 1
        if all(not lines[index].strip() for index in range(named + 1, limit)):
            stop = limit
    elif bare is not None:
        stop = bare + 1
    return "\r\n".join(lines[start:stop])
