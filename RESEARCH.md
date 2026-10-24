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

A page is the object whose class word, at object −2, is 5. The instruction is `cmp word [reg−2], 5`. It occurs 14 times in the unpacked code. The view path is one of them: `CDBVIEWPAGE` (ordinal 15) calls `FUN_1040_13c4`, which calls `FUN_1040_1420`, which calls `FUN_1040_18e4`. In `FUN_1040_18e4` the class word is compared with 5, and on a match the background is the far pointer at object `+0x47`. That is the same dword the specimen's background read uses. The far call that function makes is NE 9 `0x19F3`. Its targets are in the indirect-call section below.

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

## Quiz handlers

From `nc81test.sbk` type 10 resource 741, expanded by this reader on 24 October 2026. The decompile record, chapter 14, says the four `nc81*` books have no decoded `to handle` text. The bytes in those books are `to get`. The reader returns that source. It does not run it. The steps two of those handlers share are in `FINDINGS.md`.

`processQuizScore` in `nc81base.sbk` is one function. It writes `NIDAREC.INI` through `WritePrivateProfileStringA`. That write is not a score the reader computes. `getquizResponse` is one function. The comparison that repeats is the two handlers in `FINDINGS.md`, which call it and test `answer of this page`.

## Pattern bytes 0xFD, 0xFE, and 0xFF

From `tbdecompile/research/paint-20261021.md`. `LOCKPATTERN` in `TB80BAS` is `1098:0876`. That note says `0xFD` is hollow, `0xFE` is solid paper, and `0xFF` is solid ink, and that `1` through `0x80` is a pattern. `0xFE` is stored on backgrounds and on class `0x8`, `0xC`, and `0x10` in both books. `0xFD` is stored on class `0x8` in both books. `0xFF` is not stored on those fields in either book, so that name is not applied here. The counts are in `FINDINGS.md`.

## Indirect calls on view, load, and the class slot

From the unpacked `TB80BAS.DLL` on this machine, 24 October 2026. NE segment `N` is the Ghidra base `0x1000 + (N - 1) * 8`. A listing address `10C8:00D0` is NE segment 26, offset `0x00D0`. Bytes below are the file bytes. A segment relocation fixes the segment word; the offset in a `9A` instruction is the offset. Where the fixup is chained, the word stored in the file is the next fixup, not the segment. This is not a layout the reader uses.

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
