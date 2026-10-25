"""A ToolBook 8 reader.

It opens a book, draws a page, and runs part of the book's OpenScript.
The default command prints a report. It does not open a window, and it
does not run the startup handlers that would land on the opening page.
"""

from opentoolbook.nida import Catalog, discs_for, parse_catalog
from opentoolbook.record import Book, handler_at, procedure_for_message
from opentoolbook.shelf import named_calls, named_files

__all__ = [
    "Book",
    "Catalog",
    "discs_for",
    "handler_at",
    "named_calls",
    "named_files",
    "parse_catalog",
    "procedure_for_message",
]
