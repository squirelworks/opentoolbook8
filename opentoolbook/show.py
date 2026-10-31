"""A page, drawn from the readers.

One page unit is one twentieth of a point. One point is 96/72 pixels at
96 dpi. The fit scale multiplies that pixel size once. Pattern 254 is a
solid fill and pattern 253 is no fill. Another pattern byte is not drawn
as a hatch. A draw object's fill is the color at ``+0x1B`` and its stroke
is the color at ``+0x17``, drawn at the width the line-style byte at
``+0x22`` names: 4, 5, 6, and 9 are 1, 2, 3, and 8 pixels, and 1 is no
stroke. A button draws the picture at byte ``0x15`` of
its graphics block, or the picture at byte ``0x4B`` when the button is
checked. A button whose enabled bit, bit 0 of ``+0x26``, is 0 draws the
picture at byte ``0x39`` when that word is not 0. The border byte at
``+0x27`` is a frame in the stroke color at ``+0x17``: ``pushButton`` (7)
frames the bounds, ``radioButton3d`` (9) frames a box one pixel inside
them, and ``none`` (1) draws no frame. A letter click on a quiz page
checks that letter and unchecks the other letters, and the page is drawn
again with those states. A click on a field's hotword run is a click on
that hotword. While a button is held down it draws the
picture at byte ``0x27`` of its graphics block when that word is not 0,
and letting go draws the up picture again. A field's text is drawn at
the character height of each style run's font-table entry.
A field that
contains a shape is painted under that shape. A label that contains no
shape is painted in front of a shape that contains the label.

The page walk names classes ``0x8``, ``0x9``, ``0xA``, ``0xB``, ``0xC``,
``0xD``, ``0xE``, ``0x10``, ``0x11``, ``0x13``, ``0x15``, and ``0x19``.
Of those, the window paints rectangles, ellipses, lines, class ``0x10``
polygons, class ``0x13`` angled lines, fields, buttons, class ``0x15``
paint objects, and class ``0x19`` pictures, plus the class 4 background.
An angled line is its stored points, stroked in the color at ``+0x17``
and not filled. A class ``0xD`` record stores its bounds and colors
where class ``0x8`` does, and the window paints it as those bounds. A
paint object is its stored bitmap drawn at the left and top of its
bounds. A picture is its packed metafile drawn into its bounds, clear
where the metafile leaves the page showing. It does not paint arcs
(``0x11``). A page's and a background's objects paint in the order of their
class ``0x06`` layer list. A group is not a paint; its children are. Class
``0x12`` pies are on the walk and are not painted. Class ``0x17`` hotwords
are on the walk under their field and are not painted a second time.
"""

from __future__ import annotations

import struct
from collections.abc import Mapping
from dataclasses import dataclass, replace

from opentoolbook.background import background
from opentoolbook.bitmap import _graphic_word
from opentoolbook.field import (
    _book,
    _chars,
    _cstring,
    _field_text,
    _name_table,
    _page_handles,
    page_ids,
    _segments,
    _style_runs,
    _trailer,
    _u16,
)
from opentoolbook.page import HOTWORD, _child_nears, _object_name, _objects, layer_nears
from opentoolbook.paintobject import paint_object_rgb
from opentoolbook.picture import picture_pixels
from opentoolbook.props import UserProperties
from opentoolbook.pixels import picture_rgb
from opentoolbook.polyline import _read as _polyline
from opentoolbook.size import page_size

# One page unit is 1/20 point. One point is 96/72 pixels at 96 dpi.
UNIT_PER_POINT = 20
PIXELS_PER_POINT = 96 / 72

NO_FILL = 253

_RECTANGLE = 0x8
_BUTTON = 0x9
HOTWORD_BYTES = 17
# Button border byte +0x27.
PUSH_BUTTON = 7
RADIO_BUTTON_3D = 9
# One pixel at 96 dpi is 15 page units. The radioButton3d frame is that
# far inside the bounds. No byte stores the inset.
_RADIO_INSET = 15
_FIELD = 0xA
_GROUP = 0xB
_ELLIPSE = 0xC
_CLASS_D = 0xD
_LINE = 0xE
_POLYGON = 0x10
_ANGLED = 0x13
_PAINT_OBJECT = 0x15
_PICTURE = 0x19
_SHAPE = {_RECTANGLE, _ELLIPSE, _LINE, _POLYGON}
_DRAW = {
    _RECTANGLE: "rectangle",
    _ELLIPSE: "ellipse",
    _LINE: "line",
    _POLYGON: "polygon",
    _BUTTON: "button",
    _FIELD: "field",
}


@dataclass(frozen=True)
class Paint:
    """One thing the window draws, in page units."""

    kind: str
    object_id: int | None = None
    name: str = ""
    bounds: tuple[int, int, int, int] | None = None
    fill: tuple[int, int, int] | None = None
    stroke: tuple[int, int, int] | None = None
    pattern: int | None = None
    points: tuple[tuple[int, int], ...] = ()
    text: str | None = None
    runs: tuple[tuple[int, str | None], ...] = ()
    picture_id: int | None = None
    picture_role: str | None = None
    picture: tuple[int, int, bytes] | None = None
    mask: bytes | None = None
    frame: tuple[int, int, int, int] | None = None
    up_id: int | None = None
    checked_id: int | None = None
    invert_id: int | None = None
    hotwords: tuple[tuple[int, int, str], ...] = ()
    sizes: tuple[tuple[int, int | None], ...] = ()

    width: int = 1


@dataclass(frozen=True)
class DisplayList:
    """The page, the fit scale, and the paint list."""

    page_id: str
    width: int
    height: int
    view_width: int
    view_height: int
    scale: float
    items: tuple[Paint, ...]


def unit_to_px(unit: float, scale: float) -> float:
    """Page units to device pixels. ``scale`` is applied once."""
    return unit * (1 / UNIT_PER_POINT) * PIXELS_PER_POINT * scale


def fit_scale(width: int, height: int, view_width: int, view_height: int) -> float:
    """The scale that fits the page in the view. It is 1 when the view is the page."""
    page_w = unit_to_px(width, 1)
    page_h = unit_to_px(height, 1)
    if page_w <= 0 or page_h <= 0 or view_width <= 0 or view_height <= 0:
        return 1
    return min(view_width / page_w, view_height / page_h)


def show_page(
    data: bytes,
    page_id: str,
    view_width: int,
    view_height: int,
    props: UserProperties | None = None,
    fields: dict[str, str] | None = None,
    visible: dict[tuple[str, str | int], bool] | None = None,
    *,
    sys_level: str | None = None,
    checked: Mapping[str, bool] | None = None,
    correct: bool = False,
) -> DisplayList:
    """The display list for one page. It does not open a window.

    ``props`` holds the ``__`` names the page's ``enterPage`` reads.
    ``fields`` is field text a handler wrote after ``enterPage``.
    ``visible`` maps ``(kind, name or id)`` to whether a handler shows it.
    An object a handler hid is not on the list.
    ``sys_level`` ``None`` is missing, and a missing ``sysLevel`` is ``reader``.
    ``checked`` maps a button name, in any case, to the checked state a
    click gave it. It wins over bit 4 of that button's ``+0x26``.
    The rectangle named ``Correct`` is the answer mark. It is on the list
    only when ``correct`` is True, which is when ``setupQuizPage`` ran
    ``set visible of rectangle("correct") of page iPage to true`` for
    this page.
    """
    width, height = page_size(data)
    scale = fit_scale(width, height, view_width, view_height)
    items = _entered(data, page_id, _ordered(_stored(data, page_id, width, height)), props, sys_level)
    if not correct:
        items = tuple(item for item in items if not _answer_mark(item))
    if fields:
        items = _written(items, fields)
    if checked:
        items = _checked(data, items, checked)
    if visible:
        items = tuple(item for item in items if _shown(item, visible))
    return DisplayList(page_id, width, height, view_width, view_height, scale, items)


def refit(listed: DisplayList, view_width: int, view_height: int) -> DisplayList:
    """The same display list in a view of another size. Only the scale changes."""
    scale = fit_scale(listed.width, listed.height, view_width, view_height)
    return replace(listed, view_width=view_width, view_height=view_height, scale=scale)


def open_page(
    data: bytes,
    page_id: str,
    book: str | None = None,
    home: str | None = None,
    props: UserProperties | None = None,
    *,
    status: str | None = None,
    lesson: str | None = None,
    variables: dict[str, object] | None = None,
) -> tuple[str, ...]:
    """Open a Tk window on the page id given, at 96 dpi, fitted once.

    The page id is the one the caller passed. This function does not
    follow startup handlers. A button whose handler quotes a page opens
    that page. A quoted book is found with the same search as opening a
    book: the directory of ``book``, its parent, ``home``,
    ``home/courses``, and ``home/Nida98/Lessons``, regardless of case. A
    book that search does not find is reported on stderr with the file
    and the page, and the window stays. A quiz page with no quiz running
    still uses OK, Next, and Skip for the next page and Back for the
    previous page. The Right key runs the page's ``Next`` button and the
    Left key its ``Back`` button. Enter runs the branch the book's
    ``keyUp`` handler quotes for ``keyEnter``. Escape closes the window. ``props`` is the ``__`` store every page in
    this window reads. Resizing the window refits the page: the
    scale is computed again from the page size and the new view. The
    close button ends the Tk loop and this
    function returns. A click that raises prints the error and the window
    stays up. ``status`` is one line shown once under the page, such as
    ``MINSTB32.dll named, not shipped``. It does not stop the paint.
    ``lesson`` is the path the user passed when the window opens on
    another book. A click still searches beside it.
    ``variables`` are the system variables startup assigned.
    The window's own "Viewer back" control returns to the page it showed
    before, which is not the book's stored previous page. The title is the
    book file and the page id, and it changes on every navigation,
    including a book switch. The return is every click error the window printed,
    in order, so the caller can exit non-zero.
    """
    import tkinter as tk

    from opentoolbook.navigate import Navigator

    root = tk.Tk()
    try:
        root.update_idletasks()
        width, height = page_size(data)
        view_w = max(1, min(_pixels(width), root.winfo_screenwidth() - 48))
        view_h = max(1, min(_pixels(height), root.winfo_screenheight() - 96))
        root.title("")
        canvas = tk.Canvas(
            root,
            width=view_w,
            height=view_h,
            highlightthickness=0,
            background="#ffffff",
        )
        if status:
            tk.Label(root, text=status, anchor="w").pack(side="bottom", fill="x")
        state = {
            "props": props if props is not None else UserProperties(),
            "view": (view_w, view_h),
        }
        nav = Navigator(data, page_id, book, home, lesson, variables, state["props"])
        root.title(nav.title())
        errors: list[str] = []

        def on_back() -> None:
            if nav.back():
                redraw()
            else:
                root.bell()

        bar = tk.Frame(root)
        bar.pack(fill="x")
        # A viewer control, not a book button: it pops the pages this window showed.
        tk.Button(bar, text="\u25c0 Viewer back", command=on_back).pack(side="left")
        canvas.pack(fill="both", expand=True)

        def redraw() -> None:
            listed = nav.display(*state["view"], state["props"])
            paint(listed)

        def paint(listed: DisplayList) -> None:
            canvas.delete("all")
            draw_page(canvas, listed)
            canvas.listed = listed
            root.title(nav.title())

        def on_configure(event) -> None:
            view = (max(1, event.width), max(1, event.height))
            if view == state["view"]:
                return
            state["view"] = view
            listed = getattr(canvas, "listed", None)
            if listed is None:
                return
            paint(refit(listed, *view))

        def on_press(event) -> None:
            listed = getattr(canvas, "listed", None)
            if listed is None:
                return
            name = hotword_hit(canvas, event.x, event.y) or button_at(listed, event.x, event.y)
            state["pressed"] = name
            if not name:
                return
            held = pressed(nav.data, listed, name)
            if held != listed:
                canvas.delete("all")
                draw_page(canvas, held)

        def on_click(event) -> None:
            listed = getattr(canvas, "listed", None)
            if listed is None:
                return
            name = state.pop("pressed", None)
            if name:
                canvas.delete("all")
                draw_page(canvas, listed)
            if (hotword_hit(canvas, event.x, event.y) or button_at(listed, event.x, event.y)) != name:
                return
            result = click_reported(nav, name, errors, shown=field_texts(listed))
            if result is None:
                root.bell()
                return
            if result.beep:
                root.bell()
            for text in result.requests:
                from tkinter import messagebox

                messagebox.showinfo(nav.book_name or "ToolBook", text, parent=root)
            if result.moved or result.changed or result.checked:
                redraw()

        def on_key(event) -> None:
            listed = getattr(canvas, "listed", None)
            if listed is None:
                return
            try:
                result = press_key(nav, listed, event.keysym)
            except ValueError as exc:
                import sys

                print(exc, file=sys.stderr)
                errors.append(str(exc))
                root.bell()
                return
            if result is None:
                return
            if result.beep:
                root.bell()
            if result.moved or result.changed or result.checked:
                redraw()

        canvas.bind("<ButtonPress-1>", on_press)
        canvas.bind("<ButtonRelease-1>", on_click)
        root.bind("<Right>", on_key)
        root.bind("<Left>", on_key)
        root.bind("<Return>", on_key)
        root.bind("<KP_Enter>", on_key)
        root.bind("<Escape>", lambda _event: root.quit())
        canvas.bind("<Configure>", on_configure)
        root.protocol("WM_DELETE_WINDOW", root.quit)
        root.report_callback_exception = _report_click_error
        redraw()
        root.mainloop()
        return tuple(errors)
    finally:
        try:
            root.destroy()
        except tk.TclError:
            pass


def _report_click_error(kind, value, trace) -> None:
    """A click that raises prints its message and leaves the window up.

    A ``ValueError`` or ``OSError`` is the reader's own error, one line on
    stderr. Anything else is a bug and keeps its traceback.
    """
    import sys
    import traceback

    if isinstance(value, (ValueError, OSError)):
        print(value, file=sys.stderr)
        return
    traceback.print_exception(kind, value, trace, file=sys.stderr)


def click_reported(nav, name: str | None, errors: list[str], stream=None, shown=None):
    """Run one click. A reader error prints its one line and returns None.

    The line is the same sentence the open prints, for example
    ``nida81.tbk was not found; P310 of that book does not open``. The
    page and book stay where they were. ``shown`` is the field text the
    page shows now.
    """
    import sys

    try:
        return nav.click(name, shown)
    except ValueError as exc:
        print(exc, file=stream if stream is not None else sys.stderr)
        errors.append(str(exc))
        return None


# Right is the button named Next. Left is the button named Back.
KEY_BUTTONS = {"Right": "next", "Left": "back"}


def key_button(listed: DisplayList, key: str) -> str | None:
    """The button a key presses on this page, as the page names it, or None."""
    wanted = KEY_BUTTONS.get(key)
    if wanted is None:
        return None
    for item in listed.items:
        if item.kind == "button" and item.name.lower() == wanted:
            return item.name
    return None


def press_key(nav, listed: DisplayList, key: str):
    """Run the click of the button ``key`` presses. None when the page has no such button.

    Right and Left are the viewer's keys. Another key runs only when the
    book's ``keyUp`` handler quotes it and that branch sends ``buttonClick``
    to a button this page has.
    """
    name = key_button(listed, key)
    if name is None:
        name = _book_key_button(nav, listed, key)
    if name is None:
        return None
    return nav.click(name)


def _book_key_button(nav, listed: DisplayList, key: str) -> str | None:
    from opentoolbook.keys import key_handler

    handler = key_handler(nav.data, nav.page_id, key)
    if handler is None or handler.button is None:
        return None
    wanted = handler.button.lower()
    for item in listed.items:
        if item.kind == "button" and item.name.lower() == wanted:
            return item.name
    return None


def button_at(listed: DisplayList, x: float, y: float) -> str | None:
    """The topmost button whose device bounds contain the point."""
    for item in reversed(listed.items):
        if item.kind != "button" or item.bounds is None or not item.name:
            continue
        left, top, right, bottom = (unit_to_px(value, listed.scale) for value in item.bounds)
        if left <= x < right and top <= y < bottom:
            return item.name
    return None


def pressed(data: bytes, listed: DisplayList, name: str) -> DisplayList:
    """The display list while the named button is held down.

    A button with an invert picture draws it. A button without one, and
    every other item, is unchanged. Letting go is the list without this
    call, so the up picture comes back.
    """
    items = []
    for item in listed.items:
        if item.kind == "button" and item.name == name and item.invert_id:
            try:
                picture = picture_rgb(data, item.invert_id)
            except ValueError:
                picture = None
            if picture is not None:
                item = replace(item, picture_id=item.invert_id, picture_role="invert", picture=picture)
        items.append(item)
    return replace(listed, items=tuple(items))


def draw_page(canvas, listed: DisplayList, make_photo=None) -> None:
    """Paint a display list onto a Tk canvas. Photos stay referenced by the canvas.

    The photos of the page drawn before are deleted first, so a window
    holds the images of one page at a time. ``make_photo`` builds one
    image from PPM bytes; it is ``tkinter.PhotoImage`` when not given.
    """
    release_photos(canvas)
    photos: list = []
    canvas.photos = photos
    canvas.spans = {}
    for item in listed.items:
        _draw_item(canvas, listed.scale, item, photos, make_photo)


def release_photos(canvas) -> int:
    """Delete the images the canvas holds from its last page. Returns how many."""
    old = getattr(canvas, "photos", None) or []
    for photo in old:
        delete = getattr(photo, "delete", None)
        if delete is not None:
            delete()
            continue
        try:
            photo.tk.call("image", "delete", photo.name)
        except Exception:
            # Already gone with its interpreter.
            pass
    count = len(old)
    canvas.photos = []
    return count


def _pixels(units: int) -> int:
    return max(1, round(unit_to_px(units, 1)))


def _entered(
    data: bytes,
    page_id: str,
    items: tuple[Paint, ...],
    props: UserProperties | None = None,
    sys_level: str | None = None,
) -> tuple[Paint, ...]:
    """Run the page's enterPage text. A missing sysLevel is reader."""
    from opentoolbook.enter import cover_style, enter_fields

    indexes = [index for index, item in enumerate(items) if item.kind == "field"]
    packed = tuple((items[index].name, items[index].text or "", items[index].runs) for index in indexes)
    changed = enter_fields(data, page_id, packed, props=props, sys_level=sys_level)
    if changed == packed:
        return items
    out = list(items)
    for index, (_name, text, runs) in zip(indexes, changed):
        if text != (out[index].text or "") or runs != out[index].runs:
            sizes = cover_style(out[index].text or "", text, out[index].sizes)
            out[index] = replace(out[index], text=text, runs=runs, sizes=sizes)
    return tuple(out)


def field_texts(listed: DisplayList) -> dict[str, str]:
    """Each field name on the display list and the text it shows."""
    return {item.name: item.text or "" for item in listed.items if item.kind == "field" and item.name}


def _shown(item: Paint, visible: dict[tuple[str, str | int], bool]) -> bool:
    for key in ((item.kind, item.name.lower()), (item.kind, item.object_id)):
        if key[1] in ("", None):
            continue
        if visible.get(key) is False:
            return False
    return True


def _written(items: tuple[Paint, ...], fields: dict[str, str]) -> tuple[Paint, ...]:
    from opentoolbook.enter import cover_style

    wanted = {name.lower(): text for name, text in fields.items()}
    out = list(items)
    for index, item in enumerate(out):
        if item.kind != "field" or item.name.lower() not in wanted:
            continue
        text = wanted[item.name.lower()]
        out[index] = replace(item, text=text, runs=cover_style(item.text or "", text, item.runs))
    return tuple(out)


def _answer_mark(item: Paint) -> bool:
    return item.kind == "rectangle" and item.name.lower() == "correct"


def _stored(data: bytes, page_id: str, width: int, height: int) -> list[Paint]:
    segments = _segments(data)
    by_key = {segment.key: segment for segment in segments}
    book_segment, book_record = _book(data, segments)
    base, _table, pointers = _name_table(data)
    known = set(pointers)
    for handle in _page_handles(data, by_key, book_segment, book_record):
        segment = by_key.get(handle >> 16)
        if segment is None:
            continue
        record = segment.base + (handle & 0xFFFF)
        if record < 2 or record + 8 > len(data) or _u16(data, record - 2) != 5:
            continue
        if _chars(data, record + 6, 32) != page_id:
            continue
        paint = background(data, page_id)
        items = [_background(paint, width, height)]
        far = struct.unpack_from("<I", data, record + 0x47)[0]
        owner = by_key.get(far >> 16)
        if owner is not None:
            found = owner.base + (far & 0xFFFF)
            if found >= 2 and found + 8 <= len(data) and _u16(data, found - 2) == 4:
                items.extend(_walk(
                    data,
                    owner,
                    _trailer(data, owner),
                    base,
                    known,
                    found - owner.base,
                ))
        trailer = _trailer(data, segment)
        items.extend(_walk(data, segment, trailer, base, known, record - segment.base))
        return items
    raise ValueError(f"no page {page_id}")


def _background(paint, width: int, height: int) -> Paint:
    fill = (paint.red, paint.green, paint.blue)
    stroke = (paint.second_red, paint.second_green, paint.second_blue)
    if paint.pattern == NO_FILL:
        fill = None
    return Paint(
        "background",
        bounds=(0, 0, width, height),
        fill=fill,
        stroke=stroke,
        pattern=paint.pattern,
    )


def _walk(data, segment, trailer, base: int, known: set[int], parent: int) -> list[Paint]:
    found = _objects(data, segment)
    by_near = {at - segment.base: (at, kind) for at, kind in found}
    items: list[Paint] = []
    for at, kind in _layered(data, segment, trailer, found, parent):
        near = at - segment.base
        if kind == _GROUP:
            for child in _child_nears(data, segment, at):
                items.extend(_child(data, segment, trailer, base, known, by_near, child))
            continue
        painted = _paint(data, segment, trailer, base, known, at, kind)
        if painted is not None:
            items.append(painted)
    return items


def _layered(data, segment, trailer, found, parent: int):
    """The parent's objects in the order of its layer list, else stored order."""
    children = [(at, kind) for at, kind in found if _u16(data, at + 4) == parent]
    layers = layer_nears(data, segment, trailer, parent)
    nears = {at - segment.base for at, _kind in children}
    if not layers or set(layers) != nears:
        return children
    place = {near: index for index, near in enumerate(layers)}
    return sorted(children, key=lambda child: place[child[0] - segment.base])


def _child(data, segment, trailer, base, known, by_near, near: int) -> list[Paint]:
    child = by_near.get(near)
    if child is None:
        return []
    at, kind = child
    if kind == _GROUP:
        found: list[Paint] = []
        for nested in _child_nears(data, segment, at):
            found.extend(_child(data, segment, trailer, base, known, by_near, nested))
        return found
    painted = _paint(data, segment, trailer, base, known, at, kind)
    return [] if painted is None else [painted]


def _paint(data, segment, trailer, base, known, at: int, kind: int) -> Paint | None:
    name = _object_name(data, trailer, at) if trailer is not None else ""
    object_id = _u16(data, at)
    bounds = _bounds(data, at)
    if kind in (_RECTANGLE, _ELLIPSE, _POLYGON):
        fill, stroke, width = _stroked(data, at)
        points = _polygon_points(data, segment, at) if kind == _POLYGON else ()
        return Paint(_DRAW[kind], object_id, name, bounds, fill, stroke, data[at + 0x25], points, width=width)
    if kind == _CLASS_D:
        fill, stroke, width = _stroked(data, at)
        return Paint("class 0xD", object_id, name, bounds, fill, stroke, data[at + 0x25], width=width)
    if kind == _LINE:
        _fill, stroke, width = _stroked(data, at)
        return Paint("line", object_id, name, bounds, None, stroke, None, _line_points(data, at), width=width)
    if kind == _ANGLED:
        _fill, stroke, width = _stroked(data, at)
        try:
            points = _polyline(data, segment, at).points
        except ValueError:
            return None
        return Paint("angled line", object_id, name, bounds, None, stroke, None, points, width=width)
    if kind == _FIELD:
        text, runs = _runs(data, trailer, base, known, at)
        sizes = _sizes(data, trailer, base, known, at)
        hotwords = _hotwords(data, segment, trailer, at, len(text))
        return Paint("field", object_id, name, bounds, text=text, runs=runs, sizes=sizes, hotwords=hotwords)
    if kind == _BUTTON:
        return _button(data, segment, at, object_id, name, bounds)
    if kind == _PAINT_OBJECT:
        try:
            picture = paint_object_rgb(data, segment, at)
        except ValueError:
            return None
        return Paint("paint object", object_id, name, bounds, picture=picture)
    if kind == _PICTURE:
        try:
            drawn = picture_pixels(data, at)
        except ValueError:
            return None
        return Paint(
            "picture",
            object_id,
            name,
            bounds,
            picture=(drawn.width, drawn.height, drawn.rgb),
            mask=drawn.mask,
        )
    return None


def _checked(data: bytes, items: tuple[Paint, ...], checked: Mapping[str, bool]) -> tuple[Paint, ...]:
    """Buttons drawn with the checked state a click set, not the stored bit."""
    wanted = {name.lower(): on for name, on in checked.items()}
    out = list(items)
    for index, item in enumerate(out):
        on = wanted.get(item.name.lower()) if item.kind == "button" else None
        if on is None or item.picture_role == "disabled":
            continue
        if on and item.checked_id:
            picture_id, role = item.checked_id, "checked"
        else:
            picture_id, role = item.up_id, "up" if item.up_id else None
        if picture_id == item.picture_id:
            continue
        out[index] = replace(item, picture_id=picture_id, picture_role=role, picture=_picture(data, picture_id))
    return tuple(out)


def _picture(data: bytes, picture_id: int | None):
    if not picture_id:
        return None
    try:
        return picture_rgb(data, picture_id)
    except ValueError:
        return None


def _button(data, segment, at: int, object_id: int, name: str, bounds) -> Paint:
    up = _graphic_word(data, segment, at, 0x15)
    checked_id = _graphic_word(data, segment, at, 0x4B)
    disabled_id = _graphic_word(data, segment, at, 0x39)
    checked = (data[at + 0x26] >> 4) & 1
    enabled = data[at + 0x26] & 1
    if not enabled and disabled_id:
        picture_id = disabled_id
        role = "disabled"
    elif checked and checked_id:
        picture_id = checked_id
        role = "checked"
    else:
        picture_id = up
        role = "up" if up else None
    picture = _picture(data, picture_id)
    _fill, stroke = _colors(data, at)
    return Paint(
        "button",
        object_id,
        name,
        bounds,
        stroke=stroke,
        picture_id=picture_id,
        picture_role=role,
        picture=picture,
        frame=_frame(data[at + 0x27], bounds),
        up_id=up or None,
        checked_id=checked_id or None,
        invert_id=_graphic_word(data, segment, at, 0x27) or None,
    )


def _frame(border: int, bounds) -> tuple[int, int, int, int] | None:
    """The box a button border draws: the bounds, a smaller box, or none."""
    if bounds is None:
        return None
    left, top, right, bottom = bounds
    if border == PUSH_BUTTON:
        return bounds
    if border == RADIO_BUTTON_3D:
        inset = min(_RADIO_INSET, (right - left) // 2, (bottom - top) // 2)
        return (left + inset, top + inset, right - inset, bottom - inset)
    return None


def _runs(data, trailer, base: int, known: set[int], at: int):
    if trailer is None:
        return "", ()
    pointer = _u16(data, at + 0x24)
    text = _field_text(trailer, pointer)
    runs = []
    for raw in _style_runs(trailer, pointer):
        offset = _u16(raw, 0)
        word = _u16(raw, 2)
        face = None if word == 1 or word not in known else _cstring(data, base + word)
        runs.append((offset, face))
    return text, tuple(runs)


def font_height(data: bytes, base: int, known: set[int], word: int) -> int | None:
    """The character height, in page units, of a font-table entry.

    ``word`` is a near pointer in the list at the book record's ``+0x28``.
    The entry is the face name, then at ``+0x20`` a signed word that is
    minus the character height. None when the word is not in that list.
    """
    if word not in known or base + word + 0x22 > len(data):
        return None
    height = -struct.unpack_from("<h", data, base + word + 0x20)[0]
    return height if height > 0 else None


def _sizes(data, trailer, base: int, known: set[int], at: int) -> tuple[tuple[int, int | None], ...]:
    """Each style run's offset and character height. A run word of 1 is the field's font at ``+0x22``."""
    field = font_height(data, base, known, _u16(data, at + 0x22))
    if trailer is None:
        return ()
    found = []
    for raw in _style_runs(trailer, _u16(data, at + 0x24)):
        word = _u16(raw, 2)
        found.append((_u16(raw, 0), field if word == 1 else font_height(data, base, known, word)))
    if not found:
        return ((0, field),)
    return tuple(found)


def _hotwords(data, segment, trailer, at: int, length: int) -> tuple[tuple[int, int, str], ...]:
    """Each hotword's character range in the field, and its name.

    A style run whose word at byte 4 is the near of a class ``0x17``
    record that names this field starts the hotword. The range runs to
    the next run's offset, or to the end of the text.
    """
    if trailer is None:
        return ()
    near = at - segment.base
    end = segment.file_at + segment.size
    runs = sorted((_u16(raw, 0), _u16(raw, 4)) for raw in _style_runs(trailer, _u16(data, at + 0x24)))
    found = []
    for index, (offset, word) in enumerate(runs):
        hot = segment.base + word
        if word == 0 or hot < 4 or hot + HOTWORD_BYTES > end:
            continue
        if _u16(data, hot - 2) != HOTWORD or _u16(data, hot - 4) - word != HOTWORD_BYTES:
            continue
        if _u16(data, hot + 4) != near:
            continue
        stop = runs[index + 1][0] if index + 1 < len(runs) else length
        found.append((offset, max(offset, stop), _object_name(data, trailer, hot)))
    return tuple(found)


def hotword_at(item: Paint, offset: int) -> str | None:
    """The name of the field's hotword whose range holds ``offset``."""
    for start, stop, name in item.hotwords:
        if start <= offset < stop:
            return name or None
    return None


def hotword_hit(canvas, x: float, y: float) -> str | None:
    """The hotword drawn under a window point, from the spans ``draw_page`` drew."""
    spans = getattr(canvas, "spans", {})
    for found in reversed(canvas.find_overlapping(x, y, x, y)):
        hit = spans.get(found)
        if hit is not None:
            name = hotword_at(*hit)
            if name:
                return name
    return None

# The line-style byte at +0x22 and the export's LineStyle: 1 is none, 2 is
# dotted, and 4, 5, 6, 9 are widths 1, 2, 3, 8. Dotted draws solid at 1.
LINE_NONE = 1
_LINE_WIDTHS = {2: 1, 4: 1, 5: 2, 6: 3, 9: 8}


def line_width(data: bytes, at: int) -> int:
    """The stroke width in pixels. 0 is no stroke. A byte not read yet is 1."""
    style = data[at + 0x22]
    if style == LINE_NONE:
        return 0
    return _LINE_WIDTHS.get(style, 1)


def _stroked(data: bytes, at: int):
    fill, stroke = _colors(data, at)
    return fill, stroke, line_width(data, at)


def _colors(data: bytes, at: int):
    stroke = (data[at + 0x17], data[at + 0x18], data[at + 0x19])
    fill = (data[at + 0x1B], data[at + 0x1C], data[at + 0x1D])
    pattern = data[at + 0x25]
    if pattern == NO_FILL:
        return None, stroke
    return fill, stroke


def _bounds(data: bytes, at: int) -> tuple[int, int, int, int]:
    left, top, right, bottom = struct.unpack_from("<hhhh", data, at + 0x0F)
    return left, top, right, bottom


def _line_points(data: bytes, at: int) -> tuple[tuple[int, int], tuple[int, int]]:
    x1, y1, x2, y2 = struct.unpack_from("<hhhh", data, at + 0x26)
    return ((x1, y1), (x2, y2))


def _polygon_points(data, segment, at: int) -> tuple[tuple[int, int], ...]:
    count = _u16(data, at + 0x30)
    pointer = _u16(data, at + 0x32)
    origin = segment.base + pointer
    end = segment.file_at + segment.size
    if count == 0 or origin < 0 or origin + 4 * count > end:
        return ()
    return tuple(struct.unpack_from("<hh", data, origin + 4 * index) for index in range(count))


def _ordered(items: list[Paint]) -> tuple[Paint, ...]:
    """Fields that contain a shape go under it. Empty labels go in front."""
    guard = 0
    while guard <= len(items) + 1:
        guard += 1
        moved = _raise_shapes(items)
        if moved:
            continue
        if _raise_labels(items):
            continue
        break
    return tuple(items)


def _raise_shapes(items: list[Paint]) -> bool:
    for index, item in enumerate(items):
        if item.kind != "field" or item.bounds is None:
            continue
        inside = [
            pos
            for pos, other in enumerate(items)
            if _is_shape(other) and _contains(item.bounds, _box(other)) and pos < index
        ]
        if not inside:
            continue
        pulled = [items[pos] for pos in inside]
        for pos in reversed(inside):
            del items[pos]
        index = items.index(item)
        for offset, shape in enumerate(pulled):
            items.insert(index + 1 + offset, shape)
        return True
    return False


def _raise_labels(items: list[Paint]) -> bool:
    for index, item in enumerate(items):
        if item.kind != "field" or item.bounds is None:
            continue
        if any(_is_shape(other) and _contains(item.bounds, _box(other)) for other in items):
            continue
        holders = [
            pos
            for pos, other in enumerate(items)
            if _holds_label(other) and _contains(_box(other), item.bounds) and pos > index
        ]
        if not holders:
            continue
        last = max(holders)
        items.pop(index)
        items.insert(last, item)
        return True
    return False


def _is_shape(item: Paint) -> bool:
    return item.kind in {"rectangle", "ellipse", "line", "polygon"} and _box(item) is not None


def _holds_label(item: Paint) -> bool:
    return _is_shape(item) or (item.kind == "button" and _box(item) is not None)


def _box(item: Paint):
    return item.bounds


def _contains(outer, inner) -> bool:
    if outer is None or inner is None:
        return False
    outer_area = max(0, outer[2] - outer[0]) * max(0, outer[3] - outer[1])
    inner_area = max(0, inner[2] - inner[0]) * max(0, inner[3] - inner[1])
    if outer_area <= inner_area:
        return False
    return (
        outer[0] <= inner[0]
        and outer[1] <= inner[1]
        and outer[2] >= inner[2]
        and outer[3] >= inner[3]
    )


def _draw_item(canvas, scale: float, item: Paint, photos: list, make_photo=None) -> None:
    if make_photo is None and item.picture is not None:
        import tkinter as tk

        make_photo = tk.PhotoImage
    if item.kind == "background" and item.fill is not None and item.bounds is not None:
        canvas.create_rectangle(*_device_box(item.bounds, scale), fill=_rgb(item.fill), outline="")
        return
    width = _device_width(item.width, scale)
    outline = _rgb(item.stroke) if item.stroke is not None and item.width else ""
    if item.kind in ("rectangle", "class 0xD") and item.bounds is not None:
        canvas.create_rectangle(
            *_device_box(item.bounds, scale),
            fill=_rgb(item.fill) if item.fill is not None else "",
            outline=outline,
            width=width,
        )
        return
    if item.kind == "ellipse" and item.bounds is not None:
        canvas.create_oval(
            *_device_box(item.bounds, scale),
            fill=_rgb(item.fill) if item.fill is not None else "",
            outline=outline,
            width=width,
        )
        return
    if item.kind in ("line", "angled line") and item.width == 0:
        return
    if item.kind == "line" and len(item.points) == 2:
        flat = [unit_to_px(value, scale) for point in item.points for value in point]
        canvas.create_line(*flat, fill=_rgb(item.stroke) if item.stroke is not None else "#000000", width=width)
        return
    if item.kind == "angled line" and len(item.points) >= 2:
        flat = [unit_to_px(value, scale) for point in item.points for value in point]
        canvas.create_line(*flat, fill=_rgb(item.stroke) if item.stroke is not None else "#000000", width=width)
        return
    if item.kind == "polygon" and len(item.points) >= 2:
        flat = [unit_to_px(value, scale) for point in item.points for value in point]
        canvas.create_polygon(
            *flat,
            fill=_rgb(item.fill) if item.fill is not None else "",
            outline=outline,
            width=width,
        )
        return
    if item.kind in ("button", "paint object") and item.picture is not None and item.bounds is not None:
        width, height, rgb = _scale_rgb(item.picture[0], item.picture[1], item.picture[2], scale)
        photo = make_photo(data=_ppm(width, height, rgb))
        photos.append(photo)
        x = unit_to_px(item.bounds[0], scale)
        y = unit_to_px(item.bounds[1], scale)
        canvas.create_image(x, y, image=photo, anchor="nw")
    if item.kind == "button" and item.frame is not None:
        canvas.create_rectangle(
            *_device_box(item.frame, scale),
            fill="",
            outline=_rgb(item.stroke) if item.stroke is not None else "#000000",
        )
        return
    if item.kind in ("button", "paint object"):
        return
    if item.kind == "picture" and item.picture is not None and item.bounds is not None:
        left, top, right, bottom = _device_box(item.bounds, scale)
        width = max(1, round(right - left))
        height = max(1, round(bottom - top))
        photo = make_photo(data=_png(*_stretch(item.picture, item.mask, width, height)))
        photos.append(photo)
        canvas.create_image(left, top, image=photo, anchor="nw")
        return
    if item.kind == "field" and item.text and item.bounds is not None:
        _draw_text(canvas, scale, item)


def _draw_text(canvas, scale: float, item: Paint) -> None:
    import tkinter.font as tkfont

    shown = item.text.replace("\r\n", "\n").replace("\r", "\n")
    left = unit_to_px(item.bounds[0], scale)
    top = unit_to_px(item.bounds[1], scale)
    width = max(1, unit_to_px(item.bounds[2] - item.bounds[0], scale))
    height = max(1, unit_to_px(item.bounds[3] - item.bounds[1], scale))
    lines = max(1, shown.count("\n") + 1)
    size = max(1, int(height / lines))
    face = next((name for _offset, name in item.runs if name), None) or "TkDefaultFont"
    font = tkfont.Font(family=face, size=-size)
    longest = max((line for line in shown.split("\n")), key=len, default="")
    while size > 1 and font.measure(longest) > width:
        size -= 1
        font.configure(size=-size)
    y = top
    drawn = getattr(canvas, "spans", None)
    for start, stored, span_face in _spans_at(item.text, item.runs):
        text = stored.replace("\r\n", "\n").replace("\r", "\n")
        span_size = _size_at(item.sizes, start, scale) or size
        made = canvas.create_text(
            left,
            y,
            text=text,
            anchor="nw",
            width=width,
            fill="#000000",
            font=(span_face or "TkDefaultFont", -span_size),
        )
        if drawn is not None and item.hotwords:
            drawn[made] = (item, start)
        y += span_size * max(1, text.count("\n") + 1)


def _size_at(sizes, start: int, scale: float) -> int | None:
    """The pixel height of the run that holds stored offset ``start``."""
    height = None
    for offset, stored in sorted(sizes):
        if offset <= start:
            height = stored
    return max(1, round(unit_to_px(height, scale))) if height else None


def _spans(text: str, runs: tuple[tuple[int, str | None], ...]) -> tuple[tuple[str, str | None], ...]:
    return tuple((piece, face) for _start, piece, face in _spans_at(text, runs))


def _spans_at(text: str, runs) -> tuple[tuple[int, str, str | None], ...]:
    """Each run's start offset, its text, and its face."""
    if not runs:
        return ((0, text, None),)
    ordered = tuple(sorted(runs))
    found = []
    for index, (offset, face) in enumerate(ordered):
        end = ordered[index + 1][0] if index + 1 < len(ordered) else len(text)
        if offset < 0 or offset > len(text):
            continue
        found.append((offset, text[offset:max(offset, end)], face))
    return tuple(found) or ((0, text, None),)


def _device_width(width: int, scale: float) -> int:
    """A stored pixel width at the fit scale. At least 1, since Tk draws 0 as 1."""
    return max(1, round(width * scale))


def _device_box(bounds, scale: float) -> tuple[float, float, float, float]:
    left, top, right, bottom = bounds
    return (
        unit_to_px(left, scale),
        unit_to_px(top, scale),
        unit_to_px(right, scale),
        unit_to_px(bottom, scale),
    )


def _rgb(color: tuple[int, int, int]) -> str:
    return "#{:02x}{:02x}{:02x}".format(*color)


def _ppm(width: int, height: int, rgb: bytes) -> bytes:
    return f"P6\n{width} {height}\n255\n".encode("ascii") + rgb


def _stretch(picture, mask, width: int, height: int) -> tuple[int, int, bytes]:
    """Nearest-pixel RGBA at the given size. A pixel the mask leaves out is clear."""
    source_w, source_h, rgb = picture
    out = bytearray(width * height * 4)
    for y in range(height):
        source_y = min(source_h - 1, y * source_h // height)
        for x in range(width):
            source_x = min(source_w - 1, x * source_w // width)
            pixel = source_y * source_w + source_x
            if mask is not None and not mask[pixel]:
                continue
            dest = (y * width + x) * 4
            out[dest:dest + 3] = rgb[pixel * 3:pixel * 3 + 3]
            out[dest + 3] = 255
    return width, height, bytes(out)


def _png(width: int, height: int, rgba: bytes) -> bytes:
    import zlib

    def chunk(kind: bytes, body: bytes) -> bytes:
        return struct.pack(">I", len(body)) + kind + body + struct.pack(">I", zlib.crc32(kind + body))

    rows = b"".join(b"\x00" + rgba[y * width * 4:(y + 1) * width * 4] for y in range(height))
    return (
        b"\x89PNG\r\n\x1a\n"
        + chunk(b"IHDR", struct.pack(">IIBBBBB", width, height, 8, 6, 0, 0, 0))
        + chunk(b"IDAT", zlib.compress(rows))
        + chunk(b"IEND", b"")
    )


def _scale_rgb(width: int, height: int, rgb: bytes, scale: float) -> tuple[int, int, bytes]:
    if scale == 1:
        return width, height, rgb
    scaled_w = max(1, round(width * scale))
    scaled_h = max(1, round(height * scale))
    out = bytearray(scaled_w * scaled_h * 3)
    for y in range(scaled_h):
        source_y = min(height - 1, int(y / scale))
        for x in range(scaled_w):
            source_x = min(width - 1, int(x / scale))
            start = (source_y * width + source_x) * 3
            dest = (y * scaled_w + x) * 3
            out[dest:dest + 3] = rgb[start:start + 3]
    return scaled_w, scaled_h, bytes(out)
