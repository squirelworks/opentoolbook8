"""The statements every handler shares: ``if``, ``else``, ``end if``, ``break``, ``return``.

Opening the book, ``enterPage``, and ``buttonClick`` walk their handler
with this one loop. The caller decides what a condition is worth and
what any other line does. A condition the caller cannot decide runs
neither branch. ``end`` and ``end if`` both close an ``if``. An ``if``
line that does not end in ``then`` is still a block when the line has
no ``then`` in it. A ``linkDLL`` block is not called. ``forward`` has
no body. ``end`` at the top of a handler ends it.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Callable


@dataclass
class Flow:
    """Whether a ``break`` or a ``return`` has stopped the handler."""

    returning: bool = False
    return_value: object = None
    breaking: bool = False

    def clear(self) -> None:
        self.returning = False
        self.breaking = False


Condition = Callable[[str], "bool | None"]
Statement = Callable[[str, str], None]
Returns = Callable[[str], object]

_KEEP_GOING = ("end if", "end step", "end conditions", "end link")


def norm(line: str) -> str:
    """The line in lower case with runs of white space folded to one space."""
    return " ".join(line.strip().lower().split())


def block_if(low: str) -> str | None:
    """The condition of a block ``if`` line, or None when the line is not one."""
    if not low.startswith("if "):
        return None
    if low.endswith(" then"):
        return low[3:-5].strip()
    if " then " in low:
        return None
    return low[3:].strip()


def reader_condition(text: str, reader: bool = True) -> bool | None:
    """``sysLevel = reader`` and its negation. A missing ``sysLevel`` is ``reader``."""
    low = norm(text)
    if low in {"syslevel = reader", 'syslevel = "reader"'}:
        return reader
    if low in {"syslevel <> reader", 'syslevel <> "reader"'}:
        return not reader
    return None


def split_if(lines: list[str], index: int) -> tuple[list[str], list[str], int]:
    """``(then lines, else lines, index after the closing end)`` from ``index``."""
    taken: list[str] = []
    skipped: list[str] = []
    branch = taken
    depth = 0
    while index < len(lines):
        low = norm(lines[index])
        if block_if(low) is not None:
            depth += 1
            branch.append(lines[index])
            index += 1
            continue
        if low == "else" and depth == 0:
            branch = skipped
            index += 1
            continue
        if low in {"end", "end if"} and depth == 0:
            return taken, skipped, index + 1
        if low in {"end", "end if"}:
            depth -= 1
        branch.append(lines[index])
        index += 1
    return taken, skipped, index


def _opens(low: str) -> bool:
    return (
        block_if(low) is not None
        or low == "conditions"
        or low.startswith(("step ", "while ", "linkdll"))
    )


def _closes(low: str) -> bool:
    return low == "end" or low.startswith("end ")


def skip_block(lines: list[str], index: int) -> int:
    """The index after the block that opens at ``index``. Nested blocks are counted."""
    depth = 0
    while index < len(lines):
        low = norm(lines[index])
        if _opens(low):
            depth += 1
        elif _closes(low):
            depth -= 1
            if depth == 0:
                return index + 1
        index += 1
    return index


def walk(
    lines: list[str],
    flow: Flow,
    *,
    condition: Condition,
    statement: Statement,
    returns: Returns | None = None,
    skipped: Callable[[str], None] | None = None,
) -> object:
    """Run ``lines``. Returns the ``return`` value, or None.

    ``statement(raw, low)`` sees every line the walker does not own.
    ``returns(expression)`` is the value of ``return expression``.
    When ``skipped`` is given, a ``conditions``, ``step``, or ``while``
    block is not run. ``skipped`` gets its first line.
    """
    index = 0
    while index < len(lines):
        if flow.returning or flow.breaking:
            return flow.return_value
        raw = lines[index]
        low = norm(raw)
        if not low or low.startswith("--"):
            index += 1
            continue
        if low.startswith(("to handle", "to get", "to set")):
            index += 1
            continue
        if low.startswith("linkdll"):
            index += 1
            while index < len(lines) and not norm(lines[index]).startswith("end linkdll"):
                index += 1
            index += 1
            continue
        if low in {"end", "end if"} or (low.startswith("end ") and not low.startswith(_KEEP_GOING)):
            return flow.return_value if flow.returning else None
        if low == "forward":
            index += 1
            continue
        if skipped is not None and (low == "conditions" or low.startswith(("step ", "while "))):
            skipped(raw.strip())
            index = skip_block(lines, index)
            continue
        if low == "break":
            flow.breaking = True
            return None
        test = block_if(low)
        if test is not None:
            index += 1
            taken, other, index = split_if(lines, index)
            known = condition(test)
            if known is True:
                walk(taken, flow, condition=condition, statement=statement, returns=returns, skipped=skipped)
            elif known is False:
                walk(other, flow, condition=condition, statement=statement, returns=returns, skipped=skipped)
            if flow.returning or flow.breaking:
                return flow.return_value
            continue
        if low == "return" or low.startswith("return "):
            expr = low[6:].strip()
            flow.return_value = returns(expr) if (returns and expr) else None
            flow.returning = True
            return flow.return_value
        statement(raw, low)
        index += 1
    return flow.return_value if flow.returning else None
