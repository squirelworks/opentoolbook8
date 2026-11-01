"""A class ``0x12`` pie as the geometry words it shares with an arc.

On ``otb-pie.tbk`` a pie record runs from its id word to the next
object's header. The word before the class word is that end, as for the
other draw objects, and the record length by that formula is 59. The
last object in a directory record stores 1 there, and it runs to the end
of the record instead. The four signed words at ``+0x0F`` are the bounds.

The eight signed words from ``+0x25`` are the same five fields a class
``0x11`` arc stores: the signed pairs at ``+0x25`` and ``+0x29``, the
center at ``+0x2D``, and the half-width and half-height at ``+0x31`` and
``+0x33``. ``TB80BAS`` ``FUN_10d8_0d58`` and ``FUN_12d0_06d8`` read those
offsets for both class ``0x11`` and class ``0x12``. Message ``0x4123`` in
``FUN_13d0_0128`` writes the two pairs from angles onto that ellipse.
The reader returns those fields. The window does not fill a wedge: both
pies on ``otb-pie.tbk`` store a zero radius on one axis, and the second
``draw pie`` point is not among the pairs.
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
class Pie:
    """One class ``0x12`` record: bounds and the five arc geometry fields."""

    object_id: int
    bounds: tuple[int, int, int, int]
    points: tuple[tuple[int, int], tuple[int, int]]
    center: tuple[int, int]
    radii: tuple[int, int]


def pie_record(data: bytes, at: int) -> Pie:
    """Bounds plus the five fields ``TB80BAS`` reads for class ``0x12``."""
    words = pie_words(data, at)
    return Pie(
        struct.unpack_from("<H", data, at)[0],
        pie_bounds(data, at),
        ((words[0], words[1]), (words[2], words[3])),
        (words[4], words[5]),
        (words[6], words[7]),
    )


@dataclass(frozen=True)
class PieWords:
    """The eight stored words read as the draw-pie pairs on ``otb-pie.tbk``.

    On both pies there those pairs coincide with the arc slots: the third
    ``draw pie`` point, the first point, the third again, and the reach.
    That coincidence is how the fixture was drawn; the engine names the
    slots as in :class:`Pie`.
    """

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
