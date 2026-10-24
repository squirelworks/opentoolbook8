"""Summarise a book, a NIDA menu, or the install folder beside them.

Record text is not printed. A menu run prints course ids, titles, and
counts. A book run prints the files and calls that book names.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from opentoolbook.nida import discs_for, parse_cailt, parse_catalog, read_keydisk
from opentoolbook.record import MESSAGE_AFTER_LOAD, Book
from opentoolbook.shelf import named_calls, named_files, on_disk, parse_install_list, parse_version


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(prog="opentoolbook")
    parser.add_argument("book", nargs="?", help="a .tbk or .sbk to summarise")
    parser.add_argument("--catalog", help="a nida:m3search courses.xml")
    parser.add_argument("--cailt", nargs=2, metavar=("TABLE", "LESSON"))
    parser.add_argument("--keydisk", help="one rating folder from the key-disk creator")
    parser.add_argument("--home", help="a ToolBook install directory")
    args = parser.parse_args(argv[1:])
    if not any((args.book, args.catalog, args.cailt, args.keydisk, args.home)):
        parser.print_usage(sys.stderr)
        return 2

    if args.catalog:
        _print_catalog(Path(args.catalog))
    if args.cailt:
        table, lesson = args.cailt
        rules = parse_cailt(Path(table).read_text(encoding="latin1"))
        discs = discs_for(rules, lesson)
        print(f"lesson {lesson}")
        print("discs " + (", ".join(discs) if discs else "none"))
    if args.keydisk:
        _print_keydisk(Path(args.keydisk))
    if args.home:
        _print_home(Path(args.home), Path(args.book) if args.book else None)
    elif args.book:
        _print_book(Path(args.book), None)
    return 0


def _print_book(path: Path, home: Path | None) -> None:
    data = path.read_bytes()
    book = Book(data)
    follow = [item for item in book.records if item.wants_follow_up]
    print(f"records {len(book.records)}")
    print(f"follow-up reads {len(follow)}")
    print(f"message after a load {MESSAGE_AFTER_LOAD:#x}")
    files = named_files(data)
    calls = named_calls(data)
    print(f"named files {len(files)}")
    for name in files:
        print(f"  {name}")
    print(f"calls {len(calls)}")
    for name in calls:
        print(f"  {name}")
    if home is not None:
        present, missing = on_disk(home, files)
        print(f"in {home} present {len(present)} missing {len(missing)}")
        for name in missing:
            print(f"  missing {name}")
        table = _find(home, "CAILT.DAT")
        if table is not None:
            discs = discs_for(parse_cailt(table.read_text(encoding="latin1")), path.stem)
            print("discs " + (", ".join(discs) if discs else "none"))


def _print_catalog(path: Path) -> None:
    catalog = parse_catalog(path.read_text(encoding="latin1"))
    lessons = catalog.lessons()
    print(f"courses {len(catalog.courses)}")
    print(f"lessons {len(lessons)}")
    print(f"unique lesson ids {len(catalog.lesson_ids())}")
    for course in catalog.courses:
        print(f"{course.course_id}\t{course.title}\t{len(course.lessons())}")


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
    version_file = _find(folder, "version.ini")
    if version_file is not None:
        version, date = parse_version(version_file.read_text(encoding="latin1"))
        print(f"version {version} {date}".rstrip())
    listing = _find(folder, "toolbook.lst")
    if listing is not None:
        files = parse_install_list(listing.read_text(encoding="latin1"))
        required = tuple(item.name for item in files if not item.optional)
        optional = tuple(item.name for item in files if item.optional)
        present, missing = on_disk(folder, required)
        print(f"install required {len(required)} optional {len(optional)}")
        print(f"required present {len(present)} missing {len(missing)}")
        for name in missing:
            print(f"  missing {name}")
    apps = _find(folder, "stdapps.lst")
    if apps is not None:
        data = apps.read_bytes()
        kind = "encoded" if b"\x00" in data[:32] else "text"
        print(f"stdapps.lst {len(data)} bytes {kind}")
    catalog = _find(folder, "courses.xml")
    if catalog is not None:
        _print_catalog(catalog)
    if book is not None:
        _print_book(book, folder)


def _find(folder: Path, name: str) -> Path | None:
    if not folder.is_dir():
        raise ValueError(f"{folder} is not a directory")
    for path in folder.iterdir():
        if path.is_file() and path.name.lower() == name.lower():
            return path
    return None


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
