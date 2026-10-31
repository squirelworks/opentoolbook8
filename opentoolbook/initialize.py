"""Run the literal assignments of a system book's ``initialize*`` handler.

An assignment runs when its right side is a whole or decimal number, a quoted string,
``true``, ``false``, a parameter, or a name the handler or the store
already holds. A ``__`` name goes to the in-memory store; any other name
is local to the handler. Every other line is skipped and named: a
``linkDLL`` or ``linkDLL32`` block by its library, a call by the name it
calls, ``set ... of this book`` by its property, and a ``conditions``,
``step``, or ``while`` block by its first line. ``if sysLevel = reader``
is taken. A condition on a value the handler holds is decided. Any
other condition runs neither branch and is named. No DLL is called.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field

from opentoolbook.props import UserProperties
from opentoolbook.walk import Flow, norm, reader_condition, walk

_NAME = r"[A-Za-z_][A-Za-z0-9_]*"
_ASSIGN = re.compile(rf"^({_NAME})\s*=\s*(.+)$")
_SET = re.compile(rf"^set\s+({_NAME})\s+to\s+(.+)$", re.IGNORECASE)
_SET_OTHER = re.compile(r"^set\s+(.+?)\s+to\s+.+$", re.IGNORECASE)
_CALL = re.compile(rf"({_NAME})\s*\(")
_LINK = re.compile(r'^(linkdll(?:32)?)\s+"([^"]+)"', re.IGNORECASE)
_COMPARE = re.compile(rf"^({_NAME})\s*(=|<>|>=|<=|>|<)\s*(.+)$")
_DECLARE = ("system ", "local ")


@dataclass
class Initialized:
    """What the handler assigned, in order, and what it skipped, by name."""

    assigned: list[tuple[str, object]] = field(default_factory=list)
    skipped: list[str] = field(default_factory=list)


def run_literals(
    source: str,
    props: UserProperties,
    args: tuple[object, ...] = (),
    *,
    book_name: str | None = None,
) -> Initialized:
    """Run one handler's literal assignments into ``props``."""
    done = Initialized()
    lines = source.splitlines()
    local: dict[str, object] = {}
    for name, value in zip(_parameters(lines), args):
        local[name.lower()] = value
    for line in lines:
        linked = _LINK.match(line.strip())
        if linked is not None:
            done.skipped.append(f"{linked.group(1)} {linked.group(2)}")

    def known(name: str) -> bool:
        return name in props if UserProperties.owns(name) else name.lower() in local

    def lookup(name: str) -> object:
        return props.get(name) if UserProperties.owns(name) else local.get(name.lower())

    def value(expr: str) -> tuple[bool, object]:
        text = expr.strip()
        low = text.lower()
        if re.fullmatch(r"-?\d+", text):
            return True, int(text)
        if re.fullmatch(r"-?\d+\.\d+", text):
            return True, float(text)
        if low in {"true", "false"}:
            return True, low == "true"
        if len(text) >= 2 and text[0] == '"' and text[-1] == '"' and '"' not in text[1:-1]:
            return True, text[1:-1]
        if norm(text) == "name of this book" and book_name:
            return True, book_name
        if re.fullmatch(_NAME, text) and known(text):
            return True, lookup(text)
        return False, None

    def assign(name: str, found: object) -> None:
        if UserProperties.owns(name):
            props.set(name, found)
        else:
            local[name.lower()] = found
        done.assigned.append((name, found))

    def skip_line(text: str) -> None:
        called = _CALL.search(text)
        done.skipped.append(called.group(1) if called else text)

    def statement(raw: str, low: str) -> None:
        text = raw.strip()
        if low.startswith(_DECLARE) or _LINK.match(text) or low.startswith("unlinkdll"):
            return
        assigned = _ASSIGN.match(text)
        if assigned is not None and "(" not in assigned.group(1):
            ok, found = value(assigned.group(2))
            if ok:
                assign(assigned.group(1), found)
            else:
                skip_line(assigned.group(2))
            return
        put = _SET.match(text)
        if put is not None:
            ok, found = value(put.group(2))
            if ok and UserProperties.owns(put.group(1)):
                assign(put.group(1), found)
            else:
                done.skipped.append(put.group(1))
            return
        other = _SET_OTHER.match(text)
        if other is not None:
            done.skipped.append(other.group(1))
            return
        skip_line(text)

    def condition(text: str) -> bool | None:
        decided = reader_condition(text)
        if decided is not None:
            return decided
        compared = _COMPARE.match(text.strip())
        if compared is not None and known(compared.group(1)):
            ok, right = value(compared.group(3))
            if ok:
                return _compare(lookup(compared.group(1)), compared.group(2), right)
        done.skipped.append(f"if {text}")
        return None

    walk(
        lines,
        Flow(),
        condition=condition,
        statement=statement,
        returns=lambda _expr: None,
        skipped=done.skipped.append,
    )
    return done


def initialize(chain, name: str, props: UserProperties, args: tuple[object, ...] = ()) -> Initialized:
    """Look ``name`` up down the send chain and run its literal assignments."""
    found = chain.find(name)
    if found is None:
        raise ValueError(f"{name} is not in {', '.join(book for book, _ in chain.books) or 'any book'}")
    book, source = found
    return run_literals(source, props, args, book_name=book)


def assignments_only(source: str) -> bool:
    """True when every statement of the handler is an assignment of a literal or a name."""
    lines = source.splitlines()
    for raw in lines[1:]:
        low = norm(raw)
        if not low or low.startswith("--") or low.startswith(_DECLARE):
            continue
        if low == "end" or low.startswith("end "):
            continue
        if low.startswith("return"):
            continue
        assigned = _ASSIGN.match(raw.strip())
        if assigned is None or _CALL.search(assigned.group(2)):
            return False
    return True


def run_if_assignments(chain, name: str, props: UserProperties, args: tuple[object, ...] = ()) -> Initialized | None:
    """Run ``name`` when it reaches no DLL and its body is only assignments. None when it is skipped."""
    from opentoolbook.send import reaches_dll

    found = chain.find(name)
    if found is None:
        raise ValueError(f"{name} is not in {', '.join(book for book, _ in chain.books) or 'any book'}")
    book, source = found
    if reaches_dll(chain, name) is not None or not assignments_only(source):
        return None
    return run_literals(source, props, args, book_name=book)


def _parameters(lines: list[str]) -> list[str]:
    for line in lines:
        low = norm(line)
        if low.startswith(("to get ", "to handle ")):
            parts = line.replace(",", " ").split()
            return parts[3:]
    return []


def _compare(left: object, operator: str, right: object) -> bool | None:
    if left is None:
        left = 0
    try:
        if operator in {"=", "<>"}:
            same = str(left).lower() == str(right).lower()
            return same if operator == "=" else not same
        a, b = float(left), float(right)  # type: ignore[arg-type]
    except (TypeError, ValueError):
        return None
    return {">": a > b, "<": a < b, ">=": a >= b, "<=": a <= b}[operator]


__all__ = ["Initialized", "assignments_only", "initialize", "run_if_assignments", "run_literals"]
