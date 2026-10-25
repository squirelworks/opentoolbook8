"""The page width and height stored on the book record.

The word at ``+0x20`` is the width. The word at ``+0x1E`` is the height.
Both are signed. A blank Instructor 8.1 book stores 9000 and 6000. Both
NIDA lessons store 9360 and 6624.
"""

from __future__ import annotations

import struct

from opentoolbook.field import _book, _segments


def page_size(data: bytes) -> tuple[int, int]:
    """``(width, height)`` from the book record."""
    segments = _segments(data)
    _segment, record = _book(data, segments)
    height, width = struct.unpack_from("<hh", data, record + 0x1E)
    return width, height
