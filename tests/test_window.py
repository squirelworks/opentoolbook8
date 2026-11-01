"""The Tk window closes back to ``main``. This test needs a screen."""

import contextlib
import io
import os
import unittest
from pathlib import Path

from lesson import logic_families_path

FIXTURE = Path(__file__).parent / "fixtures" / "otb-line-rect.tbk"


def _tk():
    if not os.environ.get("DISPLAY"):
        return None, "DISPLAY is unset, so the window smoke test does not run"
    try:
        import tkinter
    except ImportError:
        return None, "this Python has no tkinter, so the window smoke test does not run"
    return tkinter, ""


class WindowCloseTests(unittest.TestCase):
    def test_the_close_button_returns_zero_from_main(self):
        tk, why = _tk()
        if tk is None:
            self.skipTest(why)
        from opentoolbook.__main__ import main

        seen = {}
        original = tk.Tk.mainloop

        def loop(root, n=0):
            def press_close():
                seen["painted"] = [item.kind for item in root.winfo_children()[0].listed.items]
                command = root.protocol("WM_DELETE_WINDOW")
                seen["command"] = command
                root.tk.call(command)

            # Let idle run once (200 ms) then close, so a dangling idle would show.
            root.after(350, press_close)
            original(root, n)

        tk.Tk.mainloop = loop
        err = io.StringIO()
        try:
            with contextlib.redirect_stderr(err):
                code = main(["opentoolbook", "--show", "", str(FIXTURE)])
        finally:
            tk.Tk.mainloop = original
        self.assertEqual(code, 0)
        self.assertTrue(seen["command"])
        self.assertEqual(seen["painted"][:2], ["background", "rectangle"])
        self.assertNotIn("invalid command name", err.getvalue())
        self.assertNotIn("on_idle", err.getvalue())

    def test_a_click_error_is_one_line_and_the_window_stays(self):
        tk, why = _tk()
        if tk is None:
            self.skipTest(why)
        from opentoolbook.show import open_page

        seen = {}
        original = tk.Tk.mainloop

        def loop(root, n=0):
            def raise_then_close():
                err = io.StringIO()
                with contextlib.redirect_stderr(err):
                    try:
                        raise ValueError("no file nida71.tbk for page P0")
                    except ValueError as exc:
                        root.report_callback_exception(ValueError, exc, exc.__traceback__)
                seen["stderr"] = err.getvalue()
                seen["alive"] = bool(root.winfo_exists())
                root.tk.call(root.protocol("WM_DELETE_WINDOW"))

            root.after(200, raise_then_close)
            original(root, n)

        tk.Tk.mainloop = loop
        try:
            open_page(FIXTURE.read_bytes(), "", str(FIXTURE))
        finally:
            tk.Tk.mainloop = original
        self.assertEqual(seen["stderr"], "no file nida71.tbk for page P0\n")
        self.assertTrue(seen["alive"])

    def test_logic_families_p300_paints_in_the_live_window(self):
        path = logic_families_path()
        if path is None:
            self.skipTest("set OPENTOOLBOOK_TBK to 9e954d01.tbk")
        tk, why = _tk()
        if tk is None:
            self.skipTest(why)
        from opentoolbook.show import open_page

        seen = {}
        original = tk.Tk.mainloop

        def loop(root, n=0):
            def press_close():
                canvas = root.winfo_children()[0]
                listed = canvas.listed
                seen["kinds"] = [item.kind for item in listed.items]
                seen["canvas"] = len(canvas.find_all())
                seen["buttons_with_picture"] = sum(
                    1
                    for item in listed.items
                    if item.kind == "button" and item.picture is not None
                )
                root.tk.call(root.protocol("WM_DELETE_WINDOW"))

            root.after(350, press_close)
            original(root, n)

        tk.Tk.mainloop = loop
        err = io.StringIO()
        try:
            with contextlib.redirect_stderr(err):
                open_page(path.read_bytes(), "P300", str(path), enter=True)
        finally:
            tk.Tk.mainloop = original
        self.assertIn("background", seen["kinds"])
        self.assertIn("field", seen["kinds"])
        self.assertIn("button", seen["kinds"])
        self.assertGreaterEqual(seen["canvas"], 3)
        self.assertGreaterEqual(seen["buttons_with_picture"], 1)
        self.assertNotIn("invalid command name", err.getvalue())
        self.assertNotIn("on_idle", err.getvalue())
