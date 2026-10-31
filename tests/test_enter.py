"""enterPage writes the greeting. The display list does not need a screen."""

import unittest
from pathlib import Path

from opentoolbook.enter import cover_style, page_source
from opentoolbook.field import field_text
from opentoolbook.script import book_handlers, resource_scripts
from opentoolbook.show import show_page

from lesson import companion, logic_families_path

GREETING = "Hello Student, this lesson is about:"
STORED = "Hello, this lesson is about:"


def _lesson():
    return logic_families_path()


class StyleTests(unittest.TestCase):
    def test_a_covering_run_covers_the_new_string(self):
        self.assertEqual(cover_style(STORED, GREETING, ((0, "Arial"),)), ((0, "Arial"),))
        old = "Hello"
        new = "Hello Student"
        self.assertEqual(
            cover_style(old, new, ((0, "Arial"), (len(old), "Courier"))),
            ((0, "Arial"), (len(new), "Courier")),
        )
        self.assertEqual(cover_style(old, new, ((0, "A"), (2, "B"))), ((0, "A"), (2, "B")))


class GreetingTests(unittest.TestCase):
    def test_p10_replaces_the_first_field_and_keeps_the_version_line(self):
        path = _lesson()
        if path is None:
            self.skipTest("set OPENTOOLBOOK_TBK to 9e954d01.tbk")
        data = path.read_bytes()
        source = page_source(data, "P10")
        self.assertIn('set text of field "First"  to "Hello" && getFirst() & ", this lesson is about:"', source)
        self.assertIn("get setSection", source)
        stored = next(item for item in show_page(data, "P10", 400, 300).items if item.kind == "field" and item.name.lower() == "first")
        self.assertEqual(stored.text, STORED)
        for page in ("PINFO", "PQINFO"):
            stored = field_text(data, page, "version")
            self.assertEqual(stored, "Version: 2.003.0001")
            listed = show_page(data, page, 400, 300)
            version = next(item for item in listed.items if item.kind == "field" and item.name.lower() == "version")
            self.assertEqual(version.text, stored)
            self.assertIn("__nidaVersion of this book", page_source(data, page))
        recs = resource_scripts(companion(path, "nc81recs.sbk").read_bytes())[0].source
        body = _body(recs, "getFirst")
        self.assertIn("return __studentFirst", body)
        self.assertNotIn("Student", body)
        base = resource_scripts(companion(path, "nc81base.sbk").read_bytes())[0].source
        section = _body(base, "setSection")
        self.assertIn("WritePrivateProfileStringA", section)
        self.assertIn("kernel32.dll", section)


def _body(source: str, name: str) -> str:
    handlers = book_handlers("book", source)
    found = next(item for item in handlers if item.name.lower() == name.lower())
    lines = []
    for line in source[found.body_start:].splitlines():
        if lines and line and not line[0].isspace() and line.lower().startswith("to "):
            break
        lines.append(line)
    return "\n".join(lines)


if __name__ == "__main__":
    unittest.main()
