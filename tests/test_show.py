"""The page window is the display list. It does not need a screen."""

import os
import unittest
from pathlib import Path

from opentoolbook.bitmap import button_checked, button_checked_picture, button_picture
from opentoolbook.polygon import polygon_points
from opentoolbook.show import fit_scale, show_page, unit_to_px
from opentoolbook.size import page_size

from lesson import companion

FIXTURE = Path(__file__).parent / "fixtures" / "otb-line-rect.tbk"
PIE = Path(__file__).parent / "fixtures" / "otb-pie.tbk"
LESSON = os.environ.get("OPENTOOLBOOK_TBK")


def _lesson():
    if not LESSON or not os.path.isfile(LESSON):
        return None
    return Path(LESSON)


class PageSizeTests(unittest.TestCase):
    def test_an_instructor_book_stores_the_page_on_the_book_record(self):
        self.assertEqual(page_size(FIXTURE.read_bytes()), (9000, 6000))
        self.assertEqual(page_size(PIE.read_bytes()), (9000, 6000))

    def test_the_lesson_and_the_system_books_store_their_own_pages(self):
        path = _lesson()
        if path is None:
            self.skipTest("set OPENTOOLBOOK_TBK to 9e954d01.tbk")
        self.assertEqual(page_size(path.read_bytes()), (9360, 6624))
        self.assertEqual(page_size(companion(path, "nida81.tbk").read_bytes()), (9360, 6624))
        for name in ("nc81base.sbk", "nc81recs.sbk", "nc81test.sbk", "nc81trnr.sbk"):
            self.assertEqual(page_size(companion(path, name).read_bytes()), (9345, 6630))


class SceneTests(unittest.TestCase):
    def test_the_instructor_page_draws_the_rectangle_at_one_scale(self):
        data = FIXTURE.read_bytes()
        width, height = page_size(data)
        view_w = round(unit_to_px(width, 1))
        view_h = round(unit_to_px(height, 1))
        shown = show_page(data, "", view_w, view_h)
        self.assertEqual(shown.scale, 1)
        self.assertEqual(unit_to_px(20, 1), 96 / 72)
        fitted = show_page(data, "", 200, 100)
        self.assertEqual(fitted.scale, fit_scale(width, height, 200, 100))
        self.assertLess(fitted.scale, 1)
        rectangle = next(item for item in fitted.items if item.kind == "rectangle")
        self.assertEqual(rectangle.bounds, (1350, 3675, 2700, 4275))
        self.assertEqual(rectangle.pattern, 254)
        self.assertEqual(rectangle.fill, (255, 255, 255))
        self.assertEqual(rectangle.stroke, (0, 0, 0))
        width_px = unit_to_px(rectangle.bounds[2] - rectangle.bounds[0], fitted.scale)
        self.assertNotEqual(width_px, unit_to_px(rectangle.bounds[2] - rectangle.bounds[0], fitted.scale * fitted.scale))
        self.assertEqual([item.kind for item in fitted.items], ["background", "rectangle", "angled line"])
        pie = show_page(PIE.read_bytes(), "", 200, 100)
        ellipse = next(item for item in pie.items if item.kind == "ellipse")
        self.assertEqual(ellipse.bounds, (700, 700, 2200, 1800))
        self.assertNotIn("rectangle", [item.kind for item in pie.items if item.object_id == ellipse.object_id])

    def test_p300_draws_the_page_the_readers_return(self):
        path = _lesson()
        if path is None:
            self.skipTest("set OPENTOOLBOOK_TBK to 9e954d01.tbk")
        data = path.read_bytes()
        shown = show_page(data, "P300", 400, 300)
        self.assertEqual(
            [(item.kind, item.object_id, item.name) for item in shown.items],
            [
                ("background", None, ""),
                ("field", 5, "Page#"),
                ("button", 16, "selection1"),
                ("button", 1, "Next"),
                ("button", 19, "MenuFrame"),
                ("field", 17, "Selection1"),
                ("button", 21, ""),
                ("field", 22, ""),
                ("field", 23, ""),
                ("button", 5, "Back"),
            ],
        )
        self.assertLess(_index(shown, "button", 19), _index(shown, "field", 17))
        background = shown.items[0]
        number = next(item for item in shown.items if item.name == "Page#")
        self.assertEqual(number.text, "P300")
        self.assertEqual(background.pattern, 254)
        self.assertEqual(background.fill, (0, 0, 191))
        self.assertEqual(background.bounds, (0, 0, 9360, 6624))
        field = next(item for item in shown.items if item.object_id == 17)
        self.assertEqual(field.text, "1. IBM PC Compatible Computer\r\n\r\n")
        self.assertEqual(field.bounds, (1995, 1293, 7590, 1608))
        self.assertEqual(field.runs, ((0, "Arial"),))
        self.assertEqual(field.fill, None)
        titles = [item.text for item in shown.items if item.kind == "field" and item.object_id in (22, 23)]
        self.assertEqual(titles, ["EQUIPMENT REQUIRED", "EQUIPMENT REQUIRED"])
        button = next(item for item in shown.items if item.name == "Next")
        self.assertEqual(button.bounds, (8907, 6210, 9342, 6630))
        self.assertEqual(button.picture_role, "up")
        self.assertEqual(button.picture_id, button_picture(data, "P300", "Next"))
        self.assertNotEqual(button.picture_id, button_checked_picture(data, "P300", "MenuFrame"))
        self.assertEqual(button.picture[:2], (29, 29))
        self.assertEqual(button.picture[2][:3], bytes((8, 8, 193)))
        frame = next(item for item in shown.items if item.name == "MenuFrame")
        self.assertEqual(frame.picture_role, "up")
        self.assertEqual(frame.picture[:2], (580, 387))
        self.assertTrue(all(item.picture_role != "checked" for item in shown.items))
        width_px = unit_to_px(button.bounds[2] - button.bounds[0], shown.scale)
        self.assertAlmostEqual(width_px, 29 * shown.scale)
        self.assertNotAlmostEqual(width_px, 29 * shown.scale * shown.scale)

    def test_a_quiz_letter_uses_the_up_picture(self):
        path = _lesson()
        if path is None:
            self.skipTest("set OPENTOOLBOOK_TBK to 9e954d01.tbk")
        data = path.read_bytes()
        shown = show_page(data, "P10210", 400, 300)
        letter = next(item for item in shown.items if item.kind == "button" and item.name == "A")
        self.assertEqual(button_checked(data, "P10210", "A"), 0)
        self.assertEqual(letter.picture_role, "up")
        self.assertEqual(letter.picture_id, button_picture(data, "P10210", "A"))
        self.assertNotEqual(letter.picture_id, button_checked_picture(data, "P10210", "A"))
        self.assertEqual(letter.picture_id, 116)
        self.assertEqual(button_checked_picture(data, "P10210", "A"), 118)

    def test_the_chip_page_after_p300_locks_the_paint_order(self):
        path = _lesson()
        if path is None:
            self.skipTest("set OPENTOOLBOOK_TBK to 9e954d01.tbk")
        data = path.read_bytes()
        chip = show_page(data, "P400", 400, 300)
        self.assertLess(_index(chip, "rectangle", 12), _index(chip, "field", 36))
        self.assertLess(_index(chip, "rectangle", 37), _index(chip, "field", 38))
        label = next(item for item in chip.items if item.kind == "field" and item.object_id == 36)
        self.assertEqual(label.text, "74LS174N  E825")
        self.assertEqual(label.fill, None)
        line = next(item for item in chip.items if item.kind == "line" and item.object_id == 39)
        self.assertEqual(line.points, ((2145, 4065), (1530, 4065)))
        self.assertEqual(len(line.points), 2)
        ellipse = next(item for item in chip.items if item.kind == "ellipse" and item.object_id == 35)
        self.assertEqual(ellipse.bounds, (5040, 4395, 5145, 4515))
        polygon = next(item for item in chip.items if item.kind == "polygon" and item.object_id == 14)
        self.assertEqual(polygon.points, polygon_points(data, "P400", 14))
        self.assertNotIn("arc", [item.kind for item in chip.items])

        later = show_page(data, "P410", 400, 300)
        self.assertLess(_index(later, "rectangle", 5), _index(later, "field", 25))
        covered = show_page(data, "P1110", 400, 300)
        self.assertLess(_index(covered, "field", 16), _index(covered, "line", 14))
        self.assertLess(_index(covered, "ellipse", 18), _index(covered, "field", 13))


class WindowTests(unittest.TestCase):
    def test_tk_draws_the_same_list_when_it_can_open(self):
        try:
            import tkinter as tk
        except Exception as exc:
            self.skipTest(f"Tk cannot open: {exc}")
        try:
            root = tk.Tk()
        except tk.TclError as exc:
            self.skipTest(f"Tk cannot open: {exc}")
        try:
            from opentoolbook.show import draw_page

            shown = show_page(FIXTURE.read_bytes(), "", 200, 120)
            canvas = tk.Canvas(root, width=200, height=120)
            draw_page(canvas, shown)
            root.update_idletasks()
            self.assertGreaterEqual(len(canvas.find_all()), 2)
        except tk.TclError as exc:
            self.skipTest(f"Tk cannot open: {exc}")
        finally:
            root.destroy()


def _index(shown, kind: str, object_id: int) -> int:
    for index, item in enumerate(shown.items):
        if item.kind == kind and item.object_id == object_id:
            return index
    raise AssertionError(f"no {kind} {object_id}")


if __name__ == "__main__":
    unittest.main()


class ResizeTests(unittest.TestCase):
    def test_a_narrower_view_refits_the_fixture(self):
        from opentoolbook.show import refit

        data = FIXTURE.read_bytes()
        self.assertEqual(page_size(data), (9000, 6000))
        wide = show_page(data, "", 600, 400)
        narrow = refit(wide, 300, 400)
        self.assertEqual(narrow.scale, fit_scale(9000, 6000, 300, 400))
        self.assertLess(narrow.scale, wide.scale)
        self.assertEqual((narrow.view_width, narrow.view_height), (300, 400))
        self.assertEqual(narrow.items, wide.items)
        self.assertEqual(narrow, show_page(data, "", 300, 400))
        # The page is 600 by 400 pixels at scale 1, so a 300-pixel view halves it.
        self.assertEqual(narrow.scale, 0.5)

    def test_a_narrower_view_refits_the_lesson(self):
        from opentoolbook.show import refit

        path = _lesson()
        if path is None:
            self.skipTest("set OPENTOOLBOOK_TBK to 9e954d01.tbk")
        data = path.read_bytes()
        self.assertEqual(page_size(data), (9360, 6624))
        wide = show_page(data, "P300", 624, 442)
        narrow = refit(wide, 312, 442)
        self.assertEqual(narrow.scale, fit_scale(9360, 6624, 312, 442))
        self.assertLess(narrow.scale, wide.scale)
        self.assertEqual(narrow.items, wide.items)
