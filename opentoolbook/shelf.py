"""The files a lesson asks for, and the install list beside it.

``toolbook.lst`` is the playback set. A leading ``*`` marks a file the
list names and this install does not ship. A lesson then names a smaller
set in its own bytes: system books, the shell, and ``initialize*`` calls.
"""

from __future__ import annotations

import re
import struct
from dataclasses import dataclass
from pathlib import Path

from opentoolbook.record import Book

_FILE = re.compile(rb"(?<![A-Za-z0-9_.])[A-Za-z0-9_]{3,16}\.(?:sbk|tbk|dll|exe)", re.I)
_INIT = re.compile(rb"initialize[A-Za-z]+", re.I)
_ENTRY = ("opensession", "gotopagelist", "entersystem", "enterapplication")


class MissingBook(ValueError):
    """A book a handler names that the shelf search does not find.

    Opening a book and clicking a button raise this same error, so the
    sentence is the same: the file, then the page of that book.
    """

    def __init__(self, name: str, page_id: str, roots: tuple[Path, ...] = ()) -> None:
        self.name = name
        self.page_id = page_id
        self.roots = roots
        super().__init__(missing_sentence(name, page_id))


def missing_sentence(name: str, page_id: str) -> str:
    """``nida81.tbk was not found; P310 of that book does not open``."""
    return f"{name} was not found; {page_id} of that book does not open"


@dataclass(frozen=True)
class InstallFile:
    name: str
    optional: bool


def named_files(data: bytes) -> tuple[str, ...]:
    """File names a book mentions, in lower case, without the version fragment."""
    found = {match.group().decode("latin1").lower() for match in _FILE.finditer(data)}
    return tuple(sorted(found))


def lesson_names(data: bytes) -> tuple[str, ...]:
    """File names in the order the lesson wrote them. The first spelling is kept."""
    found: list[str] = []
    seen: set[str] = set()
    for match in _FILE.finditer(data):
        name = match.group().decode("latin1")
        key = name.lower()
        if key in seen:
            continue
        seen.add(key)
        found.append(name)
    return tuple(found)


def named_calls(data: bytes) -> tuple[str, ...]:
    """``initialize*`` words and the four entry calls the lesson shell uses."""
    found = {match.group().decode("latin1").lower() for match in _INIT.finditer(data)}
    lowered = data.lower()
    for name in _ENTRY:
        if name.encode("ascii") in lowered:
            found.add(name)
    return tuple(sorted(found))


def parse_install_list(text: str) -> tuple[InstallFile, ...]:
    files: list[InstallFile] = []
    for raw in text.splitlines():
        line = raw.strip()
        if not line or line.startswith("["):
            continue
        optional = line.startswith("*")
        name = line[1:] if optional else line
        if name:
            files.append(InstallFile(name, optional))
    if not files:
        raise ValueError("install list is empty")
    return tuple(files)


def parse_version(text: str) -> tuple[str, str]:
    version = date = ""
    for raw in text.splitlines():
        line = raw.strip()
        if "=" not in line:
            continue
        key, _, value = line.partition("=")
        if key.lower() == "version":
            version = value.strip()
        elif key.lower() == "date":
            date = value.strip()
    return version, date


def search_roots(book: Path | None, home: Path | None) -> tuple[Path, ...]:
    """Book directory, its parent, then home. No course folder below home is named.

    The parent is the directory that holds the lesson directory. Nothing
    above that parent is searched, and nothing inside a subdirectory is searched.
    """
    roots: list[Path] = []
    if book is not None:
        book_dir = book if book.is_dir() else book.parent
        roots.append(book_dir)
        parent = book_dir.parent
        if parent != book_dir:
            roots.append(parent)
    if home is not None:
        roots.append(home)
    unique: list[Path] = []
    for root in roots:
        if root not in unique:
            unique.append(root)
    return tuple(unique)


def find_file(roots: tuple[Path, ...], name: str) -> Path | None:
    """First file whose name matches ``name`` regardless of case."""
    target = name.lower()
    for root in roots:
        if not root.is_dir():
            continue
        for path in root.iterdir():
            if path.is_file() and path.name.lower() == target:
                return path
    return None


def file_exists32(roots: tuple[Path, ...], name: str) -> int:
    """``fileExists32(name)``: 1 when the shelf finds ``name``, else 0. No DLL is called."""
    return 1 if find_file(roots, name) is not None else 0


@dataclass(frozen=True)
class FileReport:
    name: str
    path: Path | None
    note: str


@dataclass(frozen=True)
class Opened:
    book: Book
    files: tuple[FileReport, ...]


def install_flags(home: Path | None) -> dict[str, bool] | None:
    """Lower-case install-list name to whether that entry is starred.

    ``None`` means this folder has no install list.
    """
    if home is None or not home.is_dir():
        return None
    listing = find_file((home,), "toolbook.lst")
    if listing is None:
        return None
    files = parse_install_list(listing.read_text(encoding="latin1"))
    return {item.name.lower(): item.optional for item in files}


def open_book(path: Path, home: Path | None = None) -> Opened:
    """Open ``path``. A file it names and the install does not hold is reported, not fatal."""
    data = path.read_bytes()
    book = Book(data)
    roots = search_roots(path, home)
    shipped = install_flags(home)
    files = tuple(_file_report(name, roots, shipped) for name in lesson_names(data))
    return Opened(book, files)


def _file_report(name: str, roots: tuple[Path, ...], shipped: dict[str, bool] | None) -> FileReport:
    found = find_file(roots, name)
    if found is not None:
        return FileReport(name, found, "")
    if shipped is None:
        return FileReport(name, None, "")
    if name.lower() not in shipped:
        return FileReport(name, None, "named, not shipped")
    if shipped[name.lower()]:
        return FileReport(name, None, "listed, not shipped")
    return FileReport(name, None, "not found")


def unshipped_dll(path: Path, home: Path | None = None) -> str | None:
    """``MINSTB32.dll named, not shipped`` when the book's export DLL is not on the shelf.

    The name is the C string the book's PE export directory names. The
    shelf search is the one the open uses. ``None`` means the DLL was
    found or the book names no DLL. Nothing is loaded either way.
    """
    from opentoolbook.header import export_module_name

    try:
        name = export_module_name(path.read_bytes())
    except (OSError, ValueError, IndexError, struct.error):
        return None
    if not name.lower().endswith(".dll"):
        return None
    if find_file(search_roots(path, home), name) is not None:
        return None
    return f"{name} named, not shipped"


def on_disk(folder: Path, names: tuple[str, ...]) -> tuple[tuple[str, ...], tuple[str, ...]]:
    """Split ``names`` into those present in ``folder`` and those absent."""
    present = tuple(name for name in names if find_file((folder,), name) is not None)
    missing = tuple(name for name in names if find_file((folder,), name) is None)
    return present, missing
