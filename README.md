# opentoolbook8

Rebuilding ToolBook 8 from analysis, so a book can run on a current operating system.

The 16-bit runtime is `TB80RTM` and `TB80BAS`. The notes and the unpacker live in the other repositories: `tbdecompile`, `tbworldview`, `squirreldra`, and `toolbookunpacker`. Foolbook is the viewer that already opens pages. Foolcourse, Foollege, and Foolversity sit above that viewer. This repository is the runtime those books need: object records, the class procedure a load calls, and the NIDA course shell around a lesson.

A record is one object in the book's directory, with a file position and a length.
A follow-up read is the two bytes stored after that body when the entry asks for them.
The message after a load is 0xe, passed to the procedure at the start of the class slot, and the report leaves that constant out.

What works in this tree:

- The object directory, the body read, and the two-byte follow-up when the entry asks for one.
- The class procedure for message `0xE`. It is the far pointer at the start of that class's `0x76`-byte slot. The lookup uses index 0.
- The NIDA menu export (`nida:m3search`), the disc table (`CAILT.DAT`), the install list (`toolbook.lst`), and the system books a lesson names.
- One rating folder from the key-disk creator: the description, the shift calendar, the encoded settings line, and the three versioned records.

A page is not drawn here, and OpenScript is not run here. Those are what the viewer already does.

```
python -m opentoolbook path/to/book.tbk
python -m opentoolbook --catalog courses.xml
python -m opentoolbook --catalog path/to/TBK
python -m opentoolbook --cailt CAILT.DAT 9E954D01
python -m opentoolbook --home path/to/TBK path/to/book.tbk
python -m opentoolbook --keydisk path/to/rating
python -m unittest discover -s tests
```

`OPENTOOLBOOK_TBK` points the extra tests at a lesson book. Without it, the tests use synthetic books and a synthetic menu.

On a live stop with the lesson already open, handle `0x0C1E` had class word `0x0001`. The lookup returned `0x2BAF:0000`, the live selector of the class dispatcher, and `ECX` was `0x76`. The 412-byte record takes the same path. This boot did not reach that return.
