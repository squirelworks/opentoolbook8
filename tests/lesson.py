"""The private lesson the extra tests read. None of these files are checked in.

``OPENTOOLBOOK_TBK`` names the lesson. Its companions (``nida81.tbk`` and the
four ``nc81*.sbk`` books) are found the way ``open_book`` finds them: the
lesson directory, then its parent, case-insensitive. A disc copy keeps
``NC81RECS.SBK`` in upper case and the logo book one directory up, and the
tests read that layout as it is.
"""

from __future__ import annotations

import os
from pathlib import Path

from opentoolbook.shelf import find_file, search_roots

SKIP = "set OPENTOOLBOOK_TBK to 9e954d01.tbk"


def lesson_path() -> Path | None:
    """The lesson file, or ``None`` when the variable is unset or names no file."""
    value = os.environ.get("OPENTOOLBOOK_TBK")
    if not value or not os.path.isfile(value):
        return None
    return Path(value)


def companion(lesson: str | os.PathLike, name: str) -> Path:
    """The file ``name`` on the lesson's shelf.

    When the shelf has no such file the result is the path beside the
    lesson, which does not exist, so a test's own ``is_file`` check decides.
    """
    lesson = Path(lesson)
    found = find_file(search_roots(lesson, None), name)
    return found if found is not None else lesson.with_name(name)
