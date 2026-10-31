"""OpenScript syntax tree. Every node is plain data; nothing here runs."""

from __future__ import annotations

from dataclasses import dataclass, field


# Expressions ---------------------------------------------------------------

@dataclass(frozen=True)
class Lit:
    value: object


@dataclass(frozen=True)
class Name:
    name: str  # lower case
    spelling: str = ""  # as written, for an unassigned name that reads as itself


@dataclass(frozen=True)
class Index:
    base: object
    indexes: tuple


@dataclass(frozen=True)
class Call:
    name: str  # lower case
    args: tuple
    of: object | None = None  # ``f(x) of obj`` sends the function to obj
    spelling: str = ""


@dataclass(frozen=True)
class Prop:
    name: str  # lower case
    of: object  # None for a bare system property


@dataclass(frozen=True)
class Chunk:
    kind: str  # char, word, item, textline
    start: object
    end: object | None
    of: object


@dataclass(frozen=True)
class ObjRef:
    kind: str  # page, field, button, ...
    by: str  # "id", "name", "this", "next", "previous", "first", "last", "number", "none"
    value: object | None
    of: object | None


@dataclass(frozen=True)
class Special:
    name: str  # self, target, this book, ...


@dataclass(frozen=True)
class Unary:
    op: str
    operand: object


@dataclass(frozen=True)
class Binary:
    op: str
    left: object
    right: object


@dataclass(frozen=True)
class ListExpr:
    """``a, b, c`` on the right of ``=`` or as command arguments."""

    items: tuple


# Statements ----------------------------------------------------------------

@dataclass(frozen=True)
class Declare:
    scope: str  # system or local
    type: str | None
    names: tuple  # (name, dims tuple, init expr or None)
    line: int = 0


@dataclass(frozen=True)
class Assign:
    target: object
    value: object
    line: int = 0


@dataclass(frozen=True)
class Put:
    value: object
    mode: str  # into, after, before
    target: object
    line: int = 0


@dataclass(frozen=True)
class Get:
    value: object
    line: int = 0


@dataclass(frozen=True)
class Send:
    name: object  # lower-case str, or an expression that names the message
    args: tuple
    to: object | None
    line: int = 0
    within: object | None = None  # ``in viewer``
    idle: bool = False  # ``when idle``


@dataclass(frozen=True)
class Forward:
    line: int = 0


@dataclass(frozen=True)
class Return:
    value: object | None
    line: int = 0


@dataclass(frozen=True)
class Break:
    target: str | None
    line: int = 0


@dataclass(frozen=True)
class Continue:
    line: int = 0


@dataclass(frozen=True)
class If:
    cond: object
    then: tuple
    otherwise: tuple
    line: int = 0


@dataclass(frozen=True)
class Conditions:
    cases: tuple  # (expr, body)
    otherwise: tuple
    line: int = 0


@dataclass(frozen=True)
class Step:
    var: object
    start: object
    end: object
    by: object | None
    body: tuple
    line: int = 0


@dataclass(frozen=True)
class While:
    cond: object
    body: tuple
    line: int = 0


@dataclass(frozen=True)
class DoUntil:
    body: tuple
    cond: object
    line: int = 0


@dataclass(frozen=True)
class In:
    target: object
    body: tuple
    line: int = 0


@dataclass(frozen=True)
class Go:
    target: object
    line: int = 0


@dataclass(frozen=True)
class Push:
    value: object
    target: object
    line: int = 0


@dataclass(frozen=True)
class Pop:
    source: object
    target: object | None
    line: int = 0


@dataclass(frozen=True)
class Increment:
    target: object
    by: object | None
    down: bool = False
    line: int = 0


@dataclass(frozen=True)
class Clear:
    target: object
    line: int = 0


@dataclass(frozen=True)
class Request:
    prompt: object
    buttons: tuple
    line: int = 0


@dataclass(frozen=True)
class LinkDLL:
    library: object
    declarations: tuple  # raw token texts per line
    unlink: bool = False
    line: int = 0


@dataclass(frozen=True)
class Command:
    """A built-in command or a message sent by name: ``name args``."""

    name: str
    args: tuple  # expressions, or empty when ``raw`` is set
    raw: tuple = ()  # token texts when the arguments did not parse as a list
    line: int = 0


@dataclass(frozen=True)
class Param:
    name: str
    type: str | None


@dataclass(frozen=True)
class Handler:
    kind: str  # handle, get, set
    name: str  # lower case
    params: tuple
    body: tuple
    value_param: Param | None = None  # ``to set prop ... to value``
    line: int = 0


@dataclass
class Script:
    handlers: dict = field(default_factory=dict)  # lower-case name -> Handler, first wins
    errors: list = field(default_factory=list)  # (line, message)
