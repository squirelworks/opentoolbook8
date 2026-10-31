"""``setupQuizEx`` from ``nc81test.sbk``, the call the quiz menu groups make.

Group ``selection1`` on ``P10001`` through ``P10004`` runs
``error = setupQuizEx("Assessment", 2, "P10301", "P10302", "P10303")``,
with ``Pre-Test``, ``Post-Test``, or ``Quiz`` in the first place on the
other pages. The reader binds those arguments to the handler's
parameters and runs its assignments into the user property store:
quoted and numeric literals, a parameter, ``uppercase(name)``,
``pageNumber of this page``, one array element ``name[n]``,
``increment(name)``, one ``conditions`` / ``when`` branch, and ``if`` on
a number. A ``step`` loop that clears the result arrays is not run, and a
``linkDLL`` block is not called. The pool calls after it are not run.
"""

from __future__ import annotations

import re

from opentoolbook.props import UserProperties

_HEADER = re.compile(r"^to get setupquizex\s+(.*)$")
_CALL = re.compile(r"^([a-z_][a-z0-9_]*)\s*=\s*setupquizex\s*\((.*)\)$", re.IGNORECASE)
_ASSIGN = re.compile(r"^([a-z_][a-z0-9_]*)(?:\[(\d+)\])?\s*=\s*(.+)$", re.IGNORECASE)
_INCREMENT = re.compile(r"^increment\s*\(\s*([a-z_][a-z0-9_]*)\s*\)$")
_IF = re.compile(r"^if\s+([a-z_][a-z0-9_]*)\s*(=|<>|>|<)\s*([a-z0-9_\"-]+)\s+then$")
_WHEN = re.compile(r"^when\s+([a-z_][a-z0-9_]*)\s*=\s*(.+)$")
_RETURN = re.compile(r"^return\s+([a-z_][a-z0-9_]*)$")


def selection_setup(
    click_source: str,
    setup_source: str,
    props: UserProperties,
    page_number: int,
) -> int | None:
    """Run the ``setupQuizEx`` call in a group's ``buttonClick``.

    Returns that call's ``error``, or None when the click has no such call,
    or when ``__quizHelp`` is 1 and the handler breaks before the call.
    """
    lines = [_norm(line) for line in click_source.splitlines()]
    for index, line in enumerate(lines):
        if line == "if __quizhelp = 1 then" and props.get("__quizHelp") == 1:
            return None
        found = _CALL.match(_raw(click_source.splitlines()[index]))
        if found is not None:
            return setup_quiz_ex(setup_source, _arguments(found.group(2)), props, page_number)
    return None


def setup_quiz_ex(source: str, arguments: list[object], props: UserProperties, page_number: int) -> int:
    """Run ``setupQuizEx`` with ``arguments``. Returns its ``error``."""
    lines = [_raw(line) for line in source.splitlines()]
    local: dict[str, object] = {}
    body = []
    for line in lines:
        header = _HEADER.match(line.lower())
        if header is not None:
            names = [part.split()[-1].lower() for part in header.group(1).split(",") if part.strip()]
            for name, value in zip(names, arguments):
                local[name] = value
            continue
        body.append(line)
    found = _walk(body, local, props, page_number)
    return found if isinstance(found, int) else 0


def _walk(lines: list[str], local: dict[str, object], props: UserProperties, page_number: int) -> object:
    index = 0
    while index < len(lines):
        line = lines[index]
        low = line.lower()
        if not low or low.startswith(("--", "system ", "local ", "end setupquizex")) or low == "end":
            index += 1
            continue
        if low.startswith("step "):
            _body, index = _block(lines, index + 1, ("end step",))
            continue
        if low.startswith("linkdll"):
            _body, index = _block(lines, index + 1, ("end linkdll", "end linkdll32"))
            continue
        if low == "conditions":
            body, index = _block(lines, index + 1, ("end conditions", "end"))
            chosen = _when(body, local, props)
            if chosen is not None:
                found = _walk(chosen, local, props, page_number)
                if found is not None:
                    return found
            continue
        test = _IF.match(low)
        if test is not None:
            body, index = _block(lines, index + 1, ("end if",))
            left = _read(test.group(1), local, props)
            right = _value(test.group(3), local, props, page_number)
            if _compare(left, test.group(2), right):
                found = _walk(body, local, props, page_number)
                if found is not None:
                    return found
            continue
        returned = _RETURN.match(low)
        if returned is not None:
            return _read(returned.group(1), local, props)
        bumped = _INCREMENT.match(low)
        if bumped is not None:
            current = _read(bumped.group(1), local, props)
            _write(bumped.group(1), None, (current if isinstance(current, int) else 0) + 1, local, props)
            index += 1
            continue
        assigned = _ASSIGN.match(line)
        if assigned is not None:
            value = _value(assigned.group(3), local, props, page_number)
            if value is not None:
                _write(assigned.group(1), assigned.group(2), value, local, props)
        index += 1
    return None


def _value(text: str, local: dict[str, object], props: UserProperties, page_number: int) -> object | None:
    text = text.strip()
    low = text.lower()
    if len(text) >= 2 and text[0] == '"' and text[-1] == '"':
        return text[1:-1]
    if re.fullmatch(r"-?\d+", text):
        return int(text)
    if low == "pagenumber of this page":
        return page_number
    upper = re.fullmatch(r"uppercase\s*\(\s*([a-z_][a-z0-9_]*)\s*\)", low)
    if upper is not None:
        value = _read(upper.group(1), local, props)
        return value.upper() if isinstance(value, str) else None
    if re.fullmatch(r"[a-z_][a-z0-9_]*", low) and (low in local or UserProperties.owns(low)):
        return _read(low, local, props)
    return None


def _when(body: list[str], local: dict[str, object], props: UserProperties) -> list[str] | None:
    branches: list[tuple[re.Match, list[str]]] = []
    for line in body:
        found = _WHEN.match(line.lower())
        if found is not None:
            branches.append((found, []))
        elif branches:
            branches[-1][1].append(line)
    for test, lines in branches:
        expected = test.group(2).strip()
        expected_value: object = expected[1:-1] if expected.startswith('"') else expected
        if re.fullmatch(r"-?\d+", expected):
            expected_value = int(expected)
        actual = _read(test.group(1), local, props)
        if isinstance(actual, str) and isinstance(expected_value, str):
            if actual.lower() == expected_value.lower():
                return lines
        elif actual == expected_value:
            return lines
    return None


def _compare(left: object, operator: str, right: object) -> bool:
    if operator == "=":
        return left == right
    if operator == "<>":
        return left != right
    if not isinstance(left, int) or not isinstance(right, int):
        return False
    return left > right if operator == ">" else left < right


def _block(lines: list[str], index: int, ends: tuple[str, ...]) -> tuple[list[str], int]:
    body: list[str] = []
    depth = 0
    while index < len(lines):
        low = lines[index].lower()
        if depth == 0 and low in ends:
            return body, index + 1
        if (low.startswith("if ") and low.endswith(" then")) or low == "conditions" or low.startswith("step "):
            depth += 1
        elif low in ("end if", "end conditions", "end step"):
            depth -= 1
        body.append(lines[index])
        index += 1
    return body, index


def _read(name: str, local: dict[str, object], props: UserProperties) -> object:
    if UserProperties.owns(name):
        value = props.get(name)
        return 0 if value is None else value
    return local.get(name.lower(), 0)


def _write(name: str, element: str | None, value: object, local: dict[str, object], props: UserProperties) -> None:
    if element is not None:
        if not UserProperties.owns(name):
            return
        current = props.get(name)
        table = dict(current) if isinstance(current, dict) else {}
        table[int(element)] = value
        props.set(name, table)
        return
    if UserProperties.owns(name):
        props.set(name, value)
    else:
        local[name.lower()] = value


def _arguments(text: str) -> list[object]:
    found: list[object] = []
    for part in re.findall(r'"[^"]*"|[^,]+', text):
        part = part.strip()
        if part.startswith('"'):
            found.append(part[1:-1])
        elif re.fullmatch(r"-?\d+", part):
            found.append(int(part))
        elif part:
            found.append(part)
    return found


def _raw(line: str) -> str:
    return " ".join(line.strip().split())


def _norm(line: str) -> str:
    return _raw(line).lower()
