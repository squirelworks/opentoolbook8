"""A click, run on the OpenScript interpreter.

ToolBook sends ``buttonClick`` to the object under the pointer. The
message goes up the object hierarchy until a handler takes it: the
object, each group that holds it, innermost first, its page, the
page's background, the book, then each
``sysBooks`` book. ``target`` is the clicked object for every handler on
the way. ``forward`` passes the message one step up.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path

from opentoolbook.click import Follow, background_script
from opentoolbook.enter import page_source
from opentoolbook.openscript.interp import Engine, Ref
from opentoolbook.openscript.values import ScriptError, as_number, number, text
from opentoolbook.run import BookHost, parsed

# Object script classes: a button is 9, a field 0xA, a group 0xB.
_KIND = {9: "button", 0xA: "field", 0xB: "group", 0x17: "hotword"}


def _object_source(data: bytes, page_id: str, kind: str, name: str) -> str:
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


@dataclass
class ClickHost(BookHost):
    """The page on screen as the click's handlers see it."""

    fields: dict = field(default_factory=dict)
    written: list = field(default_factory=list)
    visible: list = field(default_factory=list)
    present: set = field(default_factory=set)
    asked: list = field(default_factory=list)
    inverts: list = field(default_factory=list)
    beeps: int = 0

    def __init__(self, pages, book_file, roots, page_id, fields, present, data=b"", groups=(), checked=None):
        super().__init__(pages, book_file, roots)
        self.data = data
        # The groups that hold the clicked object, innermost first.
        self.groups = tuple(groups)
        # checked of button, by lower-case name, as clicks on this page set it.
        self.checked = {name.lower(): on for name, on in (checked or {}).items()}
        self.checks: list = []
        self._page_props: dict | None = None
        self.page_id = page_id
        self.start_page = page_id
        self.fields = {name.lower(): value for name, value in (fields or {}).items()}
        self.written = []
        self.visible = []
        self.present = present
        self.asked = []
        self.inverts = []
        self.beeps = 0

    def _field_name(self, of: object) -> str | None:
        if isinstance(of, Ref) and of.kind in {"field", "recordfield"} and of.by == "name":
            return text(of.value)
        return None

    def property(self, name: str, of: object):
        found = self._field_name(of)
        if name == "text" and found is not None:
            return True, self.fields.get(found.lower(), "")
        if isinstance(of, Ref):
            if name == "object":
                return True, of.kind
            if name == "parent":
                if of.kind != "page" and self.groups and of.of is None:
                    return True, Ref("group", "name", self.groups[0], None)
                return True, Ref("page", "this", None, None)
            if of.kind == "page":
                return self._page_property(name, of)
            if of.kind == "book" and of.by == "this" and name == "pagecount":
                return True, len(self.pages)
            if name == "name" and of.by == "name":
                return True, text(of.value)
            if of.kind == "button" and of.by == "name" and name in {"checked", "enabled"}:
                return True, self._button_bit(name, text(of.value))
        return super().property(name, of)

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

    def _objects(self, page: str) -> set:
        """``(kind, lower-case name)`` of the named objects on ``page``."""
        if page.lower() == (self.page_id or "").lower() and self.present:
            return self.present
        from opentoolbook.show import show_page

        listed = show_page(self.data, page, 1, 1, None)
        return {(item.kind, item.name.lower()) for item in listed.items if item.name}

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

            self._page_props = {key.lower(): {k.lower(): v for k, v in value.items()} for key, value in page_properties(self.data).items()}
        values = self._page_props.get(page.lower(), {})
        if name in values:
            return True, values[name]
        # A user property the page does not have is null.
        return True, ""

    def _button_bit(self, name: str, button: str) -> bool:
        from opentoolbook.bitmap import button_checked, button_enabled

        if name == "checked" and button.lower() in self.checked:
            return self.checked[button.lower()]
        read = button_checked if name == "checked" else button_enabled
        try:
            return bool(read(self.data, self.page_id, button))
        except ValueError:
            return name == "enabled"

    def set_property(self, name: str, of: object, value: object) -> bool:
        found = self._field_name(of)
        if name == "text" and found is not None:
            self.fields[found.lower()] = text(value)
            self.written.append((found, text(value)))
            return True
        if name == "checked" and isinstance(of, Ref) and of.kind == "button" and of.by == "name":
            on = value is True or text(value).lower() == "true"
            page = self._page_id(of.of) if isinstance(of.of, Ref) and of.of.kind == "page" else self.page_id
            if page is None:
                return False
            if page.lower() == (self.page_id or "").lower():
                self.checked[text(of.value).lower()] = on
            self.checks.append((page, text(of.value).lower(), on))
            return True
        if name == "invert" and isinstance(of, Ref) and of.kind == "button" and of.by == "name":
            self.inverts.append((text(of.value), value is True or text(value).lower() == "true"))
            return True
        if name == "visible" and isinstance(of, Ref):
            self._show(of, value is True or text(value).lower() == "true")
            return True
        return False

    def _show(self, ref: Ref, shown: bool) -> None:
        key = int(text(ref.value)) if ref.by == "id" else text(ref.value).lower()
        self.visible.append(((ref.kind, key), shown))

    def command(self, engine: Engine, name: str, args: tuple):
        if name in {"hide", "show"} and args and isinstance(args[0], Ref):
            self._show(args[0], name == "show")
            return True, None
        if name in {"next", "previous"}:
            self.go(Ref("page", name, None, None))
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
                if ref.by == "id":
                    return True, False
                return True, text(ref.value).lower() in {page.lower() for page in self.pages}
            if isinstance(ref.of, Ref) and ref.of.kind == "page":
                page = self._page_id(ref.of)
                return True, page is not None and (ref.kind, text(ref.value).lower()) in self._objects(page)
            if ref.of is not None:
                return True, False
            key = text(ref.value).lower()
            return True, (ref.kind, key) in self.present
        return False, None

    def request(self, prompt: str, buttons: tuple[str, ...]) -> str:
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
    checked: dict | None = None,
) -> Follow | None:
    """Send ``message`` to ``button`` (kind, name), or to the page when None.

    ``chain_books`` is the list of handler maps after the background: the
    book's, then each ``sysBooks`` book's. ``beyond_page`` False stops the
    path at the page. Returns None when no handler on the path takes the
    message.
    """
    path_scripts = []
    if button is not None:
        path_scripts.append(_object_source(data, page_id, button[0], button[1]))
        path_scripts.extend(_object_source(data, page_id, "group", name) for name in groups)
    path_scripts.append(page_source(data, page_id))
    if beyond_page:
        path_scripts.append(background_script(data, page_id))
    else:
        chain_books = []
    path = [parsed(source).handlers for source in path_scripts if source]

    def lookup(kind: str, name: str) -> list:
        key = f"{kind} {name}"
        found = [handlers[key] for handlers in path if key in handlers]
        for handlers in chain_books:
            source = handlers.get(name)
            if source is None:
                continue
            handler = parsed(source).handlers.get(key)
            if handler is not None:
                found.append(handler)
        return found

    if not lookup("handle", message):
        return None
    host = ClickHost(pages, book_file, roots, page_id, fields, present or set(), data, groups, checked)
    engine = Engine(lookup, host, props=props, variables=variables, sysbooks=sysbooks)
    host.engine = engine
    target = Ref(button[0], "name", button[1], None) if button is not None else Ref("page", "this", None, None)
    try:
        engine.send(message, (), target)
    except ScriptError as exc:
        engine.errors.append(str(exc))
    page = host.page_id or page_id
    return Follow(
        page,
        host.book_name,
        tuple(host.asked),
        host.beeps,
        tuple(host.written),
        tuple(host.visible),
        tuple(host.inverts),
        tuple(host.checks),
    )
