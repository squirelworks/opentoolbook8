"""Run one handler source on the interpreter, the way a click runs, for tests."""

import re

from opentoolbook.clickrun import send_click


def run(source, pages=("P1", "P2", "P3"), page_id="P1", *, data=b"", fields=None, variables=None, book="", props=None, ask=None, args=()):
    """Send the handler's message to the page. A source with no ``to handle`` is a ``buttonClick`` body."""
    found = re.search(r"to\s+handle\s+(\w+)", source, re.IGNORECASE)
    if found is None:
        source = f"to handle buttonClick\n{source}\nend"
        message = "buttonclick"
    else:
        message = found.group(1).lower()
    return send_click(
        data, page_id, pages, book, (), [{message: source}], None,
        variables=variables, fields=fields, message=message, props=props, ask=ask, args=args,
    )
