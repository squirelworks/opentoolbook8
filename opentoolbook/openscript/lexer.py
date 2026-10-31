"""OpenScript source to logical lines of tokens.

A handler is source text. ``--`` starts a comment that runs to the end of
the line, outside a quoted string. A line that ends with ``\\`` goes on
on the next line. ``;`` ends a statement, so one source line may hold
several. A quoted string runs to the next ``"``; ``""`` inside it is one quote.
Words are not case-sensitive, so a word token is kept in its source
spelling and compared in lower case.
"""

from __future__ import annotations

import re
from dataclasses import dataclass


@dataclass(frozen=True)
class Token:
    kind: str  # "word", "number", "string", "op"
    text: str
    line: int

    @property
    def low(self) -> str:
        return self.text.lower()


@dataclass(frozen=True)
class Line:
    """One statement: its tokens and the source line it starts on (1-based)."""

    tokens: tuple[Token, ...]
    number: int


_OPS = ("<>", "<=", ">=", "&&", "=", "<", ">", "+", "-", "*", "/", "^", "&", "(", ")", "[", "]", ",", ":", ".", "@", "#", "%", "{", "}", "'", "!", "|", "?", "~", "$")
_WORD = re.compile(r"[A-Za-z_\x80-\xff][A-Za-z0-9_\x80-\xff]*")
_NUMBER = re.compile(r"(?:\d+\.\d*|\.\d+|\d+)(?:[eE][+-]?\d+)?")


class LexError(ValueError):
    pass


def logical_lines(source: str) -> list[Line]:
    """Split ``source`` into statements of tokens. Comments and blank statements are dropped."""
    lines: list[Line] = []
    current: list[Token] = []
    start = 1
    number = 0
    for raw in source.replace("\r\n", "\n").replace("\r", "\n").split("\n"):
        number += 1
        tokens, continued = _tokens(raw, number)
        if not current:
            start = number
        for token in tokens:
            if token.kind == "op" and token.text == ";":
                if current:
                    lines.append(Line(tuple(current), start))
                current = []
                start = number
                continue
            current.append(token)
        if continued:
            continue
        if current:
            lines.append(Line(tuple(current), start))
        current = []
    if current:
        lines.append(Line(tuple(current), start))
    return lines


def _tokens(raw: str, number: int) -> tuple[list[Token], bool]:
    found: list[Token] = []
    index = 0
    size = len(raw)
    while index < size:
        ch = raw[index]
        if ch in " \t\f\v\x00\x1a":
            index += 1
            continue
        if raw.startswith("--", index):
            break
        if ch == '"':
            text: list[str] = []
            at = index + 1
            while True:
                end = raw.find('"', at)
                if end < 0:
                    # An unclosed string runs to the end of the line.
                    text.append(raw[at:])
                    index = size
                    break
                text.append(raw[at:end])
                if end + 1 < size and raw[end + 1] == '"':
                    text.append('"')
                    at = end + 2
                    continue
                index = end + 1
                break
            found.append(Token("string", "".join(text), number))
            continue
        if ch == "\\":
            rest = raw[index + 1:].strip()
            if not rest or rest.startswith("--"):
                return found, True
            found.append(Token("op", "\\", number))
            index += 1
            continue
        if ch == ";":
            found.append(Token("op", ";", number))
            index += 1
            continue
        match = _NUMBER.match(raw, index) if (ch.isdigit() or (ch == "." and index + 1 < size and raw[index + 1].isdigit())) else None
        if match is not None:
            end = match.end()
            # 2a or 1st: a number glued to letters is a word, e.g. "3d".
            if end < size and (raw[end].isalpha() or raw[end] == "_"):
                word = _WORD.match(raw, end)
                found.append(Token("word", raw[index:word.end()], number))
                index = word.end()
                continue
            found.append(Token("number", match.group(), number))
            index = end
            continue
        match = _WORD.match(raw, index)
        if match is not None:
            found.append(Token("word", match.group(), number))
            index = match.end()
            continue
        for op in _OPS:
            if raw.startswith(op, index):
                found.append(Token("op", op, number))
                index += len(op)
                break
        else:
            raise LexError(f"line {number}: unexpected character {ch!r}")
    return found, False
