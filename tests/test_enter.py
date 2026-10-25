"""enterPage writes the greeting. The display list does not need a screen."""

import os
import unittest
from pathlib import Path

from opentoolbook.enter import (
    blocks_write,
    concatenate,
    cover_style,
    enter_fields,
    get_first,
    page_source,
)
from opentoolbook.field import field_text
from opentoolbook.script import book_handlers, resource_scripts
from opentoolbook.show import show_page

LESSON = os.environ.get("OPENTOOLBOOK_TBK")
GREETING = "Hello Student, this lesson is about:"
STORED = "Hello, this lesson is about:"


def _lesson():
    if not LESSON or not os.path.isfile(LESSON):
        return None
    return Path(LESSON)


class ConcatenationTests(unittest.TestCase):
    def test_and_and_is_a_space_and_and_is_not(self):
        self.assertEqual(concatenate('"A" && "B"'), "A B")
        self.assertEqual(concatenate('"A" & "B"'), "AB")
        self.assertEqual(concatenate('"A" & "B" && "C"'), "AB C")
        self.assertEqual(concatenate('"A && B" & "C"'), "A && BC")

    def test_get_first_is_the_stripped_name_or_student(self):
        self.assertEqual(get_first(None), "Student")
        self.assertEqual(get_first(""), "Student")
        self.assertEqual(get_first("   "), "Student")
        self.assertEqual(get_first("  Ada  "), "Ada")
        expression = '"Hello" && getFirst() & ", this lesson is about:"'
        self.assertEqual(concatenate(expression), GREETING)
        self.assertEqual(concatenate("name of this page", page_id="P300"), "P300")
        self.assertEqual(concatenate(expression, student_first="  Ada  "), "Hello Ada, this lesson is about:")

    def test_a_covering_run_covers_the_new_string(self):
        self.assertEqual(cover_style(STORED, GREETING, ((0, "Arial"),)), ((0, "Arial"),))
        old = "Hello"
        new = "Hello Student"
        self.assertEqual(
            cover_style(old, new, ((0, "Arial"), (len(old), "Courier"))),
            ((0, "Arial"), (len(new), "Courier")),
        )
        self.assertEqual(cover_style(old, new, ((0, "A"), (2, "B"))), ((0, "A"), (2, "B")))

    def test_an_unresolved_book_property_is_not_written(self):
        value = concatenate('"Version: " & __nidaVersion of this book')
        self.assertEqual(value, "Version: __nidaVersion of this book")
        self.assertTrue(blocks_write(value))
        self.assertFalse(blocks_write(GREETING))


class GreetingTests(unittest.TestCase):
    def test_p10_replaces_the_first_field_and_keeps_the_version_line(self):
        path = _lesson()
        if path is None:
            self.skipTest("set OPENTOOLBOOK_TBK to 9e954d01.tbk")
        data = path.read_bytes()
        source = page_source(data, "P10")
        self.assertIn('set text of field "First"  to "Hello" && getFirst() & ", this lesson is about:"', source)
        self.assertIn("get setSection", source)
        shown = show_page(data, "P10", 400, 300)
        first = next(item for item in shown.items if item.kind == "field" and item.name.lower() == "first")
        self.assertEqual(first.text, GREETING)
        self.assertNotEqual(first.text, field_text(data, "P10", "first"))
        self.assertEqual(first.runs, ((0, "Arial"),))
        text = next(item for item in shown.items if item.kind == "field" and item.name == "Text")
        self.assertEqual(text.text, "LOGIC FAMILIES")
        author = enter_fields(
            data,
            "P10",
            ((first.name, field_text(data, "P10", "first"), first.runs),),
            sys_level="author",
        )
        self.assertEqual(author[0][1], STORED)
        named = enter_fields(
            data,
            "P10",
            ((first.name, field_text(data, "P10", "first"), first.runs),),
            student_first="  Ada  ",
        )
        self.assertEqual(named[0][1], "Hello Ada, this lesson is about:")
        self.assertEqual(named[0][2], ((0, "Arial"),))
        for page in ("PINFO", "PQINFO"):
            stored = field_text(data, page, "version")
            self.assertEqual(stored, "Version: 2.003.0001")
            listed = show_page(data, page, 400, 300)
            version = next(item for item in listed.items if item.kind == "field" and item.name.lower() == "version")
            self.assertEqual(version.text, stored)
            self.assertIn("__nidaVersion of this book", page_source(data, page))
        recs = resource_scripts(path.with_name("nc81recs.sbk").read_bytes())[0].source
        body = _body(recs, "getFirst")
        self.assertIn("return __studentFirst", body)
        self.assertNotIn("Student", body)
        base = resource_scripts(path.with_name("nc81base.sbk").read_bytes())[0].source
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
