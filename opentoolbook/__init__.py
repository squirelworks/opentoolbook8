"""A ToolBook 8 reader.

It opens a book, draws a page, and runs part of the book's OpenScript.
The default command opens the book on the page its startup handlers
name, or on the first stored page when they do not name one.
``--report`` prints the book report and does not open a window.
``--show PAGE`` draws that page id and does not follow startup handlers.
``linkDLL`` is not executed. ``forward`` passes the message up the object path.
"""

from opentoolbook.record import Book, handler_at, procedure_for_message
from opentoolbook.shelf import named_calls, named_files

__all__ = [
    "Book",
    "handler_at",
    "named_calls",
    "named_files",
    "procedure_for_message",
]
