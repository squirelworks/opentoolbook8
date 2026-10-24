"""Summarise a ToolBook object directory. No record text is printed."""

from __future__ import annotations

import sys

from opentoolbook.record import MESSAGE_AFTER_LOAD, Book


def main(argv: list[str]) -> int:
    if len(argv) != 2:
        print("usage: python -m opentoolbook BOOK.tbk", file=sys.stderr)
        return 2
    with open(argv[1], "rb") as handle:
        book = Book(handle.read())
    follow = [item for item in book.records if item.wants_follow_up]
    print(f"records {len(book.records)}")
    print(f"follow-up reads {len(follow)}")
    print(f"message after a load {MESSAGE_AFTER_LOAD:#x}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
