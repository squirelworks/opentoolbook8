"""The book and page a window is on, and what one button click does to them.

This is the click path of the Tk window without the window. A button
whose ``buttonClick`` quotes a page opens that page. A quoted ``of book``
is found with the same search as opening a book: the book directory, its
parent, ``--home``, ``--home/courses``, and ``--home/Nida98/Lessons``,
regardless of case. A file that search does not find is an error that
names the file and the page. A quiz button on a page whose background
calls ``handleQuizClick`` uses the stored page list. A letter button on
that page, ``A`` through ``E``, is ``manageQuizButtons``: the letter is
checked and every other letter on the page is unchecked. The page stays.
With a ``props`` store, ``OK`` and ``Next`` there run the first block of
``gotoNextQuestionEx`` before the page changes: the checked letter and its
score go into ``__quizResponse`` and ``__quizScore`` at ``__quizIndex``.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from opentoolbook.click import follow_click, quiz_background
from opentoolbook.field import page_ids
from opentoolbook.quiznav import quiz_click
from opentoolbook.shelf import find_file, search_roots


# ``initializeTest`` sets ``__quizMaxResponse`` to 5, and
# ``manageQuizButtons`` walks ``ansiToChar(96 + i)`` up to it.
LETTERS = ("a", "b", "c", "d", "e")
# ``handleQuizClick`` calls ``gotoNextQuestionEx`` for these. ``Skip`` with a
# checked letter asks first, and without one stores nothing here.
_NEXT_QUESTION = ("ok", "next")


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
    checked: bool = False


class Navigator:
    """The window's book, page, and search roots."""

    def __init__(
        self,
        data: bytes,
        page_id: str,
        book: Path | str | None = None,
        home: Path | str | None = None,
        props=None,
    ) -> None:
        self.data = data
        self.pages = page_ids(data)
        self.page_id = page_id
        self.book = Path(book) if book else None
        self.home = Path(home) if home else None
        self.letters: dict[tuple[str, str], str] = {}
        # The ``__`` store a quiz click writes its response and score into.
        self.props = props

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

    def checked_buttons(self) -> dict[str, bool]:
        """The letter states a click set on this page, for ``show_page``."""
        letter = self.letters.get(self._key())
        if letter is None:
            return {}
        return {name: name == letter for name in LETTERS}

    def letter_states(self) -> dict[str, bool]:
        """``checked of button`` for each letter: the click state, else the stored bit."""
        from opentoolbook.show import show_page

        listed = show_page(self.data, self.page_id, 1, 1, None, self.checked_buttons())
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

    def click(self, button: str) -> Clicked:
        """Run the named button's click. The page and book change in place."""
        acted = follow_click(self.data, self.page_id, button, self.pages)
        if acted is None:
            if not quiz_background(self.data, self.page_id):
                return Clicked(False)
            name = button.strip().lower()
            if name in LETTERS:
                self.letters[self._key()] = name
                return Clicked(False, checked=True)
            if name in _NEXT_QUESTION and self.props is not None and not self._ok_beeps(name):
                self.record_answer()
            result = quiz_click(self.pages, self.page_id, button, checked=self.letters.get(self._key()))
            if result.page_id == self.page_id:
                return Clicked(False, result.beep)
            self.page_id = result.page_id
            return Clicked(True, result.beep)
        data, pages, book = self.data, self.pages, self.book
        if acted.book and acted.book.lower() != self.book_name.lower():
            book = self.find_book(acted.book, acted.page_id)
            data = book.read_bytes()
            pages = page_ids(data)
        if acted.page_id not in pages:
            return Clicked(False)
        if book == self.book and acted.page_id == self.page_id:
            return Clicked(False)
        self.data, self.pages, self.book = data, pages, book
        self.page_id = acted.page_id
        return Clicked(True)
