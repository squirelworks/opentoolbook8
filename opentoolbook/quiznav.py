"""One click on a quiz page.

Pass 1 or 2 with no choice is the ``OK`` handler: ``beep(1)`` and
``return 0``. The page stays. A list-opened page has no quiz running, so
``OK``, ``Next``, and ``Skip`` are the next page and ``Back`` is the
previous page. ``__quizPass`` 8 is the same pair of pages: ``send next``
and ``send previous``. A chosen answer does not pick a question. That
call is ``getNextQuestion``, and it returns a random pool entry.
"""

from __future__ import annotations

from dataclasses import dataclass

_NEXT = {"ok", "next", "skip"}


@dataclass(frozen=True)
class QuizClick:
    """The page after the click, and whether the script beeps."""

    page_id: str
    beep: bool
    request: str | None = None


def quiz_click(
    pages: tuple[str, ...],
    page_id: str,
    button: str,
    *,
    quiz_pass: int | None = None,
    checked: str | None = None,
    script: str | None = None,
) -> QuizClick:
    """Apply one named button on ``page_id``.

    ``quiz_pass`` ``None`` means no quiz is running. ``checked`` is the
    letter the script has checked, or empty when the reader has not.
    ``script`` is ``handleQuizClick``. The ``Skip`` request text comes from it.
    """
    name = button.strip().lower()
    choice = (checked or "").strip()
    if quiz_pass in (1, 2) and name == "ok":
        if not choice:
            return QuizClick(page_id, True)
        return QuizClick(page_id, False)
    if quiz_pass == 8 and name == "skip" and choice:
        return QuizClick(page_id, True, skip_request(script or ""))
    if quiz_pass not in (None, 8):
        return QuizClick(page_id, False)
    if name in _NEXT:
        return QuizClick(_adjacent(pages, page_id, 1), False)
    if name == "back":
        return QuizClick(_adjacent(pages, page_id, -1), False)
    return QuizClick(page_id, False)


def _adjacent(pages: tuple[str, ...], page_id: str, step: int) -> str:
    try:
        index = pages.index(page_id)
    except ValueError:
        return page_id
    moved = index + step
    if moved < 0 or moved >= len(pages):
        return page_id
    return pages[moved]


def skip_request(script: str) -> str | None:
    """The ``request`` text of the ``Skip`` branch when a letter is checked."""
    from opentoolbook.walk import Flow, block_if, is_beep, norm, request_text, split_if, walk

    lines = script.splitlines()
    for index, line in enumerate(lines):
        test = block_if(norm(line))
        if test is None or test.replace(" ", "") != 'nameofvtargetis"skip"':
            continue
        taken, _skipped, _end = split_if(lines, index + 1)
        asked: list[str] = []

        def condition(text: str) -> bool | None:
            return True if text.replace(" ", "") == 'response<>""' else None

        def statement(raw: str, _low: str) -> None:
            if is_beep(raw):
                return
            text = request_text(raw)
            if text is not None:
                asked.append(text)

        walk(taken, Flow(), condition=condition, statement=statement)
        return asked[0] if asked else None
    return None
