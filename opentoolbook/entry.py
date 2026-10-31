"""The page a book opens on.

ToolBook sends ``enterSystem``, then ``enterApplication``, then shows a
page. A quoted ``go to page`` in a branch this reader takes is that page.
The reader takes ``sysLevel = reader`` because a missing ``sysLevel`` is
``reader``. ``__studentRecords`` that has not been set is 0, so
``openSession`` returns 0 and ``gotoPageList`` does not run. The names in
``gotoPageList`` are not quoted. ``forward`` is not executed. A
``linkDLL`` line is not called. ``fileExists32`` is not called; a quoted
name in that check is looked up with the same search as the book report.

When those handlers do not name a page, the page is the first one stored
in the book's page list. That page's ``enterPage`` is read the same way.
"""

from __future__ import annotations

import re
import struct
from dataclasses import dataclass, field
from pathlib import Path

from opentoolbook.enter import _enter_page, _norm
from opentoolbook.field import page_ids
from opentoolbook.script import book_handlers, quoted_go_to, resource_scripts
from opentoolbook.shelf import find_file, open_book, search_roots

_GET = re.compile(r"^get\s+([a-z_][a-z0-9_]*)\s*\((.*)\)\s*$")
_ASSIGN = re.compile(r"^([A-Za-z_][A-Za-z0-9_]*)\s*=\s*(.+)$")
_BOOK_CALL = re.compile(r"of\s+book\s+([A-Za-z_][A-Za-z0-9_]*)\s*\(", re.IGNORECASE)
_FILE_EXISTS = re.compile(r'^fileexists32\("([^"]*)"\) = 1$')
_IT_IS = re.compile(r"^it is (\d+)$")
_COMPARE = re.compile(r"^([a-z_][a-z0-9_]*) = (false|true|\d+)$")
_MESSAGES = ("entersystem", "enterapplication")
_OTHER_STARTUP = ("opensession", "gotopagelist", "entersystem", "enterapplication")


@dataclass(frozen=True)
class Entry:
    """The page the window opens, and the book file that holds it."""

    page_id: str
    book: Path
    data: bytes
    # System variables the startup handlers assigned, by lower-case name.
    variables: dict[str, object] = field(default_factory=dict)


@dataclass
class _State:
    pages: tuple[str, ...]
    handlers: dict[str, str]
    roots: tuple[Path, ...]
    book_file: str
    variables: dict[str, object] = field(default_factory=dict)
    it: object = 0
    page_id: str | None = None
    book_name: str | None = None
    book_error: str | None = None
    returning: bool = False
    return_value: object = None
    breaking: bool = False
    stack: list[str] = field(default_factory=list)


def opening_page(path: Path, home: Path | None = None) -> Entry:
    """The page ``path`` opens on, after the startup handlers and ``enterPage``.

    The system variables those handlers assigned come back on the entry,
    so a click in the window reads the same ``lastbook`` and ``nextpage``.
    """
    variables: dict[str, object] = {}
    try:
        data = path.read_bytes()
    except OSError as exc:
        raise ValueError(f"no opening page in {path.name}: {exc}") from exc
    try:
        opened = open_book(path, home)
    except ValueError as exc:
        raise ValueError(f"no opening page in {path.name}: {exc}") from exc
    pages = _pages(data)
    handlers = _companion_handlers(opened)
    handlers.update(_handler_map(data))
    roots = search_roots(path, home)
    page, other = choose_opening(
        pages,
        handlers,
        _page_scripts(data, pages),
        roots=roots,
        book_name=path.name,
        variables=variables,
    )
    current_path = path
    current_data = data
    seen = {(path.resolve(), page.lower())}
    while other:
        found = find_file(roots, other)
        if found is None:
            raise ValueError(f"{other} was not found; {page} of that book is the opening page")
        current_path = found
        current_data = found.read_bytes()
        current_pages = _pages(current_data)
        matched = _match(current_pages, page)
        if matched is None:
            raise ValueError(f"{page} is not a page of {found.name}")
        page = matched
        key = (found.resolve(), page.lower())
        if key in seen:
            break
        seen.add(key)
        handlers.update(_handler_map(current_data))
        page, other = choose_opening(
            current_pages,
            handlers,
            _page_scripts(current_data, current_pages),
            roots=roots,
            book_name=found.name,
            startup=False,
            page_id=page,
            variables=variables,
        )
    return Entry(page, current_path, current_data, variables)


def choose_opening(
    pages: tuple[str, ...],
    handlers: dict[str, str],
    page_scripts: dict[str, str] | None = None,
    *,
    roots: tuple[Path, ...] = (),
    book_name: str = "book.tbk",
    startup: bool = True,
    page_id: str | None = None,
    variables: dict[str, object] | None = None,
) -> tuple[str, str | None]:
    """``(page id, other book or None)`` after startup and this book's ``enterPage``.

    ``handlers`` maps a lower-case handler name to its source. ``page_scripts``
    maps a page id to that page's script. An other book is a file name, not
    a path. The caller resolves it. ``variables`` is filled with the system
    variables the handlers assign.
    """
    state = _State(pages, {key.lower(): value for key, value in handlers.items()}, roots, book_name)
    if variables is not None:
        state.variables = variables
    state.page_id = page_id
    if startup:
        _run_startup(state)
        if state.page_id is None:
            if not pages:
                raise ValueError(
                    f"no opening page in {book_name}: the startup handlers do not name a page, "
                    "and the book has no stored page"
                )
            state.page_id = pages[0]
        elif state.book_name is None:
            matched = _match(pages, state.page_id)
            if matched is None:
                raise ValueError(f"{state.page_id} is not a page of {book_name}")
            state.page_id = matched
    if state.book_error and not state.book_name:
        raise ValueError(
            f"{state.book_error} was not found; {state.page_id} of the book it names is the opening page"
        )
    if state.book_name:
        return state.page_id or "", state.book_name
    scripts = page_scripts or {}
    seen: set[str] = set()
    for _hop in range(4):
        if state.book_name:
            return state.page_id or "", state.book_name
        matched = _match(pages, state.page_id or "")
        if matched is None:
            raise ValueError(f"{state.page_id} is not a page of {book_name}")
        state.page_id = matched
        if matched.lower() in seen:
            return matched, None
        seen.add(matched.lower())
        before = matched
        _follow_enter(state, _script_for(scripts, matched))
        if state.book_error and not state.book_name:
            raise ValueError(
                f"{state.book_error} was not found; {state.page_id} of the book it names is the opening page"
            )
        if state.book_name:
            return state.page_id or "", state.book_name
        if (state.page_id or "").lower() == before.lower():
            return before, None
    matched = _match(pages, state.page_id or "")
    if matched is None:
        raise ValueError(f"{state.page_id} is not a page of {book_name}")
    return matched, None


def _run_startup(state: _State) -> None:
    names = [name for name in _MESSAGES if name in state.handlers]
    if not names:
        for name in _OTHER_STARTUP:
            if name in state.handlers and name not in names:
                names.append(name)
        for name in sorted(state.handlers):
            if name.startswith("initialize") and name not in names:
                names.append(name)
    for name in names:
        _call(name, state)
        state.breaking = False
        state.returning = False


def _follow_enter(state: _State, source: str) -> None:
    handler = _enter_page(source)
    if not handler:
        return
    _walk(handler.splitlines(), state)
    state.breaking = False
    state.returning = False


def _walk(lines: list[str], state: _State) -> object:
    index = 0
    while index < len(lines):
        if state.returning or state.breaking:
            return state.return_value
        raw = lines[index]
        low = _norm(raw)
        if not low or low.startswith("--"):
            index += 1
            continue
        if low.startswith("to handle") or low.startswith("to get") or low.startswith("to set"):
            index += 1
            continue
        if low.startswith("linkdll"):
            index += 1
            while index < len(lines) and not _norm(lines[index]).startswith("end linkdll"):
                index += 1
            index += 1
            continue
        if low in {"end", "end if"} or (
            low.startswith("end ")
            and not low.startswith("end if")
            and not low.startswith("end step")
            and not low.startswith("end conditions")
            and not low.startswith("end link")
        ):
            return state.return_value if state.returning else None
        if low == "forward":
            index += 1
            continue
        if low == "break":
            state.breaking = True
            return None
        if low.startswith("if "):
            condition = low[3:-5].strip() if low.endswith(" then") else low[3:].strip()
            index += 1
            taken, skipped, index = _split_if(lines, index)
            known = _condition(condition, state)
            if known is True:
                _walk(taken, state)
            elif known is False:
                _walk(skipped, state)
            if state.returning or state.breaking:
                return state.return_value
            continue
        found = quoted_go_to(raw)
        if found is not None:
            page, book = found
            if book is None:
                book, error = _book_from_call(raw, state)
                if error:
                    state.book_error = error
            state.page_id = page
            state.book_name = book
            index += 1
            continue
        if low.startswith("return"):
            state.return_value = _return_value(low, state)
            state.returning = True
            return state.return_value
        call = _GET.match(low)
        if call is not None:
            state.it = _call(call.group(1), state)
            index += 1
            continue
        if low in {"send next", "send previous"}:
            step = 1 if low == "send next" else -1
            current = state.page_id or (state.pages[0] if state.pages else "")
            state.page_id = _step(state.pages, current, step)
            state.book_name = None
            index += 1
            continue
        assigned = _ASSIGN.match(raw.strip())
        if assigned is not None:
            value = _value(assigned.group(2).strip(), state)
            if value is not None:
                state.variables[assigned.group(1).lower()] = value
            index += 1
            continue
        index += 1
    return state.return_value if state.returning else None


def _book_from_call(line: str, state: _State) -> tuple[str | None, str | None]:
    found = _BOOK_CALL.search(line)
    if found is None:
        return None, None
    name = found.group(1)
    value = _call(name.lower(), state)
    if isinstance(value, str) and value:
        return value, None
    return None, name


def _call(name: str, state: _State) -> object:
    key = name.lower()
    if key in state.stack or key not in state.handlers or len(state.stack) > 8:
        return None
    state.stack.append(key)
    state.returning = False
    state.return_value = None
    state.breaking = False
    value = _walk(state.handlers[key].splitlines(), state)
    state.stack.pop()
    state.returning = False
    state.breaking = False
    return value


def _condition(text: str, state: _State) -> bool | None:
    low = " ".join(text.lower().split())
    if low in {'syslevel = reader', 'syslevel = "reader"'}:
        return True
    if low in {'syslevel <> reader', 'syslevel <> "reader"'}:
        return False
    exists = _FILE_EXISTS.fullmatch(low)
    if exists is not None:
        return find_file(state.roots, exists.group(1)) is not None
    compared = _IT_IS.fullmatch(low)
    if compared is not None:
        return str(state.it) == compared.group(1)
    named = _COMPARE.fullmatch(low)
    if named is not None:
        expected = _literal(named.group(2))
        if named.group(1) not in state.variables:
            return expected in (False, 0)
        return state.variables[named.group(1)] == expected
    return None


def _literal(text: str) -> object:
    if text == "false":
        return False
    if text == "true":
        return True
    if re.fullmatch(r"-?\d+", text):
        return int(text)
    return text


def _value(expr: str, state: _State) -> object | None:
    low = expr.lower()
    if low in {"false", "true"} or re.fullmatch(r"-?\d+", expr):
        return _literal(low)
    if low == "name of this book":
        return state.book_file
    if len(expr) >= 2 and expr[0] == '"' and expr[-1] == '"':
        return expr[1:-1]
    return None


def _return_value(low: str, state: _State) -> object:
    expr = low[6:].strip()
    if not expr:
        return None
    if expr in state.variables:
        return state.variables[expr]
    value = _value(expr, state)
    if value is not None:
        return value
    return expr


def _split_if(lines: list[str], index: int) -> tuple[list[str], list[str], int]:
    taken: list[str] = []
    skipped: list[str] = []
    branch = taken
    depth = 0
    while index < len(lines):
        low = _norm(lines[index])
        if low.startswith("if "):
            depth += 1
            branch.append(lines[index])
            index += 1
            continue
        if low == "else" and depth == 0:
            branch = skipped
            index += 1
            continue
        if low in {"end", "end if"} and depth == 0:
            return taken, skipped, index + 1
        if low in {"end", "end if"}:
            depth -= 1
        branch.append(lines[index])
        index += 1
    return taken, skipped, index


def _step(pages: tuple[str, ...], page_id: str, step: int) -> str:
    try:
        index = pages.index(page_id)
    except ValueError:
        return page_id
    moved = index + step
    if moved < 0 or moved >= len(pages):
        return page_id
    return pages[moved]


def _pages(data: bytes) -> tuple[str, ...]:
    try:
        return page_ids(data)
    except (ValueError, IndexError, struct.error):
        return ()


def _page_scripts(data: bytes, pages: tuple[str, ...]) -> dict[str, str]:
    from opentoolbook.enter import page_source

    found = {}
    for page_id in pages:
        try:
            found[page_id] = page_source(data, page_id)
        except (ValueError, IndexError, struct.error):
            continue
    return found


def _script_for(scripts: dict[str, str], page_id: str) -> str:
    if page_id in scripts:
        return scripts[page_id]
    for key, value in scripts.items():
        if key.lower() == page_id.lower():
            return value
    return ""


def _companion_handlers(opened) -> dict[str, str]:
    found: dict[str, str] = {}
    for item in opened.files:
        if item.path is None or item.path.suffix.lower() not in {".tbk", ".sbk"}:
            continue
        try:
            data = item.path.read_bytes()
        except OSError:
            continue
        for name, body in _handler_map(data).items():
            found.setdefault(name, body)
    return found


def _handler_map(data: bytes) -> dict[str, str]:
    found: dict[str, str] = {}
    try:
        scripts = resource_scripts(data)
    except (ValueError, IndexError, KeyError, struct.error):
        return found
    for item in scripts:
        for name, body in _bodies(item.source):
            found.setdefault(name.lower(), body)
    return found


def _bodies(source: str) -> tuple[tuple[str, str], ...]:
    headers = book_handlers("book", source)
    found = []
    for index, header in enumerate(headers):
        start = source.rfind("\n", 0, header.body_start - 1)
        start = 0 if start < 0 else start + 1
        if index + 1 < len(headers):
            end = source.rfind("\n", 0, headers[index + 1].body_start - 1)
            if end < 0:
                end = headers[index + 1].body_start
        else:
            end = len(source)
        found.append((header.name, source[start:end]))
    return tuple(found)


def _match(pages: tuple[str, ...], page_id: str) -> str | None:
    for page in pages:
        if page.lower() == page_id.lower():
            return page
    return None
