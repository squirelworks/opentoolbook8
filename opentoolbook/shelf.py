"""The files a lesson asks for, and the install list beside it.

``toolbook.lst`` is the playback set. A leading ``*`` marks a file the
list names and this install does not ship. A lesson then names a smaller
set in its own bytes: system books, the shell, and ``initialize*`` calls.
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path

_FILE = re.compile(rb"(?<![A-Za-z0-9_.])[A-Za-z0-9_]{3,16}\.(?:sbk|tbk|dll|exe)", re.I)
_INIT = re.compile(rb"initialize[A-Za-z]+", re.I)
_ENTRY = ("opensession", "gotopagelist", "entersystem", "enterapplication")


@dataclass(frozen=True)
class InstallFile:
    name: str
    optional: bool


def named_files(data: bytes) -> tuple[str, ...]:
    """File names a book mentions, in lower case, without the version fragment."""
    found = {match.group().decode("latin1").lower() for match in _FILE.finditer(data)}
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


def on_disk(folder: Path, names: tuple[str, ...]) -> tuple[tuple[str, ...], tuple[str, ...]]:
    """Split ``names`` into those present in ``folder`` and those absent."""
    have = {path.name.lower() for path in folder.iterdir() if path.is_file()}
    present = tuple(name for name in names if name.lower() in have)
    missing = tuple(name for name in names if name.lower() not in have)
    return present, missing
