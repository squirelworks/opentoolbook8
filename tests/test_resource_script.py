"""A type 10 resource stores a handler. The reader returns the text and does not call it."""

import os
import unittest
from pathlib import Path

from opentoolbook.script import resource_scripts


class ResourceScriptTests(unittest.TestCase):
    def test_type_10_bytes_are_a_handler(self):
        path = os.environ.get("OPENTOOLBOOK_TBK")
        if not path or not os.path.isfile(path):
            self.skipTest("set OPENTOOLBOOK_TBK to 9e954d01.tbk")
        self._handlers(
            Path(path).read_bytes(),
            "to handle enterPage",
            "to handle enterSystem",
        )
        nida = Path(path).with_name("nida81.tbk")
        self.assertTrue(nida.is_file())
        self._handlers(
            nida.read_bytes(),
            "To handle enterpage",
            "to handle enterApplication",
        )

    def _handlers(self, data: bytes, first: str, second: str):
        found = resource_scripts(data)
        self.assertGreaterEqual(len(found), 2)
        sources = [item.source for item in found]
        self.assertGreaterEqual(len(set(sources)), 2)
        self.assertTrue(any(item.source.startswith(first) for item in found))
        self.assertTrue(any(item.source.startswith(second) for item in found))
        self.assertEqual(len({item.resource_id for item in found}), len(found))
        for item in found:
            self.assertTrue(item.source.lower().startswith("to handle "))
            self.assertNotIn("\x00", item.source)
            lines = [line.strip() for line in item.source.splitlines() if line.strip()]
            self.assertEqual(lines[-1].lower(), "end")
            self.assertNotEqual(lines[0].lower(), "end")


if __name__ == "__main__":
    unittest.main()
