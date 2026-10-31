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

Painters live in `TB80BAS` and call GDI. Stored coordinates are page units. The scale in that record is `(coord * dpi + 720) / 1440`. At 96 dpi that is division by 15, plus a half from the 720. This reader converts a page unit as one twentieth of a point and a point as 96/72 pixels, which is the division by 15, then multiplies by the fit scale once. It does not add 720.

## The specimen

`9e954d01.tbk` names `nida81.tbk` and the `nc81*.sbk` system books and calls into them. The lesson file still opens when those files are absent. `minstb32.dll` is named and is not shipped. The filenames, the calls, and the search order are in `SETTLED.md`.

From the bytes, recorded in `FINDINGS.md`:

- The directory walk yields 206 records. `nida81.tbk` yields 114 by the same rule.
- Class `0x5` is an 81-byte page. There are 131. The object starts 14 bytes into the body. Body offset 9 is `0x80` on 129 pages and `0x81` on `P440` and `P2920`. The next three bytes are `65 00 05` on all 131. `nida81.tbk` uses `0x81` once, on `P22100`.
- The page-id walk includes `P0`, `P430`, `P440`, and `P2920`.
- Class `0x10` polygons and class `0x11` arcs are counted in `FINDINGS.md`. The readers return the stored points. The window paints the polygons. It does not paint the arcs.

The decompile record's 11.5 export of this book has 131 `Page.xml` files, 654 `IrregularPolygon` tags, and 62 `Arc` tags. Those three counts match the class `0x5`, `0x10`, and `0x11` scans. Equal counts are not a class-name binding.

## What this repository does

`python3 -m opentoolbook path/to/book.tbk` opens the book on its opening page. `--report` prints the book report and does not open a window. The opening page is the quoted `go to page` a taken startup branch names, or the first page in the book's page list when no branch names one. `enterSystem` in `9e954d01.tbk` calls `openSession` and, only when that returns 1, `gotoPageList`. `openSession` in `nc81recs.sbk` returns 0 when `__studentRecords` is 0. `getStudentInfo` sets that from `GetPrivateProfileIntA`, whose default in the script is 0, and the reader does not call the DLL. `gotoPageList` in `nc81base.sbk` says `go to page(pagename) of book(bookname)`. Those names are not quoted. A resumed session is not the page that opens. The first stored page of the lesson is `P0`. Its `enterPage`, on the reader branch, says `go to page "P0" of book getLogoBook()`. `getLogoBook` returns `nida81.tbk` unless the same file search finds `logo81.tbk` or `mrj81.tbk`. `fileExists32` is not called. `forward` has no body here.

`python3 -m opentoolbook --show P300 path/to/9e954d01.tbk` opens that page. The same display list is built without a screen. On `P10` the `enterPage` handler writes the greeting into field `first`. The facts of that paint and that write are in `SETTLED.md`. What the window does not paint, and which handlers it does not run, is under Still open.

## Core calls with no body

`forward` is a statement in the `enterPage` handler of pages `P10`, `PINFO`, and `PQINFO` in `9e954d01.tbk`. Searched 25 October 2026: none of `9e954d01.tbk`, `nida81.tbk`, `nc81base.sbk`, `nc81recs.sbk`, `nc81test.sbk`, or `nc81trnr.sbk` stores `to handle forward` or `to get forward`. The reader does not invent that body. `setSection` is not in this list: its body is `to get setSection` in `nc81base.sbk`, and that body calls `kernel32.dll`. The reader does not call the DLL.

`send next` and `send previous` are the statements `gotoNextQuestionEx` and `gotoPreviousQuestionEx` in `nc81test.sbk` run when `__quizPass` is 8. The same search found no `to handle next` and no `to handle previous`. The Next and Back handlers on page `P100` of `9e954d01.tbk` are those two statements, and the comments on those handlers are `Go to next page` and `Go to previous page`. A list-opened quiz page uses the next and previous ids in the stored page list. The reader does not invent another body.

## Where ToolBook checks for a page

From the unpacked `TB80BAS` image on this machine, searched 24 October 2026. The four bytes `80 65 00 05` and `81 65 00 05` do not occur in `TB80BAS.DLL` or in the unpacked image. No code compare uses the immediate `0x6580` or `0x6581`, and no code compare tests the size word against the constant `0x65`.

A page is the object whose class word, at object −2, is 5. The instruction is `cmp word [reg−2], 5`. It occurs 14 times in the unpacked code. The view path is one of them: `CDBVIEWPAGE` (ordinal 15) calls `FUN_1040_13c4`, which calls `FUN_1040_1420`, which calls `FUN_1040_18e4`. In `FUN_1040_18e4` the class word is compared with 5, and on a match the background is the far pointer at object `+0x47`. That is the same dword the specimen's background read uses. The far call that function makes is NE 9 `0x19F3`. Its targets are in the indirect-call section below.

The same class word is what this reader already tests. `page_ids` keeps a record when the word at −2 is 5. It does not require the flag byte to be `0x80`, so `P440` and `P2920` stay in the list. The size word at −4 is the object's end, measured from the segment base. On both books here that word is `0x65` and the page object is 81 bytes. A later TB80 book is a page when its class word is 5, with the length taken from its own size word.

Other class-5 branches in the same image, each a separate use of that compare: `FUN_1020_0e18` picks one of two pointers; `FUN_10c8_137e` does extra work when a page is destroyed; `FUN_1230_180c` returns before a draw when a parent is a page; `FUN_1578_1d34` changes a size when the class is 5 and the selector is `0x16`; `FUN_1450_06ce` requires class 5 and the words at `+2` and `+4` equal to `0xFFFF`, which is a narrower case than "any page." `FUN_10e0_0e8e` treats class 4 and class 5 alike and reads the list at `+0x2e`.

## Still open

Settled behavior is in `SETTLED.md`. These are the gaps.

The disk-to-object reader in `TB80BAS` has no export name. This tree does not call that DLL. There is no authoring path and no writer.

The default command runs `enterSystem` and `enterApplication`, and the `get` calls those handlers make, as far as a quoted `go to page` and the reader branch go. `--report` prints the startup names and does not run them. `--show` draws the page id it is given and does not follow the startup handlers. `gotoPageList` is not a quoted page. `forward` is not executed. A `linkDLL` line is not called.

Book script is expanded to source. The page window runs a subset of it: the `enterPage` field writes in `SETTLED.md`, a quoted `go to page`, `send next`, `send previous`, and the quiz-button cases. It does not execute a handler as a language. `forward` has no body in the lesson or the four system books, and the reader does not invent one. A `linkDLL` line is not called.

The page walk names classes `0x8`, `0x9`, `0xA`, `0xB`, `0xC`, `0xD`, `0xE`, `0x10`, `0x11`, `0x13`, `0x15`, and `0x19`. Of those, the window paints rectangles, ellipses, lines, class `0x10` polygons, fields, and buttons (the up picture, or the checked picture when the button is checked), plus the class 4 background. It does not paint `0xD`, arcs (`0x11`), class `0x13` point lists, `0x15`, or `0x19`. A group is not a paint; its children are. Class `0x12` pies and class `0x17` records are outside that walk, and the window does not paint them. Invert and disabled button pictures are read and not drawn. Pattern 254 is a solid fill and pattern 253 is no fill. Another pattern byte is not drawn as a hatch.

A quoted `of book` click looks for that filename in the directory of the book passed to `--show`. The report's search of the parent directory is a different path.

The low bit that makes the byte at object −5 into `0x81` has no compare in `TB80BAS` and no meaning recorded yet. Only two TB80 books are on this machine, so "any TB80 book" is the rule in the page section above, checked on those two.

On a live stop with the lesson already open, handle `0x0C1E` had class word `0x0001`. The lookup returned `0x2BAF:0000`, the live selector of the class dispatcher, and `ECX` was `0x76`. The 412-byte record takes the same path. This boot did not reach that return. That stop is not a behavior this reader implements.

## The word at byte 2 of a style run

From `tbdecompile/research/paint-20261021.md`. That note calls the list at book `+0x28` a font table, and it says a style run's word at `+2` is an entry pointer, with the value 1 meaning the field's font at `+0x22`. The bytes agree that the word is 1 or a pointer in that list, and that the pointer addresses a C string. They do not show that 1 is replaced by the word at field `+0x22`. The reader returns the C string.

## The header slot is the resource type

From the decompile record, claim G-010. `FUN_1028_218a` in `TB80BAS` reads `OBJGETHDRLONG((type + 5) * 4)`. The index is the resource type. Type 1 is the bitmap directory. Putting a resource id in that slot does not name a bitmap. The dwords are in `FINDINGS.md`.

## Keyword resource 0x77

From the decompile record, chapter 14, and `TB80CMP`. `FUN_1040_0970` expands a handler. Resource `0x77` is 994 keyword ids. Index 0 is `to`, 1 is `handle`, 564 is `system`. The list in this reader is that id order, transcribed from `openscript_analysis` `core/keywords.py` because the resource binary is not on this machine.

Checked against `9e954d01.tbk`. The `Selection1` script on page `P300` contains the bytes `90 af 80 91 83` immediately before `"P310"`. Those opcodes are keyword `0x0AF` (`go`), keyword `0` (`to`, with the trailing space the clear bit 5 asks for), and keyword `0x183` (`page`). The expanded handler is the sentence in `SETTLED.md`. A back-reference copies from the segment that holds the script, which is the rule in that chapter after the output-stream copy was rejected. The expander returns the text. The page window runs the quoted `go to page` from that text. It does not execute the rest of the handler.

## Line color bytes

From `tbdecompile/research/paint-20261021.md`. That note calls a draw object's stroke the bytes at `+0x17` and its fill the bytes at `+0x1B`, and its pattern the byte at `+0x25`. On every class `0x0E` record in both books the triples at `+0x17` and `+0x1B` have a 0 in the fourth byte. The byte at `+0x25` is not the pattern that note describes: the values are in `FINDINGS.md`, and the endpoints already occupy `+0x26`. The line reader returns the two triples. The window strokes with the triple at `+0x17`. It does not build a GDI brush, and the byte at `+0x25` is not a hatch.

## Type 10 handler

From `tbdecompile/research/paint-20261021.md`. That note says script mode 2 is a type 9 resource. In both books the page word at `+0x2A` minus 1 is an id in the type 9 directory and in the type 10 directory. The handler bytes are the count and the bytes named by the type 10 record's word at `+9`. The type 9 pointer is not those bytes. The reader returns the type 10 text. The page window runs the book's `enterPage` when that text sets field `page#`, and it runs a page's inline `enterPage` field writes. It does not call the rest of the handler.

## Quiz handlers

From `nc81test.sbk` type 10 resource 741, expanded by this reader on 24 October 2026. The decompile record, chapter 14, says the four `nc81*` books have no decoded `to handle` text. The bytes in those books are `to get`. The reader returns that source. It does not execute the `.sbk` as OpenScript. The page window applies a few of the outcomes those handlers describe: an empty OK on pass 1 or 2 beeps and stays, and a list-opened question page turns with OK, Next, Skip, and Back. The steps two of those handlers share are in `FINDINGS.md`.

`processQuizScore` in `nc81base.sbk` is one function. It writes `NIDAREC.INI` through `WritePrivateProfileStringA`. That write is not a score the reader computes. `getquizResponse` is one function. The comparison that repeats is the two handlers in `FINDINGS.md`, which call it and test `answer of this page`.

## Schema element spelling

The SumTotal objects schema names one element `IrregularPloygon`. The TB115 export of `9e954d01` names that object `IrregularPolygon`, and the class `0x10` records are that object. This reader uses `IrregularPolygon`. The schema file is left as it was shipped.

## Pattern bytes 0xFD, 0xFE, and 0xFF

From `tbdecompile/research/paint-20261021.md`. `LOCKPATTERN` in `TB80BAS` is `1098:0876`. That note says `0xFD` is hollow, `0xFE` is solid paper, and `0xFF` is solid ink, and that `1` through `0x80` is a pattern. `0xFE` is stored on backgrounds and on class `0x8`, `0xC`, and `0x10` in both books. `0xFD` is stored on class `0x8` in both books. `0xFF` is not stored on those fields in either book, so that name is not applied here. The counts are in `FINDINGS.md`. The window treats 254 as a solid fill and 253 as no fill. It does not draw another pattern byte as a hatch.

## Indirect calls on view, load, and the class slot

From the unpacked `TB80BAS.DLL` on this machine, 24 October 2026. The listing is code a call path reached. It is not a request to run Ghidra, and it is not a force-disassembly of unknown bytes. NE segment `N` is the Ghidra base `0x1000 + (N - 1) * 8`. A listing address `10C8:00D0` is NE segment 26, offset `0x00D0`. Bytes below are the file bytes. A segment relocation fixes the segment word; the offset in a `9A` instruction is the offset. Where the fixup is chained, the word stored in the file is the next fixup, not the segment. This is not a layout the reader uses.

Ghidra's listing turns some of these into `(*local)()` aimed at a string in segment `1630`. The immediates are near offsets in the same code segment. `call word ptr [bp-…]` uses `CS`.

### The 0x76 class slot

The slot index and the message are different words. The load send and the value-bus send both take the far pointer at the start of the class's `0x76` bytes. Get takes the next dword. Set takes the one after that. The message is a separate argument.

`FUN_1180_02ce` (NE 49 `0x02CE`) is a far function, `retf 0x0E` (seven words). It pushes two zeros and then calls `0x03C8`:

| NE 49 | Bytes | What they are |
|---|---|---|
| `0x02D5` | `6A 00` | index word, passed as zero |
| `0x02D7` | `6A 00` | the word beside it, also zero |
| `0x02E2` | `E8 E3 00` | near call to `0x03C8` |

`0x03C8` (`ret 0x0C`) loads the class word and returns a far pointer:

| NE 49 | Bytes | What they are |
|---|---|---|
| `0x03CD` | `C4 5E 04` | `les bx, [bp+4]`, the far pointer argument |
| `0x03D0` | `26 8B 07` | `mov ax, es:[bx]`, the class word |
| `0x03D6` | `0B C0` / `74` | class word 0 returns `DX:AX = 0` |
| `0x0476` | `6B 4E FE 76` | `imul cx, [bp-2], 0x76` |
| `0x047A` | `03 C1` | add that to the table offset |
| `0x048C` | `8B 5E 0A` | the index that `0x02CE` passed as 0 |
| `0x048F` | `C1 E3 02` | `shl bx, 2` |
| `0x0495` | `26 8B 00` | offset at `table + class*0x76 + index*4` |
| `0x0498` | `26 8B 50 02` | segment at `+2` |

The table base is the far pointer at the caller's book record `+0x163`, then the dword at `+2` of that block (offset at `+2`, segment at `+4`). That walk is the same bytes at `0x0418`–`0x0472`. It runs only when the dword at `+0x163` is not zero.

`0x02CE` then calls `0x031E`, which calls the pointer:

| NE 49 | Bytes | What they are |
|---|---|---|
| `0x0356` | `05 02 00` | add 2 to the class-word pointer's offset |
| `0x036A` | `FF 5E 14` | `call far [bp+14h]`, the pointer `0x03C8` returned |

The handler therefore receives the object, and the class word sits at object `−2`. The message is the word at the handler's `[bp+0Eh]`, not the slot index.

The load site that pushes message `0x0E` is NE 48 `0x0AE0`, inside `FUN_1178_08b2`:

```
6A 0E          push 0x0E
6A 00          push 0
6A 00          push 0
9A CE 02 ..    call far NE 49:02CE
```

The segment word is a relocation to NE 49. The two pushes immediately before `6A 0E` are `FF 76 F4` and `FF 76 F6`, the far pointer `0x03C8` dereferences. The two zeros after `6A 0E` are `0x02CE`'s first two arguments, which `0x031E` passes on to the handler. The index `0x03C8` shifts is the pair of zeros `0x02CE` itself pushes at `0x02D5` and `0x02D7`. Message `0x0E` is the third argument of `0x02CE`.

The same slot read, with the index in `DS:0374` rather than a constant 0, is NE 49 `0x0093` (`26 6B 0F 76`) and `0x0261` (`26 6B 0F 76`), then `C1 E3 02` and a far load. `0x0132` calls the pointer at `0x02AD` (`FF 5E F4`). `OBJEXPORTMSGNEAR` (NE 49 `0x04A2`) stores its first argument at `DS:0374` (`A3 74 03`) and calls `0x010C`.

#### Value bus, same stride, fixed index

`CDBGETVALUEEX`, `CDBSENDVALUEEX`, and `CDBSETVALUEEX` are NE 16. Each multiplies the low byte only:

```
B0 76        mov al, 0x76
F6 66 12     mul byte ptr [bp+12h]
C4 5E FC     les bx, [bp-4]
26 03 47 02  add ax, es:[bx+2]
26 8B 57 04  mov dx, es:[bx+4]
```

`[bp-4]` is a far pointer already in the frame. These five instructions do not name a global. The `+2` / `+4` shape is the same one the NE 49 lookup uses on the `+0x163` block.

| Call | Bytes | Dword loaded | Export |
|---|---|---|---|
| NE 16 `0x10DF` | `FF 5E CC` | `26 8B 47 04` / `26 8B 57 06` (slot `+4`) | `CDBGETVALUEEX` |
| NE 16 `0x12B8` | `FF 5E DC` | `26 8B 07` / `26 8B 57 02` (slot `+0`) | `CDBSENDVALUEEX` |
| NE 16 `0x15EC` | `FF 5E E0` | `26 8B 47 08` / `26 8B 57 0A` (slot `+8`) | `CDBSETVALUEEX` |

The `mul` immediates are at `0x1080`, `0x124E`, and `0x1582`. The call before each one is `9A D6 03` with a segment relocation to NE 47, which is `OBJLOCKNEAR` at `1170:03D6`.

The stored pointer is not a constant in the image. A static scan of relocation heads found no `0x76`-spaced table of far pointers. Which class owns `10B0:0000` is not in these instructions.

#### What one returned handler does with `0x0E`

The October trace, already in chapter 4.6, saw `0x03C8` return `10B0:0000` for one handle and `10F8:0000` for another. Those addresses are NE 23 `0x0000` and NE 32 `0x0000`.

NE 23 `0x0000` compares `[bp+0Eh]` and reaches message `0x0E` by `2D 0A 00` then `2D 04 00` (so `0x0A + 4`). The arm is `0x01AE`. Its call is `E8 25 53` at `0x01B8`, a near call to `0x54E0` (`FUN_10b0_54e0`).

NE 32 `0x0000` compares `[bp+0Eh]` with `0x3004` and above. A value below `0x3004`, including `0x0E`, falls through to `33 C0` at `0x0059` and returns 0. There is no `0x0E` arm.

### View page

`CDBVIEWPAGE` is NE 9 `0x0000`. The only indirect transfer in that segment is the switch in `FUN_1040_1420`:

`0x1442`: `2E FF A7 48 14` (`jmp word ptr cs:[bx+1448h]`), after `2D 03 00` / `3D 0F 00` / `03 C0`. The word at `0x1448 + (value-3)*2` is the arm. Values `0x7` through `0x0E` share `0x1592`. The other arms are `0x1468`, `0x1505`, `0x1523`, `0x1478`, `0x1496`, `0x14CA`, `0x1500`, `0x151E` for `0x3`, `0x4`, `0x5`, `0x6`, `0x0F`, `0x10`, `0x11`, `0x12`. That is the switch the listing already shows.

`FUN_1040_18e4` calls the class dispatcher with a direct far call, not an indirect one. At NE 9 `0x19F3` the bytes are `9A 6C 00`; the segment relocation is NE 26. The target is `10C8:006C`, `FUN_10c8_006c`.

`FUN_1040_1876`, which `FUN_1040_13f2` calls, does the same to `FUN_10c8_1216`. At NE 9 `0x18AC` the bytes are `9A 16 12 F7 10`. The word `0x10F7` is the next link in a segment-fixup chain, not a segment number. The chain head is `0x19F6`, and that relocation record names NE 26. The offset in the instruction, `0x1216`, is the real offset.

#### `FUN_10c8_006c` (NE 26 `0x006C`)

The class word is `26 8B 47 FE` at `0x0080` (`es:[bx-2]`). The call is `0x00D0`, bytes `FF 56 FE`.

| Class | Bytes that store the offset | Target |
|---|---|---|
| 4 | `0x009C` `C7 46 FE FC 02` | NE 26 `0x02FC` `FUN_10c8_02fc` (`C8 08 00 00`) |
| 5 | `0x00BC` `C7 46 FE 82 03` | NE 26 `0x0382` `FUN_10c8_0382` (`C8 0A 00 00`) |
| anything else | `0x0095` `9A` | `TB80UTL` ordinal 115. The record calls that ordinal `TOOLBOOKFATAL`. |

Class 5, when bit 1 of `[bp+6]` is set and `USER` ordinal 284 returns below `0x14`, calls NE 9 `0x0838` (`9A 38 08` at `0x00B7`, segment relocation NE 9) before the `0x0382` call. That is `FUN_1040_0838`.

#### `FUN_10c8_0000` (NE 26 `0x0000`)

Same call shape, `0x0064` bytes `FF 56 FC`, class word from `es:[bx-2]` at `0x0007`. `FUN_1040_18e4` calls `0x006C`. This entry is the same near-offset rule.

| Class | Store | Target | Also |
|---|---|---|---|
| 4 | `0x002A` `FC 02` | `0x02FC` `FUN_10c8_02fc` | `[bp+6]` set to 4 at `0x0054` |
| 5 | `0x0032` `82 03` | `0x0382` `FUN_10c8_0382` | `[bp+6]` set to 4 |
| `0x0B` | `0x003A` `64 0D` | `0x0D64` `FUN_10c8_0d64` | argument left as passed |
| `0x25` | `0x0042` `C2 0B` | `0x0BC2` `FUN_10c8_0bc2` | `[bp+0Ch]` cleared, `[bp+6]` set to 4 |
| `0x26`, and every other word | `0x004A` or `0x0022` `B6 0E` | `0x0EB6` `FUN_10c8_0eb6` | `0x26` also clears `[bp+0Ch]` and sets `[bp+6]` to 4. A word above `0x26` does not. |

`0x0EB6`, `0x0BC2`, and `0x0D64` are `enter` prologues. The listing's string-plus-offset expressions (`s_TB80NET…+4`, `s_Object_Descriptor…+0x0E`, and the rest) are these immediates read as data addresses.

#### `FUN_10c8_1216` (NE 26 `0x1216`)

Class word at `0x121D` (`26 8B 47 FE`), then `2D 04 00` / `3D 23 00`. The jump is `0x122C`, bytes `2E FF A7 32 12`. The table is 36 words at `0x1232`, index `class - 4`, classes 4 through `0x27`.

| Classes | Table arm | What the arm calls |
|---|---|---|
| 4 | `0x12C6` | direct `E8 4C 00` to `0x131E` `FUN_10c8_131e`, argument `6A 07` |
| 5 | `0x12DE` | direct `E8 94 00` to `0x137E` `FUN_10c8_137e`, argument `6A 07` |
| 8, 9, `0x0A`, `0x0C`–`0x16`, `0x19`, `0x1A`, `0x24`, `0x26`, `0x27` | `0x12AF` | `C7 46 FE FE 17`, then the shared call |
| `0x0B` | `0x12EC` | `C7 46 FE 60 17` |
| `0x25` | `0x12F4` | `C7 46 FE EA 16` |
| 6, 7, `0x17`, `0x18`, `0x1B`–`0x23` | `0x127A` | tests byte `+0x56` bit 1. If set, falls into `0x12AF` (`0x17FE`). If clear, `9A` to `TB80UTL` ordinal 115 at `0x12BF`. |

The shared call is `0x1304`, bytes `FF 56 FE`, after pushing 7.

| Immediate | Target |
|---|---|
| `0x17FE` | `FUN_10c8_17fe` (`C8 14 00 00`) |
| `0x1760` | `FUN_10c8_1760` (`C8 18 00 00`) |
| `0x16EA` | `FUN_10c8_16ea` (`C8 16 00 00`) |

### Next cluster: NE 28 `FUN_10d8_0284`

`FUN_10d8_0000` calls `0x0284`. The only caller of `FUN_10d8_0000` in this image is `FUN_1228_0438`, and the only caller of that is the `0x304A` arm of the message switch at the start of NE 31. The bytes of that arm are below.

`0x0284` reads the class with `26 8B 47 FE` at `0x0294`, then calls `0x19B2`. If bit 0 of that result is clear (`A8 01` / `74 2E` at `0x02A4`), the path reaches `0x02DF`, bytes `9A FF FF 00 00`, a `ptr32` relocation at `0x02E0` to `TB80UTL` ordinal 115, and the next instruction is the bit 3 test. If bit 3 of the word from `0x19B2` is set (`F6 46 F6 08` at `0x02E4`), it stores `0x087E` and skips the switch. Otherwise `sub ax, 8` / `cmp ax, 0x1F` and the jump at `0x0300`, bytes `2E FF A7 06 03`. Thirty-two words at `0x0306`, index `class - 8`, classes 8 through `0x27`.

The indirect call is `0x03D1`, bytes `FF 56 F8`.

| Classes | Arm | Offset stored | Function |
|---|---|---|---|
| bit 3 of the `0x19B2` result | `0x02EA` | `0x087E` | `FUN_10d8_087e` |
| 8, 9, `0x15`, `0x19`, `0x1A`, `0x27` | `0x036E` | `0x05B8` | `FUN_10d8_05b8` |
| `0x0A`, `0x24` | `0x0386` | `0x06FC` | `FUN_10d8_06fc` |
| `0x0C` | `0x038E` | `0x0900` | `FUN_10d8_0900` |
| `0x0D` | `0x0396` | `0x0978` | `FUN_10d8_0978` |
| `0x0E` | `0x039E` | `0x0B50` | `FUN_10d8_0b50` |
| `0x0F`, `0x10` | `0x03A6` | `0x0CCE` | `FUN_10d8_0cce` |
| `0x11`, `0x12` | `0x03AE` | `0x0D58` | `FUN_10d8_0d58` |
| `0x13` | `0x03B6` | `0x117C` | `FUN_10d8_117c` |
| `0x14` | `0x03BE` | `0x1332` | `FUN_10d8_1332` |
| `0x16` | `0x03C6` | `0x0834` | `FUN_10d8_0834` |
| `0x0B`, `0x17`, `0x18`, `0x1B`–`0x23`, `0x25`, `0x26` | `0x0346` | none immediately | see below |

`0x0346` is not a function. If `[bp+4] > 3` and the word at `[bp+6]+0x74` is 0, it jumps to `0x02B2` and returns 0. Otherwise it calls the far routine at offset `0x00D4` (segment relocation at `0x0361` is NE 81, so `1280:00D4`, the listing's `FUN_1280_00d4`). If that result's word at `+0x28` is 0, the direct near call `E8 BA 14` at `0x037F` goes to `0x183C` (`FUN_10d8_183c`) and returns. If `+0x28` is not 0, it stores `0x05B8` and joins the indirect call.

Each stored offset is an `enter` prologue except `0x087E`, which is the `FUN_10d8_087e` the listing already has at that address. The listing's `DAT_1630_05b8` and the string-plus-offset arms are these same immediates.

The caller of `FUN_1228_0438` is the `0x304A` arm of `FUN_10f0_0000` (NE 31 `0x0000`). That arm is a direct jump, not a missed call. After `cmp ax, 0x3043` fails high, `0x00A8` is `2D 45 30` (`sub ax, 0x3045`), `0x00B0` is `48` (`dec ax`, so `0x3046`), and `0x00B6` is `2D 04 00` (`sub ax, 4`, so `0x304A`). The jump `E9 00 02` at `0x00BB` lands at `0x02BE`. The call there is `9A 38 04` at `0x02D0`. Its segment word, `0x02F0`, is the next link of the segment chain whose head is `0x25A2`. That record names NE 70. The offset `0x0438` is the offset in the instruction, so the target is `1228:0438`, the listing's `FUN_1228_0438`. The same chain fixes the calls at `0x028B` (`9A 1C 04`, NE 70 `0x041C`, `FUN_1228_041c`), `0x02A3` (`9A 46 03`, NE 70 `0x0346`, `FUN_1228_0346`), and `0x02B5` (`9A C8 04`, NE 70 `0x04C8`, `FUN_1228_04c8`). The export at NE 70 offset 0 is a different entry. A segment fixup does not mean offset 0.

The one indirect transfer in that prologue is the jump at `0x0092`, bytes `2E FF A7 98 00`, after `2D 28 30` / `3D 07 00` / `03 C0`. Eight words at `0x0098`, index `message - 0x3028`:

| Message | Word | Arm |
|---|---|---|
| `0x3028` | `0x0266` | pushes `0xD4` and near-calls `0x1788` (`FUN_10f0_1788`) |
| `0x3029`, `0x302A` | `0x0188` | the default arm |
| `0x302B`, `0x302C`, `0x302F` | `0x01E4` | shared arm |
| `0x302D` | `0x0282` | `9A 1C 04` to NE 70 `0x041C` |
| `0x302E` | `0x0294` | `9A 46 03` to NE 70 `0x0346` |

### Not named

`call far es:[bx+1Ch]` is `26 FF 5F 1C`. On the load and lookup path the bytes before it are always:

```
26 FF 77 02     push word ptr es:[bx+2]
26 FF 37        push word ptr es:[bx]
26 C4 1F        les bx, es:[bx]
26 C4 1F        les bx, es:[bx]
26 FF 5F 1C     call far es:[bx+1Ch]
```

The two `les` load the first dword, then the first dword of that. The call is the far pointer at offset `0x1C` of the second object. The file has no relocation run that places a known function at that offset for this object. The same five instructions occur at NE 49 `0x01F9`, `0x0243`, `0x0411`, `0x045B` (the book-index walk inside the slot lookup) and at NE 48 `0x05D5`, `0x071B`, `0x0AAD`, `0x12CD`, `0x14C9`, `0x1849`, `0x1A2D`, `0x1B1D`, `0x1C09` (the loader, including the site just above the `0x0E` send). The image contains 37 copies of `26 FF 5F 1C` in all. They stay unresolved for the same reason.

NE 48 `0x1F1C` is `26 FF 5F 18` after a single `les bx, es:[bx]`. One dereference, slot `+0x18`. No constant target.

`FUN_10f0_0000` has ten more indirect calls. Each is `les bx, [bp+4]` and then `call far es:[bx+disp]`. The displacement is in the instruction. The far pointer is the argument. No relocation in this segment writes a known function into that field.

| NE 31 | Bytes | Displacement |
|---|---|---|
| `0x063B` | `26 FF 5F 04` | `+4`, after pushing `0x0B`, `0`, `0` |
| `0x0712` | `26 FF 5F 04` | `+4`, after pushing `0x0E` |
| `0x06A4`, `0x06C8` | `26 FF 5F 0C` | `+0x0C` |
| `0x073E`, `0x0774` | `26 FF 5F 08` | `+8` |
| `0x096B`, `0x09BC` | `26 FF 9F DA 03` | `+0x3DA` |
| `0x0905` | `26 FF 9F DE 03` | `+0x3DE` |
| `0x0A4A` | `26 FF 9F 4E 04` | `+0x44E` |

NE 10, the file segment: `0x0D86` is `FF 5E 04` and `0x118D` is `FF 5E 06`. Both pointers are arguments. `0x2478` is `FF 5E F6`. The pointer was returned in `DX:AX` by `KERNEL` ordinal 50 at `0x2459` (`9A`, relocation `KERNEL.50`), called with the C string at data `0x0266`, which reads `CnvFileConvert`. The body of that procedure is not in `TB80BAS`.

NE 3, the paint segment: three `jmp word ptr cs:[bx+…]` after `cmp ax, 7` (`0x2A2A`, `0x3795`, `0x52AF`). Each table entry is an arm in the same function (`mov bx, [bp+8]` or a `cmp` of a local), not another call. The one indirect call is `0x5331`, bytes `FF 5E 08`. The pointer is `[bp+8]`, an argument. This function does not choose it.

## Author install and the NIDA name list

Measured 24 October 2026 from the files on this machine. No installer, DLL, or book was copied into this repository.

The author tree is the ToolBook II Instructor 8.1 install under the Wine prefix `/tmp/tb81/wine`:

- `drive_c/Program Files/Common Files/click2learn/TBSystem`
- `drive_c/Program Files/click2learn/Instructor8`
- the other click2learn directories beside those two: `Editors`, `Filters`, `Neuron`, `Spelling`

A NIDA distribution directory was not found. Nothing under `/tmp/refs`, `/tmp/nida`, `/tmp/nida-home`, `/tmp/nida98`, or the Wine prefix holds the runtime EXEs and DLLs next to `nida81.tbk`. The shortcut `/tmp/refs/guest/tb80rtm.lnk` names `C:\TBK\TB80RTM.EXE`. That directory was not extracted. The Windows 98 disk image was not opened. The lists below do not invent a runtime directory from a book header.

What was present:

- `/tmp/refs/guest`, a folder of copied books and a few neighbors. It is not `C:\TBK`.
- `toolbook.lst` in the course home. The copies at `/tmp/nida-home/toolbook.lst`, `/tmp/nida/toolbook.lst`, and `/tmp/nida/home/toolbook.lst` are the same 592 bytes. A leading `*` is on four lines. Those four files were not found on disk. The other 42 lines are the course's name list.

The partition further down is that name list against the author filenames. Sizes are the author copies, except where a guest file is named with its own size. A name in the course list is not a claim that this reader needs that file to open a `.tbk`.

### TBSystem

70 files. `TB80*.DLL` and the EXEs in this directory are marked NE or PE when that magic was read at the offset in the DOS header. NE is the 16-bit mark. PE is the 32-bit mark. No other bytes were decoded.

| Bytes | File | Mark |
|---:|---|---|
| 1638 | `asym.ini` |  |
| 29696 | `Asymgif.ocx` |  |
| 30544 | `DIB.DRV` |  |
| 48661 | `DIBUTIL.DLL` |  |
| 253952 | `dzactx.dll` |  |
| 802816 | `ISGDI32.DLL` |  |
| 4338 | `ISGDI32.INI` |  |
| 119296 | `Oxs.dll` |  |
| 48661 | `PALOPTX.DLL` |  |
| 83520 | `PCDLIB.DLL` |  |
| 2336 | `PCDXBMP.DLL` |  |
| 33088 | `PHOTO.DLL` |  |
| 236734 | `PXENGWIN.DLL` |  |
| 67984 | `TB2FTP.DLL` |  |
| 66048 | `TB80.EXE` | PE |
| 1669 | `tb80.ini` |  |
| 207989 | `tb80actr.sbk` |  |
| 247296 | `TB80ACX.DLL` | PE |
| 85719 | `tb80aicc.sbk` |  |
| 64023 | `tb80anm.sbk` |  |
| 705824 | `TB80ATH.EXE` | NE |
| 683872 | `TB80BAS.DLL` | NE |
| 68640 | `TB80BMP.DLL` | NE |
| 193216 | `TB80CMP.DLL` | NE |
| 27552 | `TB80CVT.DLL` | NE |
| 106432 | `TB80EDT.DLL` | NE |
| 219872 | `TB80ENU1.DLL` | NE |
| 79360 | `TB80ENU2.DLL` | PE |
| 551968 | `TB80ENU3.DLL` | NE |
| 397824 | `TB80ENU4.DLL` | PE |
| 78848 | `TB80F32L.dll` | PE |
| 101152 | `TB80FLT.DLL` | NE |
| 242983 | `tb80ftp.sbk` |  |
| 140613 | `tb80hyp.sbk` |  |
| 63872 | `TB80JPG.DLL` | NE |
| 97792 | `TB80LNL.DLL` | NE |
| 23552 | `TB80MAIN.EXE` | PE |
| 24800 | `TB80MM.DLL` | NE |
| 3352 | `TB80MM.INI` |  |
| 67360 | `TB80NET.EXE` | NE |
| 206528 | `TB80OCX.DLL` | NE |
| 85952 | `TB80OLE.DLL` | NE |
| 953705 | `tb80r.sbk` |  |
| 169760 | `TB80RCA.DLL` | NE |
| 67824 | `TB80RCR.DLL` | NE |
| 109056 | `TB80RMT.DLL` | PE |
| 462080 | `TB80RTM.EXE` | NE |
| 65536 | `TB80RUN.EXE` | PE |
| 64128 | `TB80UTL.DLL` | NE |
| 75328 | `TB80VBX.DLL` | NE |
| 76512 | `TB80W16.DLL` | NE |
| 83456 | `TB80W32.DLL` | PE |
| 41783 | `TB80XTR.DLL` | NE |
| 31616 | `TBCBT.DLL` |  |
| 53248 | `TBCOM.DLL` |  |
| 66560 | `TBDB3.DLL` |  |
| 36800 | `TBDLG.DLL` |  |
| 15616 | `TBDOS.DLL` |  |
| 21952 | `TBFILE32.DLL` |  |
| 532480 | `TBINET32.DLL` |  |
| 57344 | `TBKSLICE.DLL` |  |
| 87040 | `Tbload.exe` | PE |
| 30880 | `TBPDX.DLL` |  |
| 19552 | `TBREG.DLL` |  |
| 40960 | `TBUTIL32.dll` |  |
| 40608 | `TBWIN.DLL` |  |
| 267264 | `Tlist16p.ocx` |  |
| 460744 | `TList4.ocx` |  |
| 204562 | `VEAMAA51.LEX` |  |
| 86496 | `WINSOX.EXE` | NE |

`TB80.EXE` is in this directory (66048 bytes, PE). `TB80ATH.EXE` (705824, NE), `TB80MAIN.EXE` (23552, PE), `TB80NET.EXE` (67360, NE), `TB80RTM.EXE` (462080, NE), `TB80RUN.EXE` (65536, PE), and `Tbload.exe` (87040, PE) are the other EXEs here. `WINSOX.EXE` is 86496 bytes, NE.

### Instructor8

349 files. This is the author program directory. `Inst80.exe` is the Instructor program. `Packager/PACKAGER.exe` and `Packager/PACKLIST.EXE` are the distribution builder. The other EXEs in this tree are `AUTORUN.EXE`, `decrypt.exe`, `impulse.exe`, `logread.exe`, `remover.exe`, `Repair80.exe`, `tb80ftp.exe`, `Packager/SETUP.EXE`, `Packager/Regsvr.exe`, and `Packager/_ISDEL.EXE`.


#### Instructor8 root

35 files.

| Bytes | File | Mark |
|---:|---|---|
| 421888 | `AUTORUN.EXE` | PE |
| 8798 | `Autorun.ICO` |  |
| 56969 | `axf.dtd` |  |
| 17648 | `blank.tbk` |  |
| 121249 | `decrypt.exe` | NE |
| 24615 | `DECRYPT.HLP` |  |
| 5183 | `distrib.wri` |  |
| 139487 | `impulse.exe` | NE |
| 18419 | `INST80.CNT` |  |
| 441344 | `Inst80.exe` | PE |
| 6354973 | `INST80.HLP` |  |
| 980 | `inst80.ini` |  |
| 1032 | `Inst80.pal` |  |
| 70132 | `INST80.SBK` |  |
| 545071 | `logread.exe` | PE |
| 43362 | `logread.hlp` |  |
| 902550 | `mercury.jar` |  |
| 184830 | `PATHANIM.HLP` |  |
| 95927 | `remover.exe` | PE |
| 766 | `remover.ico` |  |
| 426209 | `Repair80.exe` | PE |
| 766 | `scrwalk.ico` |  |
| 178875 | `scrwalk.tbk` |  |
| 480 | `startup.ini` |  |
| 3086352 | `tb80.sbk` |  |
| 2392403 | `tb80a.sbk` |  |
| 2120361 | `tb80acta.sbk` |  |
| 617740 | `tb80axf.sbk` |  |
| 74386 | `tb80ftp.exe` | PE |
| 100533 | `TB80FTP.HLP` |  |
| 619201 | `tb80i.sbk` |  |
| 62053 | `tb80lmx.sbk` |  |
| 1130973 | `tb80web.sbk` |  |
| 256257 | `tb80x.sbk` |  |
| 342145 | `UnInst80.isu` |  |

#### Instructor8/Catalog

126 files.

| Bytes | File | Mark |
|---:|---|---|
| 108155 | `Catalog/abullet.spb` |  |
| 109910 | `Catalog/actdelay.spb` |  |
| 8581 | `Catalog/Action Objects.ini` |  |
| 237707 | `Catalog/Action Objects.wbk` |  |
| 457027 | `Catalog/Action Objects.wbx` |  |
| 153701 | `Catalog/acttimer.spb` |  |
| 288063 | `Catalog/allmedia.spb` |  |
| 136983 | `Catalog/automenu.spb` |  |
| 101816 | `Catalog/bullets.spb` |  |
| 87495 | `Catalog/butnedit.spb` |  |
| 4113 | `Catalog/Buttons.ini` |  |
| 109543 | `Catalog/Buttons.wbk` |  |
| 297239 | `Catalog/Buttons.wbx` |  |
| 104363 | `Catalog/callout.spb` |  |
| 57947 | `Catalog/Catalog Blank Cache.tbk` |  |
| 16259 | `Catalog/Catalog Blank Category.tbk` |  |
| 16259 | `Catalog/Catalog Blank Spec Cache.tbk` |  |
| 441408 | `Catalog/Catalog Spec Cache.tbk` |  |
| 1760 | `Catalog/catalog.ini` |  |
| 24500 | `Catalog/CATOBJT.HLP` |  |
| 6759 | `Catalog/click2learn.author.ini` |  |
| 372565 | `Catalog/click2learn.author.wbk` |  |
| 455813 | `Catalog/click2learn.author.wbx` |  |
| 1048 | `Catalog/click2learn.pal` |  |
| 12196 | `Catalog/CLIPWID.HLP` |  |
| 87355 | `Catalog/clipwid.spb` |  |
| 8206 | `Catalog/Draw Objects.ini` |  |
| 149063 | `Catalog/Draw Objects.wbk` |  |
| 452985 | `Catalog/Draw Objects.wbx` |  |
| 283967 | `Catalog/dropbin.spb` |  |
| 12497 | `Catalog/EVALBOOK.HLP` |  |
| 108138 | `Catalog/evalbook.spb` |  |
| 11733 | `Catalog/EVALPAGE.HLP` |  |
| 116375 | `Catalog/evalpage.spb` |  |
| 62029 | `Catalog/extjava.spb` |  |
| 154884 | `Catalog/fldglist.spb` |  |
| 175266 | `Catalog/fldolist.spb` |  |
| 56859 | `Catalog/genedit.spb` |  |
| 11814 | `Catalog/IMAGEMAP.HLP` |  |
| 170730 | `Catalog/imagemap.spb` |  |
| 11398 | `Catalog/IMGEDIT.HLP` |  |
| 96467 | `Catalog/imgedit.spb` |  |
| 82699 | `Catalog/inetauto.spb` |  |
| 80368 | `Catalog/liblogin.spb` |  |
| 107076 | `Catalog/listedit.spb` |  |
| 120468 | `Catalog/marquee.spb` |  |
| 1721 | `Catalog/Media (Animated).ini` |  |
| 190404 | `Catalog/Media (Animated).wbk` |  |
| 218557 | `Catalog/Media (Animated).wbx` |  |
| 16259 | `Catalog/Media (Backdrops).ini` |  |
| 18613209 | `Catalog/Media (Backdrops).wbk` |  |
| 1063909 | `Catalog/Media (Backdrops).wbx` |  |
| 45418 | `Catalog/Media (Clipart).ini` |  |
| 5188295 | `Catalog/Media (Clipart).wbk` |  |
| 3826933 | `Catalog/Media (Clipart).wbx` |  |
| 35164 | `Catalog/Media (Icons).ini` |  |
| 357795 | `Catalog/Media (Icons).wbk` |  |
| 3476871 | `Catalog/Media (Icons).wbx` |  |
| 13288 | `Catalog/Media (Tiled Backdrops).ini` |  |
| 1930465 | `Catalog/Media (Tiled Backdrops).wbk` |  |
| 1044433 | `Catalog/Media (Tiled Backdrops).wbx` |  |
| 16596 | `Catalog/Media Players.ini` |  |
| 658231 | `Catalog/Media Players.wbk` |  |
| 941911 | `Catalog/Media Players.wbx` |  |
| 50275 | `Catalog/mediabtn.spb` |  |
| 268283 | `Catalog/mtchitem.spb` |  |
| 271729 | `Catalog/mtchobj.spb` |  |
| 293037 | `Catalog/multdrop.spb` |  |
| 278057 | `Catalog/multiobj.spb` |  |
| 272641 | `Catalog/multline.spb` |  |
| 288093 | `Catalog/multwid.spb` |  |
| 136 | `Catalog/My Objects.ini` |  |
| 19016 | `Catalog/My Objects.wbk` |  |
| 84849 | `Catalog/My Objects.wbx` |  |
| 272519 | `Catalog/namepart.spb` |  |
| 32862 | `Catalog/Navigation Objects.ini` |  |
| 2777159 | `Catalog/Navigation Objects.wbk` |  |
| 1500039 | `Catalog/Navigation Objects.wbx` |  |
| 149770 | `Catalog/neuron.spb` |  |
| 280045 | `Catalog/orderobj.spb` |  |
| 242801 | `Catalog/orderwid.spb` |  |
| 115230 | `Catalog/pagemenu.spb` |  |
| 3511 | `Catalog/Pages.ini` |  |
| 14289261 | `Catalog/Pages.wbk` |  |
| 776449 | `Catalog/Pages.wbx` |  |
| 6737 | `Catalog/Placeholder Objects.ini` |  |
| 179077 | `Catalog/Placeholder Objects.wbk` |  |
| 368015 | `Catalog/Placeholder Objects.wbx` |  |
| 347473 | `Catalog/popupump.spb` |  |
| 11565 | `Catalog/POPVID.HLP` |  |
| 235308 | `Catalog/popvid.spb` |  |
| 84081 | `Catalog/questext.spb` |  |
| 63165 | `Catalog/QUESTION.HLP` |  |
| 42103 | `Catalog/Questions (Multiple Choice).ini` |  |
| 1295499 | `Catalog/Questions (Multiple Choice).wbk` |  |
| 1702455 | `Catalog/Questions (Multiple Choice).wbx` |  |
| 26094 | `Catalog/Questions (True-False).ini` |  |
| 869947 | `Catalog/Questions (True-False).wbk` |  |
| 1428887 | `Catalog/Questions (True-False).wbx` |  |
| 14278 | `Catalog/Questions (Various).ini` |  |
| 540745 | `Catalog/Questions (Various).wbk` |  |
| 731987 | `Catalog/Questions (Various).wbx` |  |
| 182935 | `Catalog/realplay.spb` |  |
| 115419 | `Catalog/reset.spb` |  |
| 119229 | `Catalog/rptactn.spb` |  |
| 7865 | `Catalog/Scoring and Tracking.ini` |  |
| 192399 | `Catalog/Scoring and Tracking.wbk` |  |
| 509499 | `Catalog/Scoring and Tracking.wbx` |  |
| 282861 | `Catalog/seltext.spb` |  |
| 289965 | `Catalog/slider.spb` |  |
| 7477 | `Catalog/Text Fields.ini` |  |
| 281853 | `Catalog/Text Fields.wbk` |  |
| 690829 | `Catalog/Text Fields.wbx` |  |
| 59215 | `Catalog/textedit.spb` |  |
| 11301 | `Catalog/TIMER.HLP` |  |
| 130461 | `Catalog/timer.spb` |  |
| 15984 | `Catalog/TRIGGER.HLP` |  |
| 105809 | `Catalog/trigger.spb` |  |
| 254039 | `Catalog/truefals.spb` |  |
| 294983 | `Catalog/typein.spb` |  |
| 94720 | `Catalog/usejava.spb` |  |
| 302262 | `Catalog/vidsynch.spb` |  |
| 11801 | `Catalog/VIDWID.HLP` |  |
| 200140 | `Catalog/vidwid.spb` |  |
| 136309 | `Catalog/winmedia.spb` |  |
| 175204 | `Catalog/xmedit.spb` |  |

#### Instructor8/Media

46 files.

| Bytes | File | Mark |
|---:|---|---|
| 68734 | `Media/cbt/female/Almost.wav` |  |
| 77022 | `Media/cbt/female/Correct.wav` |  |
| 42364 | `Media/cbt/female/Excuseme.wav` |  |
| 44028 | `Media/cbt/female/Givebrk.wav` |  |
| 32636 | `Media/cbt/female/Groovy.wav` |  |
| 179582 | `Media/cbt/female/Incrrct.wav` |  |
| 30268 | `Media/cbt/female/No.wav` |  |
| 37948 | `Media/cbt/female/Nokiddng.wav` |  |
| 23228 | `Media/cbt/female/Ouch.wav` |  |
| 32492 | `Media/cbt/female/Partlyrt.wav` |  |
| 43132 | `Media/cbt/female/Righton.wav` |  |
| 57086 | `Media/cbt/female/Rusure.wav` |  |
| 39804 | `Media/cbt/female/Tryagain.wav` |  |
| 71806 | `Media/cbt/female/Trythis.wav` |  |
| 36860 | `Media/cbt/female/Urright.wav` |  |
| 43132 | `Media/cbt/female/Waycool.wav` |  |
| 26044 | `Media/cbt/female/Woops.wav` |  |
| 71934 | `Media/cbt/female/Wow.wav` |  |
| 75902 | `Media/cbt/female/Wrngagn.wav` |  |
| 31868 | `Media/cbt/female/Yes.wav` |  |
| 31804 | `Media/cbt/female/Yougotit.wav` |  |
| 13788 | `Media/cbt/female/Yup.wav` |  |
| 42364 | `Media/cbt/male/Almost1.wav` |  |
| 31228 | `Media/cbt/male/Correct1.wav` |  |
| 41340 | `Media/cbt/male/Excuse1.wav` |  |
| 57724 | `Media/cbt/male/Givebrk1.wav` |  |
| 41724 | `Media/cbt/male/Groovy1.wav` |  |
| 29244 | `Media/cbt/male/No1.wav` |  |
| 48252 | `Media/cbt/male/Nokid1.wav` |  |
| 80808 | `Media/cbt/male/Notcrct1.wav` |  |
| 35260 | `Media/cbt/male/Ouch1.wav` |  |
| 29500 | `Media/cbt/male/Partly1.wav` |  |
| 48252 | `Media/cbt/male/Righton1.wav` |  |
| 34364 | `Media/cbt/male/Rusure1.wav` |  |
| 37500 | `Media/cbt/male/Tryagai1.wav` |  |
| 34236 | `Media/cbt/male/Trythis1.wav` |  |
| 33704 | `Media/cbt/male/Urright1.wav` |  |
| 41724 | `Media/cbt/male/Waycoo1l.wav` |  |
| 27004 | `Media/cbt/male/Woops1.wav` |  |
| 23292 | `Media/cbt/male/Wow1.wav` |  |
| 38140 | `Media/cbt/male/Wrngag1.wav` |  |
| 23228 | `Media/cbt/male/Yes1.wav` |  |
| 27004 | `Media/cbt/male/Yougot1.wav` |  |
| 11292 | `Media/cbt/male/Yup1.wav` |  |
| 5473 | `Media/Flash/CORRECT.SWF` |  |
| 2770 | `Media/Flash/incorrect.swf` |  |

#### Instructor8/Packager

24 files.

| Bytes | File | Mark |
|---:|---|---|
| 322026 | `Packager/_INST32I.EX_` |  |
| 8192 | `Packager/_ISDEL.EXE` | NE |
| 6128 | `Packager/_SETUP.DLL` |  |
| 195925 | `Packager/_SETUP.LIB` |  |
| 72794 | `Packager/COMPRESS.INS` |  |
| 109056 | `Packager/ole2/COMPOBJ.DLL` |  |
| 536048 | `Packager/ole2/OC25.DLL` |  |
| 304640 | `Packager/ole2/OLE2.DLL` |  |
| 28113 | `Packager/ole2/OLE2.REG` |  |
| 57328 | `Packager/ole2/OLE2CONV.DLL` |  |
| 164960 | `Packager/ole2/OLE2DISP.DLL` |  |
| 152976 | `Packager/ole2/OLE2NLS.DLL` |  |
| 51712 | `Packager/ole2/OLE2PROX.DLL` |  |
| 12976 | `Packager/ole2/SCP.DLL` |  |
| 5472 | `Packager/ole2/STDOLE.TLB` |  |
| 157696 | `Packager/ole2/STORAGE.DLL` |  |
| 177824 | `Packager/ole2/TYPELIB.DLL` |  |
| 902744 | `Packager/PACKAGER.exe` | PE |
| 87552 | `Packager/PACKLIST.EXE` | PE |
| 995 | `Packager/PACKLIST.PIF` |  |
| 7216 | `Packager/Regsvr.exe` | NE |
| 45568 | `Packager/SETUP.EXE` | NE |
| 122452 | `Packager/SETUP.INS` |  |
| 40448 | `Packager/Tbisx32.dll` |  |

#### Instructor8/Welcome

2 files.

| Bytes | File | Mark |
|---:|---|---|
| 28633 | `Welcome/RelNotes.WRI` |  |
| 1359335 | `Welcome/Walkthrough.tbk` |  |

#### Instructor8/spclst

84 files.

| Bytes | File | Mark |
|---:|---|---|
| 213 | `spclst/OUTLINES/catalog.aof` |  |
| 246 | `spclst/OUTLINES/generic1.aof` |  |
| 283 | `spclst/OUTLINES/generic2.aof` |  |
| 307 | `spclst/OUTLINES/generic3.aof` |  |
| 228 | `spclst/OUTLINES/present.aof` |  |
| 278 | `spclst/OUTLINES/quiz1.aof` |  |
| 275 | `spclst/OUTLINES/quiz2.aof` |  |
| 329 | `spclst/OUTLINES/skill1.aof` |  |
| 371 | `spclst/OUTLINES/train1.aof` |  |
| 737031 | `spclst/spclst.spb` |  |
| 824415 | `spclst/spclstld.spb` |  |
| 677836 | `spclst/spclstqs.spb` |  |
| 1081229 | `spclst/styles/angled.ptp` |  |
| 1082937 | `spclst/styles/angledh.ptp` |  |
| 725193 | `spclst/styles/art_deco.ptp` |  |
| 512741 | `spclst/styles/bluebr1i.ptp` |  |
| 1056937 | `spclst/styles/blueintersection.ptp` |  |
| 1057947 | `spclst/styles/blueintersectionh.ptp` |  |
| 1110513 | `spclst/styles/bluelines.ptp` |  |
| 1097085 | `spclst/styles/bluelinesh.ptp` |  |
| 1062329 | `spclst/styles/coralsea.ptp` |  |
| 1062359 | `spclst/styles/coralseah.ptp` |  |
| 1064957 | `spclst/styles/earth.ptp` |  |
| 1064651 | `spclst/styles/earthh.ptp` |  |
| 1016511 | `spclst/styles/fall1i.ptp` |  |
| 890481 | `spclst/styles/finan1.ptp` |  |
| 791167 | `spclst/styles/finan1h.ptp` |  |
| 487039 | `spclst/styles/finan1i.ptp` |  |
| 746583 | `spclst/styles/granite.ptp` |  |
| 909063 | `spclst/styles/gray1.ptp` |  |
| 911183 | `spclst/styles/gray1h.ptp` |  |
| 538173 | `spclst/styles/gray1i.ptp` |  |
| 617233 | `spclst/styles/grayck1i.ptp` |  |
| 914809 | `spclst/styles/indust1.ptp` |  |
| 817577 | `spclst/styles/indust1h.ptp` |  |
| 575719 | `spclst/styles/indust1i.ptp` |  |
| 1543741 | `spclst/styles/inter1i.ptp` |  |
| 929965 | `spclst/styles/mil1.ptp` |  |
| 931067 | `spclst/styles/mil1h.ptp` |  |
| 509171 | `spclst/styles/mil1i.ptp` |  |
| 860125 | `spclst/styles/mod_offc.ptp` |  |
| 715595 | `spclst/styles/paint.ptp` |  |
| 1067185 | `spclst/styles/peacock.ptp` |  |
| 1067267 | `spclst/styles/peacockh.ptp` |  |
| 785391 | `spclst/styles/present.ptp` |  |
| 1074597 | `spclst/styles/rainbow.ptp` |  |
| 1074863 | `spclst/styles/rainbowh.ptp` |  |
| 1063159 | `spclst/styles/sky.ptp` |  |
| 1063159 | `spclst/styles/skyh.ptp` |  |
| 1072665 | `spclst/styles/space.ptp` |  |
| 1072905 | `spclst/styles/spaceh.ptp` |  |
| 856267 | `spclst/styles/stageb1.ptp` |  |
| 765425 | `spclst/styles/stageb1h.ptp` |  |
| 472213 | `spclst/styles/stageb1i.ptp` |  |
| 855969 | `spclst/styles/stager1.ptp` |  |
| 765943 | `spclst/styles/stager1h.ptp` |  |
| 474719 | `spclst/styles/stager1i.ptp` |  |
| 1065529 | `spclst/styles/strongline.ptp` |  |
| 1065611 | `spclst/styles/stronglineh.ptp` |  |
| 6281 | `spclst/styles/tbkcache.ini` |  |
| 909151 | `spclst/styles/tech1.ptp` |  |
| 799533 | `spclst/styles/tech1h.ptp` |  |
| 521769 | `spclst/styles/tech1i.ptp` |  |
| 918137 | `spclst/styles/tech2.ptp` |  |
| 790505 | `spclst/styles/tech2h.ptp` |  |
| 499089 | `spclst/styles/tech2i.ptp` |  |
| 2487623 | `spclst/styles/tech3.ptp` |  |
| 2322703 | `spclst/styles/tech3h.ptp` |  |
| 492071 | `spclst/styles/tech3i.ptp` |  |
| 1221271 | `spclst/styles/tech_4h.ptp` |  |
| 1229531 | `spclst/styles/tech_b4h.ptp` |  |
| 1235323 | `spclst/styles/tech_g4h.ptp` |  |
| 1081923 | `spclst/styles/tornedge.ptp` |  |
| 1081595 | `spclst/styles/tornedgeh.ptp` |  |
| 614057 | `spclst/styles/triang1i.ptp` |  |
| 904893 | `spclst/styles/usgov1.ptp` |  |
| 909751 | `spclst/styles/usgov1h.ptp` |  |
| 587763 | `spclst/styles/usgov1i.ptp` |  |
| 951983 | `spclst/styles/usgov2.ptp` |  |
| 877581 | `spclst/styles/usgov2h.ptp` |  |
| 549133 | `spclst/styles/usgov2i.ptp` |  |
| 922529 | `spclst/styles/usmil1.ptp` |  |
| 927027 | `spclst/styles/usmil1h.ptp` |  |
| 564949 | `spclst/styles/usmil1i.ptp` |  |

#### Instructor8/template

32 files.

| Bytes | File | Mark |
|---:|---|---|
| 573554 | `template/catalog.tbk` |  |
| 567736 | `template/catalogh.tbk` |  |
| 91798 | `template/default.tbk` |  |
| 91836 | `template/defaulth.tbk` |  |
| 590470 | `template/gen1ch.tbk` |  |
| 590576 | `template/gen1chh.tbk` |  |
| 603756 | `template/gen2ch.tbk` |  |
| 603864 | `template/gen2chh.tbk` |  |
| 517424 | `template/generic.tbk` |  |
| 517884 | `template/generich.tbk` |  |
| 661570 | `template/hr.tbk` |  |
| 660810 | `template/hrh.tbk` |  |
| 622974 | `template/learn1.tbk` |  |
| 623126 | `template/learn1h.tbk` |  |
| 357136 | `template/learn1i.tbk` |  |
| 228456 | `template/ppointi.tbk` |  |
| 648112 | `template/present.tbk` |  |
| 648172 | `template/presenth.tbk` |  |
| 577620 | `template/quiz1.tbk` |  |
| 575086 | `template/quiz1h.tbk` |  |
| 507610 | `template/quiz1i.tbk` |  |
| 548644 | `template/roi.tbk` |  |
| 548374 | `template/roih.tbk` |  |
| 976814 | `template/sales1.tbk` |  |
| 625684 | `template/sales1h.tbk` |  |
| 859786 | `template/sales2.tbk` |  |
| 860572 | `template/sales2h.tbk` |  |
| 583410 | `template/simquiz.tbk` |  |
| 583510 | `template/simquizh.tbk` |  |
| 6704 | `template/tbkcache.ini` |  |
| 597418 | `template/train1.tbk` |  |
| 596850 | `template/train1h.tbk` |  |

### Editors, Filters, Neuron, Spelling

These sit beside `TBSystem` in `Common Files/click2learn`. The Editors EXEs are author utilities: bitmap, icon, menu, palette, palette optimizer, and wave. `tb80RED.DLL` is in Editors and not in `TBSystem`.


#### Editors

23 files.

| Bytes | File | Mark |
|---:|---|---|
| 154144 | `BITED80.EXE` | NE |
| 131404 | `Bited80.hlp` |  |
| 30544 | `DIB.DRV` |  |
| 117280 | `ICONED80.EXE` | NE |
| 67383 | `Iconed80.hlp` |  |
| 16544 | `medimpt.m80` |  |
| 43968 | `MEDMANT.DLL` |  |
| 73760 | `medwavet.m80` |  |
| 63840 | `MENUED80.EXE` | NE |
| 67323 | `Menued80.hlp` |  |
| 83520 | `PALED80.EXE` | NE |
| 79127 | `Paled80.hlp` |  |
| 123296 | `PALOPT.EXE` | NE |
| 13932 | `PALOPT.HLP` |  |
| 48661 | `PALOPTX.DLL` |  |
| 99440 | `tb80bit.m80` |  |
| 169760 | `tb80RCA.DLL` | NE |
| 67824 | `tb80RCR.DLL` | NE |
| 46560 | `tb80RED.DLL` | NE |
| 121728 | `WAVEED80.EXE` | NE |
| 86217 | `Waveed80.hlp` |  |
| 40288 | `WINCOMT.DLL` |  |
| 39200 | `WRKBNCHT.DLL` |  |

#### Filters

27 files.

| Bytes | File | Mark |
|---:|---|---|
| 83968 | `IBGIF2.FLT` |  |
| 103424 | `IBJPG2.FLT` |  |
| 202240 | `IBPCD2.FLT` |  |
| 760 | `IBPCD2.INI` |  |
| 80896 | `IBPCX2.FLT` |  |
| 79360 | `IBTGA2.FLT` |  |
| 105472 | `IBTIF2.FLT` |  |
| 158208 | `IMCD32.FLT` |  |
| 173056 | `IMCD42.FLT` |  |
| 68096 | `IMCDR2.FLT` |  |
| 453 | `IMCDR2.INI` |  |
| 146944 | `IMDRW2.FLT` |  |
| 556 | `IMDRW2.INI` |  |
| 227328 | `IMDXF2.FLT` |  |
| 4719 | `IMDXF2.INI` |  |
| 160768 | `IMHG32.FLT` |  |
| 5839 | `IMHG32.INI` |  |
| 155648 | `IMPCT2.FLT` |  |
| 1303 | `IMPCT2.INI` |  |
| 84992 | `IMPIC2.FLT` |  |
| 1183 | `IMPIC2.INI` |  |
| 120832 | `IMPIF2.FLT` |  |
| 1228 | `IMPIF2.INI` |  |
| 155648 | `IMPS_2.FLT` |  |
| 6321 | `IMPS_2.INI` |  |
| 229888 | `IPHGW2.FLT` |  |
| 247 | `IPHGW2.INI` |  |

#### Neuron

9 files.

| Bytes | File | Mark |
|---:|---|---|
| 141 | `CONFIRM.REG` |  |
| 1391 | `NEURON.CNT` |  |
| 77848 | `NEURON.HLP` |  |
| 191488 | `NEURON.OCX` |  |
| 140 | `NONSEC.REG` |  |
| 119360 | `NP16NEUR.DLL` |  |
| 296960 | `NP32NEUR.DLL` |  |
| 2322 | `relnotes.wri` |  |
| 135 | `SECURE.REG` |  |

#### Spelling

1 files.

| Bytes | File | Mark |
|---:|---|---|
| 204562 | `VEAMAA51.LEX` |  |

Seven basenames occur twice. The sizes below are the two copies.

| Name | Paths |
|---|---|
| `DIB.DRV` | `Editors/DIB.DRV`, `TBSystem/DIB.DRV` |
| `PALOPTX.DLL` | `Editors/PALOPTX.DLL`, `TBSystem/PALOPTX.DLL` |
| `RelNotes.WRI` | `Neuron/relnotes.wri`, `Instructor8/Welcome/RelNotes.WRI` |
| `TB80RCA.DLL` | `Editors/tb80RCA.DLL`, `TBSystem/TB80RCA.DLL` |
| `TB80RCR.DLL` | `Editors/tb80RCR.DLL`, `TBSystem/TB80RCR.DLL` |
| `tbkcache.ini` | `Instructor8/spclst/styles/tbkcache.ini`, `Instructor8/template/tbkcache.ini` |
| `VEAMAA51.LEX` | `Spelling/VEAMAA51.LEX`, `TBSystem/VEAMAA51.LEX` |

479 files, 472 unique basenames.

### Files beside the copied books

`/tmp/refs/guest`:

| Bytes | File |
|---:|---|
| 2327983 | `9e954d01.tbk` |
| 457 | `instructor.lnk` |
| 67938 | `nc81base.sbk` |
| 34538 | `nc81recs.sbk` |
| 98408 | `nc81test.sbk` |
| 66728 | `nc81trnr.sbk` |
| 5829208 | `nida81.tbk` |
| 1238 | `seg1180.bin` |
| 683872 | `TB80BAS.DLL` |
| 1163488 | `TB80BAS.unpacked.dll` |
| 263 | `tb80rtm.lnk` |

`TB80BAS.DLL` in that folder is the same 683872 bytes as `TBSystem/TB80BAS.DLL`. The other ten names are not in the author tree. `TB80BAS.unpacked.dll`, `seg1180.bin`, `instructor.lnk`, and `tb80rtm.lnk` are in the folder and are not lines in `toolbook.lst`. `9e954d01.tbk` is the lesson copy. `instructor.lnk` names `C:\Program Files\click2learn\Instructor8\Inst80.exe`.

`/tmp/nida-home/TB80ANM.SBK` is 1 byte, and `/tmp/nida-home/courses/93954302.tbk` is 1 byte. Those are not the books.

### Course name list

`toolbook.lst`, 42 names, then the four starred lines:

```
NC81BASE.SBK
NC81TEST.SBK
NC81RECS.SBK
NC81TRNR.SBK
NC81INT.DLL
NC81REC.DLL
*NC81IMVS.TBK
NIDA81.TBK
*NIDA81S.TBK
*NIDA81F.TBK
*LOGO81.TBK
TB80F32L.DLL
TB80MAIN.EXE
TB80OCX.DLL
TB80RMT.DLL
TB80VBX.DLL
TB80ACX.DLL
TB80ANM.SBK
TB80BAS.DLL
TB80BMP.DLL
TB80CMP.DLL
TB80ENU1.DLL
TB80ENU2.DLL
TB80FLT.DLL
TB80HYP.SBK
TB80JPG.DLL
TB80LNL.DLL
TB80MM.DLL
TB80NET.EXE
TB80OLE.DLL
TB80R.SBK
TB80RCR.DLL
TB80RTM.EXE
TB80RUN.EXE
TB80UTL.DLL
TB80W16.DLL
TB80W32.DLL
TBCBT.DLL
TBDB3.DLL
TBDLG.DLL
TBDOS.DLL
TBFILE32.DLL
TBLOAD.EXE
TBPDX.DLL
TBREG.DLL
TBWIN.DLL
```

### Partition

Author names are the 472 basenames above. Distribution names are the 42 unstarred lines of `toolbook.lst`. Comparison ignores case.

**In both** (35), in course-list order. The left column is the author filename. The right column is the course-list spelling. The sizes for these names are the author copies in the tables above. `TB80BAS.DLL` is the one name in this table that was also a file in `/tmp/refs/guest`, and the two copies are the same bytes. `TB80MM.DLL` is in both lists. `TB80MM.INI` (3352 bytes, in `TBSystem`) is only in the author install.

| Author file | Course list |
|---|---|
| `TB80F32L.dll` | `TB80F32L.DLL` |
| `TB80MAIN.EXE` | `TB80MAIN.EXE` |
| `TB80OCX.DLL` | `TB80OCX.DLL` |
| `TB80RMT.DLL` | `TB80RMT.DLL` |
| `TB80VBX.DLL` | `TB80VBX.DLL` |
| `TB80ACX.DLL` | `TB80ACX.DLL` |
| `tb80anm.sbk` | `TB80ANM.SBK` |
| `TB80BAS.DLL` | `TB80BAS.DLL` |
| `TB80BMP.DLL` | `TB80BMP.DLL` |
| `TB80CMP.DLL` | `TB80CMP.DLL` |
| `TB80ENU1.DLL` | `TB80ENU1.DLL` |
| `TB80ENU2.DLL` | `TB80ENU2.DLL` |
| `TB80FLT.DLL` | `TB80FLT.DLL` |
| `tb80hyp.sbk` | `TB80HYP.SBK` |
| `TB80JPG.DLL` | `TB80JPG.DLL` |
| `TB80LNL.DLL` | `TB80LNL.DLL` |
| `TB80MM.DLL` | `TB80MM.DLL` |
| `TB80NET.EXE` | `TB80NET.EXE` |
| `TB80OLE.DLL` | `TB80OLE.DLL` |
| `tb80r.sbk` | `TB80R.SBK` |
| `TB80RCR.DLL` | `TB80RCR.DLL` |
| `TB80RTM.EXE` | `TB80RTM.EXE` |
| `TB80RUN.EXE` | `TB80RUN.EXE` |
| `TB80UTL.DLL` | `TB80UTL.DLL` |
| `TB80W16.DLL` | `TB80W16.DLL` |
| `TB80W32.DLL` | `TB80W32.DLL` |
| `TBCBT.DLL` | `TBCBT.DLL` |
| `TBDB3.DLL` | `TBDB3.DLL` |
| `TBDLG.DLL` | `TBDLG.DLL` |
| `TBDOS.DLL` | `TBDOS.DLL` |
| `TBFILE32.DLL` | `TBFILE32.DLL` |
| `Tbload.exe` | `TBLOAD.EXE` |
| `TBPDX.DLL` | `TBPDX.DLL` |
| `TBREG.DLL` | `TBREG.DLL` |
| `TBWIN.DLL` | `TBWIN.DLL` |

**Only in the course list** (7). Five of these were copied into `/tmp/refs/guest`. `NC81INT.DLL` and `NC81REC.DLL` were not found as files, so they have no size.

| Course list | Guest bytes |
|---|---|
| `NC81BASE.SBK` | 67938 |
| `NC81TEST.SBK` | 98408 |
| `NC81RECS.SBK` | 34538 |
| `NC81TRNR.SBK` | 66728 |
| `NC81INT.DLL` | not found |
| `NC81REC.DLL` | not found |
| `NIDA81.TBK` | 5829208 |

**Only in the author install** (437). Every other basename in the tables above.

```
_INST32I.EX_
_ISDEL.EXE
_SETUP.DLL
_SETUP.LIB
abullet.spb
actdelay.spb
Action Objects.ini
Action Objects.wbk
Action Objects.wbx
acttimer.spb
allmedia.spb
Almost.wav
Almost1.wav
angled.ptp
angledh.ptp
art_deco.ptp
asym.ini
Asymgif.ocx
automenu.spb
AUTORUN.EXE
Autorun.ICO
axf.dtd
BITED80.EXE
Bited80.hlp
blank.tbk
bluebr1i.ptp
blueintersection.ptp
blueintersectionh.ptp
bluelines.ptp
bluelinesh.ptp
bullets.spb
butnedit.spb
Buttons.ini
Buttons.wbk
Buttons.wbx
callout.spb
Catalog Blank Cache.tbk
Catalog Blank Category.tbk
Catalog Blank Spec Cache.tbk
Catalog Spec Cache.tbk
catalog.aof
catalog.ini
catalog.tbk
catalogh.tbk
CATOBJT.HLP
click2learn.author.ini
click2learn.author.wbk
click2learn.author.wbx
click2learn.pal
CLIPWID.HLP
clipwid.spb
COMPOBJ.DLL
COMPRESS.INS
CONFIRM.REG
coralsea.ptp
coralseah.ptp
CORRECT.SWF
Correct.wav
Correct1.wav
decrypt.exe
DECRYPT.HLP
default.tbk
defaulth.tbk
DIB.DRV
DIBUTIL.DLL
distrib.wri
Draw Objects.ini
Draw Objects.wbk
Draw Objects.wbx
dropbin.spb
dzactx.dll
earth.ptp
earthh.ptp
EVALBOOK.HLP
evalbook.spb
EVALPAGE.HLP
evalpage.spb
Excuse1.wav
Excuseme.wav
extjava.spb
fall1i.ptp
finan1.ptp
finan1h.ptp
finan1i.ptp
fldglist.spb
fldolist.spb
gen1ch.tbk
gen1chh.tbk
gen2ch.tbk
gen2chh.tbk
genedit.spb
generic.tbk
generic1.aof
generic2.aof
generic3.aof
generich.tbk
Givebrk.wav
Givebrk1.wav
granite.ptp
gray1.ptp
gray1h.ptp
gray1i.ptp
grayck1i.ptp
Groovy.wav
Groovy1.wav
hr.tbk
hrh.tbk
IBGIF2.FLT
IBJPG2.FLT
IBPCD2.FLT
IBPCD2.INI
IBPCX2.FLT
IBTGA2.FLT
IBTIF2.FLT
ICONED80.EXE
Iconed80.hlp
IMAGEMAP.HLP
imagemap.spb
IMCD32.FLT
IMCD42.FLT
IMCDR2.FLT
IMCDR2.INI
IMDRW2.FLT
IMDRW2.INI
IMDXF2.FLT
IMDXF2.INI
IMGEDIT.HLP
imgedit.spb
IMHG32.FLT
IMHG32.INI
IMPCT2.FLT
IMPCT2.INI
IMPIC2.FLT
IMPIC2.INI
IMPIF2.FLT
IMPIF2.INI
IMPS_2.FLT
IMPS_2.INI
impulse.exe
incorrect.swf
Incrrct.wav
indust1.ptp
indust1h.ptp
indust1i.ptp
inetauto.spb
INST80.CNT
Inst80.exe
INST80.HLP
inst80.ini
Inst80.pal
INST80.SBK
inter1i.ptp
IPHGW2.FLT
IPHGW2.INI
ISGDI32.DLL
ISGDI32.INI
learn1.tbk
learn1h.tbk
learn1i.tbk
liblogin.spb
listedit.spb
logread.exe
logread.hlp
marquee.spb
Media (Animated).ini
Media (Animated).wbk
Media (Animated).wbx
Media (Backdrops).ini
Media (Backdrops).wbk
Media (Backdrops).wbx
Media (Clipart).ini
Media (Clipart).wbk
Media (Clipart).wbx
Media (Icons).ini
Media (Icons).wbk
Media (Icons).wbx
Media (Tiled Backdrops).ini
Media (Tiled Backdrops).wbk
Media (Tiled Backdrops).wbx
Media Players.ini
Media Players.wbk
Media Players.wbx
mediabtn.spb
medimpt.m80
MEDMANT.DLL
medwavet.m80
MENUED80.EXE
Menued80.hlp
mercury.jar
mil1.ptp
mil1h.ptp
mil1i.ptp
mod_offc.ptp
mtchitem.spb
mtchobj.spb
multdrop.spb
multiobj.spb
multline.spb
multwid.spb
My Objects.ini
My Objects.wbk
My Objects.wbx
namepart.spb
Navigation Objects.ini
Navigation Objects.wbk
Navigation Objects.wbx
NEURON.CNT
NEURON.HLP
NEURON.OCX
neuron.spb
No.wav
No1.wav
Nokid1.wav
Nokiddng.wav
NONSEC.REG
Notcrct1.wav
NP16NEUR.DLL
NP32NEUR.DLL
OC25.DLL
OLE2.DLL
OLE2.REG
OLE2CONV.DLL
OLE2DISP.DLL
OLE2NLS.DLL
OLE2PROX.DLL
orderobj.spb
orderwid.spb
Ouch.wav
Ouch1.wav
Oxs.dll
PACKAGER.exe
PACKLIST.EXE
PACKLIST.PIF
pagemenu.spb
Pages.ini
Pages.wbk
Pages.wbx
paint.ptp
PALED80.EXE
Paled80.hlp
PALOPT.EXE
PALOPT.HLP
PALOPTX.DLL
Partly1.wav
Partlyrt.wav
PATHANIM.HLP
PCDLIB.DLL
PCDXBMP.DLL
peacock.ptp
peacockh.ptp
PHOTO.DLL
Placeholder Objects.ini
Placeholder Objects.wbk
Placeholder Objects.wbx
popupump.spb
POPVID.HLP
popvid.spb
ppointi.tbk
present.aof
present.ptp
present.tbk
presenth.tbk
PXENGWIN.DLL
questext.spb
QUESTION.HLP
Questions (Multiple Choice).ini
Questions (Multiple Choice).wbk
Questions (Multiple Choice).wbx
Questions (True-False).ini
Questions (True-False).wbk
Questions (True-False).wbx
Questions (Various).ini
Questions (Various).wbk
Questions (Various).wbx
quiz1.aof
quiz1.tbk
quiz1h.tbk
quiz1i.tbk
quiz2.aof
rainbow.ptp
rainbowh.ptp
realplay.spb
Regsvr.exe
RelNotes.WRI
remover.exe
remover.ico
Repair80.exe
reset.spb
Righton.wav
Righton1.wav
roi.tbk
roih.tbk
rptactn.spb
Rusure.wav
Rusure1.wav
sales1.tbk
sales1h.tbk
sales2.tbk
sales2h.tbk
Scoring and Tracking.ini
Scoring and Tracking.wbk
Scoring and Tracking.wbx
SCP.DLL
scrwalk.ico
scrwalk.tbk
SECURE.REG
seltext.spb
SETUP.EXE
SETUP.INS
simquiz.tbk
simquizh.tbk
skill1.aof
sky.ptp
skyh.ptp
slider.spb
space.ptp
spaceh.ptp
spclst.spb
spclstld.spb
spclstqs.spb
stageb1.ptp
stageb1h.ptp
stageb1i.ptp
stager1.ptp
stager1h.ptp
stager1i.ptp
startup.ini
STDOLE.TLB
STORAGE.DLL
strongline.ptp
stronglineh.ptp
TB2FTP.DLL
TB80.EXE
tb80.ini
tb80.sbk
tb80a.sbk
tb80acta.sbk
tb80actr.sbk
tb80aicc.sbk
TB80ATH.EXE
tb80axf.sbk
tb80bit.m80
TB80CVT.DLL
TB80EDT.DLL
TB80ENU3.DLL
TB80ENU4.DLL
tb80ftp.exe
TB80FTP.HLP
tb80ftp.sbk
tb80i.sbk
tb80lmx.sbk
TB80MM.INI
TB80RCA.DLL
tb80RED.DLL
tb80web.sbk
tb80x.sbk
TB80XTR.DLL
TBCOM.DLL
TBINET32.DLL
Tbisx32.dll
tbkcache.ini
TBKSLICE.DLL
TBUTIL32.dll
tech1.ptp
tech1h.ptp
tech1i.ptp
tech2.ptp
tech2h.ptp
tech2i.ptp
tech3.ptp
tech3h.ptp
tech3i.ptp
tech_4h.ptp
tech_b4h.ptp
tech_g4h.ptp
Text Fields.ini
Text Fields.wbk
Text Fields.wbx
textedit.spb
TIMER.HLP
timer.spb
Tlist16p.ocx
TList4.ocx
tornedge.ptp
tornedgeh.ptp
train1.aof
train1.tbk
train1h.tbk
triang1i.ptp
TRIGGER.HLP
trigger.spb
truefals.spb
Tryagai1.wav
Tryagain.wav
Trythis.wav
Trythis1.wav
typein.spb
TYPELIB.DLL
UnInst80.isu
Urright.wav
Urright1.wav
usejava.spb
usgov1.ptp
usgov1h.ptp
usgov1i.ptp
usgov2.ptp
usgov2h.ptp
usgov2i.ptp
usmil1.ptp
usmil1h.ptp
usmil1i.ptp
VEAMAA51.LEX
vidsynch.spb
VIDWID.HLP
vidwid.spb
Walkthrough.tbk
WAVEED80.EXE
Waveed80.hlp
Waycoo1l.wav
Waycool.wav
WINCOMT.DLL
winmedia.spb
WINSOX.EXE
Woops.wav
Woops1.wav
Wow.wav
Wow1.wav
WRKBNCHT.DLL
Wrngag1.wav
Wrngagn.wav
xmedit.spb
Yes.wav
Yes1.wav
Yougot1.wav
Yougotit.wav
Yup.wav
Yup1.wav
```

The four starred lines, `NC81IMVS.TBK`, `NIDA81S.TBK`, `NIDA81F.TBK`, and `LOGO81.TBK`, are not in the author install and were not found as files.

Of the files that were actually in a directory, the only basename in both the author install and `/tmp/refs/guest` is `TB80BAS.DLL`. The ten guest names listed above are the ones present only beside those copied books.

## `name of this book` in the system books

Source: the type 10 scripts of `tb80.sbk`, `tb80a.sbk`, and `tb80r.sbk` as `resource_scripts` expands them. They call `pathOfFile(name of this book)`, `shortFileName(name of this book)`, and `ASYM_ShortFileName(name of this book)`. A script that needs the short name asks for it, so the engine's `name of this book` is likely a full path. The reader returns the file name, which is what those calls would return. `nc81test.sbk` compares `__translationSourceBook = name of this book`, and `nc81bank.sbk` stores `filename = name of this book`.

## Test paths for private books

Source: the Cursor handoff that lists M1 test hygiene (2026-10-31). Lesson-specific tests take `OPENTOOLBOOK_TBK` only when that file is named `9e954d01.tbk`, so pointing the variable at another book skips instead of asserting Logic Families pages. Companions open through the same case-insensitive shelf as `open_book`. `OPENTOOLBOOK_BOOKS` names a flat folder of `.tbk` files for a startup-and-paint smoke; it is optional and skips when unset.

## Missing export DLL is a report note

Source: the Cursor handoff M2 (2026-10-31). A missing PE export DLL such as the one Instructor books name stays a shelf note for `--report`. The page window no longer draws a permanent status line for it.

## Page size and metafile records

Source: the Cursor handoff M2 (2026-10-31). Page width and height are the signed words on the book record for every book. A class `0x19` metafile is played from its own records: window org/ext, optional clip, and StretchDIB forms the reader knows; other functions are skipped. Specimen books such as `nida81.tbk` still exercise that path, but the reader does not branch on their names.

## flushMessageQueue

Source: OpenScript keyword list (`OPENCODE.md` / keyword resource) and `nc81trnr.sbk` scripts that call `flushMessageQueue()` (FINDINGS). ToolBook drains its message queue; this reader has none, so the word returns without effect as a statement or as a function.

## idle

Source: ToolBook OpenScript `idle` message (keyword list) and the handoff M5 note that the window should send it when idle. `firstIdle` already runs in the opening sequence (TB80RTM trace). The window schedules `idle` with Tk `after_idle` and then every 200 ms.

## mouseEnter and mouseLeave

Source: handler_sites on Logic Families and nida81 (SETTLED hover counts) and the handoff M5 note. The books use those messages on field scripts, not enterButton/leaveButton. The window now dispatches them on Motion and Leave.

## invert persists in object state

Source: the handoff M5 note that invert from buttonDown/buttonUp must persist (SETTLED previously cleared it on page change). ToolBook keeps object properties for the open book; invert is one of them. The on-screen invert map is rebuilt from that state for the page on screen.

## buttonDoubleClick

Source: OpenScript message list (DENNY-OBJECTS.md draw-object chart) and the handoff M5 note. The window binds Tk Double-Button-1, cancels the delayed single buttonClick, and sends buttonDoubleClick to the named button or field under the pointer.

## sysDate and sysTime

Source: OpenScript system properties (keyword list) and the handoff M5 note. `sysTime` was already answered by BookHost; both now live on the base Host so every runner sees them. `sysDateFormat` defaults to `m/d/yy`.

## Preventing_Fraud.tbk (M3)

Source: handoff M3. This environment still has no `Preventing_Fraud.tbk` and no Instructor 8.1 sample folder (workspace search; Google Drive exact-name search again returned nothing on 2026-10-31). Diagnosis of its format vs TB80 waits on that file.

## Viewer back leave/enter (M5)

Source: handoff M5. Whether Viewer back should send `leavePage` / `enterPage` (and matching background messages) is not settled from a Bochs or TB80RTM capture in this tree. The window already pops history and paints the prior page without those messages. Need a ToolBook 8 capture of Viewer back before changing that path.

## TB80.INI startup keys

Source: handoff M4 and the TB80RTM startup note in that handoff. Search order is the book's folder, then `<windows>\asym\runtime`, then `<windows>`. With no INI every key is its default and no system book is named for the reader. `startupSysBooks` seeds `sysBooks` before the class-table bound books and before the book's own `push` lines. `startupBook` / `startupWidth` / `startupHeight` are parsed for later window sizing; they do not yet change the opening page or the window size in this push.

## enterSystemBook / leaveSystemBook

Source: handoff M4. ToolBook sends those messages to a system book when it enters or leaves `sysBooks`. This reader runs the handler from that book's own script only (not the open book first). INI-seeded and class-table bound names that are present before startup handlers run do not get `enterSystemBook` in this push; only a script change of `sysBooks` does.

## Startup message order

Source: handoff M4 section 2 and the TB80RTM trace already cited in SETTLED. The seven-name log test pins the reader order on a synthetic handler set over `otb-line-rect.tbk`.

## buttonStillDown

Source: handoff M5 and the OpenScript message list. ToolBook repeats `buttonStillDown` while the mouse button is held. This reader uses a 100 ms Tk `after` timer on the pressed object, cancelled on release or double-click.

## keyChar

Source: handoff M5. ToolBook sends `keyChar` with the typed character. The window binds Tk `<Key>` for a single printable character and calls `Navigator.key_char`, which sends `keyChar` with that character on the page path.

## DLL shim table

Source: handoff M5. Windows/ToolBook `linkDLL32` names are answered from `opentoolbook/dllshims.py` plus the existing profile/fileExists answers on `BookHost`. Optional per-book `dlls/` shim folders are not wired yet.

## ask vs request

Source: handoff M5 ask edge. OpenScript keyword list has both `ask` and `request`. The parser had only `request` as a Request node; `ask … with …` fell through as a raw Command. Both now parse as Request.
