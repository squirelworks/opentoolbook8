"""Run a book's OpenScript with the interpreter in ``opentoolbook.openscript``.

A handler is looked up in the open book first, then in each ``sysBooks``
book in order. ``forward`` passes the message to the next book that has
a handler for it. The sources come from the reader's handler maps: one
source text per handler name, as the book stores it.
"""

from __future__ import annotations

import configparser
from pathlib import Path

from opentoolbook.openscript import ast as A
from opentoolbook.openscript.interp import Engine, Host, Ref
from opentoolbook.openscript.parser import parse_script
from opentoolbook.openscript.values import as_number, text

_PARSED: dict[str, A.Script] = {}


def parsed(source: str) -> A.Script:
    """The parse of ``source``, cached by its text."""
    found = _PARSED.get(source)
    if found is None:
        found = parse_script(source)
        _PARSED[source] = found
    return found


def chain_lookup(books):
    """A lookup over ``books()``: a callable that returns handler maps, first book first."""

    def lookup(kind: str, name: str) -> list:
        found = []
        key = f"{kind} {name}"
        for handlers in books():
            source = handlers.get(name)
            if source is None:
                continue
            handler = parsed(source).handlers.get(key)
            if handler is not None:
                found.append(handler)
        return found

    return lookup


# System properties a reader answers the same way every run.
_SYSTEM = {
    "syspluginmode": False,
    "sysruntime": True,
    "syssuspend": False,
    "syssuspendmessages": False,
    "syslockscreen": False,
    "syserror": "",
    "syserrornumber": 0,
}


class BookHost(Host):
    """The book the handlers run in: its pages, its file name, and its shelf.

    ``go to page "x"`` names a page of this book, and ``go to page "x" of
    book "y"`` a page of another book. ``name of this page`` is the page id
    and ``name of this book`` the file name. ``sysLevel`` is ``reader``.
    ``fileExists32`` is the shelf. ``GetPrivateProfileIntA`` and
    ``GetPrivateProfileStringA`` read an INI file the shelf finds, and
    return the default when it does not find one.
    """

    def __init__(self, pages: tuple[str, ...], book_file: str, roots: tuple[Path, ...]) -> None:
        self.pages = pages
        self.book_file = book_file
        self.roots = roots
        self.page_id: str | None = None
        self.book_name: str | None = None
        self.book_error: str | None = None

    def go(self, target: object) -> None:
        page, book = None, None
        if isinstance(target, Ref):
            if target.kind == "page":
                if target.by == "name" or target.by == "id":
                    page = self._numbered(target.value)
                elif target.by in {"next", "previous", "first", "last"}:
                    page = self._step(target.by)
                if isinstance(target.of, Ref) and target.of.kind == "book":
                    book = text(target.of.value)
                    if book == "":
                        engine = getattr(self, "engine", None)
                        self.book_error = (engine.unanswered if engine is not None else None) or "book"
                        return
            elif target.kind == "book":
                book = text(target.value)
                page = ""
        else:
            page = text(target)
        if page is None or page == "":
            return
        self.page_id = page
        self.book_name = book if book and book.lower() != self.book_file.lower() else None

    def _numbered(self, value: object) -> str:
        """A page name, or the page at that position when ``value`` is a number."""
        if isinstance(value, (int, float)) and not isinstance(value, bool) or text(value).strip().isdigit():
            index = int(as_number(value))
            if 1 <= index <= len(self.pages):
                return self.pages[index - 1]
            return ""
        wanted = text(value)
        # A page name matches regardless of case; the stored spelling is kept.
        return next((page for page in self.pages if page.lower() == wanted.lower()), wanted)

    def _step(self, by: str) -> str:
        if not self.pages:
            return ""
        if by == "first":
            return self.pages[0]
        if by == "last":
            return self.pages[-1]
        current = self.page_id or self.pages[0]
        lowered = [page.lower() for page in self.pages]
        index = lowered.index(current.lower()) if current.lower() in lowered else 0
        index += 1 if by == "next" else -1
        index = max(0, min(index, len(self.pages) - 1))
        return self.pages[index]

    def property(self, name: str, of: object) -> tuple[bool, object]:
        if of is None:
            if name == "syslevel":
                return True, "reader"
            if name in _SYSTEM:
                return True, _SYSTEM[name]
            if name == "systime":
                import time

                now = time.localtime()
                return True, (now.tm_hour * 3600 + now.tm_min * 60 + now.tm_sec) * 1000
            return False, None
        if isinstance(of, Ref) and of.by == "this":
            if name == "name" and of.kind == "page":
                return True, self.page_id or ""
            if name == "name" and of.kind == "book":
                return True, self.book_file
        return False, None

    def dll(self, library: str, name: str, args: tuple) -> tuple[bool, object]:
        if name == "fileexists32":
            return True, 1 if self.find_file(text(args[0]) if args else "") is not None else 0
        if name == "getprivateprofileinta":
            default = args[2] if len(args) > 2 else 0
            value = self._ini(args[3] if len(args) > 3 else "", args[0] if args else "", args[1] if len(args) > 1 else "")
            if value is None:
                return True, default
            try:
                return True, int(as_number(value))
            except Exception:
                return True, default
        if name == "getprivateprofilestringa":
            # (section, key, default, buffer, size, file): the INI value, else the default,
            # copied into the buffer argument and cut to size - 1 characters.
            found = self._ini(args[5] if len(args) > 5 else "", args[0] if args else "", args[1] if len(args) > 1 else "")
            value = text(found if found is not None else (args[2] if len(args) > 2 else ""))
            size = int(as_number(args[4])) if len(args) > 4 and text(args[4]).strip() else len(value) + 1
            value = value[: max(size - 1, 0)]
            self.dll_out = {3: value}
            return True, len(value)
        if name == "writeprivateprofilestringa":
            return True, 1
        return False, None

    def _ini(self, file: object, section: object, key: object) -> str | None:
        path = self.find_file(Path(text(file)).name) if text(file) else None
        if path is None:
            return None
        parser = configparser.ConfigParser(interpolation=None, strict=False)
        try:
            parser.read_string(Path(path).read_text(encoding="latin1"))
        except (OSError, configparser.Error):
            return None
        for name in parser.sections():
            if name.lower() == text(section).lower():
                for option, value in parser.items(name):
                    if option.lower() == text(key).lower():
                        return value
        return None

    def find_file(self, name: str):
        from opentoolbook.shelf import find_file

        return find_file(self.roots, name) if name else None


def engine_for(state, host: Host) -> Engine:
    """An engine over a startup ``_State``: its own handlers, then ``sysBooks``."""
    from opentoolbook.entry import _merge_sysbooks, sysbook_handlers

    def books():
        own = state.own if state.own is not None else state.handlers
        found = [own]
        for book in state.sysbooks:
            if book not in state.loaded:
                state.loaded[book] = sysbook_handlers(state.roots, book)
            found.append(state.loaded[book])
        return found

    def pushed(_name: str) -> None:
        _merge_sysbooks(state)

    engine = Engine(
        chain_lookup(books),
        host,
        props=state.props,
        variables=state.variables,
        sysbooks=state.sysbooks,
        on_push_sysbook=pushed,
    )
    host.engine = engine
    return engine
