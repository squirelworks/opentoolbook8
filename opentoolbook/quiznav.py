"""One click on a quiz page.

Pass 1 or 2 with no choice is the ``OK`` handler: ``beep(1)`` and
``return 0``. The page stays. A list-opened page has no quiz running, so
``OK``, ``Next``, and ``Skip`` are the next page and ``Back`` is the
previous page. ``__quizPass`` 8 is the same pair of pages: ``send next``
and ``send previous``. A chosen answer does not pick a question. That
call is ``getNextQuestion``, and it returns a random pool entry. On a
running pass 1, 2, or 3, ``OK`` with a letter, ``Next``, and ``Skip``
with no letter run ``gotoNextQuestionEx``: the page is the one whose
``QuestionNo`` is that entry. ``Back`` on those passes stays. ``gotoNextQuestionEx`` and
``gotoPreviousQuestionEx`` call ``setupQuizPage`` on the page they open,
and that handler sets whether the rectangle ``Correct`` is visible.
"""

from __future__ import annotations

from dataclasses import dataclass

_NEXT = {"ok", "next", "skip"}


@dataclass(frozen=True)
class QuizClick:
    """The page after the click, and whether the script beeps."""

    page_id: str
    beep: bool
    correct: bool | None = None


def quiz_click(
    pages: tuple[str, ...],
    page_id: str,
    button: str,
    *,
    quiz_pass: int | None = None,
    checked: str | None = None,
    props=None,
    question_numbers: dict[str, int] | None = None,
) -> QuizClick:
    """Apply one named button on ``page_id``.

    ``quiz_pass`` ``None`` means no quiz is running. ``checked`` is the
    letter the script has checked, or empty when the reader has not.
    With ``props`` and ``question_numbers``, a running pass 1, 2, or 3
    goes to the page ``gotoNextQuestionEx`` names.
    """
    name = button.strip().lower()
    choice = (checked or "").strip()
    if quiz_pass in (1, 2) and name == "ok":
        if not choice:
            return QuizClick(page_id, True)
        if props is None:
            return QuizClick(page_id, False)
    if quiz_pass in (1, 2, 3) and props is not None and question_numbers is not None:
        if name == "skip" and choice:
            return QuizClick(page_id, True)
        if name in _NEXT:
            from opentoolbook.pool import goto_next_question_ex

            found = goto_next_question_ex(props, pages, question_numbers)
            if found in pages and found in question_numbers:
                return QuizClick(found, False, setup_quiz_page_correct(quiz_pass))
            return QuizClick(found if found in pages else page_id, False)
        return QuizClick(page_id, False)
    if quiz_pass == 8 and name in _NEXT | {"back"} and not (name == "skip" and choice):
        moved = _adjacent(pages, page_id, -1 if name == "back" else 1)
        return QuizClick(moved, False, setup_quiz_page_correct(8) if moved != page_id else None)
    if quiz_pass == 8 and name == "skip" and choice:
        return QuizClick(page_id, True)
    if quiz_pass not in (None, 8):
        return QuizClick(page_id, False)
    if name in _NEXT:
        return QuizClick(_adjacent(pages, page_id, 1), False)
    if name == "back":
        return QuizClick(_adjacent(pages, page_id, -1), False)
    return QuizClick(page_id, False)


def setup_quiz_page_correct(quiz_pass: int | None, reader: bool = True) -> bool | None:
    """What ``setupQuizPage`` sets ``visible of rectangle("correct")`` to.

    The author level shows it. On the reader level pass 1, 2, and 3 hide
    it, and pass 4, 5, and 8 show it. Any other pass leaves it alone.
    """
    if not reader:
        return True
    if quiz_pass in (1, 2, 3):
        return False
    if quiz_pass in (4, 5, 8):
        return True
    return None


def _adjacent(pages: tuple[str, ...], page_id: str, step: int) -> str:
    try:
        index = pages.index(page_id)
    except ValueError:
        return page_id
    moved = index + step
    if moved < 0 or moved >= len(pages):
        return page_id
    return pages[moved]
