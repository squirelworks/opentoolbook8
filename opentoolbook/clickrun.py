"""A click, run on the OpenScript interpreter.

ToolBook sends ``buttonClick`` to the object under the pointer. The
message goes up the object hierarchy until a handler takes it: the
object, each group that holds it, innermost first, its page, the
page's background, the book, then each
``sysBooks`` book. ``target`` is the clicked object for every handler on
the way. ``forward`` passes the message one step up.
"""

from __future__ import annotations

from pathlib import Path

from opentoolbook.click import Follow, background_script
from opentoolbook.enter import page_source
from opentoolbook.openscript.interp import Engine, Ref
from opentoolbook.openscript.values import ScriptError, as_number, number, text
from opentoolbook.run import BookHost, parsed

# Object script classes: a button is 9, a field 0xA, a group 0xB.
_KIND = {9: "button", 0xA: "field", 0xB: "group", 0x17: "hotword"}


def _object_source(data: bytes, page_id: str, kind: str, name: str) -> str:
    """The inline script of the named object whose owner (page or background name) is ``page_id``."""
    from opentoolbook.script import object_scripts

    folded = name.lower()
    named = [item for item in object_scripts(data) if item.owner == page_id and item.name.lower() == folded]
    for item in named:
        if _KIND.get(item.kind) == kind:
            return item.source
    # A hotword is clicked by its name; it is not a listed object of the page.
    if kind == "button":
        for item in named:
            if _KIND.get(item.kind) == "hotword":
                return item.source
    return ""


def _on(value: object) -> bool:
    return value is True or text(value).strip().lower() == "true"


class ClickHost(BookHost):
    """The book as the click's handlers see it.

    A property a script sets is a write ``(owner, kind, name, property,
    value)``. ``owner`` is a page id, or the background key of a page
    for an object of its background. ``state`` holds the writes earlier
    clicks made in this book, by owner, then ``(kind, lower-case name)``.
    A property no script set is the stored one.
    """

    def __init__(self, pages, book_file, roots, page_id, fields, present, data=b"", groups=(), state=None):
        super().__init__(pages, book_file, roots)
        self.data = data
        self.page_id = page_id
        self.start_page = page_id
        # Field text the window shows now, by lower-case name.
        self.fields = {name.lower(): value for name, value in (fields or {}).items()}
        self.present = present
        # The groups that hold the clicked object, innermost first.
        self.groups = tuple(groups)
        self.state = state if state is not None else {}
        self.writes: list = []
        self.asked: list = []
        self.inverts: list = []
        self.beeps = 0
        # ``ask(prompt, buttons)`` answers ``request`` while the handler runs.
        self.ask = None
        # ``send exit`` with no handler: the window should close.
        self.exited = False
        self._page_props: dict | None = None
        self._listed: dict = {}
        self._maps: dict = {}
        # The clicked object, its kind and name, while the page it is on is on screen.
        self.clicked: tuple[str, str] | None = None
        # Page changes this run made, to stop an enterPage that goes back and forth.
        self.moves = 0

    # message paths ----------------------------------------------------------

    def _scripts(self, owner: str, kind: str, name: str) -> dict:
        key = (owner, kind, name.lower())
        if key not in self._maps:
            self._maps[key] = parsed(_object_source(self.data, owner, kind, name)).handlers
        return self._maps[key]

    def _page_path(self, page: str, background_only: bool = False) -> list:
        from opentoolbook.show import background_name

        key = ("page path", page, background_only)
        if not self.data:
            return []
        if key not in self._maps:
            found = [] if background_only else [parsed(page_source(self.data, page)).handlers]
            found.append(parsed(background_script(self.data, page)).handlers)
            self._maps[key] = found
            self._maps[("background name", page)] = background_name(self.data, page)
        return self._maps[key]

    def _path(self, target: object) -> list:
        """Handler maps from the target up to the background."""
        page = self.page_id
        if page is None:
            return []
        if not isinstance(target, Ref):
            return self._page_path(page)
        if target.kind == "book":
            return []
        if target.kind == "background":
            named = text(target.value)
            return self._page_path(named if self._page_id(Ref("page", "name", named, None)) is not None else page, background_only=True)
        if target.kind == "page":
            found = self._page_id(target)
            return self._page_path(found if found is not None else page)
        found = self._locate(target)
        if found is None:
            return self._page_path(page)
        _owner, on_page, kind, name, item = found
        path = []
        layer_owner = on_page
        if item is not None and item.layer == "background":
            self._page_path(on_page)
            layer_owner = self._maps[("background name", on_page)]
        path.append(self._scripts(layer_owner, kind, name))
        if kind == "button" and item is None:
            # A hotword is clicked by its name; it is not a listed object.
            path.append(self._scripts(layer_owner, "hotword", name))
        groups = item.groups if item is not None else ()
        path.extend(self._scripts(layer_owner, "group", group) for group in groups)
        if item is not None and item.layer == "background":
            return path + self._page_path(on_page, background_only=True)
        return path + self._page_path(on_page)

    def route(self, kind: str, name: str, target: object, chain) -> list:
        key = f"{kind} {name}"
        found = [handlers[key] for handlers in self._path(target) if key in handlers]
        return found + list(chain(kind, name))

    def go(self, target: object) -> None:
        """``go to``: within this book, leave the old page and enter the new one."""
        old = self.page_id
        super().go(target)
        new = self.page_id
        engine = getattr(self, "engine", None)
        if self.book_name or old is None or new is None or new.lower() == old.lower() or engine is None:
            return
        if self.moves >= 16:
            return
        self.moves += 1
        from opentoolbook.show import background_key

        changed = background_key(self.data, old) != background_key(self.data, new)
        self.page_id = old
        self._message(engine, "leavepage", Ref("page", "this", None, None))
        if changed:
            self._message(engine, "leavebackground", Ref("background", "page", old, None))
        self.page_id = new
        if changed:
            self._message(engine, "enterbackground", Ref("background", "page", new, None))
        self._message(engine, "enterpage", Ref("page", "this", None, None))

    def _message(self, engine: Engine, name: str, target: Ref) -> None:
        try:
            engine.send(name, (), target)
        except ScriptError as exc:
            engine.errors.append(f"{name}: {exc}")

    # objects --------------------------------------------------------------

    def _listing(self, page: str):
        if page not in self._listed:
            from opentoolbook.show import show_page

            try:
                self._listed[page] = show_page(self.data, page, 1, 1).items
            except ValueError:
                self._listed[page] = ()
        return self._listed[page]

    def _objects(self, page: str, layer: str | None = None) -> set:
        """``(kind, lower-case name)`` of the named objects on ``page``."""
        return {
            (item.kind, item.name.lower())
            for item in self._listing(page)
            if item.name and (layer is None or item.layer == layer)
        }

    def _locate(self, ref: object):
        """``(owner, page, kind, lower-case name, stored item)`` of an object reference, or None."""
        if not isinstance(ref, Ref) or ref.by not in {"name", "id"} or ref.kind in {"page", "book", "background"}:
            return None
        container = ref.of
        layer = None
        if container is None or (isinstance(container, Ref) and container.kind == "page"):
            page = self.page_id if container is None else self._page_id(container)
        elif isinstance(container, Ref) and container.kind == "background" and container.by == "page":
            page, layer = text(container.value), "background"
        else:
            return None
        if page is None:
            return None
        if ref.by == "id":
            # An object by id is kept under its name when it has one, else under the id.
            wanted = int(as_number(ref.value))
            item = next(
                (
                    item
                    for item in self._listing(page)
                    if item.kind == ref.kind and item.object_id == wanted and (layer is None or item.layer == layer)
                ),
                None,
            )
            name = item.name.lower() if item is not None and item.name else wanted
        else:
            name = text(ref.value).lower()
            item = next(
                (
                    item
                    for item in self._listing(page)
                    if item.kind == ref.kind and item.name.lower() == name and (layer is None or item.layer == layer)
                ),
                None,
            )
        if item is not None:
            layer = item.layer
        owner = self._background(page) if layer == "background" else page
        return owner, page, ref.kind, name, item

    def _background(self, page: str) -> str:
        from opentoolbook.show import background_key

        return background_key(self.data, page)

    def _read(self, owner: str, kind: str, name: str, prop: str):
        values = self.state.get(owner, {}).get((kind, name), {})
        return (True, values[prop]) if prop in values else (False, None)

    def _write(self, ref: object, prop: str, value: object) -> bool:
        found = self._locate(ref)
        if found is None:
            return False
        owner, _page, kind, name, _item = found
        self.state.setdefault(owner, {}).setdefault((kind, name), {})[prop] = value
        self.writes.append((owner, kind, name, prop, value))
        return True

    # properties -----------------------------------------------------------

    def property(self, name: str, of: object):
        if isinstance(of, Ref):
            if name == "object":
                return True, of.kind
            if name == "parent":
                if of.kind == "page":
                    page = self._page_id(of)
                    return True, Ref("background", "page", page or "", None)
                if of.kind != "page" and self.groups and of.of is None and of.by == "name":
                    return True, Ref("group", "name", self.groups[0], None)
                return True, Ref("page", "this", None, None)
            if of.kind == "page":
                return self._page_property(name, of)
            if of.kind == "book" and of.by == "this" and name == "pagecount":
                return True, len(self.pages)
            if of.kind == "book" and of.by == "this":
                stored, value = self._read("book", "book", "", name)
                if stored:
                    return True, value
                found = self._book_properties().get(name)
                if found is not None:
                    return True, found
            found = self._locate(of)
            if found is not None:
                owner, page, kind, key, item = found
                stored, value = self._read(owner, kind, key, name)
                if stored:
                    return True, value
                if name == "name":
                    return True, text(of.value)
                if name == "text" and kind in {"field", "recordfield"}:
                    if page.lower() == (self.page_id or "").lower() and key in self.fields:
                        return True, self.fields[key]
                    return True, (item.text or "") if item is not None else ""
                if name == "checked" and kind == "button":
                    return True, self._stored_bit("checked", page, text(of.value), item)
                if name == "enabled" and kind == "button":
                    return True, self._stored_bit("enabled", page, text(of.value), item)
                if name == "visible":
                    return True, item is not None
            if name == "name" and of.by == "name":
                return True, text(of.value)
        return super().property(name, of)

    def _book_properties(self) -> dict:
        """The user properties the book stores, by lower-case name."""
        if "book properties" not in self._maps:
            from opentoolbook.userprops import book_properties

            self._maps["book properties"] = book_properties(self.data) if self.data else {}
        return self._maps["book properties"]

    def _stored_bit(self, name: str, page: str, button: str, item) -> bool:
        if item is not None:
            if name == "enabled":
                return item.enabled
        from opentoolbook.bitmap import button_checked, button_enabled

        read = button_checked if name == "checked" else button_enabled
        try:
            return bool(read(self.data, page, button))
        except ValueError:
            return name == "enabled"

    def _page_id(self, ref: Ref) -> str | None:
        if ref.by == "this":
            return self.page_id
        value = ref.value
        numbered = number(value) if not isinstance(value, str) or text(value).strip().isdigit() else None
        if ref.by == "id" or numbered is not None:
            index = int(numbered if numbered is not None else as_number(value))
            return self.pages[index - 1] if 1 <= index <= len(self.pages) else None
        wanted = text(value).lower()
        return next((page for page in self.pages if page.lower() == wanted), None)

    def _page_property(self, name: str, ref: Ref):
        page = self._page_id(ref)
        if page is None:
            return False, None
        if name == "name":
            return True, page
        if name == "pagenumber":
            return True, [item.lower() for item in self.pages].index(page.lower()) + 1
        if self._page_props is None:
            from opentoolbook.quiz import page_properties

            self._page_props = {
                key.lower(): {k.lower(): v for k, v in value.items()} for key, value in page_properties(self.data).items()
            }
        values = self._page_props.get(page.lower(), {})
        if name in values:
            return True, values[name]
        # A user property the page does not have is null.
        return True, ""

    def set_property(self, name: str, of: object, value: object) -> bool:
        if name == "invert" and isinstance(of, Ref) and of.kind == "button" and of.by == "name":
            self.inverts.append((text(of.value), _on(value)))
            return True
        if name in {"checked", "enabled", "visible"}:
            value = _on(value)
        elif name == "text":
            value = text(value)
        if isinstance(of, Ref) and of.kind == "book" and of.by == "this" and name.startswith("_"):
            # A user property of this book stays set while the book is open.
            self.state.setdefault("book", {}).setdefault(("book", ""), {})[name] = value
            self.writes.append(("book", "book", "", name, value))
            return True
        return self._write(of, name, value)

    def command(self, engine: Engine, name: str, args: tuple):
        if name in {"hide", "show"} and args and isinstance(args[0], Ref):
            self._write(args[0], "visible", name == "show")
            return True, None
        if name in {"next", "previous"}:
            self.go(Ref("page", name, None, None))
            return True, None
        if name == "exit":
            # No ``to handle exit`` in the chain: close the reader window.
            self.exited = True
            return True, None
        return False, None

    def function(self, engine: Engine, name: str, args: tuple):
        if name == "isobject":
            ref = args[0] if args else None
            if not isinstance(ref, Ref):
                return True, False
            if ref.by == "this":
                return True, True
            if ref.kind == "page" and ref.of is None:
                return True, self._page_id(ref) is not None
            found = self._locate(ref)
            return True, found is not None and found[4] is not None
        return False, None

    def request(self, prompt: str, buttons: tuple[str, ...]) -> str:
        """The window's answer when it has an ``ask``; otherwise the prompt is returned to show later."""
        if self.ask is not None:
            return self.ask(prompt, buttons)
        self.asked.append(prompt)
        return ""

    def beep(self) -> None:
        self.beeps += 1


def send_click(
    data: bytes,
    page_id: str,
    pages: tuple[str, ...],
    book_file: str,
    roots: tuple[Path, ...],
    chain_books,
    button: tuple[str, str] | None,
    *,
    props=None,
    variables: dict | None = None,
    sysbooks: list | None = None,
    fields: dict | None = None,
    present: set | None = None,
    message: str = "buttonclick",
    groups: tuple[str, ...] = (),
    beyond_page: bool = True,
    state: dict | None = None,
    ask=None,
    to: Ref | None = None,
    args: tuple = (),
) -> Follow | None:
    """Send ``message`` to ``button`` (kind, name), or to the page when None.

    ``chain_books`` is the list of handler maps after the background: the
    book's, then each ``sysBooks`` book's. ``beyond_page`` False stops the
    path at the page. ``state`` is the properties earlier clicks set in
    this book, as ``ClickHost`` keeps them; it is not changed here. The
    result's ``writes`` are this click's. ``to`` sends the message to that
    reference instead, such as the book or a page's background. ``args``
    are the message arguments (for example the character of ``keyChar``).
    Returns None when no handler on the path takes the message.
    """
    if not beyond_page:
        chain_books = []

    def lookup(kind: str, name: str) -> list:
        key = f"{kind} {name}"
        found = []
        for handlers in chain_books:
            source = handlers.get(name)
            if source is None:
                continue
            handler = parsed(source).handlers.get(key)
            if handler is not None:
                found.append(handler)
        return found

    working = {owner: {key: dict(values) for key, values in objects.items()} for owner, objects in (state or {}).items()}
    host = ClickHost(pages, book_file, roots, page_id, fields, present or set(), data, groups, working)
    host.ask = ask
    if to is not None:
        target = to
    elif button is not None:
        target = Ref(button[0], "name", button[1], None)
    else:
        target = Ref("page", "this", None, None)
    if not host.route("handle", message, target, lookup):
        return None
    engine = Engine(lookup, host, props=props, variables=variables, sysbooks=sysbooks)
    host.engine = engine
    try:
        engine.send(message, args, target)
    except ScriptError as exc:
        engine.errors.append(str(exc))
    page = host.page_id or page_id
    return Follow(
        page,
        host.book_name,
        tuple(host.asked),
        host.beeps,
        inverts=tuple(host.inverts),
        writes=tuple(host.writes),
        exited=host.exited,
    )
