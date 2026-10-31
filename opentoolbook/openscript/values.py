"""OpenScript values: everything is text that may read as a number or a logical.

``null`` is the empty string. A number prints without a trailing ``.0``.
Text compares without case. Two values that both read as numbers compare
as numbers. ``true`` and ``false`` are logicals and print in lower case.
"""

from __future__ import annotations

import math


class Array:
    """A declared or dynamic array. Indexes are tuples of whole numbers."""

    def __init__(self, dims: tuple = ()) -> None:
        self.dims = dims
        self.cells: dict[tuple, object] = {}

    def get(self, index: tuple) -> object:
        return self.cells.get(index, "")

    def set(self, index: tuple, value: object) -> None:
        self.cells[index] = value

    def __repr__(self) -> str:
        return f"Array({self.cells!r})"


def text(value: object) -> str:
    if value is None:
        return ""
    if isinstance(value, bool):
        return "true" if value else "false"
    if isinstance(value, float):
        if math.isfinite(value) and value == int(value) and abs(value) < 1e15:
            return str(int(value))
        return repr(value)
    if isinstance(value, Array):
        return ""
    return str(value)


def number(value: object) -> float | int | None:
    """The number ``value`` reads as, or None."""
    if isinstance(value, bool):
        return None
    if isinstance(value, (int, float)):
        return value
    raw = text(value).strip()
    if not raw:
        return None
    try:
        return int(raw)
    except ValueError:
        pass
    if raw[:2].lower() == "0x":
        try:
            return int(raw[2:], 16)
        except ValueError:
            return None
    try:
        result = float(raw)
    except ValueError:
        return None
    return result if math.isfinite(result) else None


def as_number(value: object) -> float | int:
    """A number for arithmetic. Null is 0. Other text is an error."""
    found = number(value)
    if found is not None:
        return found
    if text(value).strip() == "":
        return 0
    raise ScriptError(f"{text(value)!r} is not a number")


def logical(value: object) -> bool | None:
    if isinstance(value, bool):
        return value
    low = text(value).strip().lower()
    if low == "true":
        return True
    if low == "false":
        return False
    return None


def truth(value: object) -> bool:
    found = logical(value)
    if found is None:
        raise ScriptError(f"{text(value)!r} is not true or false")
    return found


def same(left: object, right: object) -> bool:
    a, b = number(left), number(right)
    if a is not None and b is not None:
        return a == b
    return text(left).lower() == text(right).lower()


def compare(left: object, right: object) -> int:
    a, b = number(left), number(right)
    if a is not None and b is not None:
        return (a > b) - (a < b)
    x, y = text(left).lower(), text(right).lower()
    return (x > y) - (x < y)


def tidy(value: float | int) -> float | int:
    if isinstance(value, float) and value.is_integer() and abs(value) < 1e15:
        return int(value)
    return value


class ScriptError(RuntimeError):
    """An OpenScript execution error, such as a non-number in arithmetic."""
