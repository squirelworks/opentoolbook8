"""The files a lesson asks for, and the install list beside it.

``toolbook.lst`` is the playback set. A leading ``*`` marks a file the
list names and this install does not ship. A lesson then names a smaller
set in its own bytes: system books, the shell, and ``initialize*`` calls.
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path

from opentoolbook.record import Book

_FILE = re.compile(rb"(?<![A-Za-z0-9_.])[A-Za-z0-9_]{3,16}\.(?:sbk|tbk|dll|exe)", re.I)
_INIT = re.compile(rb"initialize[A-Za-z]+", re.I)
_ENTRY = ("opensession", "gotopagelist", "entersystem", "enterapplication")
# These belong to a key disk, not to a book report.
KEYDISK_NAMES = frozenset({"class.s3", "id.s3", "criteria.s4", "m00001.s3", "login.m3"})
# The four initialize calls are the four nc81 books. The other four are the shell.
CALL_BOOKS = {
    "initializebase": "nc81base.sbk",
    "initializerecs": "nc81recs.sbk",
    "initializetest": "nc81test.sbk",
    "initializetrnr": "nc81trnr.sbk",
    "enterapplication": "nida81.tbk",
    "entersystem": "nida81.tbk",
    "gotopagelist": "nida81.tbk",
    "opensession": "nida81.tbk",
}


@dataclass(frozen=True)
class InstallFile:
    name: str
    optional: bool


def named_files(data: bytes) -> tuple[str, ...]:
    """File names a book mentions, in lower case, without the version fragment."""
    found = {match.group().decode("latin1").lower() for match in _FILE.finditer(data)}
    found -= KEYDISK_NAMES
    return tuple(sorted(found))


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
    """Folders that can hold a file the book names, in the order to try them."""
    roots: list[Path] = []
    if book is not None:
        roots.append(book if book.is_dir() else book.parent)
    if home is not None:
        roots.append(home)
        roots.append(home / "courses")
        roots.append(home / "Nida98" / "Lessons")
        roots.append(home / "Nida98" / "Student")
    unique: list[Path] = []
    for root in roots:
        if root not in unique:
            unique.append(root)
    return tuple(unique)


def find_file(roots: tuple[Path, ...], name: str) -> Path | None:
    """First file whose name matches ``name`` regardless of case."""
    target = name.lower()
    if target in KEYDISK_NAMES:
        return None
    for root in roots:
        if not root.is_dir():
            continue
        for path in root.iterdir():
            if path.is_file() and path.name.lower() == target:
                return path
    return None


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
    files = tuple(_file_report(name, roots, shipped) for name in named_files(data))
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


def on_disk(folder: Path, names: tuple[str, ...]) -> tuple[tuple[str, ...], tuple[str, ...]]:
    """Split ``names`` into those present in ``folder`` and those absent."""
    present = tuple(name for name in names if find_file((folder,), name) is not None)
    missing = tuple(name for name in names if find_file((folder,), name) is None)
    return present, missing
