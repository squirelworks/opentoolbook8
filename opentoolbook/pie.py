"""A class ``0x12`` pie as the words it stores.

On ``otb-pie.tbk`` a pie record runs from its id word to the next
object's header. The word before the class word is that end, as for the
other draw objects, and the record length by that formula is 59. The
last object in a directory record stores 1 there, and it runs to the end
of the record instead. The four signed words at ``+0x0F`` are the bounds.
The eight signed words from ``+0x25`` are returned as stored. They are
not a settled point list, and the window does not draw a wedge.
"""

from __future__ import annotations

import struct

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
