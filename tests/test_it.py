"""``it`` is the value of the last ``get``."""

import unittest

from opentoolbook.entry import choose_opening

from test_entry import OPEN_SESSION, _handlers


def _open(body, pages=("P0", "P1", "P2")):
    handlers = {"entersystem": f"to handle enterSystem\n{body}\nend\n"}
    return choose_opening(pages, handlers)


class ItTests(unittest.TestCase):
    def test_get_a_literal_then_if_it_is_takes_the_branch(self):
        self.assertEqual(_open('get 1\nif it is 1 then\n go to page "P2"\nend if'), ("P2", None))
        self.assertEqual(_open('get 1\nif it is 0 then\n go to page "P2"\nend if'), ("P0", None))

    def test_the_next_get_replaces_it(self):
        body = 'get 1\nget 0\nif it is 1 then\n go to page "P2"\nelse\n go to page "P1"\nend if'
        self.assertEqual(_open(body), ("P1", None))

    def test_get_a_name_and_a_string(self):
        body = 'x = "yes"\nget x\nif it is "yes" then\n go to page "P2"\nend if'
        self.assertEqual(_open(body), ("P2", None))
        body = 'get "no"\nif it = "yes" then\n go to page "P2"\nend if'
        self.assertEqual(_open(body), ("P0", None))

    def test_get_a_handler_stores_its_return(self):
        handlers = {
            "entersystem": 'to handle enterSystem\nget pick()\nif it is 2 then\ngo to page "P2"\nend if\nend\n',
            "pick": "to get pick\nreturn 2\nend\n",
        }
        self.assertEqual(choose_opening(("P0", "P2"), handlers), ("P2", None))

    def test_open_session_returning_0_still_skips_goto_page_list(self):
        handlers = dict(_handlers())
        handlers["gotopagelist"] = 'to get gotoPageList\n    go to page "P1"\nend\n'
        self.assertEqual(choose_opening(("P0", "P1"), handlers), ("P0", None))
        handlers = {
            "opensession": OPEN_SESSION,
            "entersystem": 'to handle enterSystem\nget openSession()\nif it is 0 then\ngo to page "P1"\nend if\nend\n',
        }
        self.assertEqual(choose_opening(("P0", "P1"), handlers), ("P1", None))


if __name__ == "__main__":
    unittest.main()
