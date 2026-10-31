"""A page, drawn from the readers.

One page unit is one twentieth of a point. One point is 96/72 pixels at
96 dpi. The fit scale multiplies that pixel size once. Pattern 254 is a
solid fill and pattern 253 is no fill. Another pattern byte is not drawn
as a hatch. A draw object's fill is the color at ``+0x1B`` and its stroke
is the color at ``+0x17``. A button draws the picture at byte ``0x15`` of
its graphics block, or the picture at byte ``0x4B`` when the button is
checked. While a button is held down it draws the picture at byte
``0x27`` when that word is not 0, and letting go draws the up picture
again. The disabled picture is not drawn. A field that
contains a shape is painted under that shape. A label that contains no
shape is painted in front of a shape that contains the label.

The page walk names classes ``0x8``, ``0x9``, ``0xA``, ``0xB``, ``0xC``,
``0xD``, ``0xE``, ``0x10``, ``0x11``, ``0x13``, ``0x15``, and ``0x19``.
Of those, the window paints rectangles, ellipses, lines, class ``0x10``
polygons, fields, and buttons, plus the class 4 background. It does not
paint ``0xD``, arcs (``0x11``), class ``0x13`` point lists, ``0x15``, or
``0x19``. A group is not a paint; its children are. Class ``0x12`` pies
and class ``0x17`` records are outside that walk, and they are not painted.
"""

from __future__ import annotations

import struct
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
from opentoolbook.click import follow_click, quiz_background
from opentoolbook.quiznav import quiz_click
from opentoolbook.page import _child_nears, _object_name, _objects
from opentoolbook.pixels import picture_rgb
from opentoolbook.size import page_size

# One page unit is 1/20 point. One point is 96/72 pixels at 96 dpi.
UNIT_PER_POINT = 20
PIXELS_PER_POINT = 96 / 72

NO_FILL = 253

_RECTANGLE = 0x8
_BUTTON = 0x9
_FIELD = 0xA
_GROUP = 0xB
_ELLIPSE = 0xC
_LINE = 0xE
_POLYGON = 0x10
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
    invert_id: int | None = None


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


def show_page(data: bytes, page_id: str, view_width: int, view_height: int) -> DisplayList:
    """The display list for one page. It does not open a window."""
    width, height = page_size(data)
    scale = fit_scale(width, height, view_width, view_height)
    items = _entered(data, page_id, _ordered(_stored(data, page_id, width, height)))
    return DisplayList(page_id, width, height, view_width, view_height, scale, items)


def open_page(data: bytes, page_id: str, book: str | None = None) -> None:
    """Open a Tk window on the page id given, at 96 dpi, fitted once.

    The page id is the one the caller passed. This function does not
    follow startup handlers. A button whose handler quotes a page opens
    that page. A quoted book is that filename in the directory of
    ``book``, exact case, and nowhere else. A quiz page with no quiz
    running still uses OK, Next, and Skip for the next page and Back
    for the previous page.
    """
    import tkinter as tk
    from pathlib import Path

    root = tk.Tk()
    try:
        root.update_idletasks()
        width, height = page_size(data)
        view_w = max(1, min(_pixels(width), root.winfo_screenwidth() - 48))
        view_h = max(1, min(_pixels(height), root.winfo_screenheight() - 96))
        root.title(page_id)
        canvas = tk.Canvas(
            root,
            width=view_w,
            height=view_h,
            highlightthickness=0,
            background="#ffffff",
        )
        canvas.pack()
        state = {
            "data": data,
            "pages": page_ids(data),
            "page": page_id,
            "book": Path(book).name if book else "",
            "folder": Path(book).parent if book else None,
        }

        def redraw() -> None:
            listed = show_page(state["data"], state["page"], view_w, view_h)
            canvas.delete("all")
            draw_page(canvas, listed)
            canvas.listed = listed
            root.title(state["page"])

        def on_press(event) -> None:
            listed = getattr(canvas, "listed", None)
            if listed is None:
                return
            name = button_at(listed, event.x, event.y)
            state["pressed"] = name
            if not name:
                return
            held = pressed(state["data"], listed, name)
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
            if not name or button_at(listed, event.x, event.y) != name:
                return
            acted = follow_click(state["data"], state["page"], name, state["pages"])
            if acted is None:
                if not quiz_background(state["data"], state["page"]):
                    return
                result = quiz_click(state["pages"], state["page"], name)
                if result.beep:
                    root.bell()
                if result.page_id == state["page"]:
                    return
                state["page"] = result.page_id
                redraw()
                return
            if acted.book:
                folder = state["folder"]
                path = None if folder is None else folder / acted.book
                if path is None or not path.is_file():
                    return
                if path.name.lower() != state["book"].lower():
                    state["data"] = path.read_bytes()
                    state["pages"] = page_ids(state["data"])
                    state["book"] = path.name
            if acted.page_id not in state["pages"] or acted.page_id == state["page"]:
                return
            state["page"] = acted.page_id
            redraw()

        canvas.bind("<ButtonPress-1>", on_press)
        canvas.bind("<ButtonRelease-1>", on_click)
        redraw()
        root.mainloop()
    finally:
        if root.winfo_exists():
            root.destroy()


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


def draw_page(canvas, listed: DisplayList) -> None:
    """Paint a display list onto a Tk canvas. Photos stay referenced by the canvas."""
    photos: list = []
    canvas.photos = photos
    for item in listed.items:
        _draw_item(canvas, listed.scale, item, photos)


def _pixels(units: int) -> int:
    return max(1, round(unit_to_px(units, 1)))


def _entered(data: bytes, page_id: str, items: tuple[Paint, ...]) -> tuple[Paint, ...]:
    """Run the page's enterPage text. A missing sysLevel is reader."""
    from opentoolbook.enter import enter_fields

    indexes = [index for index, item in enumerate(items) if item.kind == "field"]
    packed = tuple((items[index].name, items[index].text or "", items[index].runs) for index in indexes)
    changed = enter_fields(data, page_id, packed)
    if changed == packed:
        return items
    out = list(items)
    for index, (_name, text, runs) in zip(indexes, changed):
        if text != (out[index].text or "") or runs != out[index].runs:
            out[index] = replace(out[index], text=text, runs=runs)
    return tuple(out)


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
    for at, kind in found:
        if _u16(data, at + 4) != parent:
            continue
        near = at - segment.base
        if kind == _GROUP:
            for child in _child_nears(data, segment, at):
                items.extend(_child(data, segment, trailer, base, known, by_near, child))
            continue
        painted = _paint(data, segment, trailer, base, known, at, kind)
        if painted is not None:
            items.append(painted)
    return items


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
    # The rectangle named Correct is the answer mark. No quiz pass has shown it.
    if kind == _RECTANGLE and name.lower() == "correct":
        return None
    if kind in (_RECTANGLE, _ELLIPSE, _POLYGON):
        fill, stroke = _colors(data, at)
        points = _polygon_points(data, segment, at) if kind == _POLYGON else ()
        return Paint(_DRAW[kind], object_id, name, bounds, fill, stroke, data[at + 0x25], points)
    if kind == _LINE:
        _fill, stroke = _colors(data, at)
        return Paint("line", object_id, name, bounds, None, stroke, None, _line_points(data, at))
    if kind == _FIELD:
        text, runs = _runs(data, trailer, base, known, at)
        return Paint("field", object_id, name, bounds, text=text, runs=runs)
    if kind == _BUTTON:
        return _button(data, segment, at, object_id, name, bounds)
    return None


def _button(data, segment, at: int, object_id: int, name: str, bounds) -> Paint:
    up = _graphic_word(data, segment, at, 0x15)
    checked_id = _graphic_word(data, segment, at, 0x4B)
    checked = (data[at + 0x26] >> 4) & 1
    if checked and checked_id:
        picture_id = checked_id
        role = "checked"
    else:
        picture_id = up
        role = "up" if up else None
    picture = None
    if picture_id:
        try:
            picture = picture_rgb(data, picture_id)
        except ValueError:
            picture = None
    return Paint(
        "button",
        object_id,
        name,
        bounds,
        picture_id=picture_id,
        picture_role=role,
        picture=picture,
        invert_id=_graphic_word(data, segment, at, 0x27) or None,
    )


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


def _draw_item(canvas, scale: float, item: Paint, photos: list) -> None:
    import tkinter as tk

    if item.kind == "background" and item.fill is not None and item.bounds is not None:
        canvas.create_rectangle(*_device_box(item.bounds, scale), fill=_rgb(item.fill), outline="")
        return
    if item.kind == "rectangle" and item.bounds is not None:
        canvas.create_rectangle(
            *_device_box(item.bounds, scale),
            fill=_rgb(item.fill) if item.fill is not None else "",
            outline=_rgb(item.stroke) if item.stroke is not None else "",
        )
        return
    if item.kind == "ellipse" and item.bounds is not None:
        canvas.create_oval(
            *_device_box(item.bounds, scale),
            fill=_rgb(item.fill) if item.fill is not None else "",
            outline=_rgb(item.stroke) if item.stroke is not None else "",
        )
        return
    if item.kind == "line" and len(item.points) == 2:
        flat = [unit_to_px(value, scale) for point in item.points for value in point]
        canvas.create_line(*flat, fill=_rgb(item.stroke) if item.stroke is not None else "#000000")
        return
    if item.kind == "polygon" and len(item.points) >= 2:
        flat = [unit_to_px(value, scale) for point in item.points for value in point]
        canvas.create_polygon(
            *flat,
            fill=_rgb(item.fill) if item.fill is not None else "",
            outline=_rgb(item.stroke) if item.stroke is not None else "",
        )
        return
    if item.kind == "button" and item.picture is not None and item.bounds is not None:
        width, height, rgb = _scale_rgb(item.picture[0], item.picture[1], item.picture[2], scale)
        photo = tk.PhotoImage(data=_ppm(width, height, rgb))
        photos.append(photo)
        x = unit_to_px(item.bounds[0], scale)
        y = unit_to_px(item.bounds[1], scale)
        canvas.create_image(x, y, image=photo, anchor="nw")
        return
    if item.kind == "field" and item.text and item.bounds is not None:
        _draw_text(canvas, scale, item)


def _draw_text(canvas, scale: float, item: Paint) -> None:
    import tkinter.font as tkfont

    shown = item.text.replace("\r\n", "\n").replace("\r", "\n")
    spans = _spans(shown, item.runs)
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
    for text, span_face in spans:
        canvas.create_text(
            left,
            y,
            text=text,
            anchor="nw",
            width=width,
            fill="#000000",
            font=(span_face or "TkDefaultFont", -size),
        )
        y += size * max(1, text.count("\n") + 1)


def _spans(text: str, runs: tuple[tuple[int, str | None], ...]) -> tuple[tuple[str, str | None], ...]:
    if not runs:
        return ((text, None),)
    ordered = tuple(sorted(runs))
    found = []
    for index, (offset, face) in enumerate(ordered):
        end = ordered[index + 1][0] if index + 1 < len(ordered) else len(text)
        if offset < 0 or offset > len(text):
            continue
        found.append((text[offset:max(offset, end)], face))
    return tuple(found) or ((text, None),)


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
