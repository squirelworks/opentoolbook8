"""Run the literal assignments of a system book's ``initialize*`` handler.

An assignment runs when its right side is a whole or decimal number, a quoted string,
``true``, ``false``, a parameter, or a name the handler or the store
already holds. A ``__`` name goes to the in-memory store; any other name
is local to the handler. Every other line is skipped and named: a
``linkDLL`` or ``linkDLL32`` block by its library, a call by the name it
calls, ``set ... of this book`` by its property, and a ``conditions`` or
``while`` block, or a ``step`` whose bounds are not known, by its first
line. ``__name[i]`` is element ``i`` of one stored table, the same shape
``setupQuizEx`` uses for ``__quizPages``. ``if sysLevel = reader``
is taken. A ``__`` name whose right side was skipped is listed as
unset. A condition on a value the handler holds is decided, and
``and`` joins two of them. Any other condition runs neither branch and
is named. ``step i from 1 to 100`` with known bounds runs its body. A
``return`` of a value the handler holds is the handler's value. No DLL
is called.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field

from opentoolbook.props import UserProperties
from opentoolbook.walk import Flow, norm, reader_condition, walk

_NAME = r"[A-Za-z_][A-Za-z0-9_]*"
_ASSIGN = re.compile(rf"^({_NAME}(?:\[[^\]]+\])?)\s*=\s*(.+)$")
_INDEXED = re.compile(rf"^({_NAME})\[(.+)\]$")
_STEP = re.compile(rf"^step\s+({_NAME})\s+from\s+(.+?)\s+to\s+(.+)$", re.IGNORECASE)
_TYPES = {"int", "string", "long", "word", "logical", "real", "dword", "byte", "pointer", "float", "double"}
_MAX_STEPS = 10000
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
    value: object = None
    unset: list[str] = field(default_factory=list)


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

    def key(name: str) -> str | None:
        indexed = _INDEXED.match(name.strip())
        if indexed is None:
            return name.strip()
        ok, index = value(indexed.group(2))
        if not ok:
            return None
        return f"{indexed.group(1)}[{index}]"

    def table(base: str) -> object:
        return props.get(base) if UserProperties.owns(base) else local.get(base.lower())

    def known(name: str) -> bool:
        base, index = _element(name)
        if index is not None:
            found = table(base)
            return isinstance(found, dict) and index in found
        return name in props if UserProperties.owns(name) else name.lower() in local

    def lookup(name: str) -> object:
        base, index = _element(name)
        if index is not None:
            found = table(base)
            return found.get(index) if isinstance(found, dict) else None
        return props.get(name) if UserProperties.owns(name) else local.get(name.lower())

    def value(expr: str) -> tuple[bool, object]:
        text = _unwrap(expr.strip())
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
        if _INDEXED.match(text):
            named = key(text)
            if named is not None and known(named):
                return True, lookup(named)
        return False, None

    def assign(name: str, found: object) -> None:
        base, index = _element(name)
        stored: object = found
        if index is not None:
            current = table(base)
            stored = dict(current) if isinstance(current, dict) else {}
            stored[index] = found
        if UserProperties.owns(base):
            props.set(base, stored)
        else:
            local[base.lower()] = stored
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
            named = key(assigned.group(1))
            if ok and named is not None:
                assign(named, found)
            else:
                skip_line(assigned.group(2))
                target = assigned.group(1)
                if UserProperties.owns(target) and target not in done.unset:
                    done.unset.append(target)
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

    def decide(text: str) -> bool | None:
        decided = reader_condition(text)
        if decided is not None:
            return decided
        parts = [_unwrap(part) for part in re.split(r"\s+and\s+", _unwrap(text.strip()))]
        if len(parts) > 1:
            found = [decide(part) for part in parts]
            if False in found:
                return False
            return None if None in found else True
        compared = _COMPARE.match(parts[0])
        if compared is not None and known(compared.group(1)):
            ok, right = value(compared.group(3))
            if ok:
                return _compare(lookup(compared.group(1)), compared.group(2), right)
        return None

    def condition(text: str) -> bool | None:
        decided = decide(text)
        if decided is None:
            done.skipped.append(f"if {text}")
        return decided

    def returns(expr: str) -> object:
        ok, found = value(expr)
        return found if ok else None

    flow = Flow()

    def block(first: str, body: list[str]) -> bool:
        step = _STEP.match(first)
        if step is None:
            return False
        ok_from, start = value(step.group(2))
        ok_to, stop = value(step.group(3))
        if not (ok_from and ok_to and isinstance(start, int) and isinstance(stop, int)):
            return False
        if stop - start >= _MAX_STEPS:
            return False
        for number in range(start, stop + 1):
            local[step.group(1).lower()] = number
            run(body)
            if flow.returning:
                break
            if flow.breaking:
                flow.breaking = False
                break
        return True

    def run(body: list[str]) -> object:
        return walk(
            body,
            flow,
            condition=condition,
            statement=statement,
            returns=returns,
            skipped=done.skipped.append,
            block=block,
        )

    done.value = run(lines)
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
            return [part for part in parts[3:] if part.lower() not in _TYPES]
    return []


def _element(name: str) -> tuple[str, object]:
    """``("__x", 3)`` for ``__x[3]``. The index is None for a plain name."""
    found = re.fullmatch(r"(.+)\[(.+)\]", name.strip())
    if found is None:
        return name.strip(), None
    index = found.group(2).strip()
    return found.group(1), int(index) if re.fullmatch(r"-?\d+", index) else index


def _unwrap(text: str) -> str:
    """``(x)`` is ``x`` when the parentheses wrap the whole text."""
    text = text.strip()
    while text.startswith("(") and text.endswith(")"):
        depth = 0
        for place, char in enumerate(text):
            depth += char == "("
            depth -= char == ")"
            if depth == 0 and place < len(text) - 1:
                return text
        text = text[1:-1].strip()
    return text


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
