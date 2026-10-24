"""A quiz question page.

The page has five fields, named ``Stem``, ``A``, ``B``, ``C``, and ``D``.
In the same record's trailer, the slot before a property name holds the
value: the word ``0x0009``, a length, and that many characters. Two
question pages use that for ``Answer``, ``QuestionNo``, and ``TestNo``.
"""

from __future__ import annotations

import struct
from dataclasses import dataclass

from opentoolbook.field import (
    _book,
    _chars,
    _field_text,
    _name,
    _page_handles,
    _segments,
    _trailer,
    _u16,
)

FIELD = 0xA
FIELD_BYTES = 61
PAGE = 5
CHOICES = ("A", "B", "C", "D")


@dataclass(frozen=True)
class Question:
    page_id: str
    test_no: str
    question_no: str
    answer: str
    stem: str
    choices: tuple[tuple[str, str], ...]


def questions(data: bytes) -> tuple[Question, ...]:
    """Question pages whose stem, choices, and answer property are all present."""
    segments = _segments(data)
    by_key = {segment.key: segment for segment in segments}
    book_segment, book_record = _book(data, segments)
    found: list[Question] = []
    for handle in _page_handles(data, by_key, book_segment, book_record):
        segment = by_key.get(handle >> 16)
        if segment is None:
            continue
        record = segment.base + (handle & 0xFFFF)
        if record < 2 or record + 8 > len(data) or _u16(data, record - 2) != PAGE:
            continue
        page_id = _chars(data, record + 6, 32)
        trailer = _trailer(data, segment)
        if trailer is None:
            continue
        fields = _named_fields(data, segment, trailer)
        if any(name not in fields for name in ("Stem", *CHOICES)):
            continue
        props = _properties(trailer)
        if any(name not in props for name in ("Answer", "QuestionNo", "TestNo")):
            continue
        found.append(Question(
            page_id,
            props["TestNo"],
            props["QuestionNo"],
            props["Answer"],
            fields["Stem"],
            tuple((letter, fields[letter]) for letter in CHOICES),
        ))
    return tuple(found)


def _named_fields(data: bytes, segment, trailer) -> dict[str, str]:
    end = segment.file_at + segment.size
    found: dict[str, str] = {}
    at = segment.base + 0x10
    while at + FIELD_BYTES <= end and at >= 4:
        kind = _u16(data, at - 2)
        size = _u16(data, at - 4) - (at - segment.base)
        if kind == FIELD and size == FIELD_BYTES:
            name = _name(trailer, _u16(data, at + 6))
            if name and name not in found:
                found[name] = _field_text(trailer, _u16(data, at + 0x24))
        at += 2
    return found


def _properties(trailer) -> dict[str, str]:
    blob = trailer.heaps.get(1)
    if not blob:
        return {}
    found: dict[str, str] = {}
    slots = trailer.slots
    for index in range(len(slots) - 1):
        heap, start, _one, _two = slots[index]
        next_heap, name_at, _three, _four = slots[index + 1]
        if heap != 1 or next_heap != 1 or name_at <= start or name_at >= len(blob):
            continue
        end = blob.find(b"\x00", name_at)
        if end < 0:
            continue
        name = blob[name_at:end].decode("latin-1")
        if not name or not name[0].isalpha():
            continue
        window = blob[start:name_at]
        mark = window.find(b"\x09\x00")
        if mark < 0 or mark + 4 > len(window):
            continue
        length = struct.unpack_from("<H", window, mark + 2)[0]
        value_at = mark + 4
        if length <= 0 or value_at + length > len(window):
            continue
        raw = window[value_at:value_at + length]
        if any(byte < 32 or byte >= 127 for byte in raw):
            continue
        found.setdefault(name, raw.decode("latin-1"))
    return found
