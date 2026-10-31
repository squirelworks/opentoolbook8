"""The NIDA course shell that sits around a ToolBook lesson.

A lesson book is not the course. The course is a menu export, a disc
lookup, and a key disk for one rating. None of those are the 16-bit
runtime. They are the extra files a modern reader has to understand
before it can offer the lesson the way the original shell did.

``courses.xml`` is a ``nida:m3search`` menu. Top-level ``Menu`` elements
are courses. Nested menus are modules. ``Item`` elements are lessons.

``CAILT.DAT`` maps a lesson id to Navy disc codes. ``?`` is one
character, the match is on the front of the id, and the most specific
pattern wins. ``9E954D01`` meets ``9E954??`` and that line names
``DIE??V03``, which is the zip ``die0dv03.zip``. The zip is named, not opened.

A key-disk rating folder holds a plain description, a shift calendar,
an encoded settings line, and three versioned binary records.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from xml.etree import ElementTree


@dataclass(frozen=True)
class Lesson:
    lesson_id: str
    title: str


@dataclass(frozen=True)
class Module:
    title: str
    lessons: tuple[Lesson, ...]
    children: tuple[Module, ...]


@dataclass(frozen=True)
class Course:
    course_id: str
    title: str
    modules: tuple[Module, ...]

    def lessons(self) -> tuple[Lesson, ...]:
        found: list[Lesson] = []

        def walk(module: Module) -> None:
            found.extend(module.lessons)
            for child in module.children:
                walk(child)

        for module in self.modules:
            walk(module)
        return tuple(found)


@dataclass(frozen=True)
class Catalog:
    courses: tuple[Course, ...]

    def lessons(self) -> tuple[Lesson, ...]:
        found: list[Lesson] = []
        for course in self.courses:
            found.extend(course.lessons())
        return tuple(found)

    def lesson_ids(self) -> tuple[str, ...]:
        return tuple(dict.fromkeys(item.lesson_id for item in self.lessons()))


@dataclass(frozen=True)
class DiscRule:
    pattern: str
    discs: tuple[str, ...]


@dataclass(frozen=True)
class ShiftCalendar:
    shift: str
    start: str
    end: str
    closed: tuple[str, ...]
    notes: tuple[str, ...]


@dataclass(frozen=True)
class KeyDisk:
    info: str
    shift: ShiftCalendar | None
    settings: tuple[tuple[str, str], ...]
    records: tuple[tuple[str, int, int], ...]


def parse_catalog(text: str) -> Catalog:
    root = ElementTree.fromstring(text)
    if root.tag != "Document" or root.attrib.get("type") != "nida:m3search":
        raise ValueError("not a NIDA menu export")
    courses = tuple(_course(node) for node in root.findall("Menu"))
    if not courses:
        raise ValueError("menu export has no courses")
    return Catalog(courses)


class MissingLesson(ValueError):
    """A catalog lesson whose ``.tbk`` the shelf search does not find."""

    def __init__(self, lesson_id: str, name: str, roots: tuple[Path, ...]) -> None:
        self.lesson_id = lesson_id
        self.name = name
        self.roots = roots
        super().__init__(f"{name} was not found; lesson {lesson_id} does not open")


def catalog_lesson(catalog: Catalog, folder: Path, lesson_id: str, home: Path | None = None) -> Path:
    """The ``.tbk`` for one catalog lesson id, found with the shelf rules.

    The file name is the lesson id in lower case plus ``.tbk``. It is looked
    for in the catalog folder, its parent, ``home``, ``home/courses``, and
    ``home/Nida98/Lessons``, regardless of case. An id the catalog does
    not list is an error, and so is a file the search does not find.
    """
    from opentoolbook.shelf import find_file, search_roots

    wanted = lesson_id.strip().upper()
    if wanted not in {item.upper() for item in catalog.lesson_ids()}:
        raise ValueError(f"{lesson_id} is not a lesson in the catalog")
    name = f"{wanted.lower()}.tbk"
    roots = search_roots(folder, home)
    found = find_file(roots, name)
    if found is None:
        raise MissingLesson(wanted, name, roots)
    return found


def discs_for(rules: tuple[DiscRule, ...], lesson_id: str) -> tuple[str, ...]:
    """Disc codes for one lesson id. The longest literal pattern wins."""
    match = match_discs(rules, lesson_id)
    if match is None:
        return ()
    return match[0].discs


def zip_names_for(rules: tuple[DiscRule, ...], lesson_id: str) -> tuple[str, ...]:
    """Zip file for each disc code. ``DIE??V03`` for lesson ``9E954D01`` is ``die0dv03.zip``.

    ``?`` in the lesson pattern captures those characters. They fill the
    disc code's ``?`` slots from the right. A code with no ``?`` is the
    zip name as written.
    """
    match = match_discs(rules, lesson_id)
    if match is None:
        return ()
    rule, captured = match
    names: list[str] = []
    for disc in rule.discs:
        name = _zip_name(disc, captured)
        if name is not None:
            names.append(name)
    return tuple(names)


def match_discs(rules: tuple[DiscRule, ...], lesson_id: str) -> tuple[DiscRule, str] | None:
    lesson = _lesson_key(lesson_id)
    best: DiscRule | None = None
    best_captured = ""
    best_score = -1
    for rule in rules:
        captured = _capture(rule.pattern, lesson)
        if captured is None:
            continue
        score = sum(ch != "?" for ch in rule.pattern)
        if score > best_score:
            best = rule
            best_captured = captured
            best_score = score
    if best is None:
        return None
    return best, best_captured


def parse_cailt(text: str) -> tuple[DiscRule, ...]:
    rules: list[DiscRule] = []
    for raw in text.splitlines():
        line = raw.strip()
        if not line or line.startswith("$") or "*" not in line:
            continue
        pattern, _, rest = line.partition("*")
        discs = tuple(part.strip() for part in rest.split(",") if part.strip())
        rules.append(DiscRule(pattern.strip().upper(), discs))
    if not rules:
        raise ValueError("disc table has no rules")
    return tuple(rules)


def parse_shifts(text: str) -> ShiftCalendar:
    shift = start = end = ""
    closed: list[str] = []
    notes: list[str] = []
    section = ""
    for raw in text.splitlines():
        line = raw.strip()
        if not line:
            continue
        if line.startswith("[") and line.endswith("]"):
            section = line[1:-1].lower()
            continue
        if "=" not in line:
            notes.append(line)
            continue
        key, _, value = line.partition("=")
        key = key.strip()
        value = value.strip()
        if section == "shift" and key.lower() == "shift":
            shift = value
        elif section == "shift" and key.lower() == "start":
            start = value
        elif section == "shift" and key.lower() == "end":
            end = value
        elif section == "closed" and value == "1":
            closed.append(key)
    return ShiftCalendar(shift, start, end, tuple(closed), tuple(notes))


def parse_settings(text: str) -> tuple[tuple[str, str], ...]:
    """Pairs from the encoded criteria line.

    The letters are substituted. Separators, the drive letter, and the
    digits are still in the clear, so the pairs can be stored as they
    stand. The substitution key is not in this file.
    """
    pairs: list[tuple[str, str]] = []
    for part in text.strip().strip(";").split(";"):
        if "=" not in part:
            continue
        key, _, value = part.partition("=")
        pairs.append((key.strip(), value.strip()))
    return tuple(pairs)


def read_keydisk(folder: Path) -> KeyDisk:
    info = _read_text(_find(folder, "INFO.TXT"))
    shift_path = _find(folder, "shifts.s4")
    shift = parse_shifts(_read_text(shift_path)) if shift_path else None
    criteria = _find(folder, "criteria.s5")
    settings = parse_settings(_read_text(criteria)) if criteria else ()
    records: list[tuple[str, int, int]] = []
    for name in ("CLASS.S3", "ID.S3", "M00001.S3"):
        path = _find(folder, name)
        if path is None:
            continue
        data = path.read_bytes()
        version = int.from_bytes(data[:2], "little") if len(data) >= 2 else 0
        records.append((name.lower(), version, len(data)))
    return KeyDisk(info.strip(), shift, settings, tuple(records))


def _course(node: ElementTree.Element) -> Course:
    modules = tuple(_module(child) for child in node.findall("Menu"))
    lessons = tuple(_lesson(child) for child in node.findall("Item"))
    if lessons:
        modules = (Module("", lessons, ()),) + modules
    return Course(node.attrib.get("courseid", ""), node.attrib.get("title", ""), modules)


def _module(node: ElementTree.Element) -> Module:
    return Module(
        node.attrib.get("title", ""),
        tuple(_lesson(child) for child in node.findall("Item")),
        tuple(_module(child) for child in node.findall("Menu")),
    )


def _lesson(node: ElementTree.Element) -> Lesson:
    return Lesson(node.attrib.get("lessonid", ""), node.attrib.get("title", ""))


def _lesson_key(lesson_id: str) -> str:
    name = lesson_id.strip()
    if "." in name:
        name = name.split(".", 1)[0]
    return name.upper()


def _capture(pattern: str, lesson: str) -> str | None:
    pattern = pattern.upper()
    if len(pattern) > len(lesson):
        return None
    captured: list[str] = []
    for index, ch in enumerate(pattern):
        if ch == "?":
            captured.append(lesson[index])
        elif ch != lesson[index]:
            return None
    return "".join(captured)


def _zip_name(disc: str, captured: str) -> str | None:
    fill = captured[::-1]
    index = 0
    out: list[str] = []
    for ch in disc:
        if ch == "?":
            if index >= len(fill):
                return None
            out.append(fill[index])
            index += 1
        else:
            out.append(ch)
    return "".join(out).lower() + ".zip"


def _find(folder: Path, name: str) -> Path | None:
    for path in folder.iterdir():
        if path.is_file() and path.name.lower() == name.lower():
            return path
    return None


def _read_text(path: Path | None) -> str:
    if path is None:
        return ""
    return path.read_text(encoding="latin1")
