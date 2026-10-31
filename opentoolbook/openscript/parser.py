"""OpenScript source to a syntax tree.

``parse_script(source)`` returns every handler in the source, keyed
``"<kind> <name>"`` in lower case, where kind is ``handle``, ``get``, or
``set``. A handler that does not parse is left out and its error is
listed with the line it starts on, so one bad handler does not hide the
rest of the script.
"""

from __future__ import annotations

from opentoolbook.openscript import ast as A
from opentoolbook.openscript.lexer import Line, Token, logical_lines

OBJECT_TYPES = frozenset({
    "page", "pages", "background", "backgrounds", "book", "field", "fields", "button", "buttons",
    "recordfield", "recordfields", "group", "groups", "rectangle", "roundedrectangle", "ellipse",
    "line", "angledline", "curve", "arc", "pie", "polygon", "irregularpolygon", "picture",
    "paintobject", "viewer", "window", "hotword", "hotwords", "combobox", "stage", "menu",
    "menuitem", "slider", "equation", "hyperlink", "object",
    # resources
    "bitmap", "icon", "cursor", "palette", "menubar", "graphic", "font", "resource",
})
CHUNKS = {
    "char": "char", "chars": "char", "character": "char", "characters": "char",
    "word": "word", "words": "word", "item": "item", "items": "item",
    "textline": "textline", "textlines": "textline",
}
ORDINALS = frozenset({"this", "next", "previous", "prev", "first", "last"})
TYPES = frozenset({
    "int", "integer", "long", "real", "string", "logical", "word", "dword", "byte", "point",
    "color", "date", "time", "stack", "field", "pointer", "pointer32", "short", "float",
    "double", "char", "object", "array",
})
# Words an expression stops at.
STOP = frozenset({
    "then", "to", "into", "after", "before", "onto", "by", "with", "from", "else", "of",
})
SPECIALS = frozenset({"self", "target", "selection", "focus", "mainwindow", "parent"})


class ParseError(ValueError):
    pass


def parse_script(source: str) -> A.Script:
    script = A.Script()
    lines = logical_lines(source)
    index = 0
    while index < len(lines):
        line = lines[index]
        first = line.tokens[0].low
        if first == "to" and len(line.tokens) >= 3 and line.tokens[1].low in {"handle", "get", "set"}:
            end = _handler_end(lines, index)
            try:
                handler = _handler(lines[index:end])
            except ParseError as exc:
                script.errors.append((line.number, str(exc)))
            else:
                script.handlers.setdefault(f"{handler.kind} {handler.name}", handler)
            index = end
            continue
        index += 1
    return script


def parse_statements(source: str) -> tuple:
    """Statements outside a handler, such as a ``buttonClick`` body pasted alone."""
    return _Block(logical_lines(source)).block(())


def parse_expression(text: str):
    lines = logical_lines(text)
    if len(lines) != 1:
        raise ParseError("one expression expected")
    parser = _Expr(list(lines[0].tokens))
    value = parser.expression()
    parser.done()
    return value


def _handler_end(lines: list[Line], start: int) -> int:
    """Index after the handler that starts at ``start``.

    The handler ends at the first ``end`` line, at nesting depth 0, that is
    bare or names the handler, or just before the next ``to handle`` line.
    """
    name = lines[start].tokens[2].low
    depth = 0
    for index in range(start + 1, len(lines)):
        tokens = lines[index].tokens
        first = tokens[0].low
        if first == "to" and len(tokens) >= 3 and tokens[1].low in {"handle", "get", "set"}:
            return index
        if _opens_block(tokens):
            depth += 1
            continue
        if first == "end":
            second = tokens[1].low if len(tokens) > 1 else ""
            if depth == 0 and (second in {"", name} or second not in _BLOCK_ENDS):
                return index + 1
            if depth > 0:
                depth -= 1
        elif first == "until" and depth > 0:
            depth -= 1
    return len(lines)


_BLOCK_ENDS = frozenset({"if", "conditions", "step", "while", "in", "linkdll", "linkdll32", "do"})


def _opens_block(tokens: tuple[Token, ...]) -> bool:
    first = tokens[0].low
    if first in {"conditions", "step", "while", "do", "linkdll", "linkdll32"}:
        return True
    if first == "in" and len(tokens) > 1:
        return True
    if first == "if":
        return _if_is_block(tokens)
    return False


def _if_is_block(tokens: tuple[Token, ...]) -> bool:
    """``if c`` and ``if c then`` open a block. ``if c then stmt`` is one line."""
    then = _find_word(tokens, "then", 1)
    return then < 0 or then == len(tokens) - 1


def _find_word(tokens, word: str, start: int = 0) -> int:
    depth = 0
    for index in range(start, len(tokens)):
        token = tokens[index]
        if token.kind == "op" and token.text in "([":
            depth += 1
        elif token.kind == "op" and token.text in ")]":
            depth -= 1
        elif depth == 0 and token.kind == "word" and token.low == word:
            return index
    return -1


def _handler(lines: list[Line]) -> A.Handler:
    head = lines[0].tokens
    kind = head[1].low
    name = head[2].low
    rest = list(head[3:])
    value_param = None
    if kind == "set":
        cut = _find_word(tuple(rest), "to")
        if cut >= 0:
            value = _params(rest[cut + 1:])
            value_param = value[0] if value else None
            rest = rest[:cut]
    params = _params(rest)
    body_lines = lines[1:]
    if body_lines and body_lines[-1].tokens[0].low == "end":
        last = body_lines[-1].tokens
        second = last[1].low if len(last) > 1 else ""
        if second in {"", name} or second not in _BLOCK_ENDS:
            body_lines = body_lines[:-1]
    body = _Block(body_lines).block(())
    return A.Handler(kind, name, tuple(params), body, value_param, lines[0].number)


def _params(tokens: list[Token]) -> list[A.Param]:
    params: list[A.Param] = []
    group: list[Token] = []
    for token in tokens + [Token("op", ",", 0)]:
        if token.kind == "op" and token.text == ",":
            words = [item for item in group if item.kind == "word"]
            by_ref = False
            for at, item in enumerate(words):
                if item.low == "by":
                    by_ref = any(word.low == "reference" for word in words[at + 1:])
                    words = words[:at]
                    break
            if words:
                kind = words[0].low if len(words) > 1 and words[0].low in TYPES else None
                params.append(A.Param(words[-1].low, kind, by_ref))
            group = []
        elif not (token.kind == "op" and token.text in "[]"):
            group.append(token)
    return params


class _Block:
    """Lines to statements, with blocks."""

    def __init__(self, lines: list[Line]):
        self.lines = lines
        self.index = 0

    def block(self, stops: tuple[str, ...]) -> tuple:
        """Statements until a line whose first word is in ``stops`` (not consumed) or the end."""
        body = []
        while self.index < len(self.lines):
            line = self.lines[self.index]
            first = line.tokens[0].low
            if first in stops:
                return tuple(body)
            self.index += 1
            body.append(self.statement(line))
        return tuple(body)

    def _close(self, words: tuple[str, ...]) -> None:
        """Consume an ``end`` line (optionally ``end word``)."""
        if self.index < len(self.lines):
            tokens = self.lines[self.index].tokens
            if tokens[0].low == "end" and (len(tokens) == 1 or tokens[1].low in words):
                self.index += 1
                return
        raise ParseError(f"missing end {words[0] if words else ''}".strip())

    def statement(self, line: Line):
        try:
            return self._statement(line)
        except ParseError as exc:
            if str(exc).startswith("line "):
                raise
            text = " ".join(token.text for token in line.tokens)
            raise ParseError(f"line {line.number}: {exc} in: {text[:80]}") from None

    def _statement(self, line: Line):
        tokens = list(line.tokens)
        first = tokens[0].low
        number = line.number
        if first == "if":
            return self._if(tokens, number)
        if first == "conditions":
            return self._conditions(number)
        if first == "while":
            cond = _parse(tokens[1:])
            body = self.block(("end",))
            self._close(("while",))
            return A.While(cond, body, number)
        if first == "step":
            return self._step(tokens, number)
        if first == "do" and len(tokens) == 1:
            body = self.block(("until",))
            if self.index >= len(self.lines):
                raise ParseError("do without until")
            until = self.lines[self.index].tokens
            self.index += 1
            return A.DoUntil(body, _parse(list(until[1:])), number)
        if first == "in" and len(tokens) > 1:
            target = _parse(tokens[1:])
            body = self.block(("end",))
            self._close(("in",))
            return A.In(target, body, number)
        if first in {"linkdll", "linkdll32"}:
            library = _parse(tokens[1:]) if len(tokens) > 1 else A.Lit("")
            decls = []
            while self.index < len(self.lines):
                inner = self.lines[self.index].tokens
                if inner[0].low == "end":
                    break
                decls.append(tuple(token.text for token in inner))
                self.index += 1
            self._close(("linkdll", "linkdll32"))
            return A.LinkDLL(library, tuple(decls), False, number)
        return _simple(tokens, number)

    def _if(self, tokens: list[Token], number: int):
        then = _find_word(tuple(tokens), "then", 1)
        if then >= 0 and then < len(tokens) - 1:
            cond = _parse(tokens[1:then])
            rest = tokens[then + 1:]
            other = _find_word(tuple(rest), "else")
            if other >= 0:
                return A.If(cond, (_simple(rest[:other], number),), (_simple(rest[other + 1:], number),), number)
            return A.If(cond, (_simple(rest, number),), (), number)
        cond = _parse(tokens[1:then] if then >= 0 else tokens[1:])
        body = self.block(("end", "else"))
        otherwise: tuple = ()
        if self.index < len(self.lines) and self.lines[self.index].tokens[0].low == "else":
            line = self.lines[self.index]
            self.index += 1
            if len(line.tokens) > 1:
                otherwise = (_simple(list(line.tokens[1:]), line.number),)
            otherwise += self.block(("end",))
        self._close(("if",))
        return A.If(cond, body, otherwise, number)

    def _conditions(self, number: int):
        cases = []
        otherwise: tuple = ()
        while self.index < len(self.lines):
            tokens = list(self.lines[self.index].tokens)
            first = tokens[0].low
            if first == "end":
                self._close(("conditions",))
                return A.Conditions(tuple(cases), otherwise, number)
            self.index += 1
            if first == "when":
                cond = _parse(tokens[1:])
                cases.append((cond, self.block(("when", "else", "end"))))
            elif first == "else":
                if len(tokens) > 1:
                    otherwise = (_simple(tokens[1:], number),) + self.block(("end",))
                else:
                    otherwise = self.block(("end",))
            else:
                raise ParseError(f"line {self.lines[self.index - 1].number}: {first} inside conditions")
        raise ParseError("missing end conditions")

    def _step(self, tokens: list[Token], number: int):
        parser = _Expr(tokens[1:])
        var = parser.lvalue()
        parser.expect_word("from")
        start = parser.expression()
        parser.expect_word("to")
        end = parser.expression()
        by = None
        if parser.at_word("by"):
            parser.next()
            by = parser.expression()
        parser.done()
        body = self.block(("end",))
        self._close(("step",))
        return A.Step(var, start, end, by, body, number)


def _parse(tokens: list[Token]):
    parser = _Expr(list(tokens))
    value = parser.expression()
    parser.done()
    return value


def _parse_list(tokens: list[Token]):
    parser = _Expr(list(tokens))
    value = parser.expression_list()
    parser.done()
    return value


def _value(tokens: list[Token]):
    """One expression, or a list when the tokens hold top-level commas."""
    value = _parse_list(tokens)
    return value.items[0] if len(value.items) == 1 else value


def _simple(tokens: list[Token], number: int):
    if not tokens:
        raise ParseError(f"line {number}: empty statement")
    first = tokens[0].low
    rest = tokens[1:]
    if first in {"system", "local"} and rest:
        return _declare(first, rest, number)
    if first == "get":
        return A.Get(_value(rest) if rest else A.Lit(""), number)
    if first == "return":
        return A.Return(_value(rest) if rest else None, number)
    if first == "forward" and not rest:
        return A.Forward(number)
    if first == "break":
        return A.Break(" ".join(token.low for token in rest[1:]) if rest else None, number)
    if first == "continue" and not rest:
        return A.Continue(number)
    if first == "send" and rest:
        return _send(rest, number)
    if first == "go" and rest:
        body = rest[1:] if rest[0].low == "to" else rest
        return A.Go(_parse(body), number)
    if first == "put" and rest:
        for mode in ("into", "after", "before"):
            cut = _find_word(tuple(rest), mode)
            if cut >= 0:
                return A.Put(_value(rest[:cut]), mode, _lvalue(rest[cut + 1:]), number)
    if first == "set" and rest:
        cut = _find_word(tuple(rest), "to")
        while cut >= 0:
            try:
                return A.Assign(_lvalue(rest[:cut]), _value(rest[cut + 1:]), number)
            except ParseError:
                cut = _find_word(tuple(rest), "to", cut + 1)
    if first == "push" and rest:
        cut = _find_word(tuple(rest), "onto")
        if cut >= 0:
            return A.Push(_value(rest[:cut]), _lvalue(rest[cut + 1:]), number)
    if first == "pop" and rest:
        cut = _find_word(tuple(rest), "into")
        if cut >= 0:
            return A.Pop(_lvalue(rest[:cut]), _lvalue(rest[cut + 1:]), number)
        return A.Pop(_lvalue(rest), None, number)
    if first in {"increment", "decrement"} and rest:
        cut = _find_word(tuple(rest), "by")
        target = _lvalue(rest[:cut] if cut >= 0 else rest)
        by = _parse(rest[cut + 1:]) if cut >= 0 else None
        return A.Increment(target, by, first == "decrement", number)
    if first == "clear" and rest:
        return A.Clear(_lvalue(rest), number)
    if first == "request" and rest:
        return _request(rest, number)
    if first == "unlinkdll" or first == "unlinkdll32":
        return A.LinkDLL(_parse(rest) if rest else A.Lit(""), (), True, number)
    equals = _top_equals(tokens)
    if equals > 0:
        return A.Assign(_lvalue(tokens[:equals]), _value(tokens[equals + 1:]), number)
    if tokens[0].kind == "word":
        return _command(first, rest, number)
    raise ParseError(f"line {number}: cannot read {' '.join(token.text for token in tokens)}")


def _declare(scope: str, tokens: list[Token], number: int):
    kind = None
    if tokens and tokens[0].low in TYPES and len(tokens) > 1 and tokens[1].kind == "word":
        kind = tokens[0].low
        tokens = tokens[1:]
    names = []
    group: list[Token] = []
    depth = 0
    for token in tokens + [Token("op", ",", number)]:
        if token.kind == "op" and token.text in "([":
            depth += 1
        elif token.kind == "op" and token.text in ")]":
            depth -= 1
        if depth == 0 and token.kind == "op" and token.text == ",":
            if group:
                names.append(_declared(group, number))
            group = []
        else:
            group.append(token)
    return A.Declare(scope, kind, tuple(names), number)


def _declared(group: list[Token], number: int):
    if group[0].kind != "word":
        raise ParseError(f"line {number}: bad declaration")
    name = group[0].low
    dims = []
    index = 1
    while index < len(group) and group[index].kind == "op" and group[index].text == "[":
        close = index + 1
        while close < len(group) and not (group[close].kind == "op" and group[close].text == "]"):
            close += 1
        inner = group[index + 1:close]
        dims.append(_parse(inner) if inner else None)
        index = close + 1
    init = None
    if index < len(group) and group[index].kind == "op" and group[index].text == "=":
        init = _parse(group[index + 1:])
        index = len(group)
    if index != len(group):
        raise ParseError(f"line {number}: bad declaration of {name}")
    return (name, tuple(dims), init)


def _send(tokens: list[Token], number: int):
    idle = False
    when = _find_word(tuple(tokens), "when")
    if when >= 0:
        idle = True
        tokens = tokens[:when]
    if tokens[0].kind == "op" and tokens[0].text == "(":
        depth = 0
        for close, token in enumerate(tokens):
            if token.kind == "op" and token.text == "(":
                depth += 1
            elif token.kind == "op" and token.text == ")":
                depth -= 1
                if depth == 0:
                    break
        name = _parse(tokens[1:close])
        rest = tokens[close + 1:]
    else:
        name = tokens[0].low
        rest = tokens[1:]
    within = None
    cut = _find_word(tuple(rest), "in")
    to_at = _find_word(tuple(rest), "to")
    if cut >= 0 and (to_at < 0 or cut > to_at):
        within = _parse(rest[cut + 1:])
        rest = rest[:cut]
    to = None
    cut = _find_word(tuple(rest), "to")
    if cut >= 0:
        to = _parse(rest[cut + 1:])
        rest = rest[:cut]
    if rest and rest[0].kind == "op" and rest[0].text == "(" and _closes_at_end(rest):
        rest = rest[1:-1]
    args = _parse_list(rest).items if rest else ()
    return A.Send(name, tuple(args), to, number, within, idle)


def _closes_at_end(tokens: list[Token]) -> bool:
    depth = 0
    for index, token in enumerate(tokens):
        if token.kind == "op" and token.text == "(":
            depth += 1
        elif token.kind == "op" and token.text == ")":
            depth -= 1
            if depth == 0 and index != len(tokens) - 1:
                return False
    return True


def _request(tokens: list[Token], number: int):
    cut = _find_word(tuple(tokens), "with")
    if cut < 0:
        return A.Request(_parse(tokens), (), number)
    prompt = _parse(tokens[:cut])
    parser = _Expr(tokens[cut + 1:])
    buttons = [parser.concat()]
    while parser.at_word("or"):
        parser.next()
        buttons.append(parser.concat())
    parser.done()
    return A.Request(prompt, tuple(buttons), number)


def _command(name: str, tokens: list[Token], number: int):
    if not tokens:
        return A.Command(name, (), (), number)
    if tokens[0].kind == "op" and tokens[0].text == "(" and _closes_at_end(tokens):
        inner = tokens[1:-1]
        try:
            return A.Command(name, tuple(_parse_list(inner).items) if inner else (), (), number)
        except ParseError:
            pass
    try:
        return A.Command(name, tuple(_parse_list(tokens).items), (), number)
    except ParseError:
        return A.Command(name, (), tuple(token.text for token in tokens), number)


def _top_equals(tokens: list[Token]) -> int:
    depth = 0
    for index, token in enumerate(tokens):
        if token.kind == "op" and token.text in "([":
            depth += 1
        elif token.kind == "op" and token.text in ")]":
            depth -= 1
        elif depth == 0 and token.kind == "op" and token.text == "=":
            return index
    return -1


def _lvalue(tokens: list[Token]):
    parser = _Expr(list(tokens))
    value = parser.lvalue()
    parser.done()
    return value


_MUL_WORDS = ("div", "mod", "bitand", "bitor", "bitxor", "bitshiftleft", "bitshiftright")


class _Expr:
    def __init__(self, tokens: list[Token]):
        self.tokens = tokens
        self.pos = 0
        # Inside a chunk's start or end, ``x of`` is the variable x, and ``of`` belongs to the chunk.
        self.no_prop = 0

    # token helpers
    def peek(self, offset: int = 0) -> Token | None:
        at = self.pos + offset
        return self.tokens[at] if at < len(self.tokens) else None

    def next(self) -> Token:
        token = self.peek()
        if token is None:
            raise ParseError("unexpected end of expression")
        self.pos += 1
        return token

    def at_op(self, text: str, offset: int = 0) -> bool:
        token = self.peek(offset)
        return token is not None and token.kind == "op" and token.text == text

    def at_word(self, word: str, offset: int = 0) -> bool:
        token = self.peek(offset)
        return token is not None and token.kind == "word" and token.low == word

    def expect_op(self, text: str) -> None:
        if not self.at_op(text):
            raise ParseError(f"expected {text!r}")
        self.pos += 1

    def expect_word(self, word: str) -> None:
        if not self.at_word(word):
            raise ParseError(f"expected {word!r}")
        self.pos += 1

    def done(self) -> None:
        token = self.peek()
        if token is not None:
            raise ParseError(f"unexpected {token.text!r}")

    # grammar
    def expression_list(self):
        items = [self.expression()]
        while self.at_op(","):
            self.next()
            items.append(self.expression())
        return A.ListExpr(tuple(items))

    def expression(self):
        return self.disjunction()

    def disjunction(self):
        left = self.conjunction()
        while self.at_word("or"):
            self.next()
            left = A.Binary("or", left, self.conjunction())
        return left

    def conjunction(self):
        left = self.negation()
        while self.at_word("and"):
            self.next()
            left = A.Binary("and", left, self.negation())
        return left

    def negation(self):
        if self.at_word("not"):
            self.next()
            return A.Unary("not", self.negation())
        return self.comparison()

    def comparison(self):
        left = self.concat()
        while True:
            token = self.peek()
            if token is None:
                return left
            if token.kind == "op" and token.text in {"=", "<>", "<", ">", "<=", ">="}:
                self.next()
                left = A.Binary(token.text, left, self.concat())
                continue
            if token.kind == "word" and token.low == "as" and self.peek(1) is not None and self.peek(1).kind == "word":
                self.next()
                left = A.Binary("as", left, A.Lit(self.next().low))
                continue
            if token.kind == "word" and token.low == "contains":
                self.next()
                left = A.Binary("contains", left, self.concat())
                continue
            if token.kind == "word" and token.low == "is":
                self.next()
                negate = False
                if self.at_word("not"):
                    self.next()
                    negate = True
                if self.at_word("in"):
                    self.next()
                    op = "not in" if negate else "in"
                elif self.at_word("within"):
                    self.next()
                    op = "not within" if negate else "within"
                elif (self.at_word("a") or self.at_word("an")) and self.peek(1) is not None and self.peek(1).kind == "word":
                    self.next()
                    kind = self.next().low
                    left = A.Binary("is not a" if negate else "is a", left, A.Lit(kind))
                    continue
                else:
                    op = "<>" if negate else "="
                left = A.Binary(op, left, self.concat())
                continue
            return left

    def concat(self):
        left = self.additive()
        while self.at_op("&") or self.at_op("&&"):
            op = self.next().text
            left = A.Binary(op, left, self.additive())
        return left

    def additive(self):
        left = self.multiplicative()
        while self.at_op("+") or self.at_op("-"):
            op = self.next().text
            left = A.Binary(op, left, self.multiplicative())
        return left

    def multiplicative(self):
        left = self.power()
        while self.at_op("*") or self.at_op("/") or any(self.at_word(word) for word in _MUL_WORDS):
            op = self.next().low
            left = A.Binary(op, left, self.power())
        return left

    def power(self):
        left = self.unary()
        while self.at_op("^"):
            self.next()
            left = A.Binary("^", left, self.unary())
        return left

    def unary(self):
        if self.at_op("-"):
            self.next()
            return A.Unary("-", self.unary())
        if self.at_op("+"):
            self.next()
            return self.unary()
        if self.at_word("not"):
            self.next()
            return A.Unary("not", self.unary())
        if self.at_word("bitnot") and self.peek(1) is not None:
            self.next()
            return A.Unary("bitnot", self.unary())
        return self.primary()

    def operand(self):
        """The thing after ``of``: an object, or a value without binary operators."""
        return self.unary()

    def lvalue(self):
        return self.primary()

    def primary(self):
        token = self.peek()
        if token is None:
            raise ParseError("unexpected end of expression")
        if token.kind == "number":
            self.next()
            text = token.text
            value = float(text) if any(ch in text for ch in ".eE") else int(text)
            return self._postfix(A.Lit(value))
        if token.kind == "string":
            self.next()
            return self._postfix(A.Lit(token.text))
        if token.kind == "op" and token.text == "(":
            self.next()
            saved, self.no_prop = self.no_prop, 0
            try:
                inner = self.expression_list()
            finally:
                self.no_prop = saved
            self.expect_op(")")
            value = inner.items[0] if len(inner.items) == 1 else inner
            return self._postfix(value)
        if token.kind != "word":
            raise ParseError(f"unexpected {token.text!r}")
        word = token.low
        # chunks: char 3 of x, items 2 to 4 of x
        if word in CHUNKS and self._chunk_ahead():
            self.next()
            start = self.additive_no_of()
            end = None
            if self.at_word("to"):
                self.next()
                end = self.additive_no_of()
            self.expect_word("of")
            return A.Chunk(CHUNKS[word], start, end, self.operand())
        if word in {"last", "first"} and self.peek(1) is not None and self.peek(1).low in CHUNKS and self.at_word("of", 2):
            self.next()
            kind = CHUNKS[self.next().low]
            self.expect_word("of")
            return A.Chunk(kind, A.Lit(-1 if word == "last" else 1), None, self.operand())
        if word == "my" and self.peek(1) is not None and self.peek(1).kind == "word":
            self.next()
            name = self.next().low
            if self.at_op("("):
                self.next()
                args = () if self.at_op(")") else self.expression_list().items
                self.expect_op(")")
                return self._postfix(A.Call(name, tuple(args), A.Special("self")))
            return self._postfix(A.Prop(name, A.Special("self")))
        if word in ORDINALS and self.peek(1) is not None and self.peek(1).low in OBJECT_TYPES:
            self.next()
            kind = self.next().low
            of = None
            if self.at_word("of"):
                self.next()
                of = self.operand()
            by = "previous" if word == "prev" else word
            return A.ObjRef(kind, by, None, of)
        if word in OBJECT_TYPES and self._object_ahead():
            return self._object()
        # prop of obj
        if self.at_word("of", 1) and word not in {"not"} and not self.no_prop:
            self.next()
            self.next()
            return A.Prop(word, self.operand())
        # function call
        if self.at_op("(", 1):
            self.next()
            self.next()
            args = ()
            saved, self.no_prop = self.no_prop, 0
            try:
                if not self.at_op(")"):
                    args = self.expression_list().items
            finally:
                self.no_prop = saved
            self.expect_op(")")
            if self.at_word("of") and not self.no_prop:
                self.next()
                return A.Call(word, tuple(args), self.operand(), token.text)
            return self._postfix(A.Call(word, tuple(args), None, token.text))
        if word in SPECIALS:
            self.next()
            return self._postfix(A.Special(word))
        if word in STOP or word in {"and", "or", "is", "contains", "div", "mod"}:
            raise ParseError(f"unexpected {token.text!r}")
        self.next()
        value = self._postfix(A.Name(word, token.text))
        if isinstance(value, A.Index) and self.at_word("of") and not self.no_prop:
            # extItem[0] of obj: an indexed property
            self.next()
            return A.Index(A.Prop(word, self.operand()), value.indexes)
        return value

    def additive_no_of(self):
        self.no_prop += 1
        try:
            return self.additive()
        finally:
            self.no_prop -= 1

    def _postfix(self, value):
        indexes = []
        while self.at_op("["):
            self.next()
            indexes.extend(self.expression_list().items)
            self.expect_op("]")
        if indexes:
            value = A.Index(value, tuple(indexes))
        return value

    def _chunk_ahead(self) -> bool:
        """A chunk word followed by something that ends in ``of``."""
        nxt = self.peek(1)
        if nxt is None:
            return False
        if nxt.kind == "word" and nxt.low == "of":
            return False
        depth = 0
        for index in range(self.pos + 1, len(self.tokens)):
            token = self.tokens[index]
            if token.kind == "op" and token.text in "([":
                depth += 1
            elif token.kind == "op" and token.text in ")]":
                depth -= 1
                if depth < 0:
                    return False
            elif depth == 0 and token.kind == "word" and token.low == "of":
                return True
            elif depth == 0 and token.kind == "op" and token.text == ",":
                return False
        return False

    def _object_ahead(self) -> bool:
        nxt = self.peek(1)
        if nxt is None:
            return False
        if nxt.kind in {"string", "number"}:
            return True
        if nxt.kind == "op" and nxt.text == "(":
            return True
        if nxt.kind == "word":
            if nxt.low == "id":
                return True
            if nxt.low in STOP or nxt.low in {"and", "or", "is", "contains", "div", "mod", "then"}:
                return False
            return True
        return False

    def _object(self):
        kind = self.next().low
        by = "name"
        if self.at_word("id"):
            self.next()
            by = "id"
        value = self.unary_value()
        of = None
        if self.at_word("of"):
            self.next()
            of = self.operand()
        return A.ObjRef(kind, by, value, of)

    def unary_value(self):
        """The identifier of an object: a literal, a name, a call, or a parenthesized expression."""
        token = self.peek()
        if token is None:
            raise ParseError("object without a name")
        if token.kind == "op" and token.text == "-":
            self.next()
            return A.Unary("-", self.unary_value())
        if token.kind == "word" and self.at_word("of", 1):
            # field x of ...: x is the name, not a property
            self.next()
            return A.Name(token.low, token.text)
        return self.primary()
