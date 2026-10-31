"""Windows/ToolBook DLL shims answer known names; unknown linked calls continue."""

from __future__ import annotations

import unittest

from opentoolbook.dllshims import shim
from opentoolbook.openscript.interp import Engine, Host
from opentoolbook.openscript.parser import parse_script
from opentoolbook.run import BookHost


def _engine(source: str, host=None):
    books = [parse_script(source).handlers]

    def lookup(kind, name):
        key = f"{kind} {name}"
        return [book[key] for book in books if key in book]

    return Engine(lookup, host or BookHost((), "book.tbk", ()))


class ShimTable(unittest.TestCase):
    def test_gettickcount_and_getversion(self):
        ticks = shim("kernel32.dll", "GetTickCount", ())
        self.assertTrue(ticks[0])
        self.assertIsInstance(ticks[1], int)
        version = shim("KERNEL32", "GetVersion", ())
        self.assertEqual(version, (True, 0xC0000A04))

    def test_getsystemmetrics_and_user32_noop(self):
        self.assertEqual(shim("user32.dll", "GetSystemMetrics", (0,)), (True, 1024))
        self.assertEqual(shim("user32.dll", "GetSystemMetrics", (1,)), (True, 768))
        self.assertEqual(shim("user32.dll", "MessageBoxA", ("", "", 0)), (True, 0))
        self.assertIsNone(shim("nc81rec.dll", "openSession32", ()))


class BookHostShims(unittest.TestCase):
    def test_linked_gettickcount_returns_a_number(self):
        engine = _engine(
            "to get f\n"
            '  linkDLL32 "kernel32.dll"\n'
            "    DWORD GetTickCount()\n"
            "  end\n"
            "  return GetTickCount()\n"
            "end\n"
        )
        value = engine.get("f")
        self.assertIsInstance(value, int)

    def test_unknown_linked_dll_returns_empty_and_continues(self):
        engine = _engine(
            "to get f\n"
            '  linkDLL32 "other.dll"\n'
            "    INT missingFn()\n"
            "  end\n"
            "  x = missingFn()\n"
            '  return x & "ok"\n'
            "end\n"
        )
        self.assertEqual(engine.get("f"), "ok")


if __name__ == "__main__":
    unittest.main()
