"""A letter click on a quiz page checks that letter and unchecks the rest."""

import unittest

from opentoolbook.show import Paint, _checked


def _letters(listed):
    return {
        item.name: (item.picture_id, item.picture_role)
        for item in listed.items
        if item.kind == "button" and item.name in ("A", "B", "C", "D")
    }


class CheckedStateTests(unittest.TestCase):
    def test_the_click_state_wins_over_the_stored_bit(self):
        items = (
            Paint("button", 1, "A", picture_id=10, picture_role="up", up_id=10, checked_id=12),
            Paint("button", 2, "B", picture_id=22, picture_role="checked", up_id=20, checked_id=22),
            Paint("button", 3, "C", picture_id=30, picture_role="up", up_id=30, checked_id=None),
            Paint("field", 4, "A", text="A"),
        )
        out = _checked(b"", items, {"a": True, "b": False, "c": True})
        self.assertEqual((out[0].picture_id, out[0].picture_role), (12, "checked"))
        self.assertEqual((out[1].picture_id, out[1].picture_role), (20, "up"))
        # No checked picture: the up picture stays.
        self.assertEqual((out[2].picture_id, out[2].picture_role), (30, "up"))
        self.assertIs(out[3], items[3])

    def test_no_click_state_leaves_the_list_alone(self):
        items = (Paint("button", 1, "A", picture_id=10, picture_role="up", up_id=10, checked_id=12),)
        self.assertEqual(_checked(b"", items, {"OK": True}), items)


if __name__ == "__main__":
    unittest.main()
