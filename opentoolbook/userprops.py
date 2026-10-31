"""The user properties a book stores, such as ``__nidaVersion of this book``.

The names and values live in one run of tagged blocks. Each block starts
with three words: a link word, its id, and 0. A name block holds the name
and a NUL. A value block holds a word ``n`` and then ``n`` bytes. Those
bytes are either a type word (4 or 9), a length word, the characters, and
a NUL, or the characters and a NUL alone.

Block id 1 opens the run. Block id 2 closes it and is the property table:
a word, the entry count, and 0, then one eight-byte entry per property:
value id, name id, a hash word, and 0. The run is found from the
``:HDMEDIAPATH`` name block, which every book on the shelf stores. A value
whose bytes are neither form, such as ``_oldSaveOnClose`` with type word
``0x1F``, is left out.
"""

from __future__ import annotations

import struct

_ANCHOR = b":HDMEDIAPATH\x00"
_TYPED = (4, 9)
_OPEN = 1
_TABLE = 2
# The blocks are searched this far on either side of the anchor.
_REACH = 0x1000


def book_properties(data: bytes) -> dict[str, str]:
    """Lower-case property name to its stored text. Empty when none is found."""
    anchor = data.find(_ANCHOR)
    if anchor < 6 or struct.unpack_from("<H", data, anchor - 2)[0] != 0:
        return {}
    low = max(0, anchor - _REACH)
    high = min(len(data), anchor + _REACH)
    blocks = _blocks(data, low, high)
    opens = [place for place in blocks.get(_OPEN, ()) if place < anchor]
    if not opens:
        return {}
    start = opens[-1]
    for table in blocks.get(_TABLE, ()):
        if table < anchor:
            continue
        inside = {
            ident: [place for place in places if start <= place < table]
            for ident, places in blocks.items()
        }
        found = _table(data, table, inside)
        if found is not None:
            return found
    return {}


def _blocks(data: bytes, low: int, high: int) -> dict[int, list[int]]:
    """Block id to the offsets of every payload that carries it."""
    found: dict[int, list[int]] = {}
    for at in range(low, high - 6):
        _link, ident, zero = struct.unpack_from("<HHH", data, at)
        if zero == 0 and 0 < ident < 0x1000:
            found.setdefault(ident, []).append(at + 6)
    return found


def _table(data: bytes, at: int, blocks: dict[int, list[int]]) -> dict[str, str] | None:
    if at + 6 > len(data):
        return None
    _word, count, zero = struct.unpack_from("<HHH", data, at)
    if zero != 0 or not 1 <= count <= 256 or at + 6 + 8 * count > len(data):
        return None
    found: dict[str, str] = {}
    for index in range(count):
        value_id, name_id, _hash, pad = struct.unpack_from("<HHHH", data, at + 6 + 8 * index)
        if pad != 0:
            return None
        names = [name for name in (_cstring(data, place) for place in blocks.get(name_id, ())) if name]
        if len(names) != 1:
            return None
        values = [value for value in (_value(data, place) for place in blocks.get(value_id, ())) if value is not None]
        if len(values) == 1:
            found[names[0].lower()] = values[0]
    return found


def _value(data: bytes, at: int) -> str | None:
    if at + 2 > len(data):
        return None
    size = struct.unpack_from("<H", data, at)[0]
    body = data[at + 2:at + 2 + size]
    if len(body) != size or size == 0:
        return None
    if size >= 5:
        kind, length = struct.unpack_from("<HH", body, 0)
        if kind in _TYPED and length + 5 == size and body[4 + length] == 0:
            return body[4:4 + length].decode("latin1")
    if body[-1] != 0 or size < 2 or 0 in body[:-1]:
        return None
    if any(byte < 0x20 for byte in body[:-1]):
        return None
    return body[:-1].decode("latin1")


def _cstring(data: bytes, at: int) -> str:
    end = data.find(b"\x00", at, at + 256)
    if end < 0:
        return ""
    raw = data[at:end]
    if not raw or any(byte < 0x20 or byte > 0x7E for byte in raw):
        return ""
    return raw.decode("latin1")
