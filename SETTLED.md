# Settled

Logic Families is `9e954d01.tbk`. The filenames and calls below are the ones that book names.

## Filenames

- `93954302.tbk`
- `93954d01.tbk`
- `minstb32.dll`
- `nc81base.sbk`
- `nc81recs.sbk`
- `nc81test.sbk`
- `nc81trnr.sbk`
- `nida81.tbk`
- `tb80anm.sbk`
- `tb80r.sbk`

## Calls

No call name is tied to a book by the reader. `--report` runs the book's startup handlers and prints `sysBooks` as they leave it, first item first, then each call name with the book whose handler answers it: the open book first, then each `sysBooks` book in order. On `9e954d01.tbk` startup leaves `sysBooks` as `nc81trnr.sbk`, `nc81recs.sbk`, `nc81test.sbk`, `nc81base.sbk`, `tb80r.sbk`. `enterSystem` and `enterApplication` are the lesson's own. `initializeBase` and `gotoPageList` are `nc81base.sbk`, `initializeRecs` and `openSession` are `nc81recs.sbk`, `initializeTest` is `nc81test.sbk`, and `initializeTrnr` is `nc81trnr.sbk`. A book whose startup pushes nothing, such as `otb-line-rect.tbk` or the Instructor 8.1 `Walkthrough.tbk`, prints `sysBooks 0`.

## Resolve on open

On open, those filenames are looked up in this order: the book's directory, the parent of that directory, then `--home`. The match ignores case. The report prints the path that was found. The book still opens when `minstb32.dll`, `93954302.tbk`, or `93954d01.tbk` is absent. `nida81.tbk`, `nc81base.sbk`, `nc81recs.sbk`, `nc81test.sbk`, and `nc81trnr.sbk` in the parent directory are that path. `93954302.tbk` beside the lesson stays the file in the book's directory. A name that is not in those directories stays missing. The lookup does not read any other directory.

## Field text

A field is class `0xA` and the record is 61 bytes. Its text is word 1 of the block at record `+0x24`: a trailer handle, then a capacity word, a length word, and the characters. On `9e954d01.tbk` that reads the Copyright field and the Filename field. Offset `+0x42` is past the end of the record.

## Field bounds

A class `0xA` field is 61 bytes. The four signed words at `+0x0F` are a rectangle. The reader returns that rectangle. On `9e954d01.tbk` the Copyright field on `P0` is (248, 4500, 9638, 6300) and the Stem field on `P10210` is (2430, 690, 7050, 1545). The same read holds for every such field in `nida81.tbk`.

## Polygon

A class `0x10` polygon is 53 bytes. The count is the word at `+0x30` and the near pointer at `+0x32` names the stored points, four bytes each. Every such point list in `9e954d01.tbk` lies inside the source rectangle at `+0x28`. The bounds are four words at `+0x0F`. The reader returns the stored points.

## Button bitmap

A button bitmap is an 8-byte prefix followed by a `BM` file in the huge table. The stored id is the resource id plus 1. Resource 155 of `9e954d01.tbk` is the prefix at file offset `0x50117`. The picture is 580 by 158, 8 bits per pixel.

## Huge-table bitmaps

`9e954d01.tbk` names four bitmaps in the huge table. Resource 148 is at `0x2577`, 581 by 157, 8 bits per pixel. Resource 150 is at `0x18ff7`, 580 by 387, 8 bits per pixel. Resource 155 stays at `0x50117`, 580 by 158, 8 bits per pixel. Resource 164 is at `0x1be627`, 580 by 158, 8 bits per pixel. That count is four.

## 8-bit pictures

An 8-bit picture's pixels are indexes into the color table that follows its info header. The table has the info header's color count, or 256 when that count is 0. The window draws the table color, in red, green, blue order, for each index, with rows turned top-down. It does not read index bytes as color triples. Resources 148, 150, 155, and 164 of `9e954d01.tbk` are 8 bits per pixel. The first stored byte of each is index 0. For 148, 150, and 155 that is 192, 192, 192, and for 164 it is 113, 217, 217. Resource 155 is 580 by 158, and the `textbox` button on `P450` draws it. Every type-1 picture the reader finds decodes: 49 at 8 bits and 18 at 24 bits in `9e954d01.tbk`, and 18 and 14 in `nida81.tbk`. Each of the 67 in `9e954d01.tbk` is the same RGB as the `Bitmap` file of that id in the TBKX export.

## Button picture

A class `0x09` button is 43 bytes. The word at `+0x28` is a near pointer to a graphics block. When that word is not 0, the block starts with `0x0202` and the unaligned word at byte `0x15` of the block is the picture id. That id is a type-1 resource id plus one. The reader returns it. On `9e954d01.tbk` the four huge-table bitmaps are named there by their stored ids.

## Button bounds

A class `0x09` button is 43 bytes. The four signed words at `+0x0F` are a rectangle. The reader returns that rectangle. On `9e954d01.tbk` the Next button on `P300` is (8907, 6210, 9342, 6630) and the A button on `P10210` is (2430, 1635, 2715, 1920). The same read holds for every such button in `nida81.tbk`.

## Button checked picture

A class `0x09` button's word at `+0x28` names a graphics block that starts with `0x0202`. The unaligned word at byte `0x4b` of that block is the checked picture. It is a type-1 resource id plus one, or 0 when there is no checked picture. The reader returns it. On `9e954d01.tbk` the A button on `P10210` is 118, the stored id of bitmap 117. The MenuFrame button on `P300` is 0. The same word is a stored id or 0 on every such block in `nida81.tbk`.

## Button invert picture

A class `0x09` button's graphics block starts with `0x0202`. The unaligned word at byte `0x27` of that block is the invert picture. It is a type-1 resource id plus one, or 0 when there is no invert picture. The reader returns it. On `9e954d01.tbk` the A button on `P10210` is 117, the stored id of bitmap 116. The MenuFrame button on `P300` is 0. The same word is a stored id or 0 on every such block in `nida81.tbk`. The border byte at the button record's `+0x27` is a different field.

## Invert picture on press

While the mouse button is down on a button, the window draws the picture at byte `0x27` of that button's graphics block, when that word is not 0. Letting go draws the up picture again, and the click runs on release over the same button. Releasing somewhere else does not run the click. A button whose invert word is 0, such as `MenuFrame` on `P300`, does not change while held. On `9e954d01.tbk` the A button on `P10210` draws stored id 117, bitmap 116, while held, and stored id 116, bitmap 115, after release. The headless call `pressed` returns that held display list.

## Button disabled picture

A class `0x09` button's graphics block starts with `0x0202`. The unaligned word at byte `0x39` of that block is the disabled picture. It is a type-1 resource id plus one, or 0 when there is no disabled picture. The reader returns it. On `9e954d01.tbk` the A button on `P10301` is 128, the stored id of bitmap 127. The MenuFrame button on `P300` is 0. Every such block in `nida81.tbk` is 0.

## Disabled button picture

The window draws a disabled button's disabled picture. When bit 0 of button `+0x26` is 0 and the word at byte `0x39` of the graphics block is not 0, that stored id is the picture. When the word is 0 the up picture stays. On `9e954d01.tbk` the A button on `P10302` is disabled, and the window draws stored id 128, bitmap 127. The A button on `P10301` stores 128 too, but its enabled bit is 1, so it keeps up picture 116. On the `Test` background, `Back`, `Help`, `Next`, and `Skip` are disabled on the pages that store them that way, and they draw their disabled pictures 103, 109, 115, and 112. No button in either book is both disabled with a disabled picture and checked. Every button in `nida81.tbk` stores 0 at byte `0x39`, so those buttons keep their up pictures.

## Button border

A class `0x09` button is 43 bytes. The byte at `+0x27` is the border. The reader returns that byte. On `9e954d01.tbk` the Next button on `P300` is 1 and the A button on `P10210` is 9. The export calls 1 `none`, 9 `radioButton3d`, and 7 `pushButton`. In `nida81.tbk` every such button is 1 or 7.

## Button border frame

A button's border byte at `+0x27` is drawn as a frame in the button's stroke color, the color at `+0x17`. `pushButton` (7) is a frame on the bounds the reader returns. `radioButton3d` (9) is a smaller frame, one pixel (15 page units) inside the bounds. No byte stores that inset; it is the window's choice. `none` (1) and any other byte draw no frame. The picture is drawn first and the frame on top. A button's stroke is `+0x17` and its fill is `+0x1B`, the same offsets as a draw object: the export's `RgbStroke` and `RgbFill` match those bytes on all 382 buttons in `9e954d01.tbk`. On `9e954d01.tbk`, `Next` on `P300` is border 1 and has no frame. `A` on `P10210` is border 9, bounds `2430,1635,2715,1920`, and its frame is `2445,1650,2700,1905` in black. The `OK` button on `P30000` is border 7 and its frame is its bounds `4111,3945,5323,4245`. In `nida81.tbk`, `Retry` on `P12000` is border 7 and its frame is its bounds `603,2295,3339,2721` in black. A button caption is not drawn.

## Button enabled

A class `0x09` button is 43 bytes. Bit 0 of the byte at `+0x26` is enabled. The reader returns that bit. On `9e954d01.tbk` the Next button on `P300` is 1 and the A button on `P10302` is 0. The export calls 1 `true` and 0 `false`. The same bit is 1 on 93 buttons in `nida81.tbk` and 0 on 63.

## Button checked

A class `0x09` button is 43 bytes. Bit 4 of the byte at `+0x26` is checked. The reader returns that bit. On `9e954d01.tbk` the B button on `P10211` is 1 and the A button on `P10210` is 0. The export calls 1 `true` and 0 `false`. Every such button in `nida81.tbk` is 0. The checked picture at byte `0x4b` of the graphics block is a different field.

## Letter click checks the letter

On a page whose background calls `handleQuizClick`, a click on a button named `A` through `E` is `manageQuizButtons` in `nc81test.sbk`: `set checked of button vLabel to true`, then every other `ansiToChar(96 + i)` button that is checked is set to false. `initializeTest` sets `__quizMaxResponse` to 5, so the letters are `a` to `e`, compared regardless of case. The page stays. The window keeps that letter for the page and the book, and draws the page again: the clicked letter uses the checked picture at byte `0x4b` and the other letters use the up picture at byte `0x15`, whatever bit 4 of `+0x26` stores. On `9e954d01.tbk`, after a click on `A` on `P10210`, the display list has picture 118 for `A`, 119 for `B`, 122 for `C`, and 125 for `D`. Before the click `A` is 116. On `P10211`, where `B` is stored checked, a click on `A` draws `A` checked and `B` up. A page the window has not had a letter click on keeps its stored bits. The letter is also the `checked` that `quiz_click` reads.

## Page ids

Page ids come from the walk that already finds P0: the page list at book `+0x10`, then the C string at each page record `+6`. That walk includes P0 and P430.

## Background

A class 4 background is the record named by the far reference at page `+0x47`. The class word immediately before that record is 4. The pattern byte is at `+0x4B`. Red, green, and blue are at `+0x5B`, `+0x5C`, and `+0x5D`. On `9e954d01.tbk`, Logo and Definition both use those offsets. Logo is pattern `0xFE` and color 0, 0, 191. Definition is pattern `0xFE` and color 128, 128, 128.

## Quiz question

A quiz question page has fields named `Stem`, `A`, `B`, `C`, and `D`. The trailer slot before each of `Answer`, `QuestionNo`, `TestNo`, `SourceQuestionNo`, `SourceTestNo`, and `sourcepage` is a value: the word `0x0009`, a length, and that many characters. The reader returns those six values. On `9e954d01.tbk` the twenty pages `P10210` through `P10229` use that shape. Their test and question numbers are the same numbers as the `InfoText` field on page `PQINFO`. `SourceQuestionNo` is that question number, `SourceTestNo` is that test number, and `sourcepage` is the page id.

## Polyline

A class `0x13` record is 55 bytes. The count is the word at `+0x2D` and the near pointer at `+0x2F` names the stored points, four bytes each. The four signed words at `+0x25` are the minimum x, the minimum y, the maximum x, and the maximum y of those points. The reader returns the stored points. The same read holds for every such record in `9e954d01.tbk` and in `nida81.tbk`.

## Angled line

The window paints a class `0x13` record as an angled line. The line is the stored points the polyline reader returns, in stored order, stroked in the color at `+0x17`. It is not filled. The byte at `+0x1A` and the byte at `+0x1E` are 0 on all 66 records in `9e954d01.tbk` and all 14 in `nida81.tbk`. The TBKX export of `9e954d01.tbk` names `+0x17` `RgbStroke` and `+0x1B` `RgbFill` on all 66 angled lines. Every one of the 66 point lists in `9e954d01.tbk` and the 14 in `nida81.tbk` is on the display list of the page or background that holds it. The line Instructor drew on `otb-line-rect.tbk` is that book's one class `0x13` record, object 1, from (2040, 2955) to (240, 5295) in 0, 0, 0, and it is on that page's display list after the rectangle. The window does not change the field-under-shape order for an angled line.

## Arc

Class `0x11` object 80 on page P1140 of `9e954d01.tbk` stores two points, the signed pairs at `+0x25` and `+0x29`: (1866, 5065) and (1815, 4620). Those are the points in the record. The arc is not filled. A third signed pair is at `+0x2D`. The reader returns the object id, the rectangle at `+0x0F`, and the three pairs. On `9e954d01.tbk` 43 of the 62 arcs store (5433, 3955), (5428, 3544), (5385, 3750) and 19 store (1866, 5065), (1815, 4620), (1815, 4845), each group across more than one rectangle. On `nida81.tbk` both arcs store (3465, 4126), (3316, 4320), (3465, 4320). On P1140 objects 17, 65, and 80 store the same three pairs with three different rectangles, and none of object 80's pairs is inside its rectangle (5010, 3675, 5550, 4230). The pairs are not page positions, so the window does not paint an arc. The mapping onto the rectangle is in `FINDINGS.md`.

## Missing files are reported, not fatal

Logic Families names `minstb32.dll`. That file is not in the install list. Opening the book reports `named, not shipped` and still returns the book. A name that is in the install list but absent is `not found`. A starred install-list entry that is absent is `listed, not shipped`. None of the three stops the open.

## Field style runs

Word 0 of the block at record `+0x24` is a trailer handle to a run list. The second word of that run list is a count, and that many 11-byte runs follow. The reader returns those runs. The first word of each run is an offset into the field text from word 1 of the same block. On `9e954d01.tbk` the offsets in one field strictly increase and stay at most that field's text length. Byte `+6` of each run is 0 or 4, and byte `+10` is 0. The same shape holds on `nida81.tbk`.

## Class 0x8 colors

A class `0x8` record is 41 bytes. The bytes at `+0x17`, `+0x18`, and `+0x19` are a color, and the byte at `+0x1A` is 0. The bytes at `+0x1B`, `+0x1C`, and `+0x1D` are a color, and the byte at `+0x1E` is 0. The byte at `+0x25` is the pattern. The reader returns both colors and the pattern. The same read holds for every such record in `9e954d01.tbk` and in `nida81.tbk`.

## Line

A class `0x0E` line is 53 bytes. The endpoints are the signed pairs at `+0x26`. They sit in the rectangle at `+0x0F`. The reader returns those endpoints. On `9e954d01.tbk` the two records in `FINDINGS.md` are `(2145, 4065)` to `(1530, 4065)` and `(4425, 4065)` to `(3735, 4065)`.

## Style run name

The word at byte 2 of a style run is 1, or a near pointer in the list at the book record's `+0x28`. The first word of that list is a count of the pointers. When the run word is one of those pointers, the bytes there are a C string and the reader returns it. When the word is 1, the reader returns no string. On `9e954d01.tbk` more than one of those strings occurs, the same pointer is the same string, and 1 is not in the list. The same shape holds on `nida81.tbk`.

## No hatch for class 0x8

The next class `0x8` pattern byte after 254 and 253 that occurs in both books does not exist. In `9e954d01.tbk` the bytes at `+0x25` are 254 on 143 records, 33 on 56, 253 on 41, and 4 on 3. In `nida81.tbk` they are 254 on 75, 253 on 9, and 81 on 2. Only 254 and 253 are in both. The export names 254 `solidFill` and 253 `none`, and it writes 33 and 4 as bare numbers, `Pattern="33"` and `Pattern="4"`. No byte and no Instructor note names a hatch for 33, 4, or 81. The window does not draw a hatch: such a rectangle is its fill color at `+0x1B` and its stroke at `+0x17`. On `P440` the first pattern-33 bar is `750,4830,825,5130`, filled 192, 192, 192 with a black stroke.

## Layer list

A page or a background stores one class `0x06` record of 15 bytes whose word at `+0x08` is that page's or background's near. The word at `+0x02` is a count, and the word at `+0x0C` is a trailer handle. That handle's item holds that many near words: the parent's objects, back to front. The word at `+0x00` is at least the count. On `9e954d01.tbk` each of the 131 pages has exactly one such record and its list holds the page's objects once each. The object ids in list order are the export's `Page.Objects` order on all 131 pages. On 36 of them that order is not the stored order. Each of the 44 pages of `nida81.tbk` has one such record with the same property. The 14 lesson backgrounds and 20 `nida81.tbk` backgrounds store one as well, naming the same objects in their stored order. The window paints a page's or background's objects in list order, and a group's children in its own child list order. When the list is missing or does not name the same objects, the stored order stays. The field rules in the window section then run on that order. On `P300` the list is `0x25a`, `0x2da`, `0x9c`, `0xe4`, `0x3f6`: `MenuFrame`, the `MenuTitle` group, the `selection1` group, `Next`, `Back`. `MenuFrame` is behind the `selection1` button, so a click on that button is the button and not the frame. On `P410` the list puts the chip rectangle 39 in front of rectangles 68 and 69 and ellipse 58, which the stored order painted over it.

## Hotword click

A field's hotword character range is stored. A field style run whose word at byte 4 is the near of a class `0x17` hotword that names the field starts the hotword, and the range runs to the next run's offset or the end of the text. On `9e954d01.tbk` that range is the hotword's name in all five: `tolerance` at 87 to 96 on `P1080` and `P1082`, `propagation delay` at 31 to 48 on `P1200` and `P1207`, and `impedance` at 90 to 99 on `P2070`. The display list keeps each field's ranges and names. The window draws each style run from the stored text at its stored offset, with line breaks shown as breaks, so the hotword's run is the hotword's characters. A click on the text the window drew for that run is a click on the hotword, before buttons are tested. The click runs the hotword's `buttonClick` on the same path as a button. Each of the five assigns `lastpage = name of this page` and runs `go to page "p1085"`, `"p1205"`, or `"p2075"`. A page name in a quoted `go to page` matches regardless of case, so they open `P1085`, `P1205`, and `P2075`.

## Style run size

The list at the book record's `+0x28` names font-table entries. An entry starts with the face name, and the signed word at entry `+0x20` is minus the character height in page units. A field's own font is the entry its word at `+0x22` names. A style run's size is the entry its word at byte 2 names, and a run word of 1 is the field's font. No byte of the 11-byte run is the size, and byte `+6` stays the 0 or 4 the run reader returns. The display list keeps each run's offset and height, and the window draws each span at that height in pixels. On `9e954d01.tbk` the face and the height of the `+0x22` entry match the export's `FontFace` and `FontSize` on all 496 fields the export and the walk share: the height is the point size in 96-dpi pixels times 15, so 10 points is 195, 12 is 240, 14 is 285, 16 is 315, and 6 is 120. On `P100`, `Objective1Title` has an Arial run at 0 with height 240 and an MS Sans Serif run at 18 with height 280, so the window draws them at 16 and 19 pixels. On `P900`, `Exit` has a run at 2 whose word is 1, and it takes the field's 240. Every field in `nida81.tbk` gets a height from the same read. When a script changes a field's text, the sizes move with the runs.

## Stroke width

The byte at `+0x22` of a class `0x8`, `0xC`, `0xD`, `0xE`, `0x10`, or `0x13` record is the line style. Against the export's `LineStyle` on `9e954d01.tbk` it is one value per style on every record of each class: 4 is `1` (516 lines, 221 rectangles, 43 ellipses, 62 angled lines, 649 polygons), 5 is `2` (2 lines, 2 ellipses), 6 is `3` (2 rectangles, 4 angled lines), 9 is `8` (20 rectangles), 2 is `dotted` (10 lines), and 1 is `none` (5 polygons). Every class `0xE` line in both books stores one of those bytes: 4 on 516, 2 on 10, and 5 on 2 in the lesson; 4 on 11, 1 on 6, 5 on 4, and 6 on 3 in `nida81.tbk`. The window strokes 4, 5, 6, and 9 at 1, 2, 3, and 8 pixels times the fit scale, at least 1. 1 is no stroke: a line is not drawn and a shape has no outline. 2 is drawn solid at 1 pixel; dotted is not drawn. A byte not in that list, such as 7 on four `nida81.tbk` rectangles, is 1 pixel. The color at `+0x17` is still the stroke color the reader returns. On `P1110` the red line and ellipse are 2 pixels. On `nida81.tbk` `P12000` a line is 3 pixels, and on `P22100` the 14 class `0xD` records have no outline.

## Class `0x0B`

A class `0x0B` record is 49 bytes. The four signed words at `+0x0F` are a rectangle. It is the union of the rectangles at `+0x0F` of the objects whose word at `+0x04` names the record. The reader returns that rectangle. On `9e954d01.tbk` the two records in `FINDINGS.md` are (2557, 105, 6322, 1005) and (3202, 360, 6142, 765). The same read holds for every such record in `nida81.tbk`.

## Class `0xD`

A class `0xD` record is 45 bytes. It stores its rectangle and colors where class `0x8` does. The four signed words at `+0x0F` are an ordered rectangle. The bytes at `+0x17`, `+0x18`, and `+0x19` are a color, and the byte at `+0x1A` is 0. The bytes at `+0x1B`, `+0x1C`, and `+0x1D` are a color, and the byte at `+0x1E` is 0. The byte at `+0x25` is the pattern. That holds on all 14 records in `nida81.tbk`, all on page `P22100`, and every one is pattern 254. `9e954d01.tbk` has none. The window paints the rectangle with the class `0x8` rule: the color at `+0x1B` fills it when the pattern is not 253, and the color at `+0x17` is the outline. On `P22100` object 279 is (7282, 4176, 7495, 4259), outline 96, 96, 96, fill 255, 0, 0. The corners are drawn square. The words at `+0x28` and `+0x2A` are not drawn; they are in `FINDINGS.md`.

## Class `0xC` colors

A class `0xC` record is 41 bytes. The bytes at `+0x17`, `+0x18`, and `+0x19` are a color, and the byte at `+0x1A` is 0. The bytes at `+0x1B`, `+0x1C`, and `+0x1D` are a color, and the byte at `+0x1E` is 0. The byte at `+0x25` is the pattern. The reader returns both colors and the pattern. On `9e954d01.tbk` page `P410`, both ellipses use the same pattern and the same first color as that page's background. On `nida81.tbk` page `P310`, five ellipses do the same, and other ellipses on that page do not. The same read holds for every such record in both books.

## Class `0x10` colors

A class `0x10` record is 53 bytes. The bytes at `+0x17`, `+0x18`, and `+0x19` are a color, and the byte at `+0x1A` is 0. The bytes at `+0x1B`, `+0x1C`, and `+0x1D` are a color, and the byte at `+0x1E` is 0. The byte at `+0x25` is the pattern. The reader returns both colors and the pattern. On `9e954d01.tbk` two pattern values each occur on 14 records, and within each of those groups the two colors are constant and differ from each other. The same read holds for every such record in `nida81.tbk`.

## Page records

A page names its background with the far reference at `+0x47`. The objects on the page are the records whose word at `+0x04` is that page's near offset, in the order those records are stored. A class `0x0B` group is one of those records. The objects under it are the records whose word at `+0x04` names the group, in the order of the 10-byte entries at `+0x2E`. The reader returns that background and those records. On `9e954d01.tbk` page `P300`, the group `Selection1` is a button then a field. Page `P1140` has three groups whose children are an arc, a polyline, an ellipse, a line, and a group, and one of those arcs is object 80. The same walk holds on `nida81.tbk`. On page `P310` the entries are the button at `0xB5C` and the field at `0xBDC`. On page `P370` object 38, a class `0x19` record, is under the group at `0x9C`. Where the list is not the order of the records in the segment, the reader follows the list. On pages `P410` and `P430` the last two entries of those groups are a class `0x8` record and a class `0x11` record. On `P22100` of `nida81.tbk` the class `0xC` entries are objects 301, 302, and 304. An inner class `0x13` that the list places earlier stays earlier, on `P1910`, `P1999`, `P2910`, and `P2999`.

## Class `0x12` on the page walk

The page walk returns class `0x12` pies. A pie record's end word, the word before its class word, minus its near offset is 59. The last object in a directory record stores 1 as its end word, and that object runs to the end of the record. On `otb-pie.tbk` that is pie id 2. On `9e954d01.tbk` it is the field `Review 2`, object 11 on `P10410`, at (2986, 3018, 6535, 3303) with the text `2.  Other Integrated Circuits`. The TBKX export lists that field with those bounds and that text. The walk now returns it and the window paints it. No other page of `9e954d01.tbk` or `nida81.tbk` changes. The walk returns each pie with the eight signed words stored from `+0x25`. On `otb-pie.tbk` the page is pie id 0, ellipse id 1, and pie id 2. Pie id 0 stores 1500, 3500, 1500, 1500, 1500, 3500, 0, 2000, and pie id 2 stores 500, 500, 2400, 500, 500, 500, 1900, 0. Their bounds at `+0x0F` are (600, 600, 3000, 3000) and (-1400, 500, 2400, 500). The words are not a settled point list, and the window does not draw a wedge.

## Pie wedge refused

The window does not fill a pie wedge. The eight words of both pies on `otb-pie.tbk` read the same way: the third point given to `draw pie`, the first point, the third point again, and the distance from the first point to the third on each axis. Pie id 0 was drawn `from 1500,1500 to 3500,3500 to 1500,3500` and stores (1500, 3500), (1500, 1500), (1500, 3500), (0, 2000). Pie id 2 was drawn `from 2400,500 to 1500,2200 to 500,500` and stores (500, 500), (2400, 500), (500, 500), (1900, 0). The reader returns those four pairs. The second point is not stored on either pie, so the end of the wedge is not in the words. Both pies have a zero distance on one axis. The third point plus and minus that distance is the bounds of pie id 2. Pie id 0 was given the bounds (600, 600, 3000, 3000) after it was drawn, and its words did not change, so the words are not in the coordinates of the bounds. No third pie is in the lesson or `nida81.tbk`. `DENNY-OBJECTS.md` says a pie is the part of an ellipse the author chooses and that Reshape Pie moves its end points, but it does not name a stored field for either. No wedge formula follows from two degenerate examples, and the click and double-click behavior is not recorded in `DENNY-OBJECTS.md` or `FINDINGS.md`.

## Background second color

A class 4 background stores a second color at `+0x57`, `+0x58`, and `+0x59`. The byte at `+0x5A` is 0. The reader returns that triple. On `9e954d01.tbk` twelve of the backgrounds store 0, 0, 0 and two store 255, 255, 0. On `nida81.tbk` every background stores 0, 0, 0.

## Field words

A class `0xA` field is 61 bytes. The reader returns the word at `+0x28`, the word at `+0x2A`, the word at `+0x2C`, the word at `+0x32`, and the byte at `+0x36`. On `9e954d01.tbk` the values 360, 360, 310, 50, 5 occur together on 85 fields, and 0, 0, 0, 50, 1 occur together on 258. On `nida81.tbk` those two combinations occur on 19 fields and on 100 fields. The other combinations are in `FINDINGS.md`.

## Class `0x17`

A class `0x17` record is 17 bytes. The word at `+0x04` is a near pointer to a class `0xA` field, and that field is named `Text`. The reader returns the pointer and the name. `9e954d01.tbk` has five. On `P1080` the word is `0x240`. On `P1082` it is `0x9C`. `nida81.tbk` has no class `0x17` record.

## Hotwords on the page walk

A class `0x17` record is a hotword. The page walk returns it as a child of the class `0xA` field its word at `+0x04` names, in stored order. It is not an object of the page by itself. Its name is the trailer name its word at `+0x06` names, as for other objects. On `9e954d01.tbk` the five are `tolerance` on `P1080` and `P1082`, `propagation delay` on `P1200` and `P1207`, and `impedance` on `P2070`, each under that page's field `Text`. The TBKX export lists the same five names inside the same fields. The window paints the field's text once and does not paint the hotword. A page with no hotword walks as before.

## Page body

The page body is that field, not a second store. A class `0xA` field names the character record through word 1 of the block at `+0x24`, and those bytes are the record in the gap after the page's directory body. The reader returns that file offset and the characters. On `9e954d01.tbk` page `P440` the field `Text` is the record at file `0xcbad7`. The same holds for every page of that book and of `nida81.tbk`: the text block is past the directory body, and the directory body does not hold a second copy.

## buttonClick

An object's `buttonClick` is source text. The reader expands the inline script and returns that handler. It does not call it. On `9e954d01.tbk` page `P300`, the group `Selection1` contains `go to page "P310" of book "nida81.tbk"` and the words `send next`. On `nida81.tbk` page `P340`, the buttons `Next` and `Back` contain `go to page nextpage of book lastbook`. The keyword ids are the 994 entries of TB80CMP resource `0x77`. In the `P300` script the bytes `90 af 80 91 83` are the words `go to page`.

## Quoted go to page

A `go to page` line returns the page in double quotes and, when the line has one, the book in double quotes. It returns nothing else. `send next` stays those words. `go to page nextpage of book lastbook` has no quotes, so it is not a page id. On `9e954d01.tbk` page `P300` the quoted page is `P310` and the quoted book is `nida81.tbk`. The same line on `nida81.tbk` names `P20001` of `nida81.tbk`. A quoted page with no quoted book, such as `P400`, returns that page and no book.

## Line colors

A class `0x0E` line is 53 bytes. The bytes at `+0x17`, `+0x18`, and `+0x19` are a color, and the byte at `+0x1A` is 0. The bytes at `+0x1B`, `+0x1C`, and `+0x1D` are a color, and the byte at `+0x1E` is 0. The reader returns those two colors with the endpoints. On `9e954d01.tbk` the two records in `FINDINGS.md` store 255, 252, 240 and 128, 128, 128, and twelve endpoint pairs are stored with more than one color pair. On `nida81.tbk` those two records store 64, 64, 64 and 255, 255, 255, and 96, 96, 96 and 255, 255, 255. The byte at `+0x25` is not returned.

## Lesson filename spelling

On open, each named file is keyed by the spelling the lesson stored. A later mention of the same name in another case does not add a second entry. The lookup still ignores case. `9e954d01.tbk` stores `MINSTB32.dll` and `TB80ANM.SBK`. `nida81.tbk` stores `nida71.tbk`. That file is reported and not opened. A missing name still carries `named, not shipped`, `not found`, or `listed, not shipped`.

## Resource script

A type 10 resource is 15 bytes. It starts with the words `0x0202` and `0x0001`. The word at `+9` is a near pointer. The word at that pointer is a count, and that many bytes are the handler. The last byte of the count is 0. The reader expands the whole count to source text and returns it. It does not call the handler. On `9e954d01.tbk` the scripts begin `to handle enterPage` or `to handle enterSystem`. On `nida81.tbk` they begin `To handle enterpage` or `to handle enterApplication`. The word at `+4` is not the pointer. The type 9 record with the same id does not hold these bytes.

## Shared script

A type 19 resource is 15 bytes. It starts with the word `0x0202`. The word at `+9` is a near pointer. The payload at that pointer starts `01 02 13 00`. The handler is the first `80 81` in that payload, and the reader expands until opcode 0. It does not call the handler. On `9e954d01.tbk` the four resources are 100, 101, 102, and 103. Resource 102 begins `to handle buttonClick` and contains `response = answer of this page`, then `score = 100` or `score = 0`. `nida81.tbk` has no type 19 directory.

## System book script

`nc81base.sbk`, `nc81recs.sbk`, `nc81test.sbk`, and `nc81trnr.sbk` each store one type 10 record. The same count, ending in 0, is the handler. The reader returns that whole source. It does not call the handler. The records are id 129, 268, 741, and 428. The sources begin `-- NC81BASE.SBK`, `-- NC81RECS.SBK`, `-- NC81TEST.SBK`, and `-- NC82TRNR.SBK`. The handlers inside them are `to get`. The `nc81test.sbk` source contains `to get handleQuizClick`, `to get getQuizScore`, and `to get gotoNextQuestionEx`.

## Quiz start

A `buttonClick` handler that contains the line `end buttonClick` ends on that line. The reader returns the handler through that line. It does not call it. On `9e954d01.tbk` the group `selection1` on pages `P10001`, `P10002`, `P10003`, and `P10004` ends that way. Each calls `setupQuizEx` with `2`, `"P10301"`, `"P10302"`, and `"P10303"`, then `get clearpool()`, `addObjectiveToPool(1, 110, 119, 6)`, `addObjectiveToPool(2, 120, 129, 4)`, `setuppool()`, and `get gotoNextQuestionEx()`. The first argument is `Assessment`, `Pre-Test`, `Post-Test`, or `Quiz`.

## Book handlers

A handler whose body is in an `.sbk` is a column-0 line `to get` or `to handle` in that book's type 10 source. The reader returns the handler name and the book. It does not call the handler, and it does not read a DLL. `nc81base.sbk` holds 46 `to get` handlers, from `initializeBase` through `getCurrentPath`. `nc81recs.sbk` holds 17 `to get` handlers, from `initializeRecs` through `GetVar`. `nc81test.sbk` holds 89 `to get` handlers and `to handle timerNotify`. `nc81trnr.sbk` holds 63 `to get` handlers, plus `to handle linkMemFunctions32` and `to handle unlinkMemFunctions32`. None of the four books has a `to set` line.

## Handler split

Each of those handler lines splits into a name, an argument list, and the start of the body. The name is the word after `to get` or `to handle`. The argument list is the rest of that line, with the spaces around it removed. Nothing left is no arguments. The body starts on the next line. The reader returns that split. It does not call the handler. `initializeBase` in `nc81base.sbk` takes `cmdLine`, and `specifyMenuColors` takes `color1, color2`. `writeResponse` in `nc81recs.sbk` takes `int testno, int questionno, string response, int score`. `timerNotify` in `nc81test.sbk` takes `timerId`, `clearRandomSetX` takes `int numbers[] by reference`, and `getNextQuestion` takes no arguments. `linkMemFunctions32` in `nc81trnr.sbk` takes no arguments, and `sendFaults130` takes `string faults`. `getExternalValue` is followed by a blank line, and that blank line is where its body starts.

## Export module name

The bytes before the object store are a PE file. Data directory 0 is the export directory. The reader returns the C string its Name field points at. On `otb-line-rect.tbk` that string is `MINSTB32.dll` at file offset `0x258`, and the directory lists zero exports. `nida81.tbk` and `9e954d01.tbk` store the same name at that offset. `nida81.tbk` has no other `.dll` name.

## Page size

The book record stores the page width at `+0x20` and the page height at `+0x1E`. Both are signed words. The reader returns those words for every book; it does not hard-code a lesson size. On `otb-line-rect.tbk` and `otb-pie.tbk` they are 9000 and 6000. On `9e954d01.tbk` and `nida81.tbk` they are 9360 and 6624. On `nc81base.sbk`, `nc81recs.sbk`, `nc81test.sbk`, and `nc81trnr.sbk` they are 9345 and 6630. One page unit is 1/20 point. One point is 96/72 pixels at 96 dpi. The fit scale multiplies that pixel size once.

## Page window

`python3 -m opentoolbook --show P300 path/to/9e954d01.tbk` opens that page. The display list is the same list without a screen. The background is painted from the class 4 reader. Pattern 254 is a solid fill of the color at `+0x5B`. Pattern 253 paints no fill. A rectangle, ellipse, or polygon uses the color at `+0x1B` as its fill and the color at `+0x17` as its stroke. A line is the two endpoints at `+0x26`, in the stroke color. A polygon is the stored points. A field paints its text, its bounds, and the style-run faces. A button paints its bounds and the picture at byte `0x15` of the graphics block. The picture at byte `0x4B` is drawn only when bit 4 of button `+0x26` is set. A button whose enabled bit, bit 0 of `+0x26`, is 0 draws the picture at byte `0x39` when that word is not 0, and keeps the up picture when it is 0. On `P10210` the A button is not checked, so the window uses picture 116 and not picture 118. After a click on A it uses picture 118. A field whose bounds contain a non-text shape is painted under that shape. A label whose bounds contain no shape is painted in front of a later shape or button that contains the label. On `P300` the selection text is in front of `MenuFrame`. On `P400` the part number is in front of the chip rectangle. On `P410` the label stored behind the chip rectangle is painted in front of it. On `P1110` the field that contains a line is painted under that line, and the label that contains nothing is painted in front of the ellipse.

An inline type-1 picture stores a `BM` file eight bytes after `01 02 01 00`. On `9e954d01.tbk` that marker is at byte 18 of all 63 inline pictures. On `nida81.tbk` it is at byte 18 of 21 pictures and at byte 36 of the other 2. A huge-table picture keeps the `BM` file after the 8-byte prefix.

## Window resize

Resizing the window refits the page. The canvas fills the window. A `Configure` event with a new canvas size computes the fit scale again from the stored page size and that view: 9360 by 6624 on the lesson, 9000 by 6000 on the fixtures. The paint list is unchanged and only the scale moves. A 600 by 400 view of `otb-line-rect.tbk` is scale 1, and a 300 by 400 view of the same page is scale 0.5. There are no scroll bars.

## No enterButton or leaveButton

`handler_sites` finds every `to handle NAME` line in a book's expanded scripts: inline object scripts, type 10 scripts, and type 19 shared scripts. Handler names are stored as keyword tokens, so a byte search of the file does not see them. On `9e954d01.tbk`, `nida81.tbk`, `nc81base.sbk`, `nc81recs.sbk`, `nc81test.sbk`, and `nc81trnr.sbk` there is no `enterButton` handler and no `leaveButton` handler. The window dispatches neither message. The hover handlers the books do have are `mouseEnter` and `mouseLeave`, 19 of each on `9e954d01.tbk` and 3 of each on `nida81.tbk`, all in inline scripts of class `0xA` fields such as `Selection1` on `P300`, and none in the system books. The window sends `mouseLeave` to the prior object and `mouseEnter` to the new one on pointer motion, and `mouseLeave` when the pointer leaves the canvas. `Navigator.message` runs those handlers the same way as `buttonDown`. A synthetic `mouseEnter` that goes to another page opens that page.

## Window close

The window's close button ends the Tk loop. `open_page` returns, and `python3 -m opentoolbook --show PAGE book.tbk` exits 0. Before this, closing the window raised `TclError` from the destroyed root. A click whose handler raises `ValueError` or `OSError` prints that error's one line on stderr and the window stays up on the same page. Any other exception keeps its traceback and the window also stays up. The smoke test opens `otb-line-rect.tbk` and presses close. It is skipped with a message when `DISPLAY` is unset or the Python has no `tkinter`.

## Page photos

Drawing a page deletes the Tk images of the page drawn before it, then makes the new page's images. The window holds the photos of one page at a time. On `9e954d01.tbk` P300 has five button pictures and P400 has four, and P300, Next to P400, Back to P300, and so on keeps the window at five and four images, whether or not something else still holds a reference to an old photo. There is no bitmap cache across pages or books.

## Export DLL in the window

The book's PE export directory names `MINSTB32.dll`. When the shelf search the open uses does not find a file of that name, ignoring case, `unshipped_dll` returns `MINSTB32.dll named, not shipped`. The window does not show that line under the page. `--report` prints it on the named-files list as `MINSTB32.dll  named, not shipped` when the DLL is absent. It is not loaded, it does not stop the open, and the page still paints. On `9e954d01.tbk` with no DLL on disk the bare command still opens `P0` of `nida81.tbk`. A `MINSTB32.DLL` that the search finds clears the note.

## One missing-book sentence

Opening a book and clicking a button raise the same error when the shelf search does not find a book a handler quotes. It is one sentence: the file, then the page of that book, `nida81.tbk was not found; P310 of that book does not open`. On `9e954d01.tbk` with no `nida81.tbk` on the shelf, the bare command prints `nida81.tbk was not found; P0 of that book does not open` on stderr and exits 2, and `Selection1` on `P300` prints `nida81.tbk was not found; P310 of that book does not open` and the window stays on `P300`. `--show` on a book file that does not exist prints that sentence with the `--show` page and exits 2. `--show` on a page id the book does not store prints `no page` and that id and exits 2. Neither prints a traceback. When a click printed an error during the window's life, closing the window exits 1. Otherwise it exits 0.

## nida71.tbk stays missing

`nida81.tbk` quotes `go to page "P12060" of book "nida71.tbk"` in the `Retry` button of pages `P12000`, `P12001`, `P12002`, and `P12003`. The file is not shipped and is not vendored, and the shelf search does not find it. That line sits under `when it is 60`, after `get verifyVoltages130a(...)`. No book, lesson or system book has a `verifyVoltages130a` handler, so on the interpreter the call is unanswered, `it` is not 60, and the click does not reach the `nida71.tbk` line. `Retry` on all four pages stays on the page and prints nothing.

## Arrow keys

The Right key runs the click of the button named `Next` on the page, and the Left key the click of the button named `Back`. The name match ignores case and takes buttons from the page and from its background. It is the same path as clicking that button, including `enterPage` on the page it lands on. On `P300` of `9e954d01.tbk` Right opens `P400` and Left opens `P100`. On `P400` Left opens `P300`, the page its `Back` handler quotes. On the question page `P10210` Right is the `Test` background's `Next` and opens `P10211`. A page with neither button ignores the keys. Escape closes the window. The book's own key handlers are not run.

## Keys the book script binds

Search of the expanded scripts (inline object scripts, type 10, and type 19) of `9e954d01.tbk`, `nida81.tbk`, and the four system books for `keyDown`, `keyUp`, `keyChar`, and `__quizDisableMenuKey`:

- `9e954d01.tbk` type 10 script 376 holds `enterSystem`, so it is the book script. Its `to handle keyup key` quotes `keyf1`, `keyf2`, `keyf4`, `keyf5` through `keyf9`, `keyf11`, `keyf12`, and `keyEnter` in a `conditions` block when `__quizHelp` is 0, and `keyEnter` and `keyF5` when it is not. `keyf10` is commented out. `keyF4` is guarded by `__quizDisableMenuKey = 0`.
- Type 10 scripts 372, 373, and 374 each have an empty `to handle keyUp` and a `to handle keyDown key` that calls `handleQuizKey` for `keyF7`. A page record whose mode byte at `+0x30` has low bits 2 names its own type 10 script by the word at `+0x2A`: `P10301` is 373 and `P10302` is 374 on the lesson, and `P12000`, `P12001`, and `P12002` are 159, 160, and 161 on `nida81.tbk`. `P10303` names 375 and `P12003` names 162, and neither book stores that resource. No stored page or background names 372.
- `nida81.tbk` type 10 script 165 holds `enterApplication` and a `to handle keyup key` with the same F-key and `keyEnter` branches. Its `keyf4` branch says `go to page "p900" of book lastbook`.
- Type 19 shared script 100 has `to handle keyUp key` that sends `buttonClick` to button `Accept` on `keyEnter` when `getQuizMode()` is 0. Shared script 101 has `keyChar`. Shared script 103 has an empty `keyUp`, a `keyDown` for `keyF5` and `keyF7`, and a `keyChar`, all calling `handleQuizKey`.
- `nc81base.sbk` sets `__quizDisableMenuKey` to 0 and to 1. None of the four system books has a key handler. Inline object scripts send `keyup keyF2` and `keyup keyF5` to the page, and define no key handler.

The window binds one of those keys. Enter is `keyEnter` in the book's `keyUp`: on the lesson that branch is `send buttonClick to button "next"` inside `if isObject(button("Next"))`, so Enter runs the click of the page's `Next` button, and on `P300` it opens `P400`. On `nida81.tbk` the same branch adds `visible` and `enabled` checks that the reader does not evaluate. A page whose own type 10 script has a `keyUp` handles the key there: `P10301` and `P10302` have an empty one, so Enter does nothing on them. The other quoted keys are not bound through that static `keyUp` branch walker, because their branches are `request`, `open viewer`, `send exit`, or `get` calls such as `specialFunctions` that the walker does not run. Shared-script key handlers on resources 100, 101, and 103 are still not bound, because no stored object is known to own those scripts.

PageUp (`keyPrior`), PageDown (`keyNext`), Up, Down, and F1–F12 send `keyDown` to the page with that OpenScript key constant as the argument, then up the page, background, book, `sysBooks` path, when a handler answers. A synthetic `keyDown` that goes to another page when the key is `keyNext` opens that page for PageDown and stays for PageUp. Right, Left, and Enter still prefer the Next/Back/`keyUp` button paths before `keyDown`.

## Report stays headless

After the window changes, `--report` still prints only the record count, the follow-up reads, the files the book names, and the startup call names, and it opens no window. `--report book.tbk` and `book.tbk --report` print the same report. With `--home`, all four orders of `--home DIR`, `--report`, and the book print the same install-and-book report, and none opens a window. `--home` without a book still prints the install folder and opens nothing. A book with `--home` and no `--report` opens the window and prints nothing. The report runs in a Python that cannot import `tkinter`. On `otb-line-rect.tbk` with no DLL on the shelf the report names `MINSTB32.dll  named, not shipped` on the named-files list. With an install list that does not name it, that same note appears.

## Enter page greeting

On `P10` of `9e954d01.tbk` the `enterPage` handler sets the text of field `First` to `"Hello" && getFirst() & ", this lesson is about:"` when `sysLevel` is `reader`, and to `"Hello, this lesson is about:"` otherwise. The field's stored name is `first`. A missing `sysLevel` is `reader`. `getFirst` in `nc81recs.sbk` returns `__studentFirst`. The reader strips the ends of that variable, and returns `Student` when it is empty. `&&` concatenates with a space. `&` concatenates. That `enterPage` runs on the interpreter when the window enters `P10`, and the window then shows `Hello Student, this lesson is about:`. `show_page` alone is the stored page and runs no script, so it shows the stored `Hello, this lesson is about:`. The one style run at offset 0, face `Arial`, covered the stored string and covers the new string. The field `Text` stays `LOGIC FAMILIES`.

`get setSection("Intro")` calls `setSection` in `nc81base.sbk`. That handler writes through `kernel32.dll`. The reader does not call the DLL, and the greeting does not use the return. `forward` has no handler body in the lesson or the four system books. The reader does not invent one.

On `PINFO` and `PQINFO` the handler sets field `version` to `"Version: " & __nidaVersion of this book`. The book stores that user property (see "Stored user properties"), so the field reads `Version: 2.003.0001` from the property. A value that still contains `__` and `of this book` because the book stores no such property is not written, and the stored line stays.

## Class `0x15` paint object

A class `0x15` record is 89 bytes. It is a bitmap, not a container. The four signed words at `+0x0F` are the bounds. The byte at `+0x26` is the pattern, 254 on all five records in `9e954d01.tbk` and the one in `nida81.tbk`. The dword at `+0x29` is the pixel byte count. The dword at `+0x2D` is the stored byte count when the pixels are packed, and 0 when they are stored as is. The word at `+0x4D` is a 1-based row of the huge table at header `+0x104`. That row's first dword is the stored byte count and its third dword is the file offset of the bytes. The word at `+0x4F` is the palette color count. The word at `+0x51` is a near pointer to a 40-byte bitmap info header, and that many palette entries follow it. All six records hold each of those reads.

Packed bytes are blocks. Each block is a word that counts its codes, then those codes. A code below `0xF6` repeats the next byte the code plus three times. A code of `0xF6` or more copies the next `code - 0xF5` bytes. A block does not start on the last byte of a 64 KB span of the packed bytes; that byte is skipped. The four packed records in `9e954d01.tbk` use two streams, each one block, of 2605 and 2147 codes, and each unpacks to exactly the pixel byte count. Those bytes equal the pixels of `PaintObject16.bmp` and `PaintObject20.bmp` in the TBKX export of that book, which calls the class `PaintObject` and names the same bounds.

The window draws the bitmap at the left and top of the bounds, at one bitmap pixel per screen pixel times the fit scale. On `9e954d01.tbk`, `P450` draws object 2 at (0, 0, 9360, 6630), 624 by 442, 24 bits. The `Test` background draws object 16 at the top, 627 by 24, and object 20 at the bottom, 627 by 28, both 8 bits with a palette. On `nida81.tbk`, `P0` draws object 4, 554 by 390, 24 bits. A record whose bytes do not unpack to the pixel byte count is not painted.

## Class `0x19` picture

A class `0x19` record is 89 bytes. It is a picture: a Windows metafile with bounds. It is not a filled shape, so the window does not use the class `0x8` fill rule for it. The four signed words at `+0x0F` are the bounds. The byte at `+0x26` is 254. The dword at `+0x29` is the metafile byte count. The dword at `+0x2D` is the stored byte count when the metafile is packed, and 0 when it is stored as is. The word at `+0x4D` is a 1-based row of the huge table at header `+0x104`, and that row's third dword is the file offset of the stored bytes. All 39 records in `nida81.tbk` hold those reads. 33 are packed and 6 are not, and every one gives exactly its metafile byte count.

Packed bytes are blocks. Each block is a word that counts its codes, then those codes. A code below `0xF6` repeats the next byte the code plus three times. A code of `0xF6` or more copies the next `code - 0xF5` bytes. A block does not start on the last byte of a 64 KB span of the packed bytes; that byte is skipped. Three of the 33 packed pictures need that skip.

The reader walks the metafile's own records. It plays `SetWindowOrg`, `SetWindowExt`, an optional `IntersectClipRect`, and one or two `StretchDIB` records with 8-bit DIBs; every other function is skipped. Without a clip record the clip is the window. One `StretchDIB` with `SRCCOPY` is the picture. Two records are `SRCPAINT` then `SRCAND` over the same rectangle. On every pixel of those pairs, either the first DIB is black and the second is white, and the page shows through, or the result does not depend on the page and is the first AND the second. The reader draws the DIBs into the window extent, clipped, and returns that picture with a mask. The window stretches the picture to the bounds. All 39 pictures in `nida81.tbk` paint that way: two use one `SRCCOPY`, and 37 use the pair. Nine of the 39 bounds are not 15 units per window pixel, so a picture is resized with its bounds. On `P310` object 36 is a 372 by 397 picture in (1080, 945, 6645, 6900). On `P370` object 38 is under the group at `0x9C` and is drawn. A metafile with no window, or with StretchDIB counts or ROPs the reader does not play, is not painted.

## Quiz page click

The background a page names is painted under the page. Its fields and buttons use the same readers as the page. Class `0x15` paint objects on that background are painted, as the section "Class `0x15` paint object" says. On the `Test` background the buttons are `Back`, `OK`, `Help`, `Skip`, and `Next`, and each has an up picture. The book `enterPage` sets field `page#` to the name of the page when that field is on the background. On `P300` that field reads `P300`.

`P10210` is a question page. Its letter buttons keep the up picture. The checked picture stays off the page while no letter is checked. The rectangle named `Correct` sits on the answer and its pattern is 253. It is not painted. No quiz pass has shown it, and a letter is not drawn as the correct answer. Shared script 103 and the `Test` background both call `handleQuizClick`. In `nc81test.sbk` that handler, when `__quizPass` is in `1,2` and `getQuizResponse()` is empty, runs `beep(1)` and `return 0`. The page stays. A checked letter on that pass does not beep, and it does not change the page: `gotoNextQuestionEx` calls `getNextQuestion`, and that returns `getNextRandomX` of the pool. The pool is not a page id.

A list-opened question page has no quiz running. `OK`, `Next`, and `Skip` go to the next page in the stored page list. `Back` goes to the previous page. On `9e954d01.tbk` those pages around `P10210` are `P10004` and `P10211`. A letter click stays. `__quizPass` 8 is the same next and previous pages: `gotoNextQuestionEx` runs `send next`, and `gotoPreviousQuestionEx` runs `send previous`. `Skip` on that pass, when a letter is checked, runs `beep(1)` and a request, so the page stays.

## Button click

A `buttonClick` handler runs on the interpreter (see "Clicks on the interpreter"). A quoted `go to page` opens that page. A quoted `of book` names that file. The window finds it with the same search as opening a book: the book's directory, its parent, `--home`, regardless of case. `--show` passes `--home` to the window too. A file that search does not find is an error that names the file and the page, for example `nida81.tbk was not found; P310 of that book does not open`. The window prints that line on stderr and stays on the page. With `nida81.tbk` only in the lesson's parent directory, `Selection1` on `P300` opens `P310` of that file. After the window changes books, the search still starts from the book the user passed on the command line: that book's directory and its parent, then the directory of the book on screen and its parent, then the `--home` folders. When the bare command opens `9e954d01.tbk` and the window lands on `P0` of `nida81.tbk` from `--home`, a click from that page still finds a file that sits beside the lesson, and `--home` stays on the window. `break` stops the handler, so the `send next` after it does not run. `send next` and `send previous` are the next and previous pages in the stored page list. On `P300` of `9e954d01.tbk`, `Next` opens `P400`, `Back` opens `P100`, and `Selection1` opens `P310` of `nida81.tbk`. `go to page nextpage of book lastbook` has no quotes. It reads those two system variables, which `Selection1` on `P300` set to the page and the book it left. A click no handler takes does not change the page.

## Version strings

Resource type 16 in the PE resource directory is a version resource. The reader returns `FileDescription`, `InternalName`, `OriginalFilename`, `ProductVersion`, and `CompanyName` from that resource. On `otb-line-rect.tbk`, `nida81.tbk`, and `9e954d01.tbk` those strings are `Toolbook II`, `TB80`, `TB80.EXE`, `8.10.131`, and `Click2learn, Inc.`. The same five strings are in `nc81base.sbk`, `nc81recs.sbk`, `nc81test.sbk`, and `nc81trnr.sbk`.

## Opening the book

`python3 -m opentoolbook path/to/book.tbk` opens a Tk window on the book's opening page. `enterSystem` runs, then `enterApplication`, then `enterBook`, each when a handler in the book or in `sysBooks` answers it. No other handler runs at startup because of its name: a book with only `openSession` or `initialize*` handlers runs none of them. Those handlers run on the OpenScript interpreter, which calls a `get` handler in the book or in a book in `sysBooks` and passes `forward` up the path. A `go to page` they run is the page.

`openSession` returns 0 when `__studentRecords` has not been set. `if it is 1` does not run, so `gotoPageList` does not run. `gotoPageList` says `go to page(pagename) of book(bookname)`. Those names are not quoted. The list is filled by the session DLL, which is not called. A resumed session is not the page the window opens.

When the startup handlers do not name a page, the opening page is the first page in the page list at book `+0x10`. That page's `enterPage` runs the same way. On `P0` of `9e954d01.tbk` the reader branch is `go to page "P0" of book getLogoBook()`. `getLogoBook` in `nc81base.sbk` sets the book to `nida81.tbk`, then to `logo81.tbk` when that file is found, otherwise to `mrj81.tbk` when that file is found. `fileExists32` is answered by the shelf, not a DLL. The quoted name is found by the same search as the report: the lesson directory, its parent, then `--home`. The window opens on `P0` of that book. `otb-line-rect.tbk` has no such handlers. Its one stored page is the opening page, and that page id is empty.

A book with no startup page and no stored page is an error. The error names the book. A handler that does not return a book name is an error. The error names the handler and the page. A book file the search does not find is an error. The error names that file and the page.

`python3 -m opentoolbook path/to/book.tbk --report` prints the record count, the follow-up reads, the files the book names, and the startup call names. It does not open a window. `--report path/to/book.tbk` prints the same report. `--home` with a book and without `--report` opens the book and searches that install. It does not print the install list. `--home` without a book still prints the install folder.

`python3 -m opentoolbook --show P300 path/to/book.tbk` opens a Tk window on the page id in the command. It does not follow those startup handlers to the book's opening page. The paint and the OpenScript that window runs are the sections above. The page walk also finds class `0x11`, and the window does not paint it. It paints class `0x13` as an angled line, class `0xD` as its bounds, class `0x15` as its stored bitmap, and class `0x19` as its picture. Class `0x12` pies are on that walk and are not painted. Class `0x17` hotwords are on that walk under their field and are not painted a second time.

## User properties

A `__` name is a system variable the lesson and the four system books declare, such as `system string __studentFirst` in `getFirst` of `nc81recs.sbk`. The reader keeps those names in one in-memory store. A name is case-insensitive. A value lives for the process and nothing is written to a student-record file. A name that was never set reads as nothing, and nothing is `false` or 0 in a condition. Startup, the window, and every page's `enterPage` share the same store. On `9e954d01.tbk` startup leaves `__import` at `false`, because `enterApplication` assigns it. `getFirst` returns `__studentFirst` from the store. When that name is set to `Ada`, the display list for `P10` shows `Hello Ada, this lesson is about:` with the same `Arial` run at offset 0. Empty or unset `__studentFirst` still shows `Hello Student, this lesson is about:`. `__studentRecords` and `openSession` do not change.

## Lesson tests

`python3 -m unittest discover -s tests` passes with no lesson on disk. Every test that reads Logic Families takes the path from `OPENTOOLBOOK_TBK` through `tests/lesson.py` `logic_families_path`, which is that file only when its name is `9e954d01.tbk` regardless of case. When the variable is unset, names no file, or names another book such as `nida81.tbk`, those tests skip instead of erroring. `lesson_path` still returns any existing path the variable names. Nothing from the lesson, `nida81.tbk`, or the `nc81*.sbk` books is checked in. A test that opens a companion opens it only through `companion`, which is `find_file` over `search_roots` of the lesson: the lesson directory, then its parent, case-insensitive, the same shelf `open_book` uses. No lesson test builds `path.with_name("nc81….sbk")` or `path.with_name("nida81.tbk")`. A disc copy with `NC81RECS.SBK` and `NC81TEST.SBK` in upper case beside the lesson and `NIDA81.TBK` one directory up passes the same tests as a flat lower-case copy: `companion` returns those paths and their bytes. When the shelf has no such file, `companion` returns the path beside the lesson, so the test's own `is_file` check fails or skips as before. A test that builds a `Navigator` on the logo book and follows a name back to the lesson passes `lesson=`, the same shelf the window keeps, because on a disc copy the lesson is in `Lessons/` below the logo book and not on the logo book's own shelf. A file name a test compares is compared in lower case.

## Books-folder smoke

`OPENTOOLBOOK_BOOKS` may name a directory of `.tbk` files. When it is set to an existing directory, `tests/test_books_smoke.py` opens every `.tbk` in that folder (not in subfolders), runs that book's startup through `opening_page`, and paints the opening page with `show_page`. Any exception fails that book. When the variable is unset or names no directory, the smoke test skips. A synthetic folder of the Instructor fixtures opens and paints without error.

## Statement walker

There is no statement walker. Startup, `enterPage`, every click, and `send_message` run on the OpenScript interpreter; `walk.py` is gone. The interpreter's own `if`, `else`, `end if`, `break`, `return` and `conditions` are the control flow. A handler that links a DLL still returns without running in `send_message`.

## Logo page click

`P0` of `nida81.tbk` has no button. The page paints the background, field `Page#`, field `Copyright`, and one unnamed field. Its only handler is the page's own `buttonClick`: `system lastbook`, `system nextpage`, `go to page (nextpage) of book(lastbook)`. It has no `enterPage`; the book `enterPage` sets `page#` to `P0`. A click that hits no button, or a button with no `buttonClick`, goes to the page's `buttonClick`. So the way off logo `P0` is a click anywhere on the page.

`go to page (name) of book(name)` reads those two system variables. When a handler this runner executed assigned both a string, the window opens that page of that book, with the book found by the click search. A page id matches regardless of case. With `--show P0` no handler has assigned them, so the click stays on `P0`. The page the click opens is whatever `nextpage` and `lastbook` hold; the logo page quotes none.

## Back to the lesson from the logo book

`P0` of `9e954d01.tbk` runs `lastbook = name of this book` and `nextpage = "p10"` in its `enterPage`, before `go to page "P0" of book getLogoBook()`. Startup runs that handler, so `lastbook` is `9e954d01.tbk` and `nextpage` is `p10`. The system variables startup assigned stay on the window. A click on logo `P0` of `nida81.tbk` then runs `go to page (nextpage) of book(lastbook)` and opens `P10` of `9e954d01.tbk`, found with the lesson's shelf. With `nida81.tbk` and the system books in `--home` and the lesson in another folder, the bare command opens `P0` of `nida81.tbk`, and one click on that page lands on `P10` of the lesson.

## Cross-book fixtures

A page whose byte at `+0x30` has low bits 0 stores its script inline. The word at `+0x2A` is a near pointer into the page's segment. At that pointer is a skip word, that many bytes, a count word, and that many bytes that expand to the source. The block's end word, at the pointer minus 4, is the pointer plus 2, the skip, 2, the count, and 1 or 2 more bytes. That holds on all 18 inline page scripts in `9e954d01.tbk` and the one in `nida81.tbk`, and the class word at the pointer minus 2 is 0 on all 19. A byte below `0x80` expands to itself and a 0 byte ends the handler.

`tests/fixtures/otb_cross_a.tbk` and `tests/fixtures/otb_cross_b.tbk` are `otb-line-rect.tbk` with one change each, written by `tests/crossbook.py`. B's empty page id at `+6` is `P0`. A's page has an inline `enterPage` with skip 0 and plain characters: `go to page "P0" of book "otb_cross_b.tbk"`. Its segment record is copied to the end of the file with that block appended, and the leaf entry names the new position and length. `opening_page` on A opens `P0` of B. B is found by the shelf, so it may sit beside A or in A's parent, in any case. With no B, the error names `otb_cross_b.tbk` and `P0`. The display list, the page records, and the record count are the line-rect book's. The names use `_` because the report reads a file name as letters, digits, and `_`. ToolBook has not opened these two books.

## `it`

`it` is the value of the last `get`. `get name()` stores what that handler returns. `get 1`, `get "text"`, `get true`, and `get` of a name the handler already assigned store that value. Another `get` replaces it. `if it is 1` and `if it = 1` compare against that value. A quoted value compares without case. `it` that was never set is 0. `openSession` returns 0 when `__studentRecords` is unset, so `if it is 1` in `enterSystem` does not run and `gotoPageList` does not run. After `get` of an expression the reader cannot evaluate, `it` is unset again.

## Name of this page and this book

`name of this page` is the page id. `name of this book` is the book's file name, such as `9e954d01.tbk`. The interpreter answers both. The book `enterPage` of `9e954d01.tbk` says `set text of field "page#" of parent of this page to name of this page`, so after the window enters `P300` field `Page#` reads `P300` from that expression; the stored text is `P100`. No page id is special-cased.

## Send to the system books

`sysBooks` is a list of book names, first item first. `sysBooks` reads as those names joined by commas. `sysBooks = "a.sbk,b.sbk"` replaces the list. `push "name" onto sysBooks` puts that name first, and a name already in the list moves to the front. `put "name" after sysBooks` appends; `put "name" before sysBooks` inserts at the front. `pop sysBooks` removes the first name into `it` (or into the name after `into`). `clear sysBooks` empties the list. Names are compared without case. `"name" is not in sysBooks` and `"name" is in sysBooks` are decided from that list. Handler lookup is the open book, then each `sysBooks` book in order, and the first book that has the name wins. A pushed book is found with the same search as the book report. A name the search does not find stays in the list and answers no handler; the handler chain and `--report` book list omit that name. On Logic Families, startup leaves `tb80anm.sbk` in `sysBooks` from the class table even when that file is not beside the lesson, and the chain then has five system books instead of six. When a script adds a book, that book's own `enterSystemBook` runs if it has one; when a script removes a book, that book's `leaveSystemBook` runs if it has one. A synthetic helper that logs on enter and leave records `enter leave` across a push then a pop. Startup seeds `sysBooks` from `TB80.INI` `startupSysBooks` when that file is found (see below), then appends the book's bound system books that the list still lacks, then runs the book's own handlers. With no INI and no bound names the list starts empty and only the open book's handlers answer. No system book is named by the reader itself, and no handler of a book the open book merely mentions is in the chain.

`enterSystem` of `9e954d01.tbk` pushes `tb80r.sbk`, then `nc81base.sbk` and runs `get initializebase(cmdLine)`, then `nc81test.sbk` and `initializetest()`, `nc81recs.sbk` and `initializerecs()`, and `nc81trnr.sbk` and `initializetrnr()`, each under `if "x" is not in sysBooks`. Each `get` finds its handler because the push before it put that book in the chain. The four `initialize*` handlers run in full on the interpreter, as the section "OpenScript interpreter" says; the reader keeps no copy of them. The window still opens on `P0` of `nida81.tbk`.

## Window title

The window title is the book file name, a dash, and the page id, such as `nida81.tbk - P0`. It changes on every navigation, including a book switch. The bare command on `9e954d01.tbk` opens with `nida81.tbk - P0`. `Next` from `P300` of the lesson shows `9e954d01.tbk - P400`, and `Selection1` from `P300` shows `nida81.tbk - P310`. A window opened without a book file shows the page id alone.

## Viewer history

The window keeps the stack of book and page it has shown, apart from the stored page list. A click that changes the page pushes the page that was on screen. The window's own `Viewer back` control, above the page, pops that stack and shows that page of that book. It is a viewer control, not a book button. A book button that says `send previous` still opens the previous page in the stored list. On `9e954d01.tbk`, `Next` from `P300` opens `P400`, and `Viewer back` returns to `P300`. `Selection1` from `P300` opens `P310` of `nida81.tbk`, whose stored previous page is `P0`, and `Viewer back` returns to `P300` of the lesson. With nothing shown before, `Viewer back` beeps and the page stays.

## Menu button

The `Menu` button on `P450`, `P1001`, `P2001`, `P10003`, `P10004`, and `P10410` of `9e954d01.tbk` runs `get gotoMenuPage()`, on the interpreter. `gotoMenuPage` in `nc81base.sbk` sets `menupage = getMenuPage()`, calls `setupMenuPage(menupage, __lessonMode)`, and runs `go to page(menupage)`. `getMenuPage` sets `menupage` to `"P900"` and `__quizDisableMenuKey` to 0. Then its `conditions` block on `__lessonMode` runs one `when`: for 0, when `__quizAssessment` is 0, `__quizDisableMenuKey` becomes 1 and `menupage` becomes `"P10001"`; for 1, when `__quizPreTest` is 0, the same with `"P10002"`. A page the book does not have becomes `"P900"`. Startup runs `initializeBase` and leaves `__lessonMode` 2, so `Menu` on `P450` opens `P900`. `setupMenuPage` sets selection colors and enabled flags on the menu page.

## Quiz setup from the menu groups

Group `selection1` on `P10001`, `P10002`, `P10003`, and `P10004` of `9e954d01.tbk` runs on the interpreter. When `__quizHelp` is 1 it asks `You are already in the quiz review!` and breaks. Otherwise it runs `error = setupQuizEx(type, 2, "P10301", "P10302", "P10303")`, where type is `Assessment`, `Pre-Test`, `Post-Test`, or `Quiz`, so `__quizType` is 0, 1, 2, or 3. `__quizPages` holds `P10301`, `P10302`, and `P10303`, `__quizObjectiveCount` is 2, `__quizIndex` is 1, `__quizStartPage` is the page number, `__quizAttempts` goes up by one, and `__quizPass` is 1. When `__quizMaxAttempts` is not 0 and the attempts pass it, `setupQuizEx` returns 1, the group asks `You have already attempted the quiz the maximum number of times!  Contact your instructor.` and the page stays. Otherwise the group builds the pool and runs `gotoNextQuestionEx`, which opens the first question, `P10210` with `random` at its lowest value.

## Question pool

The quiz menu group runs `get clearpool()`, then `addObjectiveToPool(1, 110, 119, 6)` and `addObjectiveToPool(2, 120, 129, 4)`, then `if setuppool() = -1`. The reader runs those three handlers from `nc81test.sbk` in that order, with the same steps. `clearPool` sets elements 1 through 10 of `__poolCount` to 0 and of `__poolQuestions` to empty. `addObjectiveToPool(1, 110, 119, 6)` stores `110,111,…,119` at element 1 of `__poolQuestions` and 6 at element 1 of `__poolCount`. `setupPool` hands every objective whose count is not 0 to `addQuestionsFromPool`. That sets `__quizIndex` to 0, picks that many different positions in the comma list with `addToRandomSetX`, and appends the question numbers at those positions to `__quizNumbers`, counting `__quizCount` up. One objective `(1, 110, 119, 6)` gives six different numbers, each from 110 to 119. On `P10001` the pool is ten numbers: six from 110 to 119, then four from 120 to 129. `random(n)` is a whole number from 1 to `n`, drawn from a generator the caller seeds, so one seed always gives the same pool. `getNextQuestion` returns the next stored question number and -1 after the last. It returns a question number, not a page id. The `__lessonMode = 6` branch of `setupPool` is not taken, because `__lessonMode` comes from `NIDAREC.INI` through a DLL and stays unset. Opening a question page is item 42.

## Next question page

`gotoNextQuestionEx` in `nc81test.sbk` opens a question page on a running pass, on the interpreter. `setupQuizEx` sets `__quizPass` to 1. On pass 1, 2, or 3 it calls `getNextQuestion`, and on pass 2 it skips numbers that already have a response. It then steps `i` from `__quizStartPage` to `pageCount of this book` and opens the first page whose `questionNo` is that number, after `setupQuizPage(i)`. On `9e954d01.tbk` the twenty pages `P10210` through `P10229` hold question numbers 110 through 129. After the last question, pass 1 opens element 3, 1, or 2 of `__quizPages` by `__quizMode` 0, 1, or 2; startup leaves `__quizMode` 0, so pass 1 ends on `P10303`. With no quiz running, `__quizPass` is null and no branch names a page, so the page stays.

## Correct mark

The rectangle `Correct` on a question page is shown by one line in `setupQuizPage` of `nc81test.sbk`: `set visible of rectangle("correct") of page iPage to true`. That line runs at the author level, and at the reader level under `when __quizPass = 4 or __quizPass = 5` and `when __quizPass = 8`. Under `when __quizPass = 1`, `= 2`, and `= 3` it is set to false. The display list leaves `Correct` off until a script sets it visible. Pass 8 is set only by `initializeBase` when the command line has `/Quester` and at least six words, so a reader opening the lesson does not reach it.

## Letter response and score

`answer of this page` is the page's stored `Answer` property, the value `quiz.questions` already returns. The response and score lines a running quiz reaches are the first block of `gotoNextQuestionEx` in `nc81test.sbk`, which `handleQuizClick` calls for `OK` and `Next`: `if __quizPass <= 3 and __quizIndex > 0 then`, `response = getQuizResponse()`, `score = 0`, `if response = answer of this page then score = 100`, then `get storeQuestionResponse(testNo of this page, questionNo of this page, response, score)`. `getQuizResponse` returns the last of `ansiToChar(96 + i)`, `i` from 1 to `__quizMaxResponse` (5), whose button is checked, so the response is a lower-case letter. OpenScript compares strings without case, so `c` matches `Answer` `C`. A checked state is what a script set, and otherwise the stored checked bit. `storeQuestionResponse` writes element `__quizIndex` of `__quizAttempted` (1), `__quizTestNo`, `__quizQuestionNo`, `__quizResponse`, and `__quizScore`. These handlers run on the interpreter, and each array is one `__` name holding an array. With no `__quizPass` or `__quizIndex` set, the block stores nothing. The section "Quiz on the interpreter" has the clicks on `P10210`. Shared script 102 has the same `response = answer of this page` and `score = 100` lines, but it reads `text of field "response"`, and no click on these pages reaches it. `storeQuestionSkipped` and `getQuizScore` are item 40.

## Skipped questions and the quiz score

With no letter checked, the first block of `gotoNextQuestionEx` calls `storeQuestionSkipped(testNo of this page, questionNo of this page)`. That handler writes only `__quizTestNo` and `__quizQuestionNo` at `__quizIndex`. Its `__quizAttempted` line is commented out, and it writes no response or score. `OK` with `__quizPass` in `1,2` and no letter checked does not reach that block, because `handleQuizClick` beeps and returns 0 first. `Next` does reach it. `getQuizScore` in `nc81test.sbk` steps `i` from 1 to `__quizCount`, adds `__quizScore[i]`, and returns `score div count`, or 0 when the count is 0. An element nothing stored adds 0. The responses are stored at `__quizIndex`, not appended, so a second store at the same index replaces the first. On the interpreter, scores 100 and 0 with `__quizCount` 2 give 50, and scores 100 and 100 with a count of 3 give 66.

## Shared script 103 on a quiz click

Shared script 103's `buttonClick` is one line, `get handleQuizClick(target)`, the same line as the `Test` background's `buttonClick` on `P10210` through `P10229`. A click on a question page that no object script takes reaches that background handler, which runs `handleQuizClick` from `nc81test.sbk` on the interpreter, as the section "Quiz on the interpreter" says. With no quiz running (`__quizPass` null), `OK` and `Next` there reach `gotoNextQuestionEx` with no branch that names a page, so the page stays. Which object links a page to resource 103 is not settled. The word `0x0068` (104) after the record of each of the twenty quiz pages is one candidate in FINDINGS. Resources 100 and 101 are not run, because no click reaches them.

## buttonDown and buttonUp

`handler_sites` finds 19 `buttonDown` and 19 `buttonUp` handlers on `9e954d01.tbk`, all in inline scripts of class `0xA` fields, and none in `nc81base.sbk`, `nc81recs.sbk`, `nc81test.sbk`, or `nc81trnr.sbk`. Each is the field of a menu choice, such as `Selection1` on `P300`, `selection 2`, `Selection T`, and `Exit` on `P900`, and `selection1` and `Selection2` on `P10001`. Each `buttonDown` is `if isObject(button "X") then set invert of button "X" to true`, and each `buttonUp` sets it to `false`, where `X` is the button behind that field. The window sends `buttonDown` on mouse-down and `buttonUp` on mouse-up to the topmost named button or field under the pointer, when that object's inline script has the handler. While the button stays down, the window sends `buttonStillDown` to that object every 100 ms when its script has that handler, and cancels the timer on mouse-up or double-click. A synthetic `buttonStillDown` that goes to another page opens that page. A double-click sends `buttonDoubleClick` to that object and cancels the delayed single `buttonClick`. A synthetic `buttonDoubleClick` that goes to another page opens that page. `isObject` is true when the page shows an object of that kind and name. A `set invert of button` line draws that button's invert picture until a `false`; the invert stays in object state across a page change. Pressing on `Selection1` on `P300` draws bitmap 153 on button `selection1` and leaves the page where it is. Letting go draws the up picture again, then the `buttonClick` runs on mouse-up as before. A `buttonUp` handler runs the same lines a `buttonClick` does, so a fixture `buttonUp` with `go to page "P3"` opens `P3`. When it opens another page, no `buttonClick` follows. An object with neither handler keeps the stored invert picture on press.

## Clicks on the interpreter

A click sends `buttonClick` on the OpenScript interpreter. The message goes to the clicked object, then each group that holds it, innermost first, then the page, the page's background, the book, and each `sysBooks` book in order, until a handler takes it. `forward` passes it one step up, and `target` is the clicked object for every handler on the way. A click that hits no object starts at the page. A hotword is clicked by its name; its class `0x17` script is the object script. `buttonDown` and `buttonUp` go the same way. `set invert of button`, field text, `hide`, `show`, `visible`, `request` and `beep` are the page the handlers see. `isObject` is true when the book has that page, or the page shows an object of that kind and name or id; otherwise it is false. `hide`, `show` and `set visible` reach an object by name or by `id`; an object with no name is kept under its id. The old line runner (`run_handler`, `follow_click`, `page_click`) is gone; a click has one runner.

On `P300` of `9e954d01.tbk`, button `selection1` has no script; it sits in group `Selection1`, whose `buttonClick` opens `P310` of `nida81.tbk`. On `P10002`, the same click runs `setupQuizEx` from `nc81test.sbk`, which stores `__quizPages` as the array `P10301`, `P10302`, `P10303` with `__quizPass` 1 and `__quizType` 1. The reader's own copy of that setup is no longer called. With the props startup leaves (`__lessonMode` 2), `Menu` on `P450` runs `gotoMenuPage` and opens `P900`; with `__lessonMode` 0 and `__quizAssessment` 0 it opens `P10001` and sets `__quizDisableMenuKey` to 1.


## Quiz on the interpreter

A quiz runs from the book's own scripts on the interpreter. The reader has no quiz path of its own. On `9e954d01.tbk` with the startup props and `sysBooks`, `selection1` on `P10002` runs `setupQuizEx`, `clearPool`, `addObjectiveToPool` twice, `setupPool` and `gotoNextQuestionEx` from `nc81test.sbk`. With `random` at its lowest value, `__quizNumbers` is `110` to `115` then `120` to `123`, and the click opens `P10210` (question 110) with `__quizPass` 1 and `__quizIndex` 1. A letter runs `manageQuizButtons`: `A` is checked, and then `b` checks `B` and unchecks `A`. `C` then `OK` stores response `c`, score 100 (the page's `Answer` is `C`) and question 110 at index 1, and opens `P10211`. `OK` with no letter beeps and stays. On pass 1 `setupQuizPage` disables the background's `Next` and `Back`, so they get no click, and fills its fields: `Index` reads `Question 1.` and `PageText` reads `Testing`. After `OK`, `Index` reads `Question 2.`. The checked states are kept by page; `back` to `P10210` shows `A` still checked.

What the scripts read is the object model the click host answers: a page's user properties (`answer`, `questionNo`, `testNo`, and the rest; a missing one is null), `pageCount of this book`, `pageNumber of` a page, `page i` by number in `go to` and property reads, `checked` and `enabled` of a button (a click's state, else the stored bit), `object of` and `parent of` the target, and `isObject` of an object on another page. An array argument to a parameter declared `by reference` is shared with the caller; any other array argument is a copy. `flushMessageQueue` as a statement, and `flushMessageQueue()` as a function, are no-ops that return: this reader has no queued messages to drain. A synthetic handler that calls both continues and reads `it` as empty from the function.

## Object state

A property a script sets on an object stays set while the book is open, as ToolBook keeps it in the open book. The window keeps `text`, `checked`, `enabled`, `visible`, and `invert` by book, then by owner, then by object kind and name. The owner is the page for a page object and the page's background for a background object, so a background field a script writes shows on every page of that background. `field "x" of parent of page n` is a field of page n's background. A property no script set is the stored one. A button whose `enabled` is false, stored or set, gets no `buttonClick`; a disabled button with a disabled picture draws it. `invert` from `buttonDown` and `buttonUp` stays in that object state across a page change: on `9e954d01.tbk`, `buttonDown` on `Selection1` of `P300` leaves `invert` true for button `selection1` on `P300`, `Next` opens `P400` with an empty on-screen invert map, and Viewer back to `P300` draws the invert picture again.

## Book and page scripts in type 10 resources

The book's own script is a type 10 resource when the low two bits of the byte at `+0x26` of the book record are 2; the word at `+0x24` is that resource id plus 1. In `9e954d01.tbk` the word is 377, so the book script is resource 376 (`enterSystem`, `enterApplication`, `author`, `reader`, `enterBook`, `enterPage`, `keyUp`). In `nida81.tbk` it is 166, resource 165. The Instructor 8.1 books store 0 there and have no book script. A page or background whose byte at `+0x30` has low bits 2 keeps its script the same way: the word at `+0x2A` is the resource id plus 1. On `9e954d01.tbk` those are `P10301`, `P10302`, and `P10303`, resources 372 to 374. The book's handler map is the book script only; page scripts are read with their page. Before this, every type 10 resource went into the book's handlers, first one first, so the end-of-test page `enterPage` stood in for the book's. `button_clicks` now finds 252 `buttonClick` handlers in `9e954d01.tbk`: 249 inline and 3 in those page resources.

## DLL string buffers

A `STRING` argument to a linked DLL function is the variable's buffer: what the function writes there comes back into the variable after the call. The reader answers `GetPrivateProfileStringA(section, key, default, buffer, size, file)` with the INI value the shelf finds, else the default, cut to `size - 1` characters, written into the buffer argument; the function returns its length. `getStudentInfo` in `nc81recs.sbk` sets `__studentFirst` to `"First"` and 19 spaces, then calls it with default `"Student"` and size 21. With no `NIDAREC.INI` on the shelf, `__studentFirst` is `Student` after startup, and `__studentId` is `ID`.

## Windows and ToolBook DLL shims

A `linkDLL` / `linkDLL32` function the host knows is answered from a shim table, not by loading a DLL. `kernel32` `GetTickCount` returns milliseconds since process start (wrapped to 32 bits). `GetVersion` returns `0xC0000A04` (Win98-style). `user32` `GetSystemMetrics(0)` and `(1)` return 1024 and 768; other metric indexes return 0. Named `user32` UI calls such as `MessageBoxA` and `SendMessageA` return 0 and do nothing. `fileExists32` and the `GetPrivateProfile*` / `WritePrivateProfileStringA` answers stay as above. A linked function this table does not name returns empty and the handler continues; a synthetic `missingFn()` then `"ok"` returns `ok`. NIDA DLLs are not in the table.

## Page messages

A message goes to the object it names and up from there: an object, the groups that hold it, its page, the page's background, the book, then each `sysBooks` book. A message to a background starts at the background, and a message to the book starts at the book. `forward` follows the same path. A `go to page` inside the book sends `leavePage` to the old page, `leaveBackground` to the old background and `enterBackground` to the new one when the two pages have different backgrounds, then `enterPage` to the new page, all while the handler that ran `go` is still running. A page name matches regardless of case. A go to a page of another book opens that book and sends `enterBook`, `enterBackground`, then `enterPage` to it. On `9e954d01.tbk`, `Next` on `P300` (background `Solid`) sends `leavePage`, `leaveBackground`, `enterBackground`, `enterPage` and opens `P400` (background `Text`); the book's `enterPage` writes `P400` into field `page#` of that background.

## Opening messages

Opening a book sends `enterSystem`, `enterApplication` and `enterBook` to the book, then `enterWindow` to the book, `enterBackground` to the opening page's background, `enterPage` to the opening page, and `firstIdle` to the page, the order a TB80RTM trace of `nida81.tbk` shows. Each goes up the page, background, book, `sysBooks` path. A synthetic book whose handlers append each of those seven names to a log records exactly `enterSystem enterApplication enterBook enterWindow enterBackground enterPage firstIdle`. The opening page is the page a startup handler went to, else the first stored page. A go to another book during any of them stops the sequence; that book gets `enterBook`, `enterBackground` and `enterPage`. Properties the handlers set go to the window. After the window paints, it sends `idle` to the page on screen whenever Tk is idle, then again every 200 ms while the window stays up. `Navigator.idle` is that send. A synthetic `idle` handler that does `go to page "P2"` opens that page. A page whose id is empty is still a page. A fixture with no system-book script and no INI still opens with `sysBooks` empty, so it gets no `tb80r.sbk` handlers.

`shortFileName(path)` returns the path unchanged, since the books on hand name 8.3 files. `tb80r.sbk`'s `enterPage` uses it to clear duplicate `sysBooks` entries; with no answer, every entry looked like the same name and all but one were cleared. On `9e954d01.tbk` the window opens on `P0` of `nida81.tbk` with `sysBooks` `nc81trnr.sbk`, `nc81recs.sbk`, `nc81test.sbk`, `nc81base.sbk`, `tb80anm.sbk`, `tb80r.sbk`. All 43 Instructor 8.1 books open.

`sysTime` is milliseconds since local midnight. `sysDate` is today's local date as text, shaped by `sysDateFormat` (default `m/d/yy`). The format tokens are `yyyy`, `yy`, `mm`, `m`, `dd`, and `d`. Setting `sysDateFormat` changes later `sysDate` reads. A synthetic handler that sets `yyyy-mm-dd` then `m/d/yy` returns both spellings for a fixed clock.

A printable key in the window sends `keyChar` to the page with that one character as the argument, then up the page, background, book, `sysBooks` path. Right, Left, Return, and Escape keep their own bindings and do not send `keyChar`. A synthetic `keyChar` that goes to another page when the character is `a` opens that page for `a` and stays for `b`.

`ask` is the same statement as `request`: the prompt and optional `with` buttons, the answer in `it`. A synthetic `ask "Leave?" with "Yes" or "No"` that goes to another page when `it` is `Yes` opens that page for `Yes` and stays for `No`.

## TB80.INI

The reader looks for `TB80.INI` in the book's folder, then `<windows>\asym\runtime`, then `<windows>`. `--windows` names that Windows directory. `--ini PATH` uses that file and skips the search. The keys read are `startupSysBooks` (comma list, lower-cased), `startupBook`, `startupWidth`, and `startupHeight`. A missing file or key keeps the default: no startup system books, no startup book, and no startup size. `otb-line-rect.tbk` with no INI still opens with `sysBooks` empty. An INI next to a copy of that fixture that says `startupSysBooks=seed.sbk,Other.SBK` leaves `sysBooks` as `seed.sbk`, `other.sbk` before any bound names, and `--report` prints those names. Bound names already listed by the INI are not repeated.

## The display list runs no script

`show_page` is the page as the book stores it, with the properties scripts set laid over it: field text, `visible`, `checked` and `enabled`. It does not run `enterPage`; that runs on the interpreter when the window enters a page, and its writes are in the object state. `--show` enters the page it opens with `enterBackground` and `enterPage`. A user property of this book, such as `__nidaVersion of this book`, is the value the book stores until a script sets it, so `PINFO` and `PQINFO` show `Version: 2.003.0001`. The old `enterPage` field walker (`enter_fields`, `concatenate`, `getFirst` in Python, the `sysLevel` author branch) is gone.
