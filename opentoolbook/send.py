"""``send name`` to the open book, then to the books in ``sysBooks``.

The handler is looked up in the open book first, then in each book of
``sysBooks`` in order. ``sysBooks`` is what the book's own startup
handlers pushed onto it. No system book is named here. The books are
found with the same search as the book report. A handler whose body links or unlinks a DLL
(``linkDLL``, ``linkDLL32``, or ``unlinkDLL``) returns without running, so no DLL is
called. Every other handler runs on the OpenScript interpreter.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from pathlib import Path

_LINK = re.compile(r"^\s*(?:un)?linkdll(32)?\b", re.IGNORECASE | re.MULTILINE)


@dataclass(frozen=True)
class Sent:
    """What ``send name`` did. ``book`` is the file that holds the handler."""

    name: str
    book: str | None
    value: object = None
    skipped: bool = False
    page_id: str | None = None
    book_name: str | None = None


@dataclass(frozen=True)
class Chain:
    """Handlers by book, in lookup order. Each map is lower-case name to source."""

    books: tuple[tuple[str, dict[str, str]], ...] = field(default_factory=tuple)

    def find(self, name: str) -> tuple[str, str] | None:
        """``(book, source)`` of the first book that has ``name``."""
        key = name.lower()
        for book, handlers in self.books:
            if key in handlers:
                return book, handlers[key]
        return None

    def merged(self) -> dict[str, str]:
        """One map in which the first book that has a name wins."""
        found: dict[str, str] = {}
        for _book, handlers in self.books:
            for key, value in handlers.items():
                found.setdefault(key, value)
        return found


def calls_dll(source: str) -> bool:
    """True when the handler links or unlinks a DLL."""
    return _LINK.search(source) is not None


_CALLS = re.compile(r"([A-Za-z_][A-Za-z0-9_]*)\s*\(")


def reaches_dll(chain: Chain, name: str, seen: set[str] | None = None) -> str | None:
    """The handler on the path from ``name`` that links a DLL, or None.

    ``name`` itself counts. A call is a name followed by ``(`` that the
    chain holds. Each handler is followed once.
    """
    seen = set() if seen is None else seen
    key = name.lower()
    if key in seen:
        return None
    seen.add(key)
    found = chain.find(key)
    if found is None:
        return None
    _book, source = found
    if calls_dll(source):
        return name
    body = "\n".join(source.splitlines()[1:])
    for called in _CALLS.findall(body):
        reached = reaches_dll(chain, called, seen)
        if reached is not None:
            return reached
    return None


def handler_chain(
    data: bytes,
    book_name: str,
    roots: tuple[Path, ...],
    sysbooks: tuple[str, ...] = (),
) -> Chain:
    """The open book, then each ``sysBooks`` book the search finds, in order."""
    from opentoolbook.entry import _handler_map
    from opentoolbook.shelf import find_file

    books = [(book_name, _handler_map(data))]
    for name in sysbooks:
        found = find_file(roots, name)
        if found is None:
            continue
        try:
            books.append((found.name, _handler_map(found.read_bytes())))
        except OSError:
            continue
    return Chain(tuple(books))


def send_message(
    chain: Chain,
    name: str,
    *,
    pages: tuple[str, ...] = (),
    page_id: str | None = None,
    roots: tuple[Path, ...] = (),
    book_name: str = "book.tbk",
    props=None,
) -> Sent:
    """Send ``name`` down ``chain`` on the interpreter. A handler that links a DLL is skipped."""
    from opentoolbook.openscript.interp import Engine
    from opentoolbook.openscript.values import ScriptError
    from opentoolbook.props import UserProperties
    from opentoolbook.run import BookHost, chain_lookup

    found = chain.find(name)
    if found is None:
        return Sent(name, None)
    book, source = found
    if calls_dll(source):
        return Sent(name, book, skipped=True)
    host = BookHost(pages, book_name, roots)
    host.page_id = page_id
    engine = Engine(
        chain_lookup(lambda: [handlers for _book, handlers in chain.books]),
        host,
        props=props if props is not None else UserProperties(),
    )
    host.engine = engine
    try:
        if engine.handles(name):
            value = engine.send(name)
        else:
            value = engine.get(name)
    except ScriptError:
        value = None
    moved = host.page_id if host.page_id != page_id else None
    return Sent(name, book, value, page_id=moved, book_name=host.book_name)
