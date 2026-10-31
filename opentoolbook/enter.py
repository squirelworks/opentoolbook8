"""The enterPage statements the page window runs.

``getFirst`` returns ``__studentFirst`` with the ends stripped, or
``Student`` when that variable is empty. A missing ``sysLevel`` is
``reader``. ``&&`` is one operator and is recognized before ``&``. A
value that still contains ``__`` and ``of this book`` is not written
over the field.

The page's handler runs first, then the background's ``enterBackground``
and ``enterPage``, then the book's ``enterPage``, the order ``forward``
passes the message. A later write to the same field wins.
"""

from __future__ import annotations

from opentoolbook.field import _book, _chars, _page_handles, _segments, _u16
from opentoolbook.script import _script, resource_scripts

_PAGE = 5


def get_first(student_first: str | None) -> str:
    """``__studentFirst`` with the ends stripped, or ``Student`` when empty."""
    if student_first is None:
        return "Student"
    stripped = student_first.strip()
    return stripped if stripped else "Student"


def concatenate(
    expression: str,
    *,
    student_first: str | None = None,
    page_id: str | None = None,
) -> str:
    """Join one expression. ``&&`` inserts a space. ``&`` does not."""
    tokens = list(_tokens(expression))
    parts: list[list[tuple[str, str, str]]] = [[]]
    operators: list[str] = []
    for kind, value, source in tokens:
        if kind in {"and", "andand"}:
            parts.append([])
            operators.append(kind)
            continue
        parts[-1].append((kind, value, source))
    values = [_operand(part, student_first, page_id) for part in parts]
    result = values[0] if values else ""
    for operator, value in zip(operators, values[1:]):
        result = f"{result} {value}" if operator == "andand" else result + value
    return result


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


def blocks_write(value: str) -> bool:
    """True when the value still names an unresolved property of this book."""
    return "__" in value and "of this book" in value.lower()


def enter_fields(
    data: bytes,
    page_id: str,
    fields: tuple[tuple[str, str, tuple[tuple[int, str | None], ...]], ...],
    *,
    student_first: str | None = None,
    sys_level: str | None = None,
) -> tuple[tuple[str, str, tuple[tuple[int, str | None], ...]], ...]:
    """Field text after the page's ``enterPage`` handler.

    ``fields`` is ``(name, text, runs)`` in paint order. ``sys_level``
    ``None`` is missing, and a missing ``sysLevel`` is ``reader``.
    """
    from opentoolbook.click import background_script

    handler = _enter_page(page_source(data, page_id))
    behind = background_script(data, page_id)
    backdrop = [found for found in (_handler(behind, "enterbackground"), _enter_page(behind)) if found]
    book = _book_enter(data)
    if not handler and not book and not backdrop:
        return fields
    reader = (sys_level is None) or sys_level.lower() == "reader"
    names = tuple(name for name, _text, _runs in fields)
    found = []
    for source in [handler, *backdrop, book]:
        if source:
            found.extend(_assignments(source.splitlines(), reader, student_first, page_id, names))
    out = list(fields)
    for name, value in found:
        if blocks_write(value):
            continue
        for index, (field_name, text, runs) in enumerate(out):
            if field_name.lower() != name.lower():
                continue
            out[index] = (field_name, value, cover_style(text, value, runs))
    return tuple(out)


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


def _assignments(
    lines: list[str],
    reader: bool,
    student_first: str | None,
    page_id: str,
    names: tuple[str, ...],
):
    index = 0
    while index < len(lines):
        low = _norm(lines[index])
        if low.startswith("if ") and low.endswith(" then"):
            condition = low[3:-5].strip()
            index += 1
            taken, skipped, index = _split_if(lines, index)
            chosen = _branch(condition, reader, names, taken, skipped)
            if chosen is not None:
                yield from _assignments(chosen, reader, student_first, page_id, names)
            continue
        found = _set_text(lines[index])
        if found is not None:
            name, expression = found
            yield name, concatenate(expression, student_first=student_first, page_id=page_id)
        index += 1


def _branch(condition: str, reader: bool, names: tuple[str, ...], taken: list[str], skipped: list[str]):
    if condition in {"syslevel = reader", 'syslevel = "reader"'}:
        return taken if reader else skipped
    if condition in {"syslevel = author", 'syslevel = "author"'}:
        return skipped if reader else taken
    folded = condition.replace(" ", "")
    if folded == 'isobject(field"page#"ofparentofthispage)':
        if any(name.lower() == "page#" for name in names):
            return taken
        return skipped
    return None


def _split_if(lines: list[str], index: int):
    taken: list[str] = []
    skipped: list[str] = []
    branch = taken
    depth = 0
    while index < len(lines):
        low = _norm(lines[index])
        if low.startswith("if ") and low.endswith(" then"):
            depth += 1
            branch.append(lines[index])
            index += 1
            continue
        if low == "else" and depth == 0:
            branch = skipped
            index += 1
            continue
        if low == "end if" and depth == 0:
            return taken, skipped, index + 1
        if low == "end if":
            depth -= 1
        branch.append(lines[index])
        index += 1
    return taken, skipped, index


def _set_text(line: str) -> tuple[str, str] | None:
    text = line.strip()
    if not text.lower().startswith("set text of field "):
        return None
    mark = text.find('"')
    if mark < 0:
        return None
    end = text.find('"', mark + 1)
    if end < 0:
        return None
    name = text[mark + 1:end]
    rest = text[end + 1:].strip()
    folded = rest.lower()
    parent = "of parent of this page"
    if folded.startswith(parent):
        rest = rest[len(parent):].strip()
        folded = rest.lower()
    if not folded.startswith("to "):
        return None
    return name, rest[3:].strip()


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


def _operand(tokens: list[tuple[str, str, str]], student_first: str | None, page_id: str | None) -> str:
    if len(tokens) == 1 and tokens[0][0] == "str":
        return tokens[0][1]
    if (
        len(tokens) == 3
        and tokens[0][0] == "word"
        and tokens[0][1].lower() == "getfirst"
        and tokens[1][0] == "("
        and tokens[2][0] == ")"
    ):
        return get_first(student_first)
    if page_id is not None and _source(tokens).lower() == "name of this page":
        return page_id
    return _source(tokens)


def _source(tokens: list[tuple[str, str, str]]) -> str:
    out = []
    for index, (kind, _value, source) in enumerate(tokens):
        if index and kind != ")" and tokens[index - 1][0] != "(":
            out.append(" ")
        out.append(source)
    return "".join(out)


def _tokens(expression: str):
    index = 0
    size = len(expression)
    while index < size:
        char = expression[index]
        if char.isspace():
            index += 1
            continue
        if char == '"':
            chars: list[str] = []
            index += 1
            while index < size:
                if expression[index] == '"':
                    if index + 1 < size and expression[index + 1] == '"':
                        chars.append('"')
                        index += 2
                        continue
                    index += 1
                    break
                chars.append(expression[index])
                index += 1
            yield "str", "".join(chars), ""
            continue
        if expression.startswith("&&", index):
            yield "andand", "&&", "&&"
            index += 2
            continue
        if char == "&":
            yield "and", "&", "&"
            index += 1
            continue
        if char in "()":
            yield char, char, char
            index += 1
            continue
        start = index
        while index < size and (expression[index].isalnum() or expression[index] == "_"):
            index += 1
        if index == start:
            yield "word", char, char
            index += 1
            continue
        word = expression[start:index]
        yield "word", word, word


def _norm(line: str) -> str:
    return " ".join(line.strip().lower().split())
