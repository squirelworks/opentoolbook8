"""``gotoMenuPage`` from ``nc81base.sbk``, the call a lesson ``Menu`` button makes.

``gotoMenuPage`` sets ``menupage = getMenuPage()``, calls
``setupMenuPage(menupage, __lessonMode)``, and goes to ``page(menupage)``.
``getMenuPage`` starts from a quoted page, then a ``conditions`` block on
``__lessonMode`` may replace it with another quoted page when a quiz flag
is 0, and a page the book does not have falls back to the first quoted
page. Only the ``when`` branch that matches the value in the user
property store runs. An unset ``__`` name is 0. ``setupMenuPage`` sets
field colors and the enabled state of the menu selections; it does not
change the page, and it is not run here.
"""

from __future__ import annotations

import re

from opentoolbook.props import UserProperties

_QUOTED = re.compile(r'^([a-z_][a-z0-9_]*)\s*=\s*"([^"]*)"$')
_NUMBER = re.compile(r"^([a-z_][a-z0-9_]*)\s*=\s*(-?\d+)$")
_WHEN = re.compile(r"^when\s+([a-z_][a-z0-9_]*)\s*=\s*(-?\d+)$")
_IF = re.compile(r"^if\s+([a-z_][a-z0-9_]*)\s*=\s*(-?\d+)\s+then$")
_MISSING = re.compile(r"^if\s+not\s+isobject\s*\(\s*page\s+([a-z_][a-z0-9_]*)\s*\)\s+then$")
_RETURN = re.compile(r"^return\s+([a-z_][a-z0-9_]*)$")


def goto_menu_page(
    handlers: dict[str, str],
    pages: tuple[str, ...],
    props: UserProperties,
) -> str | None:
    """The page ``gotoMenuPage`` opens, or None when its text is not the known shape."""
    goto = handlers.get("gotomenupage", "")
    lines = [_norm(line) for line in goto.splitlines()]
    if "menupage = getmenupage()" not in lines:
        return None
    if not any(line.replace(" ", "") == "gotopage(menupage)" for line in lines):
        return None
    return get_menu_page(handlers.get("getmenupage", ""), pages, props)


def get_menu_page(source: str, pages: tuple[str, ...], props: UserProperties) -> str | None:
    """Walk ``getMenuPage``. ``__`` assignments are written to ``props``."""
    if not source:
        return None
    local: dict[str, object] = {}
    lines = [_norm(line) for line in source.splitlines()]
    lines = [line for line in lines if line and not line.startswith("--")]
    result = _walk(lines, local, pages, props)
    if not isinstance(result, str):
        return None
    return next((page for page in pages if page.lower() == result), result)


def _walk(lines: list[str], local: dict[str, object], pages, props) -> object:
    index = 0
    while index < len(lines):
        line = lines[index]
        if line.startswith(("to get", "system ", "local ")):
            index += 1
            continue
        if line == "conditions":
            body, index = _block(lines, index + 1, ("end", "end conditions"))
            chosen = _when(body, local, props)
            if chosen is not None:
                found = _walk(chosen, local, pages, props)
                if found is not None:
                    return found
            continue
        missing = _MISSING.match(line)
        if missing is not None:
            body, index = _block(lines, index + 1, ("end if",))
            name = local.get(missing.group(1))
            if not isinstance(name, str) or not any(page.lower() == name.lower() for page in pages):
                found = _walk(body, local, pages, props)
                if found is not None:
                    return found
            continue
        test = _IF.match(line)
        if test is not None:
            body, index = _block(lines, index + 1, ("end if",))
            if _read(test.group(1), local, props) == int(test.group(2)):
                found = _walk(body, local, pages, props)
                if found is not None:
                    return found
            continue
        returned = _RETURN.match(line)
        if returned is not None:
            return local.get(returned.group(1))
        assigned = _QUOTED.match(line) or _NUMBER.match(line)
        if assigned is not None:
            value: object = assigned.group(2)
            if assigned.re is _NUMBER:
                value = int(assigned.group(2))
            _write(assigned.group(1), value, local, props)
        index += 1
    return None


def _when(body: list[str], local: dict[str, object], props) -> list[str] | None:
    """The lines of the first ``when`` whose test holds."""
    branches: list[tuple[re.Match, list[str]]] = []
    depth = 0
    for line in body:
        found = _WHEN.match(line)
        if found is not None and depth == 0:
            branches.append((found, []))
            continue
        if line.startswith("if ") or line == "conditions":
            depth += 1
        elif line in ("end if", "end", "end conditions"):
            depth -= 1
        if branches:
            branches[-1][1].append(line)
    for test, lines in branches:
        if _read(test.group(1), local, props) == int(test.group(2)):
            return lines
    return None


def _block(lines: list[str], index: int, ends: tuple[str, ...]) -> tuple[list[str], int]:
    body: list[str] = []
    depth = 0
    while index < len(lines):
        line = lines[index]
        if depth == 0 and line in ends:
            return body, index + 1
        if (line.startswith("if ") and line.endswith(" then")) or line == "conditions":
            depth += 1
        elif line in ("end if", "end", "end conditions"):
            depth -= 1
        body.append(line)
        index += 1
    return body, index


def _read(name: str, local: dict[str, object], props: UserProperties) -> object:
    if UserProperties.owns(name):
        value = props.get(name)
        return 0 if value is None else value
    return local.get(name, 0)


def _write(name: str, value: object, local: dict[str, object], props: UserProperties) -> None:
    if UserProperties.owns(name):
        props.set(name, value)
    else:
        local[name] = value


def _norm(line: str) -> str:
    return " ".join(line.strip().lower().split())
