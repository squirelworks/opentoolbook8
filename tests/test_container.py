"""A class 0x0B rectangle is the union of the objects that name it."""

import os
import unittest
from pathlib import Path

from opentoolbook.container import stored_containers

from lesson import companion


class ContainerTests(unittest.TestCase):
    def test_bounds_are_the_union_of_the_named_objects(self):
        path = os.environ.get("OPENTOOLBOOK_TBK")
        if not path or not os.path.isfile(path):
            self.skipTest("set OPENTOOLBOOK_TBK to 9e954d01.tbk")
        self._union(Path(path).read_bytes())
        nida = companion(path, "nida81.tbk")
        self.assertTrue(nida.is_file())
        self._union(nida.read_bytes())

    def _union(self, data: bytes):
        found = stored_containers(data)
        self.assertGreaterEqual(len(found), 2)
        self.assertGreaterEqual(len({item.bounds for item in found}), 2)
        for item in found:
            self.assertGreaterEqual(len(item.children), 1)
            left = min(child[0] for child in item.children)
            top = min(child[1] for child in item.children)
            right = max(child[2] for child in item.children)
            bottom = max(child[3] for child in item.children)
            self.assertEqual(item.bounds, (left, top, right, bottom))
            self.assertGreater(right, left)
            self.assertGreater(bottom, top)


if __name__ == "__main__":
    unittest.main()
