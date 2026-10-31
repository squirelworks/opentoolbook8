"""Open a book, or print a report, a NIDA menu, or an install folder.

``python3 -m opentoolbook book.tbk`` opens the book on the page its
startup handlers name, or on the first stored page when they do not
name one. ``--report`` prints the record count, the files the book
names, and the startup call names, and does not open a window.
``--show PAGE`` opens that page id and does not follow startup handlers.

A ``linkDLL`` line is not called. ``forward`` is not executed.
``gotoPageList`` names pages that are not quoted, so a resumed session
is not the page the window opens on. Record text is not printed. A menu
run prints course ids, titles, and counts.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from opentoolbook.entry import opening_page
from opentoolbook.nida import discs_for, parse_cailt, parse_catalog, read_keydisk, zip_names_for
from opentoolbook.show import open_page
from opentoolbook.shelf import (
    CALL_BOOKS,
    find_file,
    named_calls,
    open_book,
    parse_install_list,
    parse_version,
    search_roots,
    unshipped_dll,
)


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(prog="opentoolbook")
    parser.add_argument(
        "book",
        nargs="?",
        help="a .tbk or .sbk. Opens the book on its opening page",
    )
    parser.add_argument(
        "--report",
        action="store_true",
        help="print the book report and do not open a window",
    )
    parser.add_argument("--catalog", help="courses.xml, or a folder that contains it")
    parser.add_argument(
        "--cailt",
        nargs=2,
        metavar=("TABLE", "LESSON"),
        help="CAILT.DAT and a lesson id; print that lesson's disc codes",
    )
    parser.add_argument("--keydisk", help="one rating folder from the key-disk creator")
    parser.add_argument(
        "--home",
        help="a ToolBook install directory. With a book, also search it for named files",
    )
    parser.add_argument(
        "--show",
        metavar="PAGE",
        help="open a Tk window on this page id. Does not follow startup handlers",
    )
    args = parser.parse_args(argv[1:])
    if args.show:
        if not args.book:
            parser.print_usage(sys.stderr)
            return 2
        opened = Path(args.book)
        home = Path(args.home) if args.home else None
        open_page(opened.read_bytes(), args.show, str(opened), args.home, status=unshipped_dll(opened, home))
        return 0
    if args.book and not args.report:
        if any((args.catalog, args.cailt, args.keydisk)):
            code = _print_side(args)
            if code:
                return code
        home = Path(args.home) if args.home else None
        try:
            entry = opening_page(Path(args.book), home)
        except ValueError as exc:
            print(exc, file=sys.stderr)
            return 2
        open_page(
            entry.data,
            entry.page_id,
            str(entry.book),
            args.home,
            entry.props,
            status=unshipped_dll(entry.book, home),
            lesson=args.book,
        )
        return 0
    if not any((args.book, args.catalog, args.cailt, args.keydisk, args.home)):
        parser.print_usage(sys.stderr)
        return 2

    if args.catalog:
        courses, programs = _catalog_paths(Path(args.catalog))
        if courses is None and programs is None:
            print(f"no courses.xml in {args.catalog}", file=sys.stderr)
            return 2
        if courses is None:
            _print_programs(programs)
        else:
            _print_catalogs(courses, programs)
    if args.cailt:
        table, lesson = args.cailt
        _print_discs(Path(table).read_text(encoding="latin1"), lesson, ())
    if args.keydisk:
        _print_keydisk(Path(args.keydisk))
    if args.home:
        _print_home(Path(args.home), Path(args.book) if args.book else None)
    elif args.book:
        _print_book(Path(args.book), None)
    return 0


def _print_side(args) -> int:
    """Print a catalog, a disc row, or a key disk. ``--home`` is not a report here."""
    if args.catalog:
        courses, programs = _catalog_paths(Path(args.catalog))
        if courses is None and programs is None:
            print(f"no courses.xml in {args.catalog}", file=sys.stderr)
            return 2
        if courses is None:
            _print_programs(programs)
        else:
            _print_catalogs(courses, programs)
    if args.cailt:
        table, lesson = args.cailt
        _print_discs(Path(table).read_text(encoding="latin1"), lesson, ())
    if args.keydisk:
        _print_keydisk(Path(args.keydisk))
    return 0


def _print_book(path: Path, home: Path | None) -> None:
    opened = open_book(path, home)
    book = opened.book
    follow = [item for item in book.records if item.wants_follow_up]
    print(f"records {len(book.records)}")
    print(f"follow-up reads {len(follow)}")
    calls = named_calls(book.data)
    print(f"named by the book {len(opened.files)}")
    for item in opened.files:
        if item.path is not None:
            print(f"  {item.name}  {item.path}")
        elif item.note:
            print(f"  {item.name}  {item.note}")
        else:
            print(f"  {item.name}")
    print(f"calls {len(calls)}")
    for name in calls:
        owner = CALL_BOOKS.get(name)
        print(f"  {name}  {owner}" if owner else f"  {name}")
    if home is not None:
        roots = search_roots(path, home)
        _print_shipped(home, roots)
        table = _find(home, "CAILT.DAT")
        if table is not None:
            _print_discs(table.read_text(encoding="latin1"), path.stem, roots)


def _print_catalogs(courses: Path, programs: Path | None) -> None:
    catalog = parse_catalog(courses.read_text(encoding="latin1"))
    lessons = catalog.lessons()
    course_ids = set(catalog.lesson_ids())
    print(f"courses {len(catalog.courses)}")
    print(f"lessons {len(lessons)}")
    print(f"courses.xml unique lesson ids {len(course_ids)}")
    for course in catalog.courses:
        print(f"{course.course_id}\t{course.title}\t{len(course.lessons())}")
    if programs is None:
        return
    program_ids = set(parse_catalog(programs.read_text(encoding="latin1")).lesson_ids())
    print(f"programs.xml unique lesson ids {len(program_ids)}")
    _print_id_diff("courses.xml", course_ids - program_ids)
    _print_id_diff("programs.xml", program_ids - course_ids)


def _print_programs(programs: Path) -> None:
    program_ids = set(parse_catalog(programs.read_text(encoding="latin1")).lesson_ids())
    print(f"programs.xml unique lesson ids {len(program_ids)}")


def _print_id_diff(label: str, ids: set[str]) -> None:
    ordered = tuple(sorted(ids))
    print(f"only in {label} {len(ordered)}")
    for lesson_id in ordered:
        print(f"  {lesson_id}")


def _print_keydisk(folder: Path) -> None:
    disk = read_keydisk(folder)
    print(disk.info)
    if disk.shift is not None:
        print(f"shift {disk.shift.shift} {disk.shift.start}-{disk.shift.end}")
        print(f"closed days {len(disk.shift.closed)}")
    print(f"settings {len(disk.settings)}")
    for name, version, size in disk.records:
        print(f"{name} version {version} bytes {size}")


def _print_home(folder: Path, book: Path | None) -> None:
    if not folder.is_dir():
        raise ValueError(f"{folder} is not a directory")
    version_file = _find(folder, "version.ini")
    if version_file is not None:
        version, date = parse_version(version_file.read_text(encoding="latin1"))
        print(f"version {version} {date}".rstrip())
    apps = _find(folder, "stdapps.lst")
    if apps is not None:
        data = apps.read_bytes()
        print(f"stdapps.lst {len(data)} bytes")
        print("  " + " ".join(f"{byte:02x}" for byte in data[:32]))
    courses, programs = _catalog_paths(folder)
    if courses is not None:
        _print_catalogs(courses, programs)
    if book is not None:
        _print_book(book, folder)
    else:
        _print_shipped(folder, search_roots(None, folder))


def _print_shipped(folder: Path, roots: tuple[Path, ...]) -> None:
    listing = _find(folder, "toolbook.lst")
    if listing is None:
        return
    files = parse_install_list(listing.read_text(encoding="latin1"))
    required = tuple(item for item in files if not item.optional)
    optional = tuple(item for item in files if item.optional)
    print("shipped by the install")
    print(f"required {len(required)}")
    for item in required:
        found = find_file(roots, item.name)
        if found is None:
            print(f"  {item.name}  not found")
        else:
            print(f"  {item.name}  {found}")
    print("listed, not shipped")
    for item in optional:
        print(f"  {item.name}")


def _print_discs(text: str, lesson: str, roots: tuple[Path, ...]) -> None:
    rules = parse_cailt(text)
    discs = discs_for(rules, lesson)
    print(f"lesson {lesson}")
    print("discs " + (", ".join(discs) if discs else "none"))
    for name in zip_names_for(rules, lesson):
        found = find_file(roots, name)
        if found is not None:
            print(f"  {name}  {found}")


def _catalog_paths(path: Path) -> tuple[Path | None, Path | None]:
    if path.is_dir():
        return _find(path, "courses.xml"), _find(path, "programs.xml")
    folder = path.parent
    if path.name.lower() == "programs.xml":
        return _find(folder, "courses.xml"), path
    programs = _find(folder, "programs.xml")
    return path, programs


def _find(folder: Path, name: str) -> Path | None:
    if not folder.is_dir():
        return None
    for path in folder.iterdir():
        if path.is_file() and path.name.lower() == name.lower():
            return path
    return None


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
