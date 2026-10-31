"""A class ``0x12`` pie as the words it stores.

On ``otb-pie.tbk`` a pie record runs from its id word to the next
object's header. The word before the class word is that end, as for the
other draw objects, and the record length by that formula is 59. The
last object in a directory record stores 1 there, and it runs to the end
of the record instead. The four signed words at ``+0x0F`` are the bounds.
The eight signed words from ``+0x25`` are returned as stored. They are
not a settled point list, and the window does not draw a wedge.

On both pies of ``otb-pie.tbk`` the words read as four pairs: the third
point given to ``draw pie``, the first point, the third point again, and
the distance from the first point to the third on each axis. The second
point is not stored. Both pies have a zero distance on one axis, and the
words of pie id 0 did not follow its new bounds, so the pairs do not name
a wedge.
"""

from __future__ import annotations

import struct
from dataclasses import dataclass

PIE = 0x12
# The end-word formula on pie id 0 of otb-pie.tbk.
PIE_BYTES = 59
WORDS = 8


def pie_bounds(data: bytes, at: int) -> tuple[int, int, int, int]:
    left, top, right, bottom = struct.unpack_from("<hhhh", data, at + 0x0F)
    return left, top, right, bottom


def pie_words(data: bytes, at: int) -> tuple[int, ...]:
    """The eight signed words from ``+0x25``."""
    if at + 0x25 + 2 * WORDS > len(data):
        raise ValueError("pie words are past the file")
    return struct.unpack_from(f"<{WORDS}h", data, at + 0x25)


@dataclass(frozen=True)
class PieWords:
    """The eight stored words read as four pairs."""

    third: tuple[int, int]
    first: tuple[int, int]
    third_again: tuple[int, int]
    reach: tuple[int, int]


def pie_pairs(words: tuple[int, ...]) -> PieWords:
    """Split the eight words. This names the stored order; it does not draw."""
    if len(words) != WORDS:
        raise ValueError("a pie stores eight words")
    return PieWords(
        (words[0], words[1]),
        (words[2], words[3]),
        (words[4], words[5]),
        (words[6], words[7]),
    )
