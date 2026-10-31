"""A window holds the photos of one page at a time."""

import os
import unittest
from dataclasses import replace
from pathlib import Path

from opentoolbook.show import Paint, draw_page, release_photos, show_page

FIXTURE = Path(__file__).parent / "fixtures" / "otb-line-rect.tbk"


class FakePhoto:
    live = 0

    def __init__(self, data):
        self.data = data
        self.alive = True
        FakePhoto.live += 1

    def delete(self):
        if self.alive:
            self.alive = False
            FakePhoto.live -= 1


class FakeCanvas:
    def __init__(self):
        self.images = []

    def create_image(self, x, y, image, anchor):
        self.images.append(image)

    def __getattr__(self, name):
        if name.startswith("create_"):
            return lambda *a, **k: None
        raise AttributeError(name)


def _pictures(listed):
    """Only the items that make a photo, so no font is needed."""
    return replace(listed, items=tuple(item for item in listed.items if item.picture is not None))


def _lesson():
    path = os.environ.get("OPENTOOLBOOK_TBK")
    if not path or not os.path.isfile(path):
        return None
    return Path(path)


class PhotoCountTests(unittest.TestCase):
    def setUp(self):
        FakePhoto.live = 0

    def test_redrawing_a_page_replaces_its_photos(self):
        listed = show_page(FIXTURE.read_bytes(), "", 600, 400)
        button = Paint("button", 1, "Next", (0, 0, 300, 300), picture=(2, 2, b"\xff" * 12))
        listed = replace(listed, items=(button, button))
        canvas = FakeCanvas()
        for _ in range(5):
            draw_page(canvas, listed, FakePhoto)
            self.assertEqual(FakePhoto.live, 2)
            self.assertEqual(len(canvas.photos), 2)
        self.assertEqual(release_photos(canvas), 2)
        self.assertEqual(FakePhoto.live, 0)
        self.assertEqual(canvas.photos, [])

    def test_p300_to_p400_to_p300_stays_bounded(self):
        from opentoolbook.click import follow_click
        from opentoolbook.field import page_ids

        path = _lesson()
        if path is None:
            self.skipTest("set OPENTOOLBOOK_TBK to 9e954d01.tbk")
        data = path.read_bytes()
        pages = page_ids(data)
        page = "P300"
        canvas = FakeCanvas()
        counts = []
        for button in (None, "Next", "Back", "Next", "Back"):
            if button is not None:
                page = follow_click(data, page, button, pages).page_id
            draw_page(canvas, _pictures(show_page(data, page, 624, 442)), FakePhoto)
            counts.append((page, FakePhoto.live))
        pages = [page for page, _live in counts]
        self.assertEqual(pages, ["P300", "P400", "P300", "P400", "P300"])
        live = [count for _page, count in counts]
        self.assertEqual(live[0], live[2])
        self.assertEqual(live[0], live[4])
        self.assertEqual(live[1], live[3])
        self.assertGreater(live[0], 0)
        self.assertEqual(len(canvas.images), sum(live))


if __name__ == "__main__":
    unittest.main()
