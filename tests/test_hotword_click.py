"""A click on a hotword's characters runs that hotword's buttonClick."""

import unittest
from pathlib import Path

from opentoolbook.navigate import Navigator
from opentoolbook.show import Paint, hotword_at, show_page
from lesson import logic_families_path

HOTWORDS = {
    "P1080": ((87, 96, "tolerance"), "P1085"),
    "P1082": ((87, 96, "tolerance"), "P1085"),
    "P1200": ((31, 48, "propagation delay"), "P1205"),
    "P1207": ((31, 48, "propagation delay"), "P1205"),
    "P2070": ((90, 99, "impedance"), "P2075"),
}


def _lesson():
    return logic_families_path()


def _tk():
    try:
        import tkinter

        root = tkinter.Tk()
    except Exception:
        return None
    return root


class HotwordAtTests(unittest.TestCase):
    def test_the_range_names_the_hotword(self):
        field = Paint("field", 1, "Text", text="a tolerance b", hotwords=((2, 11, "tolerance"),))
        self.assertIsNone(hotword_at(field, 1))
        self.assertEqual(hotword_at(field, 2), "tolerance")
        self.assertEqual(hotword_at(field, 10), "tolerance")
        self.assertIsNone(hotword_at(field, 11))

    def test_a_field_with_no_hotword(self):
        self.assertIsNone(hotword_at(Paint("field", 1, "Text", text="plain"), 0))


@unittest.skipUnless(_lesson(), "set OPENTOOLBOOK_TBK to Logic Families")
class LessonHotwordTests(unittest.TestCase):
    def setUp(self):
        self.data = _lesson().read_bytes()

    def test_each_hotword_range_is_its_name(self):
        for page_id, (expected, _target) in HOTWORDS.items():
            fields = [item for item in show_page(self.data, page_id, 800, 600).items if item.hotwords]
            self.assertEqual(len(fields), 1, page_id)
            field = fields[0]
            self.assertEqual(field.hotwords, (expected,), page_id)
            start, stop, name = expected
            self.assertEqual(field.text[start:stop], name, page_id)

    def test_each_hotword_click_goes_to_its_definition_page(self):
        for page_id, ((_start, _stop, name), target) in HOTWORDS.items():
            nav = Navigator(self.data, page_id)
            clicked = nav.click(name)
            self.assertTrue(clicked.moved, page_id)
            self.assertEqual(nav.page_id, target, page_id)
            self.assertEqual(nav.variables.get("lastpage"), page_id)

    def test_impedance_definition_helpnext_returns_via_lastpage(self):
        from opentoolbook.entry import opening_page

        path = _lesson()
        opened = opening_page(path)
        nav = Navigator(
            self.data,
            "P2070",
            path,
            props=opened.props,
            sysbooks=opened.sysbooks,
            variables=dict(opened.variables),
        )
        self.assertTrue(nav.click("impedance").moved)
        self.assertEqual(nav.page_id, "P2075")
        self.assertEqual(nav.variables.get("lastpage"), "P2070")
        self.assertEqual(nav.title(), "9e954d01.tbk - P2075")
        texts = {
            item.name: item.text
            for item in nav.display(800, 600).items
            if item.kind == "field"
        }
        self.assertEqual(texts.get(""), "DEFINITION")
        self.assertTrue(nav.click("HelpNext").moved)
        self.assertEqual(nav.page_id, "P2070")
        self.assertEqual(nav.title(), "9e954d01.tbk - P2070")

    def test_a_drawn_hotword_is_hit_in_the_window(self):
        root = _tk()
        if root is None:
            self.skipTest("no Tk display")
        try:
            import tkinter

            from opentoolbook.show import draw_page, hotword_hit

            canvas = tkinter.Canvas(root, width=624, height=442)
            canvas.pack()
            draw_page(canvas, show_page(self.data, "P1080", 624, 442))
            root.update()
            hits = {
                start: hotword_hit(canvas, (box[0] + box[2]) / 2, (box[1] + box[3]) / 2)
                for made, (_field, start) in canvas.spans.items()
                for box in [canvas.bbox(made)]
            }
            self.assertEqual(hits[87], "tolerance")
            self.assertEqual(canvas.itemcget(next(m for m, (_f, s) in canvas.spans.items() if s == 87), "text"), "tolerance")
        finally:
            root.destroy()


if __name__ == "__main__":
    unittest.main()
