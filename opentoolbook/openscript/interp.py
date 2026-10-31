"""Run OpenScript handlers.

``Engine`` runs parsed handlers against a ``Host``. The host is the
window, the book, and the page: it answers ``go to``, object properties,
and the system properties the engine does not keep itself. The engine
keeps variables, ``it``, ``sysBooks``, arrays, and the handler chain.

Names
    A name a handler declared ``system`` is shared by every handler. A
    ``__`` system name lives in the ``UserProperties`` store the rest of
    the reader reads. Any other name is local to the handler run. A name
    that is neither assigned nor declared nor a constant reads as its own
    spelling, so ``sysLevel = reader`` compares with the word ``reader``.

Messages
    ``send name`` and a statement that starts with a name that is not a
    command run the first handler for that message in the chain.
    ``forward`` runs the next one. A message no handler takes goes to the
    host, which ignores it unless it is a built-in.

Functions
    ``f(x)`` runs a ``to get f`` handler in the chain, else a built-in
    function, else a function a ``linkDLL`` block declared, which the host
    answers. A DLL function the host does not answer returns null.
"""

from __future__ import annotations

import random as _random
from dataclasses import dataclass, field
from typing import Callable

from opentoolbook.openscript import ast as A
from opentoolbook.openscript.values import (
    Array,
    ScriptError,
    as_number,
    compare,
    logical,
    number,
    same,
    text,
    tidy,
    truth,
)
from opentoolbook.props import UserProperties

CONSTANTS = {
    "true": True,
    "false": False,
    "null": "",
    "empty": "",
    "tab": "\t",
    "cr": "\r",
    "lf": "\n",
    "crlf": "\r\n",
    "space": " ",
    "quote": '"',
    "comma": ",",
}
# Statements run per top-level call before the engine gives up.
STEP_LIMIT = 200_000
DEPTH_LIMIT = 64


@dataclass(frozen=True)
class Ref:
    """An object reference: kind, how it was named, the name or id, and its container."""

    kind: str
    by: str
    value: object
    of: object = None

    def __str__(self) -> str:
        if self.by in {"this", "next", "previous", "first", "last"}:
            head = f"{self.by} {self.kind}"
        elif self.by == "id":
            head = f"{self.kind} id {text(self.value)}"
        else:
            head = f'{self.kind} "{text(self.value)}"'
        return head if self.of is None else f"{head} of {self.of}"


class Host:
    """What the engine asks the world. Every method has a do-nothing default."""

    page_id: str = ""
    book_name: str = ""

    def go(self, target: object) -> None:
        """``go to`` an object reference or text."""

    def property(self, name: str, of: object) -> tuple[bool, object]:
        """``(found, value)`` for ``name of of``. ``of`` is None for a system property."""
        return False, None

    def set_property(self, name: str, of: object, value: object) -> bool:
        return False

    def command(self, engine: "Engine", name: str, args: tuple) -> tuple[bool, object]:
        """A built-in message no handler took. ``(handled, value)``."""
        return False, None

    def function(self, engine: "Engine", name: str, args: tuple) -> tuple[bool, object]:
        """A built-in function the engine does not know. ``(handled, value)``."""
        return False, None

    def dll(self, library: str, name: str, args: tuple) -> tuple[bool, object]:
        """A function a ``linkDLL`` block declared. ``(answered, value)``."""
        return False, None

    def request(self, prompt: str, buttons: tuple[str, ...]) -> str:
        """``request``: the button chosen. The default chooses nothing."""
        return ""

    def beep(self) -> None:
        pass

    def find_file(self, name: str) -> object:
        """A path for ``name`` on the shelf, or None."""
        return None


class _Return(Exception):
    def __init__(self, value: object) -> None:
        self.value = value


class _Break(Exception):
    pass


class _Continue(Exception):
    pass


@dataclass
class Frame:
    handler: A.Handler | None
    message: str
    kind: str
    chain_index: int
    args: tuple
    locals: dict = field(default_factory=dict)
    system: set = field(default_factory=set)
    target: object = None


# A handler table: ``(kind, name)`` to every handler for it, first in the chain first.
Lookup = Callable[[str, str], list]


class Engine:
    def __init__(
        self,
        lookup: Lookup,
        host: Host | None = None,
        props: UserProperties | None = None,
        variables: dict | None = None,
        sysbooks: list | None = None,
        on_push_sysbook: Callable[[str], None] | None = None,
        lenient: bool = True,
    ) -> None:
        self.lookup = lookup
        self.host = host or Host()
        self.props = props if props is not None else UserProperties()
        # System variables other than ``__`` names, by lower-case name.
        self.globals: dict = variables if variables is not None else {}
        self.sysbooks: list = sysbooks if sysbooks is not None else []
        self.on_push_sysbook = on_push_sysbook
        self.dll_functions: dict[str, str] = {}
        self.frames: list[Frame] = []
        self.steps = 0
        self.requests: list[str] = []
        self.beeps = 0
        self.skipped: list[str] = []
        # Lenient: a statement that raises a ScriptError is named in ``errors``
        # and the handler goes on with the next statement. ToolBook would stop.
        self.lenient = lenient
        self.errors: list[str] = []
        # The last function no handler, built-in, or DLL answered.
        self.unanswered: str | None = None
        # Arguments a DLL function wrote, by position, from the last call.
        self.dll_out: dict[int, object] = {}

    # entry points ---------------------------------------------------------

    def _handlers(self, kind: str, name: str, target: object = None) -> list:
        """The handlers for a message, first first. A host with ``route`` decides the
        object path from the target; otherwise ``lookup`` is the whole chain."""
        route = getattr(self.host, "route", None)
        if route is None:
            return self.lookup(kind, name)
        return route(kind, name, target if target is not None else self._target(), self.lookup)

    def send(self, name: str, args: tuple = (), target: object = None) -> object:
        """Send message ``name``. Returns the handler's return value, or None."""
        key = name.lower()
        handlers = self._handlers("handle", key, target)
        if handlers:
            return self._run(handlers[0], key, "handle", 0, args, target)
        handled, value = self._builtin_command(key, args)
        return value if handled else None

    def get(self, name: str, args: tuple = (), target: object = None) -> object:
        """``name(args)``: a ``to get`` handler, a built-in, or a DLL function."""
        key = name.lower()
        handlers = self._handlers("get", key, target)
        if handlers:
            return self._run(handlers[0], key, "get", 0, args, target)
        return self._builtin_function(key, args)

    def handles(self, name: str, target: object = None) -> bool:
        return bool(self._handlers("handle", name.lower(), target))

    # running --------------------------------------------------------------

    def _run(self, handler: A.Handler, message: str, kind: str, index: int, args: tuple, target: object) -> object:
        if len(self.frames) >= DEPTH_LIMIT:
            raise ScriptError(f"{message}: handlers nest too deep")
        frame = Frame(handler, message, kind, index, tuple(args), target=target if target is not None else self._target())
        for position, param in enumerate(handler.params):
            value = args[position] if position < len(args) else ""
            if isinstance(value, Array) and not param.by_ref:
                copied = Array(value.dims)
                copied.cells = dict(value.cells)
                value = copied
            frame.locals[param.name] = value
        if handler.value_param is not None and len(args) > len(handler.params):
            frame.locals[handler.value_param.name] = args[len(handler.params)]
        frame.locals.setdefault("it", "")
        self.frames.append(frame)
        try:
            self._block(handler.body)
        except _Return as done:
            return done.value
        except (_Break, _Continue):
            return None
        finally:
            self.frames.pop()
        return None

    def _target(self) -> object:
        return self.frames[-1].target if self.frames else None

    @property
    def frame(self) -> Frame:
        if not self.frames:
            self.frames.append(Frame(None, "", "handle", 0, ()))
        return self.frames[-1]

    def run_statements(self, body: tuple, target: object = None) -> object:
        """Run statements outside a handler, in a fresh frame."""
        frame = Frame(None, "", "handle", 0, (), target=target)
        frame.locals["it"] = ""
        self.frames.append(frame)
        try:
            self._block(body)
        except _Return as done:
            return done.value
        except (_Break, _Continue):
            return None
        finally:
            self.frames.pop()
        return None

    def _block(self, body: tuple) -> None:
        for statement in body:
            self.steps += 1
            if self.steps > STEP_LIMIT:
                raise ScriptError("the script ran too long")
            self._statement(statement)

    def _statement(self, node) -> None:
        method = getattr(self, "_do_" + type(node).__name__)
        if not self.lenient:
            method(node)
            return
        try:
            method(node)
        except ScriptError as exc:
            where = self.frames[-1].message if self.frames else ""
            self.errors.append(f"{where} line {getattr(node, 'line', 0)}: {exc}")

    def _do_Declare(self, node: A.Declare) -> None:
        for name, dims, init in node.names:
            if node.scope == "system":
                self.frame.system.add(name)
                if dims and not isinstance(self._read_global(name), Array):
                    self._write_global(name, Array(tuple(dims)))
                elif not dims and not self._known_global(name):
                    pass
            else:
                if dims:
                    self.frame.locals[name] = Array(tuple(dims))
                else:
                    self.frame.locals.setdefault(name, "")
            if init is not None:
                self._assign(A.Name(name, name), self.eval(init))

    def _do_Assign(self, node: A.Assign) -> None:
        self._assign(node.target, self.eval(node.value))

    def _do_Put(self, node: A.Put) -> None:
        value = text(self.eval(node.value))
        if node.mode == "into":
            self._assign(node.target, self.eval(node.value))
            return
        old = text(self.eval(node.target))
        self._assign(node.target, old + value if node.mode == "after" else value + old)

    def _do_Get(self, node: A.Get) -> None:
        self.frame.locals["it"] = self.eval(node.value)

    def _do_Send(self, node: A.Send) -> None:
        name = node.name if isinstance(node.name, str) else text(self.eval(node.name)).strip().lower()
        args = tuple(self.eval(arg) for arg in node.args)
        target = self.eval(node.to) if node.to is not None else None
        if node.idle:
            self.skipped.append(f"send {name} when idle")
            return
        self.frame.locals["it"] = self.frame.locals.get("it", "")
        self.send(name, args, target)

    def _do_Forward(self, node: A.Forward) -> None:
        frame = self.frame
        if frame.handler is None:
            return
        handlers = self._handlers(frame.kind, frame.message, frame.target)
        index = frame.chain_index + 1
        if index < len(handlers):
            value = self._run(handlers[index], frame.message, frame.kind, index, frame.args, frame.target)
            if frame.kind == "get":
                raise _Return(value)
            return
        if frame.kind == "handle":
            self._builtin_command(frame.message, frame.args)

    def _do_Return(self, node: A.Return) -> None:
        raise _Return(self.eval(node.value) if node.value is not None else None)

    def _do_Break(self, node: A.Break) -> None:
        if node.target:
            raise _Return(None)
        raise _Break()

    def _do_Continue(self, node: A.Continue) -> None:
        raise _Continue()

    def _do_If(self, node: A.If) -> None:
        if self.condition(node.cond):
            self._block(node.then)
        else:
            self._block(node.otherwise)

    def _do_Conditions(self, node: A.Conditions) -> None:
        for cond, body in node.cases:
            if self.condition(cond):
                self._block(body)
                return
        self._block(node.otherwise)

    def _do_Step(self, node: A.Step) -> None:
        start = as_number(self.eval(node.start))
        end = as_number(self.eval(node.end))
        by = as_number(self.eval(node.by)) if node.by is not None else 1
        if by == 0:
            raise ScriptError("step by 0")
        value = start
        while (by > 0 and value <= end) or (by < 0 and value >= end):
            self._assign(node.var, tidy(value))
            try:
                self._block(node.body)
            except _Break:
                return
            except _Continue:
                pass
            value = as_number(self.eval(node.var)) + by

    def _do_While(self, node: A.While) -> None:
        while self.condition(node.cond):
            try:
                self._block(node.body)
            except _Break:
                return
            except _Continue:
                continue

    def _do_DoUntil(self, node: A.DoUntil) -> None:
        while True:
            try:
                self._block(node.body)
            except _Break:
                return
            except _Continue:
                pass
            if self.condition(node.cond):
                return

    def _do_In(self, node: A.In) -> None:
        self.eval(node.target)
        self._block(node.body)

    def _do_Go(self, node: A.Go) -> None:
        self.host.go(self.eval(node.target))

    def _do_Push(self, node: A.Push) -> None:
        value = self.eval(node.value)
        if _is_sysbooks(node.target):
            self.push_sysbook(text(value))
            return
        old = text(self.eval(node.target))
        item = text(value)
        self._assign(node.target, item if old == "" else item + "," + old)

    def _do_Pop(self, node: A.Pop) -> None:
        old = text(self.eval(node.source))
        if old == "":
            first, rest = "", ""
        else:
            first, _, rest = old.partition(",")
        self._assign(node.source, rest)
        if node.target is not None:
            self._assign(node.target, first)
        else:
            self.frame.locals["it"] = first

    def _do_Increment(self, node: A.Increment) -> None:
        by = as_number(self.eval(node.by)) if node.by is not None else 1
        old = as_number(self.eval(node.target))
        self._assign(node.target, tidy(old - by if node.down else old + by))

    def _do_Clear(self, node: A.Clear) -> None:
        if _is_sysbooks(node.target):
            self.sysbooks.clear()
            return
        self._assign(node.target, "")

    def _do_Request(self, node: A.Request) -> None:
        prompt = text(self.eval(node.prompt))
        buttons = tuple(text(self.eval(button)) for button in node.buttons)
        self.requests.append(prompt)
        self.frame.locals["it"] = self.host.request(prompt, buttons)

    def _do_LinkDLL(self, node: A.LinkDLL) -> None:
        library = text(self.eval(node.library)).lower()
        if node.unlink:
            for name, lib in list(self.dll_functions.items()):
                if lib == library:
                    del self.dll_functions[name]
            return
        for words in node.declarations:
            if "(" in words:
                at = words.index("(")
                if at >= 1:
                    self.dll_functions[words[at - 1].lower()] = library
            elif len(words) >= 2:
                self.dll_functions[words[-1].lower()] = library

    def _do_Command(self, node: A.Command) -> None:
        args = tuple(self.eval(arg) for arg in node.args)
        if node.raw:
            args = node.raw
        if node.name in {"beep"}:
            self.beeps += 1
            self.host.beep()
            return
        handlers = self._handlers("handle", node.name)
        if handlers:
            self._run(handlers[0], node.name, "handle", 0, args, None)
            return
        handled, _value = self._builtin_command(node.name, args)
        if not handled:
            self.skipped.append(node.name)

    # sysBooks ---------------------------------------------------------------

    def push_sysbook(self, name: str) -> None:
        key = name.strip().lower()
        if key in self.sysbooks:
            self.sysbooks.remove(key)
        self.sysbooks.insert(0, key)
        if self.on_push_sysbook is not None:
            self.on_push_sysbook(key)

    # built-ins -------------------------------------------------------------

    def _builtin_command(self, name: str, args: tuple) -> tuple[bool, object]:
        return self.host.command(self, name, args)

    def _builtin_function(self, name: str, args: tuple) -> object:
        function = _FUNCTIONS.get(name)
        if function is not None:
            return function(self, args)
        handled, value = self.host.function(self, name, args)
        if handled:
            return value
        library = self.dll_functions.get(name)
        if library is not None:
            self.host.dll_out = {}
            answered, value = self.host.dll(library, name, args)
            self.dll_out = dict(getattr(self.host, "dll_out", {}) or {})
            return value if answered else ""
        handled, value = self.host.dll("", name, args)
        if handled:
            return value
        self.skipped.append(name + "()")
        self.unanswered = name
        return ""

    # names -------------------------------------------------------------------

    def _known_global(self, name: str) -> bool:
        if UserProperties.owns(name):
            return name in self.props
        return name in self.globals

    def _read_global(self, name: str) -> object:
        if UserProperties.owns(name):
            value = self.props.get(name)
            return "" if value is None else value
        return self.globals.get(name, "")

    def _write_global(self, name: str, value: object) -> None:
        if UserProperties.owns(name):
            self.props.set(name, value)
        else:
            self.globals[name] = value

    def _is_system(self, name: str) -> bool:
        return name in self.frame.system

    def read_name(self, node: A.Name) -> object:
        name = node.name
        frame = self.frame
        if name in frame.locals and name not in frame.system:
            return frame.locals[name]
        if name in frame.system:
            return self._read_global(name)
        if name in CONSTANTS:
            return CONSTANTS[name]
        if name == "sysbooks":
            return ",".join(self.sysbooks)
        found, value = self.host.property(name, None)
        if found:
            return value
        return node.spelling or name

    def _assign(self, target, value: object) -> None:
        if isinstance(target, A.Name):
            name = target.name
            if name == "sysbooks":
                self.sysbooks[:] = [item.strip().lower() for item in text(value).split(",") if item.strip()]
                return
            if name in self.frame.system:
                self._write_global(name, value)
                return
            if name == "it" or name in self.frame.locals:
                self.frame.locals[name] = value
                return
            if self.host.set_property(name, None, value):
                return
            self.frame.locals[name] = value
            return
        if isinstance(target, A.Index):
            container = self._array_for(target.base)
            container.set(self._index(target.indexes), value)
            return
        if isinstance(target, A.Chunk):
            old = text(self.eval(target.of))
            start = int(as_number(self.eval(target.start)))
            end = int(as_number(self.eval(target.end))) if target.end is not None else start
            self._assign(target.of, put_chunk(old, target.kind, start, end, text(value)))
            return
        if isinstance(target, A.Prop):
            of = self.eval(target.of) if target.of is not None else None
            if not self.host.set_property(target.name, of, value):
                self.skipped.append(f"set {target.name}")
            return
        raise ScriptError(f"cannot assign to {type(target).__name__}")

    def _array_for(self, base) -> Array:
        if isinstance(base, A.Name):
            current = self.read_name(base) if (base.name in self.frame.locals or base.name in self.frame.system) else None
            if isinstance(current, Array):
                return current
            array = Array()
            self._assign(base, array)
            return array
        value = self.eval(base)
        if isinstance(value, Array):
            return value
        raise ScriptError("not an array")

    def _index(self, indexes: tuple) -> tuple:
        return tuple(int(as_number(self.eval(item))) for item in indexes)

    # expressions -------------------------------------------------------------

    def condition(self, node) -> bool:
        value = self.eval(node)
        found = logical(value)
        if found is None:
            raise ScriptError(f"{text(value)!r} is not true or false")
        return found

    def eval(self, node) -> object:
        kind = type(node)
        if kind is A.Lit:
            return node.value
        if kind is A.Name:
            return self.read_name(node)
        if kind is A.Binary:
            return self._binary(node)
        if kind is A.Unary:
            value = self.eval(node.operand)
            if node.op == "not":
                return not truth(value)
            if node.op == "bitnot":
                return ~int(as_number(value)) & 0xFFFFFFFF
            return tidy(-as_number(value))
        if kind is A.Call:
            args = tuple(self.eval(arg) for arg in node.args)
            target = self.eval(node.of) if node.of is not None else None
            self.unanswered = None
            self.dll_out = {}
            value = self.get(node.name, args, target)
            if self.unanswered == node.name:
                self.unanswered = node.spelling or node.name
            out, self.dll_out = self.dll_out, {}
            for position, written in out.items():
                # A STRING argument is the variable's buffer; the DLL's text comes back into it.
                if position < len(node.args) and isinstance(node.args[position], (A.Name, A.Index)):
                    self._assign(node.args[position], written)
            return value
        if kind is A.Index:
            base = self.eval(node.base)
            if isinstance(base, Array):
                return base.get(self._index(node.indexes))
            return ""
        if kind is A.Chunk:
            source = text(self.eval(node.of))
            start = int(as_number(self.eval(node.start)))
            end = int(as_number(self.eval(node.end))) if node.end is not None else start
            return get_chunk(source, node.kind, start, end)
        if kind is A.Prop:
            of = self.eval(node.of) if node.of is not None else None
            return self._property(node.name, of)
        if kind is A.ObjRef:
            value = self.eval(node.value) if node.value is not None else None
            of = self.eval(node.of) if node.of is not None else None
            return Ref(node.kind, node.by, value, of)
        if kind is A.Special:
            if node.name == "self" or node.name == "target":
                return self._target()
            found, value = self.host.property(node.name, None)
            return value if found else node.name
        if kind is A.ListExpr:
            return ",".join(text(self.eval(item)) for item in node.items)
        raise ScriptError(f"cannot evaluate {kind.__name__}")

    def _property(self, name: str, of: object) -> object:
        found, value = self.host.property(name, of)
        if found:
            return value
        self.skipped.append(f"{name} of")
        return ""

    def _binary(self, node: A.Binary) -> object:
        op = node.op
        if op == "and":
            return truth(self.eval(node.left)) and truth(self.eval(node.right))
        if op == "or":
            return truth(self.eval(node.left)) or truth(self.eval(node.right))
        left = self.eval(node.left)
        if op == "is a" or op == "is not a":
            result = _is_a(left, text(node.right.value))
            return result if op == "is a" else not result
        if op == "as":
            return left
        right = self.eval(node.right)
        if op == "=":
            return same(left, right)
        if op == "<>":
            return not same(left, right)
        if op in {"<", ">", "<=", ">="}:
            order = compare(left, right)
            return {"<": order < 0, ">": order > 0, "<=": order <= 0, ">=": order >= 0}[op]
        if op == "&":
            return text(left) + text(right)
        if op == "&&":
            return text(left) + " " + text(right)
        if op == "contains":
            return text(right).lower() in text(left).lower()
        if op in {"in", "not in"}:
            inside = text(left).lower() in text(right).lower()
            return inside if op == "in" else not inside
        if op in {"within", "not within"}:
            return False if op == "within" else True
        a, b = as_number(left), as_number(right)
        if op == "+":
            return tidy(a + b)
        if op == "-":
            return tidy(a - b)
        if op == "*":
            return tidy(a * b)
        if op == "/":
            if b == 0:
                raise ScriptError("division by zero")
            return tidy(a / b)
        if op == "div":
            if b == 0:
                raise ScriptError("division by zero")
            return int(a / b)
        if op == "mod":
            if b == 0:
                raise ScriptError("division by zero")
            return tidy(a - b * int(a / b))
        if op == "^":
            return tidy(a ** b)
        x, y = int(a), int(b)
        if op == "bitand":
            return x & y
        if op == "bitor":
            return x | y
        if op == "bitxor":
            return x ^ y
        if op == "bitshiftleft":
            return (x << y) & 0xFFFFFFFF
        if op == "bitshiftright":
            return x >> y
        raise ScriptError(f"unknown operator {op}")


def _is_sysbooks(node) -> bool:
    return isinstance(node, A.Name) and node.name == "sysbooks"


def _is_a(value: object, kind: str) -> bool:
    if kind in {"number", "int", "integer", "long", "real", "word", "dword", "byte"}:
        return number(value) is not None
    if kind == "logical":
        return logical(value) is not None
    if kind == "string":
        return True
    return False


# chunks ----------------------------------------------------------------------

def _pieces(source: str, kind: str) -> list[tuple[int, int]]:
    """Spans of each char, word, item, or textline in ``source``."""
    if kind == "char":
        return [(index, index + 1) for index in range(len(source))]
    if kind == "item":
        spans, start = [], 0
        for index, ch in enumerate(source):
            if ch == ",":
                spans.append((start, index))
                start = index + 1
        if source:
            spans.append((start, len(source)))
        return spans
    if kind == "textline":
        spans, start, index = [], 0, 0
        while index < len(source):
            if source[index] in "\r\n":
                spans.append((start, index))
                if source[index] == "\r" and index + 1 < len(source) and source[index + 1] == "\n":
                    index += 1
                start = index + 1
            index += 1
        if start < len(source):
            spans.append((start, len(source)))
        return spans
    spans, index = [], 0
    while index < len(source):
        while index < len(source) and source[index] in " \t\r\n":
            index += 1
        if index >= len(source):
            break
        start = index
        while index < len(source) and source[index] not in " \t\r\n":
            index += 1
        spans.append((start, index))
    return spans


def get_chunk(source: str, kind: str, start: int, end: int) -> str:
    spans = _pieces(source, kind)
    count = len(spans)
    if start < 0:
        start = count + 1 + start
    if end < 0:
        end = count + 1 + end
    if start < 1 or start > count or end < start:
        return ""
    end = min(end, count)
    return source[spans[start - 1][0]:spans[end - 1][1]]


def put_chunk(source: str, kind: str, start: int, end: int, value: str) -> str:
    spans = _pieces(source, kind)
    count = len(spans)
    if start < 0:
        start = count + 1 + start
    if end < 0:
        end = count + 1 + end
    if start < 1:
        start = 1
    if end < start:
        end = start
    if start > count:
        separator = {"item": ",", "textline": "\r\n", "word": " ", "char": ""}[kind]
        pad = separator * (start - count - (0 if count else 1)) if separator else ""
        if count and separator:
            pad = separator * (start - count)
        return source + pad + value
    end = min(end, count)
    return source[:spans[start - 1][0]] + value + source[spans[end - 1][1]:]


def count_chunks(source: str, kind: str) -> int:
    return len(_pieces(source, kind))


# built-in functions ------------------------------------------------------------

def _arg(args: tuple, index: int) -> object:
    return args[index] if index < len(args) else ""


def _ansi_to_char(engine: Engine, args: tuple) -> str:
    code = int(as_number(_arg(args, 0)))
    return bytes([code & 0xFF]).decode("latin1")


def _char_to_ansi(engine: Engine, args: tuple) -> int:
    value = text(_arg(args, 0))
    return value.encode("latin1", "replace")[0] if value else 0


def _offset(engine: Engine, args: tuple) -> int:
    needle, haystack = text(_arg(args, 0)).lower(), text(_arg(args, 1)).lower()
    found = haystack.find(needle)
    return found + 1 if found >= 0 else 0


def _random_n(engine: Engine, args: tuple) -> int:
    limit = int(as_number(_arg(args, 0)))
    return _random.randint(1, limit) if limit >= 1 else 0


def _min(engine: Engine, args: tuple):
    values = [as_number(item) for item in _flat(args)]
    return tidy(min(values)) if values else ""


def _max(engine: Engine, args: tuple):
    values = [as_number(item) for item in _flat(args)]
    return tidy(max(values)) if values else ""


def _flat(args: tuple) -> list:
    found = []
    for item in args:
        found.extend(part for part in text(item).split(",") if part.strip() != "")
    return found


def _round(engine: Engine, args: tuple):
    value = as_number(_arg(args, 0))
    places = int(as_number(_arg(args, 1))) if len(args) > 1 else 0
    factor = 10 ** places
    scaled = abs(value) * factor
    rounded = int(scaled + 0.5) / factor
    return tidy(rounded if value >= 0 else -rounded)


def _trunc(engine: Engine, args: tuple):
    return int(as_number(_arg(args, 0)))


_FUNCTIONS: dict[str, Callable[[Engine, tuple], object]] = {
    "charcount": lambda engine, args: count_chunks(text(_arg(args, 0)), "char"),
    "wordcount": lambda engine, args: count_chunks(text(_arg(args, 0)), "word"),
    "itemcount": lambda engine, args: count_chunks(text(_arg(args, 0)), "item"),
    "textlinecount": lambda engine, args: count_chunks(text(_arg(args, 0)), "textline"),
    "uppercase": lambda engine, args: text(_arg(args, 0)).upper(),
    "lowercase": lambda engine, args: text(_arg(args, 0)).lower(),
    "ansitochar": _ansi_to_char,
    "chartoansi": _char_to_ansi,
    "offset": _offset,
    "random": _random_n,
    "abs": lambda engine, args: tidy(abs(as_number(_arg(args, 0)))),
    "min": _min,
    "max": _max,
    "round": _round,
    "truncate": _trunc,
    "trunc": _trunc,
    "isnumber": lambda engine, args: number(_arg(args, 0)) is not None,
    "isobject": lambda engine, args: isinstance(_arg(args, 0), Ref),
}
