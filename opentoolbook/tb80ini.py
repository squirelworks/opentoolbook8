"""``TB80.INI`` keys that seed the runtime before a book's own scripts run.

Search order (handoff / TB80RTM): the book's folder, then
``<windows>\\asym\\runtime``, then ``<windows>``. An explicit path from
``--ini`` wins and skips the search. With no INI every key keeps its
default: no ``startupSysBooks``, no ``startupBook``, and no
startup width or height.
"""

from __future__ import annotations

import configparser
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class Tb80Ini:
    """Runtime defaults from ``TB80.INI``. Empty tuples and Nones are the no-INI defaults."""

    path: Path | None
    startup_sysbooks: tuple[str, ...] = ()
    startup_book: str | None = None
    startup_width: int | None = None
    startup_height: int | None = None


_DEFAULTS = Tb80Ini(path=None)


def find_tb80_ini(book: Path | None, windows: Path | None = None, override: Path | None = None) -> Path | None:
    """The first ``TB80.INI`` on the search path, or ``override`` when given."""
    if override is not None:
        return override if override.is_file() else None
    roots: list[Path] = []
    if book is not None:
        folder = book if book.is_dir() else book.parent
        roots.append(folder)
    if windows is not None:
        roots.append(windows / "asym" / "runtime")
        roots.append(windows)
    seen: list[Path] = []
    for root in roots:
        if root in seen or not root.is_dir():
            continue
        seen.append(root)
        for path in root.iterdir():
            if path.is_file() and path.name.lower() == "tb80.ini":
                return path
    return None


def read_tb80_ini(book: Path | None, windows: Path | None = None, override: Path | None = None) -> Tb80Ini:
    """Parse ``TB80.INI`` for the startup keys. Missing file or keys yield defaults."""
    path = find_tb80_ini(book, windows, override)
    if path is None:
        return _DEFAULTS
    try:
        text = path.read_text(encoding="latin1")
    except OSError:
        return _DEFAULTS
    parser = configparser.ConfigParser(interpolation=None, strict=False)
    try:
        # Allow keys above the first section.
        parser.read_string("[DEFAULT]\n" + text)
    except configparser.Error:
        return Tb80Ini(path=path)
    values = _merged(parser)
    return Tb80Ini(
        path=path,
        startup_sysbooks=_sysbooks(values.get("startupsysbooks")),
        startup_book=_nonempty(values.get("startupbook")),
        startup_width=_int(values.get("startupwidth")),
        startup_height=_int(values.get("startupheight")),
    )


def _merged(parser: configparser.ConfigParser) -> dict[str, str]:
    found: dict[str, str] = {}
    for section in parser.sections():
        for key, value in parser.items(section):
            found.setdefault(key.lower(), value.strip())
    for key, value in parser.defaults().items():
        found.setdefault(key.lower(), value.strip())
    return found


def _sysbooks(raw: str | None) -> tuple[str, ...]:
    if not raw:
        return ()
    return tuple(part.strip().lower() for part in raw.split(",") if part.strip())


def _nonempty(raw: str | None) -> str | None:
    if raw is None or raw.strip() == "":
        return None
    return raw.strip()


def _int(raw: str | None) -> int | None:
    if raw is None or raw.strip() == "":
        return None
    try:
        return int(raw.strip(), 10)
    except ValueError:
        return None
