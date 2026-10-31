"""The question pool the quiz menu groups build in ``nc81test.sbk``.

``clearPool`` sets ``__poolCount`` and ``__poolQuestions`` to 0 and
empty at elements 1 through 10. ``addObjectiveToPool(obj, start, stop,
count)`` stores the numbers ``start`` through ``stop`` as one comma list
at element ``obj`` of ``__poolQuestions``, and ``count`` at element
``obj`` of ``__poolCount``. ``setupPool`` passes every objective whose
count is not 0 to ``addQuestionsFromPool``. That handler picks ``count``
different positions in the list with ``addToRandomSetX`` and appends
the question numbers at those positions to ``__quizNumbers``, counting
``__quizCount`` up and setting ``__quizIndex`` to 0. ``getNextQuestion``
copies ``__quizCount`` and ``__quizIndex`` into ``__xCount`` and
``__xIndex`` and calls ``getNextRandomX``, which returns -1 at the end
and otherwise the next stored question number. A question number is not
a page id.

OpenScript ``random(n)`` is a whole number from 1 to ``n``. The reader
draws it from the ``random.Random`` it is given, so a seeded generator
gives the same pool every time. The ``__lessonMode = 6`` branch of
``setupPool`` reads ``__menuOption``, which ``initializeBase`` fills from
``NIDAREC.INI`` through a DLL. ``__lessonMode`` is unset, so that branch
is not taken.
"""

from __future__ import annotations

import random as _random
import re

from opentoolbook.props import UserProperties

_OBJECTIVES = 10
_SET_LIMIT = 200


def clear_pool(props: UserProperties) -> int:
    """``clearPool``. Returns 0."""
    props.set("__poolCount", {index: 0 for index in range(1, _OBJECTIVES + 1)})
    props.set("__poolQuestions", {index: "" for index in range(1, _OBJECTIVES + 1)})
    return 0


def add_objective_to_pool(props: UserProperties, obj: int, start: int, stop: int, count: int) -> int:
    """``addObjectiveToPool(obj, start, stop, count)``. Returns 0."""
    counts = dict(_table(props, "__poolCount"))
    questions = dict(_table(props, "__poolQuestions"))
    counts[obj] = count
    questions[obj] = ",".join(str(number) for number in range(start, stop + 1))
    props.set("__poolCount", counts)
    props.set("__poolQuestions", questions)
    return 0


def setup_pool(props: UserProperties, rng: _random.Random) -> int:
    """``setupPool``. Returns 0. The ``__lessonMode = 6`` branch is not run."""
    counts = _table(props, "__poolCount")
    questions = _table(props, "__poolQuestions")
    for obj in range(1, _OBJECTIVES + 1):
        count = counts.get(obj, 0)
        if count:
            add_questions_from_pool(props, str(questions.get(obj, "")), int(count), rng)
    return 0


def add_questions_from_pool(props: UserProperties, pool: str, count: int, rng: _random.Random) -> int:
    """``addQuestionsFromPool(pool, count)``. Returns ``addToRandomSetX``'s error."""
    props.set("__quizIndex", 0)
    words = pool.replace(",", " ").split()
    numbers: dict[int, int] = {}
    props.set("__xCount", 0)
    props.set("__xIndex", 0)
    error = add_to_random_set_x(props, numbers, 1, len(words), count, rng)
    quiz = dict(_table(props, "__quizNumbers"))
    total = _int(props.get("__quizCount"))
    for index in range(1, count + 1):
        total += 1
        position = numbers.get(index, -1)
        word = words[position - 1] if 1 <= position <= len(words) else ""
        quiz[total] = int(word) if re.fullmatch(r"-?\d+", word) else word
    props.set("__quizCount", total)
    props.set("__quizNumbers", quiz)
    return error


def add_to_random_set_x(
    props: UserProperties,
    numbers: dict[int, int],
    start: int,
    stop: int,
    count: int,
    rng: _random.Random,
) -> int:
    """``addToRandomSetX``: ``count`` different numbers from ``start`` to ``stop``."""
    base = _int(props.get("__xCount"))
    if base + count > _SET_LIMIT or count > stop - start + 1:
        return 1
    for step in range(1, count + 1):
        r = _openscript_random(rng, stop - start + 1) + start - 1
        while True:
            if all(numbers.get(base + j) != r for j in range(1, step + 1)):
                numbers[base + step] = r
                break
            r += 1
            if r > stop:
                r = start
    props.set("__xCount", base + count)
    props.set("__xIndex", 0)
    return 0


def get_next_question(props: UserProperties) -> int:
    """``getNextQuestion``: the next question number, or -1 after the last."""
    props.set("__xCount", _int(props.get("__quizCount")))
    props.set("__xIndex", _int(props.get("__quizIndex")))
    found = get_next_random_x(props, _table(props, "__quizNumbers"))
    props.set("__quizCount", props.get("__xCount"))
    props.set("__quizIndex", props.get("__xIndex"))
    return found


def get_next_random_x(props: UserProperties, numbers: dict) -> int:
    """``getNextRandomX``: -1 when ``__xIndex`` reached ``__xCount``."""
    index = _int(props.get("__xIndex"))
    if index >= _int(props.get("__xCount")):
        return -1
    index += 1
    props.set("__xIndex", index)
    found = numbers.get(index, -1)
    return found if isinstance(found, int) else -1


_POOL_LINE = re.compile(
    r"^(?:get\s+|[a-z_][a-z0-9_]*\s*=\s*|if\s+)"
    r"(clearpool|addobjectivetopool|setuppool)\s*\(([^)]*)\)",
    re.IGNORECASE,
)


def pool_from_click(source: str, props: UserProperties, rng: _random.Random) -> int | None:
    """Run a menu group's ``clearpool``, ``addObjectiveToPool``, and ``setuppool`` lines in order.

    Returns ``setuppool``'s value, or None when the handler calls no pool function.
    """
    result = None
    for line in source.splitlines():
        found = _POOL_LINE.match(" ".join(line.strip().split()))
        if found is None:
            continue
        name = found.group(1).lower()
        if name == "clearpool":
            clear_pool(props)
        elif name == "addobjectivetopool":
            values = [int(part) for part in found.group(2).split(",") if part.strip()]
            if len(values) == 4:
                add_objective_to_pool(props, *values)
        else:
            result = setup_pool(props, rng)
    return result


def _openscript_random(rng: _random.Random, limit: int) -> int:
    return rng.randint(1, max(1, limit))


def _table(props: UserProperties, name: str) -> dict:
    found = props.get(name)
    return found if isinstance(found, dict) else {}


def _int(value: object) -> int:
    return value if isinstance(value, int) and not isinstance(value, bool) else 0


def goto_next_question_ex(
    props: UserProperties,
    pages: tuple[str, ...],
    question_numbers: dict[str, int],
) -> str | None:
    """The page ``gotoNextQuestionEx`` opens on a running pass 1, 2, or 3.

    ``question_numbers`` maps a page id to its stored ``QuestionNo``. The
    page is the first one from ``__quizStartPage`` on whose question number
    is ``getNextQuestion``'s result. After the last question, pass 1 opens
    ``__quizPages`` element 3, 1, or 2 by ``__quizMode`` 0, 1, or 2, pass 2
    opens element 1 or 2 by mode 1 or 2, and pass 3 opens element 2 on
    mode 2. None when the handler names no page.
    """
    quiz_pass = _int(props.get("__quizPass"))
    if quiz_pass not in (1, 2, 3):
        return None
    number = get_next_question(props)
    if quiz_pass == 2:
        responses = _table(props, "__quizResponse")
        while number != -1 and responses.get(_int(props.get("__quizIndex")), "") != "":
            number = get_next_question(props)
    if number >= 0:
        start = max(1, _int(props.get("__quizStartPage")))
        for page_id in pages[start - 1:]:
            if question_numbers.get(page_id) == number:
                return page_id
        return None
    mode = _int(props.get("__quizMode"))
    element = {
        1: {0: 3, 1: 1, 2: 2},
        2: {1: 1, 2: 2},
        3: {2: 2},
    }[quiz_pass].get(mode)
    if element is None:
        return None
    found = _table(props, "__quizPages").get(element)
    return found if isinstance(found, str) and found else None
