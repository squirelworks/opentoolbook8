"""The OpenScript interpreter: lexer, parser, and engine on synthetic handlers."""

import unittest

from opentoolbook.openscript import ast as A
from opentoolbook.openscript.interp import Engine, Host, Ref, get_chunk, put_chunk
from opentoolbook.openscript.lexer import logical_lines
from opentoolbook.openscript.parser import parse_script
from opentoolbook.props import UserProperties


def _engine(*sources, host=None, props=None):
    books = [parse_script(source).handlers for source in sources]

    def lookup(kind, name):
        key = f"{kind} {name}"
        return [book[key] for book in books if key in book]

    return Engine(lookup, host or Host(), props=props)


class LexerTests(unittest.TestCase):
    def test_doubled_quote_comment_continuation_and_semicolon(self):
        lines = logical_lines('x = "a ""b"" c" -- note\ny = 1 + \\\n 2; z = 3\n')
        self.assertEqual(len(lines), 3)
        self.assertEqual(lines[0].tokens[2].text, 'a "b" c')
        self.assertEqual([token.text for token in lines[1].tokens], ["y", "=", "1", "+", "2"])
        self.assertEqual(lines[2].tokens[0].text, "z")


class ParserTests(unittest.TestCase):
    def test_handlers_by_kind_and_name(self):
        script = parse_script(
            "to handle buttonClick\n  go to page \"P2\"\nend\n"
            "to get twice n\n  return n * 2\nend twice\n"
            "to set caption to value\n  forward\nend\n"
        )
        self.assertEqual(sorted(script.handlers), ["get twice", "handle buttonclick", "set caption"])
        self.assertEqual(script.handlers["get twice"].params[0].name, "n")
        self.assertEqual(script.errors, [])

    def test_object_property_and_chunk_forms(self):
        body = parse_script(
            "to handle x\n"
            "  text of field \"Stem\" of this page = item 2 of list\n"
            "  if char 1 to 3 of s is in \"abc\" then beep\n"
            "end\n"
        ).handlers["handle x"].body
        assign = body[0]
        self.assertIsInstance(assign.target, A.Prop)
        self.assertIsInstance(assign.target.of, A.ObjRef)
        self.assertEqual(assign.target.of.kind, "field")
        self.assertIsInstance(assign.value, A.Chunk)
        self.assertIsInstance(body[1], A.If)

    def test_a_bad_handler_does_not_hide_the_next(self):
        script = parse_script("to handle bad\n  x = (\nend\nto handle good\n  beep\nend\n")
        self.assertIn("handle good", script.handlers)
        self.assertEqual(len(script.errors), 1)


class EngineTests(unittest.TestCase):
    def test_system_names_are_shared_and_locals_are_not(self):
        engine = _engine(
            "to handle a\n  system s\n  s = 5\n  l = 6\n  send b\nend\n"
            "to handle b\n  system s\n  get s + 1\n  return it\nend\n"
            "to get c\n  return l\nend\n"
        )
        engine.send("a")
        self.assertEqual(engine.globals["s"], 5)
        self.assertEqual(engine.send("b"), 6)
        # l was local to a; here it reads as its own name.
        self.assertEqual(engine.get("c"), "l")

    def test_double_underscore_system_names_go_to_the_store(self):
        props = UserProperties()
        engine = _engine("to handle a\n  system int __score\n  __score = 3\nend\n", props=props)
        engine.send("a")
        self.assertEqual(props.get("__score"), 3)

    def test_an_unassigned_system_name_is_null_not_false(self):
        engine = _engine("to get a\n  system __x\n  return __x = false\nend\n"
                         "to get b\n  system __x\n  return __x = null\nend\n")
        self.assertIs(engine.get("a"), False)
        self.assertIs(engine.get("b"), True)

    def test_loops_conditions_and_arrays(self):
        engine = _engine(
            "to get f\n"
            "  local int a[3]\n"
            "  step i from 1 to 3\n    a[i] = i * i\n  end\n"
            "  total = 0\n  n = 0\n"
            "  while n < 3\n    increment n\n    total = total + a[n]\n  end while\n"
            "  conditions\n    when total = 14\n      return \"ok\" & total\n    else\n      return \"no\"\n  end\n"
            "end\n"
        )
        self.assertEqual(engine.get("f"), "ok14")

    def test_forward_runs_the_next_book(self):
        engine = _engine(
            "to handle m\n  system log\n  put \"book \" after log\n  forward\nend\n",
            "to handle m\n  system log\n  put \"sbk\" after log\nend\n",
        )
        engine.send("m")
        self.assertEqual(engine.globals["log"], "book sbk")

    def test_push_onto_sysbooks_and_membership(self):
        pushed = []
        engine = _engine(
            "to get f\n"
            "  if \"a.sbk\" is not in sysBooks\n    push \"A.sbk\" onto sysBooks\n  end\n"
            "  push \"b.sbk\" onto sysBooks\n"
            "  return sysBooks\n"
            "end\n"
        )
        engine.on_push_sysbook = pushed.append
        self.assertEqual(engine.get("f"), "b.sbk,a.sbk")
        self.assertEqual(pushed, ["a.sbk", "b.sbk"])

    def test_go_to_hands_the_host_an_object_reference(self):
        class Recorder(Host):
            went = None

            def go(self, target):
                Recorder.went = target

        engine = _engine("to handle g\n  system nextpage, lastbook\n  go to page (nextpage) of book(lastbook)\nend\n",
                         host=Recorder())
        engine.globals.update(nextpage="P10", lastbook="x.tbk")
        engine.send("g")
        self.assertEqual(Recorder.went, Ref("page", "name", "P10", Ref("book", "name", "x.tbk", None)))

    def test_a_script_error_is_named_and_the_handler_goes_on(self):
        engine = _engine("to get f\n  x = \"a\" + 1\n  return 2\nend\n")
        self.assertEqual(engine.get("f"), 2)
        self.assertEqual(len(engine.errors), 1)

    def test_linked_dll_functions_go_to_the_host(self):
        class Shim(Host):
            def dll(self, library, name, args):
                return (True, 7) if (library, name) == ("kernel32.dll", "gettickcount") else (False, None)

        engine = _engine('to get f\n  linkDLL32 "kernel32.dll"\n    DWORD GetTickCount()\n  end\n'
                         '  return GetTickCount() + nothere()\nend\n', host=Shim())
        self.assertEqual(engine.get("f"), 7)
        self.assertIn("nothere()", engine.skipped)


class ReferenceTests(unittest.TestCase):
    def test_an_array_by_reference_is_shared_and_otherwise_copied(self):
        engine = _engine(
            "to get fill int a[] by reference\n  a[1] = 7\n  return 0\nend\n"
            "to get keep int a[]\n  a[1] = 9\n  return 0\nend\n"
            "to get f\n  local int n[]\n  get fill(n)\n  get keep(n)\n  return n[1]\nend\n"
        )
        self.assertEqual(engine.get("f"), 7)


class DllBufferTests(unittest.TestCase):
    def test_get_private_profile_string_fills_the_buffer_with_the_default(self):
        from opentoolbook.run import BookHost

        engine = _engine(
            'to get f\n  system string __first\n  linkDLL32 "kernel32.dll"\n'
            "    INT GetPrivateProfileStringA(STRING, STRING, STRING, STRING, INT, STRING)\n  end linkDLL32\n"
            '  __first = "First                   "\n'
            '  n = GetPrivateProfileStringA("Student", "First", "Student", __first, 21, "NIDAREC.INI")\n'
            '  return n & ":" & __first\nend\n',
            host=BookHost((), "book.tbk", ()),
            props=UserProperties(),
        )
        self.assertEqual(engine.get("f"), "7:Student")


class ChunkTests(unittest.TestCase):
    def test_get_and_put(self):
        self.assertEqual(get_chunk("a,b,c", "item", 2, 2), "b")
        self.assertEqual(get_chunk("one two  three", "word", 2, 3), "two  three")
        self.assertEqual(get_chunk("abc", "char", -1, -1), "c")
        self.assertEqual(put_chunk("a,b,c", "item", 2, 2, "x"), "a,x,c")
        self.assertEqual(put_chunk("a", "item", 3, 3, "z"), "a,,z")


if __name__ == "__main__":
    unittest.main()
