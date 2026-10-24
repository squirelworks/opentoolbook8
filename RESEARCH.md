# ToolBook

Notes gathered while reading the product and the specimen books. This file is not a second `SETTLED.md`. A behavior the reader implements is written there. A field that repeats in `9e954d01.tbk` is written in `FINDINGS.md`.

Each section names its source. A sentence from the decompile record is that record's claim. It is not a layout the reader uses.

## Sources

Public pages, read 24 October 2026 (Asia/Tokyo):

- Wikipedia, "ToolBook".
- Platte Canyon, *The EnterPage* 3-01 (Asymetrix becomes click2learn.com) and 6-04 (Click2learn merges with Docent).
- Denny Dedmore, [dennydedmore.com/toolbook](https://dennydedmore.com/toolbook/).

The October 2026 decompile record is the graded notes from the NE images (`TB80BAS`, `TB80RTM`, `TB80CMP`, and the modules beside them). Grades in that record stay in that record.

The specimen is `9e954d01.tbk` (Logic Families) and, where a second book is named, `nida81.tbk`.

## Product

ToolBook is a Windows training program. A file is a book, a book holds pages, and a page holds objects with handlers. Asymetrix shipped version 1.0 in 1990 and showed it with Windows 3.0. The company became click2learn.com in 1999 and SumTotal Systems in the March 2004 merger with Docent. Version 8.1 is the 2001 release. Version 9.0, in 2007, is the first version described as a 32-bit product. Version 9.01 is the last Assistant. Version 9.5 drops the Instructor name and adds the TBKX export. Version 11.5, in December 2012, is the last release. SumTotal ended sales, support, and activation on 31 December 2021.

OpenScript runs in the native engine. The Actions Editor is a smaller language that also publishes to a browser. The Navy lessons of this generation are native books. The specimen's version word is `01 00 00 08`.

## The 8.1 engine

From the decompile record. The images in that set are 16-bit NE. Windows 98 through 32-bit XP can run them.

| Module | Role |
|---|---|
| `TB80RUN` | 32-bit launcher. Starts `TB80NET` with the book on the command line. |
| `TB80NET` | 16-bit network provider. |
| `TB80RTM` | The window (`TBKMain`, `TBKClient`, `TBKChildWindow`). `WM_PAINT` goes to `CLIENTTOPAGE`, then `CDBPAINTCLIENT`. |
| `TB80BAS` | Book server. 606 exports. File open, view page, view background, paint, twip scale. |
| `TB80CMP` | Compiles and expands OpenScript. Keyword resource `0x77` has 994 entries. |
| `TB80BMP` | Bitmap blit. Ordinal 3 reads a bitmap. |

`CDBFILEOPEN` is ordinal 8. `CDBVIEWPAGE` is 15. `CDBVIEWBKGND` is 18. `CDBPAINTCLIENT` is 26. `CDBSENDCREATE`, ordinal 51, creates objects from Instructor. A lesson open does not call it. The October 2026 trace reads an object body by the length in the directory and then sends message `0xE`. The function that does that read has no export name.

Painters live in `TB80BAS` and call GDI. Stored coordinates are twips. The scale in that record is `(coord * dpi + 720) / 1440`. At 96 dpi that is division by 15. This reader does not apply that scale.

## The specimen

`9e954d01.tbk` names `nida81.tbk` and the `nc81*.sbk` system books and calls into them. The lesson file still opens when those files are absent. `minstb32.dll` is named and is not shipped. The filenames, the calls, and the search order are in `SETTLED.md`.

From the bytes, recorded in `FINDINGS.md`:

- The directory walk yields 206 records. `nida81.tbk` yields 114 by the same rule.
- Class `0x5` is an 81-byte page. There are 131. The object starts 14 bytes into the body. Body offset 9 is `0x80` on 129 pages and `0x81` on `P440` and `P2920`. The next three bytes are `65 00 05` on all 131. `nida81.tbk` uses `0x81` once, on `P22100`.
- The page-id walk includes `P0`, `P430`, `P440`, and `P2920`.
- Class `0x10` polygons and class `0x11` arcs are counted in `FINDINGS.md`. The reader returns the stored points.

The decompile record's 11.5 export of this book has 131 `Page.xml` files, 654 `IrregularPolygon` tags, and 62 `Arc` tags. Those three counts match the class `0x5`, `0x10`, and `0x11` scans. Equal counts are not a class-name binding.

## What this repository does

A page can be read when the bytes name the text, the page, and the stored shapes. That is partial: field text, page ids, background pattern and color, stored polygon points, arc endpoints, four huge bitmaps, and the twenty quiz records are read. They are not composed into a page.

A lesson can be walked when Next, Back, the menus, and the quiz follow the handlers. Menu and quiz targets are known as text. Nothing sends them.

A lesson can be run when the system books load, the initialize calls do what the DLLs imply, pictures land on their widgets, and the unnamed reader is implemented. That is not started. There is no window, no script engine, and no GDI.

## Where ToolBook checks for a page

From the unpacked `TB80BAS` image on this machine, searched 24 October 2026. The four bytes `80 65 00 05` and `81 65 00 05` do not occur in `TB80BAS.DLL` or in the unpacked image. No code compare uses the immediate `0x6580` or `0x6581`, and no code compare tests the size word against the constant `0x65`.

A page is the object whose class word, at object −2, is 5. The instruction is `cmp word [reg−2], 5`. It occurs 14 times in the unpacked code. The view path is one of them: `CDBVIEWPAGE` (ordinal 15) calls `FUN_1040_13c4`, which calls `FUN_1040_1420`, which calls `FUN_1040_18e4`. There the class word is compared with 5, and on a match the background is the far pointer at object `+0x47`. That is the same dword the specimen's background read uses.

The same class word is what this reader already tests. `page_ids` keeps a record when the word at −2 is 5. It does not require the flag byte to be `0x80`, so `P440` and `P2920` stay in the list. The size word at −4 is the object's end, measured from the segment base. On both books here that word is `0x65` and the page object is 81 bytes. A later TB80 book is a page when its class word is 5, with the length taken from its own size word.

Other class-5 branches in the same image, each a separate use of that compare: `FUN_1020_0e18` picks one of two pointers; `FUN_10c8_137e` does extra work when a page is destroyed; `FUN_1230_180c` returns before a draw when a parent is a page; `FUN_1578_1d34` changes a size when the class is 5 and the selector is `0x16`; `FUN_1450_06ce` requires class 5 and the words at `+2` and `+4` equal to `0xFFFF`, which is a narrower case than "any page." `FUN_10e0_0e8e` treats class 4 and class 5 alike and reads the list at `+0x2e`.

## Still open

The disk-to-object reader has no export name. The property that points a widget at a bitmap, other than the four huge-table pictures, is not settled. Fill, stroke, parent, and z-order are not a settled paint. OpenScript in the file is not expanded or run by this reader. The low bit that makes the byte at object −5 into `0x81` has no compare in `TB80BAS` and no meaning recorded yet. Only two TB80 books are on this machine, so "any TB80 book" is the rule above, checked on those two.

## The word at byte 2 of a style run

From `tbdecompile/research/paint-20261021.md`. That note calls the list at book `+0x28` a font table, and it says a style run's word at `+2` is an entry pointer, with the value 1 meaning the field's font at `+0x22`. The bytes agree that the word is 1 or a pointer in that list, and that the pointer addresses a C string. They do not show that 1 is replaced by the word at field `+0x22`. The reader returns the C string.

## The header slot is the resource type

From the decompile record, claim G-010. `FUN_1028_218a` in `TB80BAS` reads `OBJGETHDRLONG((type + 5) * 4)`. The index is the resource type. Type 1 is the bitmap directory. Putting a resource id in that slot does not name a bitmap. The dwords are in `FINDINGS.md`.

## Keyword resource 0x77

From the decompile record, chapter 14, and `TB80CMP`. `FUN_1040_0970` expands a handler. Resource `0x77` is 994 keyword ids. Index 0 is `to`, 1 is `handle`, 564 is `system`. The list in this reader is that id order, transcribed from `openscript_analysis` `core/keywords.py` because the resource binary is not on this machine.

Checked against `9e954d01.tbk`. The `Selection1` script on page `P300` contains the bytes `90 af 80 91 83` immediately before `"P310"`. Those opcodes are keyword `0x0AF` (`go`), keyword `0` (`to`, with the trailing space the clear bit 5 asks for), and keyword `0x183` (`page`). The expanded handler is the sentence in `SETTLED.md`. A back-reference copies from the segment that holds the script, which is the rule in that chapter after the output-stream copy was rejected. The reader does not call the handler.

## Line color bytes

From `tbdecompile/research/paint-20261021.md`. That note calls a draw object's stroke the bytes at `+0x17` and its fill the bytes at `+0x1B`, and its pattern the byte at `+0x25`. On every class `0x0E` record in both books the triples at `+0x17` and `+0x1B` have a 0 in the fourth byte. The byte at `+0x25` is not the pattern that note describes: the values are in `FINDINGS.md`, and the endpoints already occupy `+0x26`. The reader returns the two triples. It does not choose a brush.

## Type 10 handler

From `tbdecompile/research/paint-20261021.md`. That note says script mode 2 is a type 9 resource. In both books the page word at `+0x2A` minus 1 is an id in the type 9 directory and in the type 10 directory. The handler bytes are the count and the bytes named by the type 10 record's word at `+9`. The type 9 pointer is not those bytes. The reader returns the type 10 text. It does not call the handler.
