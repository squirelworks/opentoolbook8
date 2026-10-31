"""Windows and ToolBook DLL shims for ``linkDLL`` / ``linkDLL32``.

Only the names listed here are answered. An unknown linked function
returns empty from the engine and the script continues. NIDA DLLs are
not shimmed here.
"""

from __future__ import annotations

import time

# Libraries this table covers, lower-case, with and without ``.dll``.
_KERNEL = frozenset({"kernel32.dll", "kernel32"})
_USER = frozenset({"user32.dll", "user32"})
_TBFILE = frozenset({"tbfile32.dll", "tbfile32", "tbfile.dll", "tbfile"})

# user32 calls that books link and that this reader treats as no-ops.
_USER_NOOP = frozenset(
    {
        "messageboxa",
        "messageboxw",
        "messagebox",
        "sendmessagea",
        "sendmessagew",
        "sendmessage",
        "postmessagea",
        "postmessagew",
        "postmessage",
        "setwindowtexta",
        "setwindowtextw",
        "showwindow",
        "updatewindow",
        "enablewindow",
        "setfocus",
        "getfocus",
        "bringwindowtotop",
    }
)

# Fixed SM_CXSCREEN / SM_CYSCREEN when the host has no display size.
_SCREEN = (1024, 768)

# Win98-style GetVersion: major 4, minor 10, platform NT bit clear, Win32s clear.
_WIN98_VERSION = 0xC0000A04


def shim(library: str, name: str, args: tuple) -> tuple[bool, object] | None:
    """``(answered, value)`` for a known shim, or ``None`` when this table has no entry.

    ``library`` may be empty when the engine asks by bare name after a
    ``linkDLL`` miss. A match on the function name alone is enough for the
    names in this table.
    """
    lib = library.strip().lower()
    key = name.strip().lower()
    if key == "gettickcount" and (not lib or lib in _KERNEL):
        return True, int(time.monotonic() * 1000) & 0xFFFFFFFF
    if key == "getversion" and (not lib or lib in _KERNEL):
        return True, _WIN98_VERSION
    if key == "getsystemmetrics" and (not lib or lib in _USER):
        index = int(args[0]) if args else 0
        if index == 0:
            return True, _SCREEN[0]
        if index == 1:
            return True, _SCREEN[1]
        return True, 0
    if key in _USER_NOOP and (not lib or lib in _USER):
        return True, 0
    return None
