"""The book and page a window is on, and what one button click does to them.

This is the click path of the Tk window without the window. A button
whose ``buttonClick`` quotes a page opens that page. A quoted ``of book``
is found with the same search as opening a book: the book directory, its
parent, ``--home``, ``--home/courses``, and ``--home/Nida98/Lessons``,
regardless of case. After the window changes books, the search still
starts from the lesson the user opened, then the book on screen, then
``--home``. A file that search does not find is an error that names the
file and the page, in the same sentence as the open:
``nida81.tbk was not found; P310 of that book does not open``. A click
that hits no button, or a button with no ``buttonClick``, goes to the
page's own ``buttonClick``. A quiz button on a page whose background
calls ``handleQuizClick`` uses the stored page list. A page id matches
regardless of case. Field text a click writes stays on the page until
the page changes.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from opentoolbook.click import follow_click, page_click, quiz_background
from opentoolbook.field import page_ids
from opentoolbook.quiznav import quiz_click
from opentoolbook.shelf import MissingBook, find_file, search_roots


@dataclass(frozen=True)
class Clicked:
    """Whether the page changed, whether the script beeped, and whether a field changed."""

    moved: bool
    beep: bool = False
    changed: bool = False


class Navigator:
    """The window's book, page, and search roots."""

    def __init__(
        self,
        data: bytes,
        page_id: str,
        book: Path | str | None = None,
        home: Path | str | None = None,
        lesson: Path | str | None = None,
        variables: dict[str, object] | None = None,
    ) -> None:
        self.data = data
        self.pages = page_ids(data)
        self.page_id = page_id
        self.book = Path(book) if book else None
        self.home = Path(home) if home else None
        # The path the user passed. It stays when the window changes books.
        self.lesson = Path(lesson) if lesson else self.book
        # System variables a handler this runner executed assigned, by lower-case name.
        self.variables: dict[str, object] = {key.lower(): value for key, value in (variables or {}).items()}
        # Field text a click wrote, by field name. Cleared when the page changes.
        self.fields: dict[str, str] = {}

    @property
    def book_name(self) -> str:
        return self.book.name if self.book is not None else ""

    def roots(self) -> tuple[Path, ...]:
        """Where a quoted ``of book`` is looked for.

        The lesson's directory and its parent, then the directory of the
        book on screen and its parent, then the ``--home`` folders.
        """
        found: list[Path] = []
        for root in search_roots(self.lesson, None) + search_roots(self.book, self.home):
            if root not in found:
                found.append(root)
        return tuple(found)

    def find_book(self, name: str, page_id: str) -> Path:
        """The file a quoted ``of book`` names. Raises :class:`MissingBook`."""
        roots = self.roots()
        found = find_file(roots, name)
        if found is None:
            raise MissingBook(name, page_id, roots)
        return found

    def click(self, button: str | None, shown: dict[str, str] | None = None) -> Clicked:
        """Run one click. ``button`` None is a click that hits no button.

        The page and book change in place. ``shown`` is the field text the
        page shows now. Field text the click writes is kept in ``fields``
        until the page changes.
        """
        acted = None
        if button:
            acted = follow_click(self.data, self.page_id, button, self.pages, shown)
        if acted is None:
            acted = page_click(self.data, self.page_id, self.pages, self.variables, shown)
        if acted is None:
            if not button or not quiz_background(self.data, self.page_id):
                return Clicked(False)
            result = quiz_click(self.pages, self.page_id, button)
            if result.page_id == self.page_id:
                return Clicked(False, result.beep)
            self.page_id = result.page_id
            self.fields = {}
            return Clicked(True, result.beep)
        changed = bool(acted.fields)
        for name, text in acted.fields:
            self.fields[name] = text
        data, pages, book = self.data, self.pages, self.book
        if acted.book and acted.book.lower() != self.book_name.lower():
            book = self.find_book(acted.book, acted.page_id)
            data = book.read_bytes()
            pages = page_ids(data)
        page = _match(pages, acted.page_id)
        if page is None:
            return Clicked(False, changed=changed)
        if book == self.book and page == self.page_id:
            return Clicked(False, changed=changed)
        self.data, self.pages, self.book = data, pages, book
        self.page_id = page
        self.fields = {}
        return Clicked(True)


def _match(pages: tuple[str, ...], page_id: str) -> str | None:
    for page in pages:
        if page.lower() == page_id.lower():
            return page
    return None
