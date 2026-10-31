"""The page a book opens on.

ToolBook sends ``enterSystem``, ``enterApplication``, then ``enterBook``, then shows a
page. A quoted ``go to page`` in a branch this reader takes is that page.
The reader takes ``sysLevel = reader`` because a missing ``sysLevel`` is
``reader``. ``it`` is the value of the last ``get``. ``__studentRecords``
that has not been set is 0, so ``openSession`` returns 0 and ``gotoPageList`` does not run. The names in
``gotoPageList`` are not quoted. ``forward`` is not executed. A
``linkDLL`` line is not called. ``fileExists32`` is not a DLL call here:
it is 1 when the book report's search finds the quoted name, else 0.

When those handlers do not name a page, the page is the first one stored
in the book's page list. That page's ``enterPage`` is read the same way.
"""

from __future__ import annotations

import re
import struct
from dataclasses import dataclass, field
from pathlib import Path

from opentoolbook.classtbl import bound_sysbooks
from opentoolbook.enter import _enter_page
from opentoolbook.field import page_ids
from opentoolbook.props import UserProperties
from opentoolbook.script import book_handlers, quoted_go_to, resource_scripts
from opentoolbook.send import calls_dll
from opentoolbook.shelf import MissingBook, file_exists32, find_file, open_book, search_roots
from opentoolbook.walk import norm, reader_condition, this_name, walk

_SEND = re.compile(r"^send\s+([a-z_][a-z0-9_]*)$")
_GET = re.compile(r"^get\s+([a-z_][a-z0-9_]*)\s*\((.*)\)\s*$")
_ASSIGN = re.compile(r"^([A-Za-z_][A-Za-z0-9_]*)\s*=\s*(.+)$")
_BOOK_CALL = re.compile(r"of\s+book\s+([A-Za-z_][A-Za-z0-9_]*)\s*\(", re.IGNORECASE)
_FILE_EXISTS = re.compile(r'^fileexists32\(\s*"([^"]*)"\s*\)$')
_FILE_EXISTS_IS = re.compile(r'^fileexists32\(\s*"([^"]*)"\s*\)\s*(=|<>)\s*(-?\d+)$')
_GET_VALUE = re.compile(r"^get\s+(.+)$")
_IT_IS = re.compile(r'^it (?:is|=) (-?\d+|true|false|"[^"]*")$')
_COMPARE = re.compile(r"^([a-z_][a-z0-9_]*) = (false|true|\d+)$")
_MESSAGES = ("entersystem", "enterapplication", "enterbook")
_PUSH_SYSBOOKS = re.compile(r'^push\s+"([^"]+)"\s+onto\s+sysbooks$')
_IN_SYSBOOKS = re.compile(r'^"([^"]+)"\s+is\s+(not\s+)?in\s+sysbooks$')


@dataclass(frozen=True)
class Entry:
    """The page the window opens, and the book file that holds it."""

    page_id: str
    book: Path
    data: bytes
    props: UserProperties = field(default_factory=UserProperties)
    # System variables the startup handlers assigned, by lower-case name.
    variables: dict[str, object] = field(default_factory=dict)
    # ``sysBooks`` after startup, first item first, in lower case.
    sysbooks: tuple[str, ...] = ()


@dataclass
class _State:
    pages: tuple[str, ...]
    handlers: dict[str, str]
    roots: tuple[Path, ...]
    book_file: str
    variables: dict[str, object] = field(default_factory=dict)
    props: UserProperties = field(default_factory=UserProperties)
    it: object = 0
    page_id: str | None = None
    book_name: str | None = None
    book_error: str | None = None
    returning: bool = False
    return_value: object = None
    breaking: bool = False
    stack: list[str] = field(default_factory=list)
    skipped: list[str] = field(default_factory=list)
    # ``sysBooks``, first item first. A pushed book's handlers follow the open book's.
    sysbooks: list[str] = field(default_factory=list)
    own: dict[str, str] | None = None
    loaded: dict[str, dict[str, str]] = field(default_factory=dict)


def opening_page(path: Path, home: Path | None = None, props: UserProperties | None = None) -> Entry:
    """The page ``path`` opens on, after the startup handlers and ``enterPage``.

    The ``__`` names those handlers assign are kept in ``props`` and
    returned on the entry, so the window reads the same values. The
    system variables those handlers assigned come back on the entry too,
    so a click in the window reads the same ``lastbook`` and ``nextpage``.
    """
    if props is None:
        props = UserProperties()
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
    roots = search_roots(path, home)
    handlers = _handler_map(data)
    sysbooks = add_bound_sysbooks([], data, roots)
    page, other = choose_opening(
        pages,
        handlers,
        _page_scripts(data, pages),
        roots=roots,
        book_name=path.name,
        props=props,
        variables=variables,
        sysbooks=sysbooks,
    )
    current_path = path
    current_data = data
    seen = {(path.resolve(), page.lower())}
    while other:
        found = find_file(roots, other)
        if found is None:
            raise MissingBook(other, page, roots)
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
        handlers = _handler_map(current_data)
        page, other = choose_opening(
            current_pages,
            handlers,
            _page_scripts(current_data, current_pages),
            roots=roots,
            book_name=found.name,
            startup=False,
            page_id=page,
            props=props,
            variables=variables,
            sysbooks=sysbooks,
        )
    return Entry(page, current_path, current_data, props, variables, tuple(sysbooks))


def choose_opening(
    pages: tuple[str, ...],
    handlers: dict[str, str],
    page_scripts: dict[str, str] | None = None,
    *,
    roots: tuple[Path, ...] = (),
    book_name: str = "book.tbk",
    startup: bool = True,
    page_id: str | None = None,
    props: UserProperties | None = None,
    variables: dict[str, object] | None = None,
    sysbooks: list[str] | None = None,
) -> tuple[str, str | None]:
    """``(page id, other book or None)`` after startup and this book's ``enterPage``.

    ``handlers`` maps a lower-case handler name to its source. ``page_scripts``
    maps a page id to that page's script. An other book is a file name, not
    a path. The caller resolves it. ``props`` keeps the ``__`` names the
    handlers assign. ``variables`` is filled with the system
    variables the handlers assign.
    """
    state = _State(pages, {key.lower(): value for key, value in handlers.items()}, roots, book_name)
    if props is not None:
        state.props = props
    if variables is not None:
        state.variables = variables
    if sysbooks is not None:
        state.sysbooks = sysbooks
        _merge_sysbooks(state)
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
        raise MissingBook(state.book_error, state.page_id or "", state.roots)
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
            raise MissingBook(state.book_error, state.page_id or "", state.roots)
        if state.book_name:
            return state.page_id or "", state.book_name
        if (state.page_id or "").lower() == before.lower():
            return before, None
    matched = _match(pages, state.page_id or "")
    if matched is None:
        raise ValueError(f"{state.page_id} is not a page of {book_name}")
    return matched, None


def _run_startup(state: _State) -> None:
    """``enterSystem``, ``enterApplication``, then ``enterBook``, each when a handler answers it."""
    engine, host = _engine(state)
    for name in _MESSAGES:
        if engine.handles(name):
            _guarded(engine, lambda name=name: engine.send(name))
        if host.book_error:
            break
    _sync(state, host, engine)


def _engine(state: _State):
    from opentoolbook.run import BookHost, engine_for

    host = BookHost(state.pages, state.book_file, state.roots)
    host.page_id = state.page_id
    host.book_name = state.book_name
    return engine_for(state, host), host


def _guarded(engine, run) -> None:
    from opentoolbook.openscript.values import ScriptError

    try:
        run()
    except ScriptError as exc:
        engine.skipped.append(f"error: {exc}")


def _sync(state: _State, host, engine) -> None:
    state.page_id = host.page_id
    state.book_name = host.book_name
    if host.book_error and not state.book_error:
        state.book_error = host.book_error
    state.skipped.extend(engine.skipped)


def _follow_enter(state: _State, source: str) -> None:
    """Run the page's own ``enterPage``. ``forward`` passes it to the book and ``sysBooks``."""
    from opentoolbook.run import parsed

    handler = parsed(source).handlers.get("handle enterpage") if source else None
    if handler is None:
        return
    engine, host = _engine(state)
    _guarded(engine, lambda: engine._run(handler, "enterpage", "handle", -1, (), None))
    _sync(state, host, engine)


def _walk(lines: list[str], state: _State) -> object:
    return walk(
        lines,
        state,
        condition=lambda text: _condition(text, state),
        statement=lambda raw, low: _statement(raw, low, state),
        returns=lambda expr: _return_value(expr, state),
    )


def _statement(raw: str, low: str, state: _State) -> None:
    pushed = _PUSH_SYSBOOKS.fullmatch(low)
    if pushed is not None:
        push_sysbook(state, pushed.group(1))
        return
    found = quoted_go_to(raw)
    if found is not None:
        page, book = found
        if book is None:
            book, error = _book_from_call(raw, state)
            if error:
                state.book_error = error
        state.page_id = page
        state.book_name = book
        return
    exists = _FILE_EXISTS.fullmatch(low[4:].strip()) if low.startswith("get ") else None
    if exists is not None:
        state.it = file_exists32(state.roots, exists.group(1))
        return
    call = _GET.match(low)
    if call is not None:
        state.it = _call(call.group(1), state)
        return
    got = _GET_VALUE.match(raw.strip())
    if got is not None:
        state.it = _get_value(got.group(1).strip(), state)
        return
    if low in {"send next", "send previous"}:
        step = 1 if low == "send next" else -1
        current = state.page_id or (state.pages[0] if state.pages else "")
        state.page_id = _step(state.pages, current, step)
        state.book_name = None
        return
    sent = _SEND.match(low)
    if sent is not None:
        _send(sent.group(1), state)
        return
    assigned = _ASSIGN.match(raw.strip())
    if assigned is not None:
        value = _value(assigned.group(2).strip(), state)
        if value is not None:
            _assign(state, assigned.group(1), value)


def _send(name: str, state: _State) -> object:
    """``send name``: the handler runs unless it links a DLL."""
    body = state.handlers.get(name.lower())
    if body is None:
        return None
    if calls_dll(body):
        state.skipped.append(name.lower())
        return None
    return _call(name, state)


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
    low = norm(text)
    member = _IN_SYSBOOKS.fullmatch(low)
    if member is not None:
        present = member.group(1).lower() in state.sysbooks
        return not present if member.group(2) else present
    reader = reader_condition(low)
    if reader is not None:
        return reader
    exists = _FILE_EXISTS_IS.fullmatch(low)
    if exists is not None:
        same = file_exists32(state.roots, exists.group(1)) == int(exists.group(3))
        return same if exists.group(2) == "=" else not same
    alone = _FILE_EXISTS.fullmatch(low)
    if alone is not None:
        return file_exists32(state.roots, alone.group(1)) == 1
    compared = _IT_IS.fullmatch(low)
    if compared is not None:
        expected = compared.group(1)
        if expected.startswith('"'):
            return str(state.it if state.it is not None else "").lower() == expected[1:-1]
        return _same(state.it, _literal(expected))
    named = _COMPARE.fullmatch(low)
    if named is not None:
        expected = _literal(named.group(2))
        if not _known(state, named.group(1)):
            return expected in (False, 0)
        return _lookup(state, named.group(1)) == expected
    return None


def push_sysbook(state: _State, name: str) -> None:
    """``push "name" onto sysBooks``: the book goes first in ``sysBooks``.

    Handler lookup is the open book, then each book in ``sysBooks`` in
    order. A book the shelf does not find is still listed and adds no
    handler. The name is kept in lower case.
    """
    key = name.lower()
    if key in state.sysbooks:
        state.sysbooks.remove(key)
    state.sysbooks.insert(0, key)
    _merge_sysbooks(state)


def _merge_sysbooks(state: _State) -> None:
    """Handlers: the open book's own, then each ``sysBooks`` book in order."""
    if state.own is None:
        state.own = dict(state.handlers)
    merged = dict(state.own)
    for book in state.sysbooks:
        if book not in state.loaded:
            state.loaded[book] = sysbook_handlers(state.roots, book)
        for handler, body in state.loaded[book].items():
            merged.setdefault(handler, body)
    state.handlers.clear()
    state.handlers.update(merged)


def add_bound_sysbooks(sysbooks: list[str], data: bytes, roots: tuple[Path, ...]) -> list[str]:
    """Append the book's bound system books that ``sysBooks`` lacks, as a book open does.

    A bound book that the shelf finds adds its own bound books the same
    way, because it is an open book too. Names are kept in lower case.
    """
    pending = [data]
    while pending:
        for name in bound_sysbooks(pending.pop(0)):
            key = name.lower()
            if key in sysbooks:
                continue
            sysbooks.append(key)
            found = find_file(roots, key)
            if found is not None:
                try:
                    pending.append(found.read_bytes())
                except OSError:
                    pass
    return sysbooks


def sysbook_handlers(roots: tuple[Path, ...], name: str) -> dict[str, str]:
    """Handlers of one ``sysBooks`` book found on the shelf, or none."""
    found = find_file(roots, name)
    if found is None:
        return {}
    try:
        return _handler_map(found.read_bytes())
    except OSError:
        return {}


def _assign(state: _State, name: str, value: object) -> None:
    if UserProperties.owns(name):
        state.props.set(name, value)
    else:
        state.variables[name.lower()] = value


def _known(state: _State, name: str) -> bool:
    if UserProperties.owns(name):
        return name in state.props
    return name.lower() in state.variables


def _lookup(state: _State, name: str) -> object:
    if UserProperties.owns(name):
        return state.props.get(name)
    return state.variables.get(name.lower())


def _get_value(expr: str, state: _State) -> object:
    """The value ``get expr`` stores in ``it``: a literal, a name, or nothing."""
    value = _value(expr, state)
    if value is not None:
        return value
    if re.fullmatch(r"[A-Za-z_][A-Za-z0-9_]*", expr) and _known(state, expr):
        return _lookup(state, expr)
    return None


def _same(found: object, expected: object) -> bool:
    if found is None:
        return expected in (False, 0)
    if isinstance(expected, bool) or isinstance(found, bool):
        return str(found).lower() == str(expected).lower()
    return str(found) == str(expected)


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
    named = this_name(low, state.page_id, state.book_file)
    if named is not None:
        return named
    exists = _FILE_EXISTS.fullmatch(low)
    if exists is not None:
        return file_exists32(state.roots, exists.group(1))
    if len(expr) >= 2 and expr[0] == '"' and expr[-1] == '"':
        return expr[1:-1]
    return None


def _return_value(expr: str, state: _State) -> object:
    if _known(state, expr):
        return _lookup(state, expr)
    value = _value(expr, state)
    if value is not None:
        return value
    return expr


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
