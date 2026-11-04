"""``forward`` passes the running message to the next handler on the object path.

The path is SETTLED "Page messages": the object, its page, the page's background, the book,
then each ``sysBooks`` book. The engine's ``_do_Forward`` runs the handler after the running
one in that list, with the same message, arguments and target. Synthetic handlers only.
"""

import unittest

from opentoolbook.openscript.interp import Engine, Host
from opentoolbook.openscript.parser import parse_script

LOG = "  system log\n  put \"{name} \" after log\n"


def _handler(name, message="m", forward=True):
    body = LOG.format(name=name)
    return f"to handle {message} a\n{body}  put a after log\n" + ("  forward\n" if forward else "") + "end\n"


class PathHost(Host):
    """button, page, background: the object path a ``route`` host gives the engine."""

    def __init__(self, layers):
        super().__init__()
        self.layers = [parse_script(source).handlers for source in layers]
        self.commands = []

    def command(self, engine, name, args):
        self.commands.append((name, args))
        return True, None

    def route(self, kind, name, target, chain):
        key = f"{kind} {name}"
        return [layer[key] for layer in self.layers if key in layer] + list(chain(kind, name))


def _engine(objects, books):
    parsed = [parse_script(source).handlers for source in books]

    def lookup(kind, name):
        key = f"{kind} {name}"
        return [book[key] for book in parsed if key in book]

    return Engine(lookup, PathHost(objects))


class ForwardTests(unittest.TestCase):
    def test_each_level_runs_then_forwards_to_the_next(self):
        engine = _engine([_handler("button"), _handler("page"), _handler("background")],
                         [_handler("book"), _handler("sbk", forward=False)])
        engine.send("m", ("1",))
        self.assertEqual(engine.globals["log"], "button 1page 1background 1book 1sbk 1")

    def test_a_handler_that_does_not_forward_ends_the_path(self):
        engine = _engine([_handler("button"), _handler("page", forward=False), _handler("background")],
                         [_handler("book")])
        engine.send("m", ("x",))
        self.assertEqual(engine.globals["log"], "button xpage x")

    def test_a_level_with_no_handler_is_skipped(self):
        engine = _engine([_handler("button"), "", _handler("background", forward=False)], [])
        engine.send("m", ("2",))
        self.assertEqual(engine.globals["log"], "button 2background 2")


    def test_past_the_last_handler_the_host_gets_the_built_in_command(self):
        engine = _engine([_handler("page", "hide")], [])
        engine.send("hide", ("3",))
        self.assertEqual((engine.globals["log"], engine.host.commands), ("page 3", [("hide", ("3",))]))

if __name__ == "__main__":
    unittest.main()
