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
calls ``handleQuizClick`` uses the stored page list. A letter button on
that page, ``A`` through ``E``, is ``manageQuizButtons``: the letter is
checked and every other letter on the page is unchecked. The page stays.
With a ``props`` store, ``OK`` and ``Next`` there run the first block of
``gotoNextQuestionEx`` before the page changes: the checked letter and its
score go into ``__quizResponse`` and ``__quizScore`` at ``__quizIndex``.
A page id matches
regardless of case. A ``request`` the click runs is returned with the
result, and the window shows it. Field text a click writes, and objects
it hides or shows, stay that way on the page until the page changes.

The navigator keeps the stack of ``(book, page)`` it has shown, apart from
the stored page list. ``back`` pops that stack. A book button that says
``send previous`` still uses the stored page list.

The page a click lands on runs its ``enterPage`` the way the opening
page does. A quoted ``go to page`` there moves the window again, to
another book when it names one. Its field writes are in the display list.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from opentoolbook.click import follow_click, page_click, quiz_background, quiz_setup_click
from opentoolbook.enter import _enter_page, page_source
from opentoolbook.field import page_ids
from opentoolbook.props import UserProperties
from opentoolbook.quiznav import quiz_click
from opentoolbook.shelf import MissingBook, find_file, open_book, search_roots

# A page whose enterPage moves to another page is followed this many times.
_HOPS = 4


@dataclass(frozen=True)
class Clicked:
    """Whether the page changed, and whether the script beeped."""

    moved: bool
    beep: bool = False
    requests: tuple[str, ...] = ()
    changed: bool = False
    checked: bool = False


# ``initializeTest`` sets ``__quizMaxResponse`` to 5, and
# ``manageQuizButtons`` walks ``ansiToChar(96 + i)`` up to it.
LETTERS = ("a", "b", "c", "d", "e")
# ``handleQuizClick`` calls ``gotoNextQuestionEx`` for these. ``Skip`` with a
# checked letter asks first, and without one stores nothing here.
_NEXT_QUESTION = ("ok", "next")


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
        props: UserProperties | None = None,
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
        self._handlers: dict[Path | None, dict[str, str]] = {}
        # The __ names this window's handlers read and write.
        self.props = props if props is not None else UserProperties()
        # Pages shown before this one, oldest first: (book, page id, book bytes).
        self.history: list[tuple[Path | None, str, bytes]] = []
        # Field text a click wrote, by field name. Cleared when the page changes.
        self.fields: dict[str, str] = {}
        # Objects a click hid or showed, by (kind, name or id). Cleared when the page changes.
        self.visible: dict[tuple[str, str | int], bool] = {}
        self.letters: dict[tuple[str, str], str] = {}

    @property
    def book_name(self) -> str:
        return self.book.name if self.book is not None else ""

    def title(self) -> str:
        """The window title: the book file and the page id."""
        if not self.book_name:
            return self.page_id
        return f"{self.book_name} - {self.page_id}"

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

        The page shown before a click that moves is pushed on ``history``.
        """
        before = (self.book, self.page_id, self.data)
        result = self._click(button, shown)
        if result.moved:
            self.history.append(before)
        return result

    def back(self) -> bool:
        """Pop the viewer's history. False when nothing was shown before."""
        if not self.history:
            return False
        book, page_id, data = self.history.pop()
        if data is not self.data:
            self.pages = page_ids(data)
        self.book, self.page_id, self.data = book, page_id, data
        self.fields = {}
        self.visible = {}
        return True

    def _click(self, button: str | None, shown: dict[str, str] | None) -> Clicked:
        acted = None
        if button:
            quiz_setup_click(self.data, self.page_id, button, self.pages, self.handlers(), self.props)
            acted = follow_click(
                self.data, self.page_id, button, self.pages, self.variables, self.book_name, shown, call=self.call
            )
        if acted is None:
            acted = page_click(self.data, self.page_id, self.pages, self.variables, self.book_name, shown)
        if acted is None:
            if not button or not quiz_background(self.data, self.page_id):
                return Clicked(False)
            name = button.strip().lower()
            if name in LETTERS:
                self.letters[self._key()] = name
                return Clicked(False, checked=True)
            if name in _NEXT_QUESTION and self.props is not None and not self._ok_beeps(name):
                self.record_answer()
            result = quiz_click(self.pages, self.page_id, button, checked=self.letters.get(self._key()))
            asked = (result.request,) if result.request else ()
            if result.page_id == self.page_id:
                return Clicked(False, result.beep, asked)
            self.page_id = result.page_id
            self.fields = {}
            self.visible = {}
            return Clicked(True, result.beep, asked)
        beep, asked = acted.beeps > 0, acted.requests
        changed = bool(acted.fields or acted.visible)
        for name, text in acted.fields:
            self.fields[name] = text
        for key, shown_now in acted.visible:
            self.visible[key] = shown_now
        data, pages, book = self.data, self.pages, self.book
        if acted.book and acted.book.lower() != self.book_name.lower():
            book = self.find_book(acted.book, acted.page_id)
            data = book.read_bytes()
            pages = page_ids(data)
        page = _match(pages, acted.page_id)
        if page is None:
            return Clicked(False, beep, asked, changed)
        if book == self.book and page == self.page_id:
            return Clicked(False, beep, asked, changed)
        self.data, self.pages, self.book = data, pages, book
        self.page_id = page
        self.fields = {}
        self.visible = {}
        self.enter()
        return Clicked(True, beep, asked)

    def call(self, name: str) -> str | None:
        """The page a ``get name()`` line in a click goes to, or None.

        ``gotoMenuPage`` is the one call that opens a page.
        """
        from opentoolbook.menu import goto_menu_page

        if name.lower() != "gotomenupage":
            return None
        return goto_menu_page(self.handlers(), self.pages, self.props)

    def display(self, view_width: int, view_height: int, props: UserProperties | None = None):
        """The display list of the page on screen, after its ``enterPage``."""
        from opentoolbook.show import show_page

        return show_page(self.data, self.page_id, view_width, view_height, props, fields=self.fields, visible=self.visible, checked=self.checked_buttons())

    def checked_buttons(self) -> dict[str, bool]:
        """The letter states a click set on this page, for ``show_page``."""
        letter = self.letters.get(self._key())
        if letter is None:
            return {}
        return {name: name == letter for name in LETTERS}

    def letter_states(self) -> dict[str, bool]:
        """``checked of button`` for each letter: the click state, else the stored bit."""
        from opentoolbook.show import show_page

        listed = show_page(self.data, self.page_id, 1, 1, None, checked=self.checked_buttons())
        return {
            item.name.lower(): item.picture_role == "checked"
            for item in listed.items
            if item.kind == "button" and item.name.lower() in LETTERS
        }

    def record_answer(self) -> int | None:
        """Store this page's checked letter and score. None when nothing is stored."""
        from opentoolbook.quiz import questions
        from opentoolbook.quizscore import record_answer

        question = next((item for item in questions(self.data) if item.page_id == self.page_id), None)
        if question is None:
            return None
        return record_answer(
            self.props,
            self.letter_states(),
            question.answer,
            question.test_no,
            question.question_no,
        )

    def _ok_beeps(self, name: str) -> bool:
        """``OK`` with ``__quizPass`` in ``1,2`` and no letter beeps and returns 0 first."""
        from opentoolbook.quizscore import get_quiz_response

        if name != "ok" or self.props.get("__quizPass") not in (1, 2):
            return False
        return get_quiz_response(self.letter_states()) == ""

    def _key(self) -> tuple[str, str]:
        return (str(self.book or ""), self.page_id)

    def enter(self) -> None:
        """Run the ``enterPage`` of the page on screen and follow a quoted move."""
        from opentoolbook.entry import choose_opening

        for _hop in range(_HOPS):
            source = page_source(self.data, self.page_id)
            if not _enter_page(source):
                return
            page, other = choose_opening(
                self.pages,
                self.handlers(),
                {self.page_id: source},
                roots=self.roots(),
                book_name=self.book_name,
                startup=False,
                page_id=self.page_id,
                variables=self.variables,
            )
            data, pages, book = self.data, self.pages, self.book
            if other and other.lower() != self.book_name.lower():
                book = self.find_book(other, page)
                data = book.read_bytes()
                pages = page_ids(data)
            matched = next((item for item in pages if item.lower() == page.lower()), None)
            if matched is None:
                raise ValueError(f"{page} is not a page of {book.name if book else 'this book'}")
            if book == self.book and matched == self.page_id:
                return
            self.data, self.pages, self.book, self.page_id = data, pages, book, matched

    def handlers(self) -> dict[str, str]:
        """Handler bodies this book and the books it names define, by lower-case name."""
        from opentoolbook.entry import _companion_handlers, _handler_map

        key = self.book
        if key not in self._handlers:
            found: dict[str, str] = {}
            if self.book is not None:
                found.update(_companion_handlers(open_book(self.book, self.home)))
            found.update(_handler_map(self.data))
            self._handlers[key] = found
        return self._handlers[key]


def _match(pages: tuple[str, ...], page_id: str) -> str | None:
    for page in pages:
        if page.lower() == page_id.lower():
            return page
    return None
