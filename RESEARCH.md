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

The sentence `ICs are classified into logic families based on voltage requirements` is one example of text in the gap after `P440`'s body and before the next directory record.

## What this repository does

A page can be read when the bytes name the text, the page, and the stored shapes. That is partial: field text, page ids, background pattern and color, stored polygon points, arc endpoints, four huge bitmaps, and the twenty quiz records are read. They are not composed into a page.

A lesson can be walked when Next, Back, the menus, and the quiz follow the handlers. Menu and quiz targets are known as text. Nothing sends them.

A lesson can be run when the system books load, the initialize calls do what the DLLs imply, pictures land on their widgets, and the unnamed reader is implemented. That is not started. There is no window, no script engine, and no GDI.

## Still open

The disk-to-object reader has no export name. The property that points a widget at a bitmap, other than the four huge-table pictures, is not settled. Fill, stroke, parent, and z-order are not a settled paint. OpenScript in the file is not expanded or run by this reader. The low bit that makes a page header `81 65` instead of `80 65` has no meaning recorded yet.
