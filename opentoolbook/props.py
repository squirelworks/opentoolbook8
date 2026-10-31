"""The ``__`` names the book's handlers read and write.

The system books declare these with ``system string __studentFirst`` and
the like. A name is case-insensitive. A value lives for the process and
is never written to a student-record file. A name that was never set
reads as ``None``.
"""

from __future__ import annotations


class UserProperties:
    """``__`` names to values, shared by startup, ``enterPage``, and clicks."""

    def __init__(self, values: dict[str, object] | None = None) -> None:
        self._values: dict[str, object] = {}
        for name, value in (values or {}).items():
            self.set(name, value)

    @staticmethod
    def owns(name: str) -> bool:
        """True when ``name`` is a ``__`` name this store keeps."""
        return name.startswith("__") and len(name) > 2

    def get(self, name: str, default: object = None) -> object:
        return self._values.get(name.lower(), default)

    def set(self, name: str, value: object) -> None:
        if not self.owns(name):
            raise ValueError(f"{name} is not a __ name")
        self._values[name.lower()] = value

    def __contains__(self, name: object) -> bool:
        return isinstance(name, str) and name.lower() in self._values

    def items(self) -> tuple[tuple[str, object], ...]:
        return tuple(sorted(self._values.items()))

    def __repr__(self) -> str:
        return f"UserProperties({dict(self.items())!r})"
