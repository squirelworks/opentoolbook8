"""The page a book opens on.

ToolBook sends ``enterSystem``, ``enterApplication``, then ``enterBook``,
then shows a page. Those handlers run on the OpenScript interpreter. A
``go to page`` they run is the opening page. When they name none, the
page is the first one stored in the book's page list, and that page
then gets ``enterWindow``, ``enterBackground``, ``enterPage`` and
``firstIdle``.
"""

from __future__ import annotations

import struct
from dataclasses import dataclass, field
from pathlib import Path

from opentoolbook.classtbl import bound_sysbooks
from opentoolbook.field import page_ids
from opentoolbook.props import UserProperties
from opentoolbook.script import book_handlers
from opentoolbook.shelf import MissingBook, find_file, open_book, search_roots
from opentoolbook.tb80ini import read_tb80_ini

_MESSAGES = ("entersystem", "enterapplication", "enterbook")
# After those three, the window and the opening page, in the order a TB80RTM trace shows.
_PAGE_MESSAGES = ("enterwindow", "enterbackground", "enterpage", "firstidle")
# A book the window switches to gets these.
_SWITCH_MESSAGES = ("enterbook", "enterbackground", "enterpage")


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
    # Properties the startup handlers set, by book path, then owner, then (kind, name).
    objects: dict = field(default_factory=dict)


@dataclass
class _State:
    pages: tuple[str, ...]
    handlers: dict[str, str]
    roots: tuple[Path, ...]
    book_file: str
    variables: dict[str, object] = field(default_factory=dict)
    props: UserProperties = field(default_factory=UserProperties)
    page_id: str | None = None
    book_name: str | None = None
    book_error: str | None = None
    skipped: list[str] = field(default_factory=list)
    # ``sysBooks``, first item first. A pushed book's handlers follow the open book's.
    sysbooks: list[str] = field(default_factory=list)
    own: dict[str, str] | None = None
    loaded: dict[str, dict[str, str]] = field(default_factory=dict)
    data: bytes = b""
    # Properties the handlers set in this book, by owner, then (kind, name).
    objects: dict = field(default_factory=dict)


def opening_page(
    path: Path,
    home: Path | None = None,
    props: UserProperties | None = None,
    *,
    windows: Path | None = None,
    ini: Path | None = None,
) -> Entry:
    """The page ``path`` opens on, after the startup handlers and ``enterPage``.

    The ``__`` names those handlers assign are kept in ``props`` and
    returned on the entry, so the window reads the same values. The
    system variables those handlers assigned come back on the entry too,
    so a click in the window reads the same ``lastbook`` and ``nextpage``.
    ``windows`` is the Windows directory for the ``TB80.INI`` search.
    ``ini`` is an explicit ``TB80.INI`` path that skips that search.
    """
    if props is None:
        props = UserProperties()
    variables: dict[str, object] = {}
    try:
        data = path.read_bytes()
    except OSError as exc:
        raise ValueError(f"no opening page in {path.name}: {exc}") from exc
    try:
        open_book(path, home)
    except ValueError as exc:
        raise ValueError(f"no opening page in {path.name}: {exc}") from exc
    pages = _pages(data)
    roots = search_roots(path, home)
    handlers = _handler_map(data)
    settings = read_tb80_ini(path, windows=windows, override=ini)
    sysbooks = list(settings.startup_sysbooks)
    sysbooks = add_bound_sysbooks(sysbooks, data, roots)
    objects: dict = {}
    page, other = choose_opening(
        pages,
        handlers,
        _page_scripts(data, pages),
        roots=roots,
        book_name=path.name,
        props=props,
        variables=variables,
        sysbooks=sysbooks,
        data=data,
        objects=objects.setdefault(str(path), {}),
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
            data=current_data,
            objects=objects.setdefault(str(found), {}),
        )
    return Entry(page, current_path, current_data, props, variables, tuple(sysbooks), objects)


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
    data: bytes = b"",
    objects: dict | None = None,
) -> tuple[str, str | None]:
    """``(page id, other book or None)`` after startup and this book's ``enterPage``.

    ``handlers`` maps a lower-case handler name to its source. ``page_scripts``
    maps a page id to that page's script. An other book is a file name, not
    a path. The caller resolves it. ``props`` keeps the ``__`` names the
    handlers assign. ``variables`` is filled with the system
    variables the handlers assign. With ``data`` the messages run on the
    page, background, book, and ``sysBooks`` path, and ``objects`` keeps
    the properties they set. Startup sends ``enterSystem``,
    ``enterApplication`` and ``enterBook``, then ``enterWindow``,
    ``enterBackground``, ``enterPage`` and ``firstIdle`` on the opening
    page. A book opened after a switch (``startup`` False) gets
    ``enterBook``, ``enterBackground`` and ``enterPage``.
    """
    state = _State(pages, {key.lower(): value for key, value in handlers.items()}, roots, book_name)
    state.data = data
    if objects is not None:
        state.objects = objects
    if props is not None:
        state.props = props
    if variables is not None:
        state.variables = variables
    if sysbooks is not None:
        state.sysbooks = sysbooks
        _merge_sysbooks(state)
    state.page_id = page_id
    if data:
        return _open_on_page(state, startup)
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


def _open_on_page(state: _State, startup: bool) -> tuple[str, str | None]:
    """Send the opening messages on the interpreter. ``(page id, other book or None)``."""
    engine, host = _engine(state)
    from opentoolbook.openscript.interp import Ref

    def moved() -> bool:
        return bool(host.book_name) or bool(host.book_error)

    if startup:
        for name in _MESSAGES:
            _guarded(engine, lambda name=name: engine.send(name, (), Ref("book", "this", None, None)))
            if moved():
                break
        if not moved():
            if host.page_id is None:
                if not state.pages:
                    raise ValueError(
                        f"no opening page in {state.book_file}: the startup handlers do not name a page, "
                        "and the book has no stored page"
                    )
                host.page_id = state.pages[0]
            matched = _match(state.pages, host.page_id)
            if matched is None:
                raise ValueError(f"{host.page_id} is not a page of {state.book_file}")
            host.page_id = matched
        names = _PAGE_MESSAGES
    else:
        names = _SWITCH_MESSAGES
    for name in names if not moved() else ():
        if name == "enterwindow":
            to = Ref("book", "this", None, None)
        elif name == "enterbackground":
            to = Ref("background", "page", host.page_id, None)
        elif name == "enterbook":
            to = Ref("book", "this", None, None)
        else:
            to = Ref("page", "this", None, None)
        _guarded(engine, lambda name=name, to=to: engine.send(name, (), to))
        if moved():
            break
    _sync(state, host, engine)
    if state.book_error and not state.book_name:
        raise MissingBook(state.book_error, state.page_id or "", state.roots)
    if state.book_name:
        return state.page_id or "", state.book_name
    matched = _match(state.pages, state.page_id or "")
    if matched is None:
        raise ValueError(f"{state.page_id} is not a page of {state.book_file}")
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

    if state.data:
        from opentoolbook.clickrun import ClickHost

        host = ClickHost(state.pages, state.book_file, state.roots, state.page_id, {}, set(), state.data, (), state.objects)
    else:
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
    """The book script's handlers by lower-case name. Page scripts are not in it."""
    from opentoolbook.script import book_script

    found: dict[str, str] = {}
    for name, body in _bodies(book_script(data)):
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
