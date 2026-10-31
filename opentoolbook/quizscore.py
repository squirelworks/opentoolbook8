"""The response and score a quiz question page stores when the quiz moves on.

The lines are in ``nc81test.sbk``. ``getQuizResponse`` walks
``ansiToChar(96 + i)`` from 1 to ``__quizMaxResponse`` and returns the
last letter whose button is checked, or empty. ``gotoNextQuestionEx``
begins::

    if  __quizPass <= 3  and  __quizIndex > 0  then
        response = getQuizResponse()
        score = 0
        if  response <> ""  then
            if  response = answer of this page  then
                score = 100
            end if
            get storeQuestionResponse(testNo of this page, questionNo of this page, response, score)
        ...

``storeQuestionResponse`` writes element ``__quizIndex`` of
``__quizAttempted`` (1), ``__quizTestNo``, ``__quizQuestionNo``,
``__quizResponse``, and ``__quizScore``. OpenScript compares strings
without case, so the lower-case letter matches an upper-case ``Answer``.
"""

from __future__ import annotations

from opentoolbook.props import UserProperties

# ``initializeTest`` sets ``__quizMaxResponse = 5``.
MAX_RESPONSE = 5


def get_quiz_response(checked: dict[str, bool], max_response: int = MAX_RESPONSE) -> str:
    """``getQuizResponse``: the last checked letter from ``a``, or empty."""
    states = {name.lower(): bool(value) for name, value in checked.items()}
    response = ""
    for index in range(1, max_response + 1):
        letter = chr(96 + index)
        if states.get(letter):
            response = letter
    return response


def answer_score(response: str, answer: str) -> int:
    """100 when ``response = answer of this page``, and 0 otherwise."""
    return 100 if response.lower() == answer.strip().lower() else 0


def store_question_response(
    props: UserProperties,
    test: int | str,
    question: int | str,
    response: str,
    score: int,
) -> int:
    """``storeQuestionResponse``: element ``__quizIndex`` of the five arrays. Returns 0."""
    index = _int(props.get("__quizIndex"))
    for name, value in (
        ("__quizAttempted", 1),
        ("__quizTestNo", _number(test)),
        ("__quizQuestionNo", _number(question)),
        ("__quizResponse", response),
        ("__quizScore", score),
    ):
        table = props.get(name)
        stored = dict(table) if isinstance(table, dict) else {}
        stored[index] = value
        props.set(name, stored)
    return 0


def record_answer(
    props: UserProperties,
    checked: dict[str, bool],
    answer: str,
    test: int | str,
    question: int | str,
) -> int | None:
    """The first block of ``gotoNextQuestionEx`` for a checked letter.

    Returns the stored score, or None when that block stores no response:
    ``__quizPass`` is above 3, ``__quizIndex`` is 0, or no letter is
    checked. The skipped branch is not this function.
    """
    if _int(props.get("__quizPass")) > 3 or _int(props.get("__quizIndex")) <= 0:
        return None
    response = get_quiz_response(checked)
    if not response:
        return None
    score = answer_score(response, answer)
    store_question_response(props, test, question, response, score)
    return score


def _int(value: object) -> int:
    return value if isinstance(value, int) and not isinstance(value, bool) else 0


def _number(value: int | str) -> int | str:
    if isinstance(value, str) and value.strip().lstrip("-").isdigit():
        return int(value.strip())
    return value
