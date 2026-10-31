"""The book and page a window is on, and what one button click does to them.

This is the click path of the Tk window without the window. A button
whose ``buttonClick`` quotes a page opens that page. A quoted ``of book``
is found with the same search as opening a book: the book directory, its
parent, ``--home``, ``--home/courses``, and ``--home/Nida98/Lessons``,
regardless of case. A file that search does not find is an error that
names the file and the page. A quiz button on a page whose background
calls ``handleQuizClick`` uses the stored page list. A ``request`` the
click runs is returned with the result, and the window shows it.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from opentoolbook.click import follow_click, quiz_background
from opentoolbook.field import page_ids
from opentoolbook.quiznav import quiz_click
from opentoolbook.shelf import find_file, search_roots


class MissingBook(ValueError):
    """A book a click names that the search does not find."""

    def __init__(self, name: str, page_id: str, roots: tuple[Path, ...]) -> None:
        self.name = name
        self.page_id = page_id
        self.roots = roots
        super().__init__(f"{name} was not found; {page_id} of that book is the page the click opens")


@dataclass(frozen=True)
class Clicked:
    """Whether the page changed, and whether the script beeped."""

    moved: bool
    beep: bool = False
    requests: tuple[str, ...] = ()


class Navigator:
    """The window's book, page, and search roots."""

    def __init__(
        self,
        data: bytes,
        page_id: str,
        book: Path | str | None = None,
        home: Path | str | None = None,
    ) -> None:
        self.data = data
        self.pages = page_ids(data)
        self.page_id = page_id
        self.book = Path(book) if book else None
        self.home = Path(home) if home else None

    @property
    def book_name(self) -> str:
        return self.book.name if self.book is not None else ""

    def roots(self) -> tuple[Path, ...]:
        """Where a quoted ``of book`` is looked for."""
        return search_roots(self.book, self.home)

    def find_book(self, name: str, page_id: str) -> Path:
        """The file a quoted ``of book`` names. Raises :class:`MissingBook`."""
        roots = self.roots()
        found = find_file(roots, name)
        if found is None:
            raise MissingBook(name, page_id, roots)
        return found

    def click(self, button: str) -> Clicked:
        """Run the named button's click. The page and book change in place."""
        acted = follow_click(self.data, self.page_id, button, self.pages)
        if acted is None:
            if not quiz_background(self.data, self.page_id):
                return Clicked(False)
            result = quiz_click(self.pages, self.page_id, button)
            asked = (result.request,) if result.request else ()
            if result.page_id == self.page_id:
                return Clicked(False, result.beep, asked)
            self.page_id = result.page_id
            return Clicked(True, result.beep, asked)
        beep, asked = acted.beeps > 0, acted.requests
        data, pages, book = self.data, self.pages, self.book
        if acted.book and acted.book.lower() != self.book_name.lower():
            book = self.find_book(acted.book, acted.page_id)
            data = book.read_bytes()
            pages = page_ids(data)
        if acted.page_id not in pages:
            return Clicked(False, beep, asked)
        if book == self.book and acted.page_id == self.page_id:
            return Clicked(False, beep, asked)
        self.data, self.pages, self.book = data, pages, book
        self.page_id = acted.page_id
        return Clicked(True, beep, asked)
