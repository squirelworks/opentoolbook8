"""Open a book, or print a report or an install folder.

``python3 -m opentoolbook book.tbk`` opens the book on the page its
startup handlers name, or on the first stored page when they do not
name one. ``--report`` prints the record count, the files the book
names, and the startup call names, and does not open a window.
``--show PAGE`` opens that page id and does not follow startup handlers.

A ``linkDLL`` line is not called. ``forward`` is not executed.
``gotoPageList`` names pages that are not quoted, so a resumed session
is not the page the window opens on. Record text is not printed.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from opentoolbook.entry import opening_page
from opentoolbook.send import handler_chain
from opentoolbook.show import open_page
from opentoolbook.shelf import (
    find_file,
    missing_sentence,
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
        try:
            data = opened.read_bytes()
        except OSError:
            print(missing_sentence(opened.name, args.show), file=sys.stderr)
            return 2
        home = Path(args.home) if args.home else None
        try:
            errors = open_page(
                data,
                args.show,
                str(opened),
                args.home,
                status=unshipped_dll(opened, home),
                sysbooks=_startup_sysbooks(opened, home),
            )
        except ValueError as exc:
            print(exc, file=sys.stderr)
            return 2
        return 1 if errors else 0
    if args.book and not args.report:
        home = Path(args.home) if args.home else None
        try:
            entry = opening_page(Path(args.book), home)
        except ValueError as exc:
            print(exc, file=sys.stderr)
            return 2
        errors = open_page(
            entry.data,
            entry.page_id,
            str(entry.book),
            args.home,
            entry.props,
            status=unshipped_dll(entry.book, home),
            lesson=args.book,
            variables=entry.variables,
            sysbooks=entry.sysbooks,
        )
        return 1 if errors else 0
    if not any((args.book, args.home)):
        parser.print_usage(sys.stderr)
        return 2

    if args.home:
        _print_home(Path(args.home), Path(args.book) if args.book else None)
    elif args.book:
        _print_book(Path(args.book), None)
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
    sysbooks = _startup_sysbooks(path, home)
    print(f"sysBooks {len(sysbooks)}")
    for name in sysbooks:
        print(f"  {name}")
    chain = handler_chain(book.data, path.name, search_roots(path, home), sysbooks)
    print(f"calls {len(calls)}")
    for name in calls:
        found = chain.find(name)
        print(f"  {name}  {found[0]}" if found else f"  {name}")
    if home is not None:
        roots = search_roots(path, home)
        _print_shipped(home, roots)


def _startup_sysbooks(path: Path, home: Path | None) -> tuple[str, ...]:
    """``sysBooks`` after the book's own startup handlers, or none when startup fails."""
    try:
        return opening_page(path, home).sysbooks
    except ValueError:
        return ()










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






def _find(folder: Path, name: str) -> Path | None:
    if not folder.is_dir():
        return None
    for path in folder.iterdir():
        if path.is_file() and path.name.lower() == name.lower():
            return path
    return None


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
