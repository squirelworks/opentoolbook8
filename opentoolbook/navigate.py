"""The book and page a window is on, and what one button click does to them.

This is the click path of the Tk window without the window. A button
whose ``buttonClick`` quotes a page opens that page. A quoted ``of book``
is found with the same search as opening a book: the book directory, its
parent, ``--home``,
regardless of case. After the window changes books, the search still
starts from the lesson the user opened, then the book on screen, then
``--home``. A file that search does not find is an error that names the
file and the page, in the same sentence as the open:
``nida81.tbk was not found; P310 of that book does not open``. A click
runs on the OpenScript interpreter (``clickrun.send_click``): the
message goes to the object, the groups that hold it, the page, the
background, the book and then each ``sysBooks`` book, until a handler
takes it. On a page whose background calls ``handleQuizClick`` the path
stops at the page for now, and a quiz button uses the stored page list. A letter button on
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

from opentoolbook.click import object_handler, quiz_background
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
        sysbooks: tuple[str, ...] = (),
    ) -> None:
        self.data = data
        # ``sysBooks`` startup left, first item first. Their handlers follow the book's.
        self.sysbooks = tuple(sysbooks)
        self.pages = page_ids(data)
        self.page_id = page_id
        self.book = Path(book) if book else None
        self.home = Path(home) if home else None
        # The path the user passed. It stays when the window changes books.
        self.lesson = Path(lesson) if lesson else self.book
        # System variables a handler this runner executed assigned, by lower-case name.
        self.variables: dict[str, object] = {key.lower(): value for key, value in (variables or {}).items()}
        self._handlers: dict[Path | None, dict[str, str]] = {}
        self._chains: dict = {}
        # The __ names this window's handlers read and write.
        self.props = props if props is not None else UserProperties()
        # Pages shown before this one, oldest first: (book, page id, book bytes).
        self.history: list[tuple[Path | None, str, bytes]] = []
        # Field text a click wrote, by field name. Cleared when the page changes.
        self.fields: dict[str, str] = {}
        # Objects a click hid or showed, by (kind, name or id). Cleared when the page changes.
        self.visible: dict[tuple[str, str | int], bool] = {}
        self.letters: dict[tuple[str, str], str] = {}
        # Buttons a buttonDown or buttonUp handler set the invert of, by lower-case name.
        self.inverted: dict[str, bool] = {}

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
        self.inverted = {}
        return True

    def _click(self, button: str | None, shown: dict[str, str] | None) -> Clicked:
        acted = self._send(("button", button) if button else None, "buttonclick", shown)
        if acted is None:
            if not button or not quiz_background(self.data, self.page_id):
                return Clicked(False)
            name = button.strip().lower()
            if name in LETTERS:
                self.letters[self._key()] = name
                return Clicked(False, checked=True)
            if name in _NEXT_QUESTION and self.props is not None and not self._ok_beeps(name):
                self.record_answer()
            result = self.quiz_click(button)
            asked = (result.request,) if result.request else ()
            if result.page_id == self.page_id:
                return Clicked(False, result.beep, asked)
            self.page_id = result.page_id
            self.fields = {}
            self.visible = {}
            self.inverted = {}
            return Clicked(True, result.beep, asked)
        return self._apply(acted)

    def message(self, kind: str, name: str, message: str, shown: dict[str, str] | None = None) -> Clicked | None:
        """Send ``buttonDown`` or ``buttonUp`` to one object. None when its script has no such handler.

        ``kind`` is ``button`` or ``field``. ``set invert of button`` lines
        go to ``inverted``. ``isObject`` asks the page on screen.
        """
        source = object_handler(self.data, self.page_id, kind, name, message)
        if source is None:
            return None
        before = (self.book, self.page_id, self.data)
        acted = self._send((kind, name), message.lower(), shown)
        if acted is None:
            return None
        result = self._apply(acted)
        if result.moved:
            self.history.append(before)
        return result

    def _send(self, target: tuple[str, str] | None, message: str, shown: dict[str, str] | None):
        """Send ``message`` along the object path on the interpreter. None when nothing takes it."""
        from opentoolbook.clickrun import send_click
        from opentoolbook.show import show_page

        listed = show_page(self.data, self.page_id, 1, 1, None)
        present = {(item.kind, item.name.lower()) for item in listed.items if item.name}
        groups: tuple[str, ...] = ()
        if target is not None:
            for item in listed.items:
                if item.kind == target[0] and item.name.lower() == target[1].lower():
                    groups = item.groups
                    break
        return send_click(
            self.data,
            self.page_id,
            self.pages,
            self.book_name,
            self.roots(),
            [handlers for _book, handlers in self.chain().books],
            target,
            props=self.props,
            variables=self.variables,
            sysbooks=list(self.sysbooks),
            fields=shown,
            present=present,
            message=message,
            groups=groups,
            # The quiz background's buttonClick still goes to the reader's quiz path.
            beyond_page=not quiz_background(self.data, self.page_id),
        )

    def _apply(self, acted) -> Clicked:
        beep, asked = acted.beeps > 0, acted.requests
        for button, inverted in acted.inverts:
            self.inverted[button.lower()] = inverted
        changed = bool(acted.fields or acted.visible or acted.inverts)
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
        self.inverted = {}
        self.enter()
        return Clicked(True, beep, asked)

    def quiz_click(self, button: str):
        """``get handleQuizClick(target)``, the one line of shared script 103's ``buttonClick``.

        ``__quizPass`` comes from the store. On a running pass the store and
        each question page's ``QuestionNo`` go to ``gotoNextQuestionEx``.
        """
        from opentoolbook.quiz import questions

        quiz_pass = self.props.get("__quizPass")
        if not isinstance(quiz_pass, int) or isinstance(quiz_pass, bool):
            quiz_pass = None
        numbers = None
        if quiz_pass in (1, 2, 3):
            numbers = {
                item.page_id: int(item.question_no)
                for item in questions(self.data)
                if item.question_no.strip().isdigit()
            }
        return quiz_click(
            self.pages,
            self.page_id,
            button,
            quiz_pass=quiz_pass,
            checked=self.letters.get(self._key()),
            props=self.props if numbers is not None else None,
            question_numbers=numbers,
            script=self.handlers().get("handlequizclick", ""),
        )

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

        from opentoolbook.show import pressed

        listed = show_page(self.data, self.page_id, view_width, view_height, props, fields=self.fields, visible=self.visible, checked=self.checked_buttons())
        for name, inverted in self.inverted.items():
            if inverted:
                listed = pressed(self.data, listed, name)
        return listed

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
                props=self.props,
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

    def chain(self):
        """Handler maps by book: this book's, then each ``sysBooks`` book's."""
        from opentoolbook.send import handler_chain

        key = self.book
        if not hasattr(self, "_chains"):
            self._chains = {}
        if key not in self._chains:
            self._chains[key] = handler_chain(self.data, self.book_name, self.roots(), self.sysbooks)
        return self._chains[key]

    def handlers(self) -> dict[str, str]:
        """Handler bodies by lower-case name: this book's, then each ``sysBooks`` book's."""
        key = self.book
        if key not in self._handlers:
            self._handlers[key] = self.chain().merged()
        return self._handlers[key]


def _match(pages: tuple[str, ...], page_id: str) -> str | None:
    for page in pages:
        if page.lower() == page_id.lower():
            return page
    return None
