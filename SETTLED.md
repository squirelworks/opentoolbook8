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

`initializebase`, `initializerecs`, `initializetest`, and `initializetrnr` are the four `nc81*.sbk` books.

- `initializebase` is `nc81base.sbk`
- `initializerecs` is `nc81recs.sbk`
- `initializetest` is `nc81test.sbk`
- `initializetrnr` is `nc81trnr.sbk`

The other four calls are `nida81.tbk`.

- `enterapplication` is `nida81.tbk`
- `entersystem` is `nida81.tbk`
- `gotopagelist` is `nida81.tbk`
- `opensession` is `nida81.tbk`

## Resolve on open

On open, those filenames are looked up in this order: the book's directory, the parent of that directory, `--home`, `--home/courses`, then `--home/Nida98/Lessons`. The match ignores case. The report prints the path that was found. The book still opens when `minstb32.dll`, `93954302.tbk`, or `93954d01.tbk` is absent. `nida81.tbk`, `nc81base.sbk`, `nc81recs.sbk`, `nc81test.sbk`, and `nc81trnr.sbk` in the parent directory are that path. `93954302.tbk` beside the lesson stays the file in the book's directory. A name that is not in those directories stays missing. The lookup does not read any other directory.

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

The book record stores the page width at `+0x20` and the page height at `+0x1E`. Both are signed words. On `otb-line-rect.tbk` and `otb-pie.tbk` they are 9000 and 6000. On `9e954d01.tbk` and `nida81.tbk` they are 9360 and 6624. On `nc81base.sbk`, `nc81recs.sbk`, `nc81test.sbk`, and `nc81trnr.sbk` they are 9345 and 6630. One page unit is 1/20 point. One point is 96/72 pixels at 96 dpi. The fit scale multiplies that pixel size once.

## Page window

`python3 -m opentoolbook --show P300 path/to/9e954d01.tbk` opens that page. The display list is the same list without a screen. The background is painted from the class 4 reader. Pattern 254 is a solid fill of the color at `+0x5B`. Pattern 253 paints no fill. A rectangle, ellipse, or polygon uses the color at `+0x1B` as its fill and the color at `+0x17` as its stroke. A line is the two endpoints at `+0x26`, in the stroke color. A polygon is the stored points. A field paints its text, its bounds, and the style-run faces. A button paints its bounds and the picture at byte `0x15` of the graphics block. The picture at byte `0x4B` is drawn only when bit 4 of button `+0x26` is set. A button whose enabled bit, bit 0 of `+0x26`, is 0 draws the picture at byte `0x39` when that word is not 0, and keeps the up picture when it is 0. On `P10210` the A button is not checked, so the window uses picture 116 and not picture 118. After a click on A it uses picture 118. A field whose bounds contain a non-text shape is painted under that shape. A label whose bounds contain no shape is painted in front of a later shape or button that contains the label. On `P300` the selection text is in front of `MenuFrame`. On `P400` the part number is in front of the chip rectangle. On `P410` the label stored behind the chip rectangle is painted in front of it. On `P1110` the field that contains a line is painted under that line, and the label that contains nothing is painted in front of the ellipse.

An inline type-1 picture stores a `BM` file eight bytes after `01 02 01 00`. On `9e954d01.tbk` that marker is at byte 18 of all 63 inline pictures. On `nida81.tbk` it is at byte 18 of 21 pictures and at byte 36 of the other 2. A huge-table picture keeps the `BM` file after the 8-byte prefix.

## Opening a catalog lesson

`python3 -m opentoolbook --catalog path/to/courses.xml --open 9E954D01` opens one lesson the catalog lists. `--catalog` may also be the folder that holds `courses.xml`. The lesson file is the id in lower case plus `.tbk`, `9e954d01.tbk`. It is found with the shelf rules: the catalog's folder, its parent, `--home`, `--home/courses`, and `--home/Nida98/Lessons`, regardless of case. That file then opens the way the bare command opens a book, on its opening page. The id match ignores case. An id the catalog does not list prints `9E954D01 is not a lesson in the catalog` and exits 2. A lesson file the search does not find prints `9e954d01.tbk was not found; lesson 9E954D01 does not open` and exits 2, and no window opens. `--open` without `--catalog`, or with a book, `--show`, or `--report`, prints the usage and exits 2. Without `--open` the catalog printout is unchanged.

## Window resize

Resizing the window refits the page. The canvas fills the window. A `Configure` event with a new canvas size computes the fit scale again from the stored page size and that view: 9360 by 6624 on the lesson, 9000 by 6000 on the fixtures. The paint list is unchanged and only the scale moves. A 600 by 400 view of `otb-line-rect.tbk` is scale 1, and a 300 by 400 view of the same page is scale 0.5. There are no scroll bars.

## No enterButton or leaveButton

`handler_sites` finds every `to handle NAME` line in a book's expanded scripts: inline object scripts, type 10 scripts, and type 19 shared scripts. Handler names are stored as keyword tokens, so a byte search of the file does not see them. On `9e954d01.tbk`, `nida81.tbk`, `nc81base.sbk`, `nc81recs.sbk`, `nc81test.sbk`, and `nc81trnr.sbk` there is no `enterButton` handler and no `leaveButton` handler. The window dispatches neither message. The hover handlers the books do have are `mouseEnter` and `mouseLeave`, 19 of each on `9e954d01.tbk` and 3 of each on `nida81.tbk`, all in inline scripts of class `0xA` fields such as `Selection1` on `P300`, and none in the system books. Those are hover, and the window does not dispatch them either.

## Window close

The window's close button ends the Tk loop. `open_page` returns, and `python3 -m opentoolbook --show PAGE book.tbk` exits 0. Before this, closing the window raised `TclError` from the destroyed root. A click whose handler raises `ValueError` or `OSError` prints that error's one line on stderr and the window stays up on the same page. Any other exception keeps its traceback and the window also stays up. The smoke test opens `otb-line-rect.tbk` and presses close. It is skipped with a message when `DISPLAY` is unset or the Python has no `tkinter`.

## Page photos

Drawing a page deletes the Tk images of the page drawn before it, then makes the new page's images. The window holds the photos of one page at a time. On `9e954d01.tbk` P300 has five button pictures and P400 has four, and P300, Next to P400, Back to P300, and so on keeps the window at five and four images, whether or not something else still holds a reference to an old photo. There is no bitmap cache across pages or books.

## Export DLL in the window

The book's PE export directory names `MINSTB32.dll`. When the shelf search the open uses does not find a file of that name, ignoring case, the window shows one line under the page: `MINSTB32.dll named, not shipped`. The line is shown once, for `--show` and for the bare command. It is not loaded, it does not stop the open, and the page still paints. On `9e954d01.tbk` with no DLL on disk the bare command still opens `P0` of `nida81.tbk`. A `MINSTB32.DLL` that the search finds removes the line.

## One missing-book sentence

Opening a book and clicking a button raise the same error when the shelf search does not find a book a handler quotes. It is one sentence: the file, then the page of that book, `nida81.tbk was not found; P310 of that book does not open`. On `9e954d01.tbk` with no `nida81.tbk` on the shelf, the bare command prints `nida81.tbk was not found; P0 of that book does not open` on stderr and exits 2, and `Selection1` on `P300` prints `nida81.tbk was not found; P310 of that book does not open` and the window stays on `P300`. `--show` on a book file that does not exist prints that sentence with the `--show` page and exits 2. `--show` on a page id the book does not store prints `no page` and that id and exits 2. Neither prints a traceback. When a click printed an error during the window's life, closing the window exits 1. Otherwise it exits 0.

## nida71.tbk stays missing

`nida81.tbk` quotes `go to page "P12060" of book "nida71.tbk"` in the `Retry` button of pages `P12000`, `P12001`, `P12002`, and `P12003`. The file is not shipped and is not vendored. The shelf search does not find it, so a click that reaches that line is the missing-book error: `nida71.tbk was not found; P12060 of that book does not open`. The window prints it and stays on the page. That holds for `Retry` on all four pages. The runner skips the `if ntries = 4 then` branch it cannot decide, as the Statement walker section says, so the first quoted `go to page` before `break` is the `nida71.tbk` line on each page. `verifyswitches130a`, whose result picks the branch, has no body in the lesson or the four system books, so the branch ToolBook takes is not known.

## A missing lesson names its disc

When `--catalog ... --open` does not find the lesson file, the same shelf search looks for `CAILT.DAT`, regardless of case. When it finds the table, the error adds the disc codes the table maps for that lesson id, with the most specific pattern winning as in `--cailt`. Against a table whose lines are `9E954??* DIE??V03` and `9E954D0?* DIE-EXACT`, lesson `9E954D01` prints `9e954d01.tbk was not found; lesson 9E954D01 does not open; CAILT.DAT puts it on disc DIE-EXACT` and exits 2. Two codes print as `discs` with a comma. A table with no line for the lesson adds `CAILT.DAT names no disc for it`. With no table on the shelf the error is unchanged. No window opens, and no zip is fetched.

## Arrow keys

The Right key runs the click of the button named `Next` on the page, and the Left key the click of the button named `Back`. The name match ignores case and takes buttons from the page and from its background. It is the same path as clicking that button, including `enterPage` on the page it lands on. On `P300` of `9e954d01.tbk` Right opens `P400` and Left opens `P100`. On `P400` Left opens `P300`, the page its `Back` handler quotes. On the question page `P10210` Right is the `Test` background's `Next` and opens `P10211`. A page with neither button ignores the keys. Escape closes the window. The book's own key handlers are not run.

## Keys the book script binds

Search of the expanded scripts (inline object scripts, type 10, and type 19) of `9e954d01.tbk`, `nida81.tbk`, and the four system books for `keyDown`, `keyUp`, `keyChar`, and `__quizDisableMenuKey`:

- `9e954d01.tbk` type 10 script 376 holds `enterSystem`, so it is the book script. Its `to handle keyup key` quotes `keyf1`, `keyf2`, `keyf4`, `keyf5` through `keyf9`, `keyf11`, `keyf12`, and `keyEnter` in a `conditions` block when `__quizHelp` is 0, and `keyEnter` and `keyF5` when it is not. `keyf10` is commented out. `keyF4` is guarded by `__quizDisableMenuKey = 0`.
- Type 10 scripts 372, 373, and 374 each have an empty `to handle keyUp` and a `to handle keyDown key` that calls `handleQuizKey` for `keyF7`. A page record whose mode byte at `+0x30` has low bits 2 names its own type 10 script by the word at `+0x2A`: `P10301` is 373 and `P10302` is 374 on the lesson, and `P12000`, `P12001`, and `P12002` are 159, 160, and 161 on `nida81.tbk`. `P10303` names 375 and `P12003` names 162, and neither book stores that resource. No stored page or background names 372.
- `nida81.tbk` type 10 script 165 holds `enterApplication` and a `to handle keyup key` with the same F-key and `keyEnter` branches. Its `keyf4` branch says `go to page "p900" of book lastbook`.
- Type 19 shared script 100 has `to handle keyUp key` that sends `buttonClick` to button `Accept` on `keyEnter` when `getQuizMode()` is 0. Shared script 101 has `keyChar`. Shared script 103 has an empty `keyUp`, a `keyDown` for `keyF5` and `keyF7`, and a `keyChar`, all calling `handleQuizKey`.
- `nc81base.sbk` sets `__quizDisableMenuKey` to 0 and to 1. None of the four system books has a key handler. Inline object scripts send `keyup keyF2` and `keyup keyF5` to the page, and define no key handler.

The window binds one of those keys. Enter is `keyEnter` in the book's `keyUp`: on the lesson that branch is `send buttonClick to button "next"` inside `if isObject(button("Next"))`, so Enter runs the click of the page's `Next` button, and on `P300` it opens `P400`. On `nida81.tbk` the same branch adds `visible` and `enabled` checks that the reader does not evaluate. A page whose own type 10 script has a `keyUp` handles the key there: `P10301` and `P10302` have an empty one, so Enter does nothing on them. The other quoted keys are not bound, because their branches are `request`, `open viewer`, `send exit`, or `get` calls such as `specialFunctions` that the reader does not run. `keyDown`, `keyChar`, and the shared-script key handlers are not bound, because no stored object is known to own scripts 100, 101, or 103.

## Enter page greeting

On `P10` of `9e954d01.tbk` the `enterPage` handler sets the text of field `First` to `"Hello" && getFirst() & ", this lesson is about:"` when `sysLevel` is `reader`, and to `"Hello, this lesson is about:"` otherwise. The field's stored name is `first`. A missing `sysLevel` is `reader`. `getFirst` in `nc81recs.sbk` returns `__studentFirst`. The reader strips the ends of that variable, and returns `Student` when it is empty. `&&` is one operator and is recognized before `&`. `&&` concatenates with a space. `&` concatenates. The display list for `P10` shows `Hello Student, this lesson is about:`. The one style run at offset 0, face `Arial`, covered the stored string and covers the new string. The field `Text` stays `LOGIC FAMILIES`.

`get setSection("Intro")` calls `setSection` in `nc81base.sbk`. That handler writes through `kernel32.dll`. The reader does not call the DLL, and the greeting does not use the return. `forward` has no handler body in the lesson or the four system books. The reader does not invent one.

On `PINFO` and `PQINFO` the handler sets field `version` to `"Version: " & __nidaVersion of this book`. That value still contains `__` and `of this book`, so it is not written. The stored line `Version: 2.003.0001` stays.

## Class `0x15` paint object

A class `0x15` record is 89 bytes. It is a bitmap, not a container. The four signed words at `+0x0F` are the bounds. The byte at `+0x26` is the pattern, 254 on all five records in `9e954d01.tbk` and the one in `nida81.tbk`. The dword at `+0x29` is the pixel byte count. The dword at `+0x2D` is the stored byte count when the pixels are packed, and 0 when they are stored as is. The word at `+0x4D` is a 1-based row of the huge table at header `+0x104`. That row's first dword is the stored byte count and its third dword is the file offset of the bytes. The word at `+0x4F` is the palette color count. The word at `+0x51` is a near pointer to a 40-byte bitmap info header, and that many palette entries follow it. All six records hold each of those reads.

Packed bytes are blocks. Each block is a word that counts its codes, then those codes. A code below `0xF6` repeats the next byte the code plus three times. A code of `0xF6` or more copies the next `code - 0xF5` bytes. A block does not start on the last byte of a 64 KB span of the packed bytes; that byte is skipped. The four packed records in `9e954d01.tbk` use two streams, each one block, of 2605 and 2147 codes, and each unpacks to exactly the pixel byte count. Those bytes equal the pixels of `PaintObject16.bmp` and `PaintObject20.bmp` in the TBKX export of that book, which calls the class `PaintObject` and names the same bounds.

The window draws the bitmap at the left and top of the bounds, at one bitmap pixel per screen pixel times the fit scale. On `9e954d01.tbk`, `P450` draws object 2 at (0, 0, 9360, 6630), 624 by 442, 24 bits. The `Test` background draws object 16 at the top, 627 by 24, and object 20 at the bottom, 627 by 28, both 8 bits with a palette. On `nida81.tbk`, `P0` draws object 4, 554 by 390, 24 bits. A record whose bytes do not unpack to the pixel byte count is not painted.

## Class `0x19` picture

A class `0x19` record is 89 bytes. It is a picture: a Windows metafile with bounds. It is not a filled shape, so the window does not use the class `0x8` fill rule for it. The four signed words at `+0x0F` are the bounds. The byte at `+0x26` is 254. The dword at `+0x29` is the metafile byte count. The dword at `+0x2D` is the stored byte count when the metafile is packed, and 0 when it is stored as is. The word at `+0x4D` is a 1-based row of the huge table at header `+0x104`, and that row's third dword is the file offset of the stored bytes. All 39 records in `nida81.tbk` hold those reads. 33 are packed and 6 are not, and every one gives exactly its metafile byte count.

Packed bytes are blocks. Each block is a word that counts its codes, then those codes. A code below `0xF6` repeats the next byte the code plus three times. A code of `0xF6` or more copies the next `code - 0xF5` bytes. A block does not start on the last byte of a 64 KB span of the packed bytes; that byte is skipped. Three of the 33 packed pictures need that skip.

Every metafile plays `SaveDC`, `SetBkMode`, `SetWindowOrg`, `SetWindowExt`, `SetStretchBltMode`, `IntersectClipRect`, `SetPolyFillMode`, and `SetROP2`. Then it plays one or two `StretchDIB` records with 8-bit DIBs, then `SetROP2`, `RestoreDC`, and the end record. Two pictures play one `StretchDIB` with `SRCCOPY`. The other 37 play `SRCPAINT`, then `SRCAND` over the same rectangle. On every pixel of those 37, either the first DIB is black and the second is white, and the page shows through, or the result does not depend on the page and is the first AND the second. The reader draws the DIBs into the window extent, clipped, and returns that picture with a mask. The window stretches the picture to the bounds. Nine of the 39 bounds are not 15 units per window pixel, so a picture is resized with its bounds. On `P310` object 36 is a 372 by 397 picture in (1080, 945, 6645, 6900). On `P370` object 38 is under the group at `0x9C` and is drawn. A metafile with any other record list is not painted.

## Quiz page click

The background a page names is painted under the page. Its fields and buttons use the same readers as the page. Class `0x15` paint objects on that background are painted, as the section "Class `0x15` paint object" says. On the `Test` background the buttons are `Back`, `OK`, `Help`, `Skip`, and `Next`, and each has an up picture. The book `enterPage` sets field `page#` to the name of the page when that field is on the background. On `P300` that field reads `P300`.

`P10210` is a question page. Its letter buttons keep the up picture. The checked picture stays off the page while no letter is checked. The rectangle named `Correct` sits on the answer and its pattern is 253. It is not painted. No quiz pass has shown it, and a letter is not drawn as the correct answer. Shared script 103 and the `Test` background both call `handleQuizClick`. In `nc81test.sbk` that handler, when `__quizPass` is in `1,2` and `getQuizResponse()` is empty, runs `beep(1)` and `return 0`. The page stays. A checked letter on that pass does not beep, and it does not change the page: `gotoNextQuestionEx` calls `getNextQuestion`, and that returns `getNextRandomX` of the pool. The pool is not a page id.

A list-opened question page has no quiz running. `OK`, `Next`, and `Skip` go to the next page in the stored page list. `Back` goes to the previous page. On `9e954d01.tbk` those pages around `P10210` are `P10004` and `P10211`. A letter click stays. `__quizPass` 8 is the same next and previous pages: `gotoNextQuestionEx` runs `send next`, and `gotoPreviousQuestionEx` runs `send previous`. `Skip` on that pass, when a letter is checked, runs `beep(1)` and a request, so the page stays.

## Button click

A `buttonClick` handler is the text the reader already returns. A quoted `go to page` opens that page. A quoted `of book` names that file. The window finds it with the same search as opening a book: the book's directory, its parent, `--home`, `--home/courses`, and `--home/Nida98/Lessons`, regardless of case. `--show` passes `--home` to the window too. A file that search does not find is an error that names the file and the page, for example `nida81.tbk was not found; P310 of that book does not open`. The window prints that line on stderr and stays on the page. With `nida81.tbk` only in the lesson's parent directory, `Selection1` on `P300` opens `P310` of that file. After the window changes books, the search still starts from the book the user passed on the command line: that book's directory and its parent, then the directory of the book on screen and its parent, then the `--home` folders. When the bare command opens `9e954d01.tbk` and the window lands on `P0` of `nida81.tbk` from `--home/courses`, a click from that page still finds a file that sits beside the lesson, and `--home` stays on the window. `break` stops the handler, so the `send next` after it does not run. `send next` and `send previous` are the next and previous pages in the stored page list. On `P300` of `9e954d01.tbk`, `Next` opens `P400`, `Back` opens `P100`, and `Selection1` opens `P310` of `nida81.tbk`. `go to page nextpage of book lastbook` has no quotes. It reads those two system variables, and the page stays when a handler this runner executed has not assigned them a string (see "Next page of last book"). A button with no handler does not change the page, except the quiz buttons whose background calls `handleQuizClick`.

## Version strings

Resource type 16 in the PE resource directory is a version resource. The reader returns `FileDescription`, `InternalName`, `OriginalFilename`, `ProductVersion`, and `CompanyName` from that resource. On `otb-line-rect.tbk`, `nida81.tbk`, and `9e954d01.tbk` those strings are `Toolbook II`, `TB80`, `TB80.EXE`, `8.10.131`, and `Click2learn, Inc.`. The same five strings are in `nc81base.sbk`, `nc81recs.sbk`, `nc81test.sbk`, and `nc81trnr.sbk`.

## Opening the book

`python3 -m opentoolbook path/to/book.tbk` opens a Tk window on the book's opening page. `enterSystem` runs, then `enterApplication`, when the book defines them. A `get` call in a branch the reader takes runs that handler when its body is in the book or in a companion the report's search finds. A quoted `go to page` in a taken branch is the page. A missing `sysLevel` is `reader`, so `sysLevel = "reader"` is the branch that runs. `forward` is not executed. A `linkDLL` line is not called.

`openSession` returns 0 when `__studentRecords` has not been set. `if it is 1` does not run, so `gotoPageList` does not run. `gotoPageList` says `go to page(pagename) of book(bookname)`. Those names are not quoted. The list is filled by the session DLL, which is not called. A resumed session is not the page the window opens.

When the startup handlers do not name a page, the opening page is the first page in the page list at book `+0x10`. That page's `enterPage` is read the same way. On `P0` of `9e954d01.tbk` the reader branch is `go to page "P0" of book getLogoBook()`. `getLogoBook` in `nc81base.sbk` sets the book to `nida81.tbk`, then to `logo81.tbk` when that file is found, otherwise to `mrj81.tbk` when that file is found. `fileExists32` is not called. The quoted name is found by the same search as the report: the lesson directory, its parent, then `--home`, `--home/courses`, and `--home/Nida98/Lessons`. The window opens on `P0` of that book. `otb-line-rect.tbk` has no such handlers. Its one stored page is the opening page, and that page id is empty.

A book with no startup page and no stored page is an error. The error names the book. A handler that does not return a book name is an error. The error names the handler and the page. A book file the search does not find is an error. The error names that file and the page.

`python3 -m opentoolbook path/to/book.tbk --report` prints the record count, the follow-up reads, the files the book names, and the startup call names. It does not open a window. `--report path/to/book.tbk` prints the same report. `--home` with a book and without `--report` opens the book and searches that install. It does not print the install list. `--home` without a book still prints the install folder.

`python3 -m opentoolbook --show P300 path/to/book.tbk` opens a Tk window on the page id in the command. It does not follow those startup handlers to the book's opening page. The paint and the OpenScript that window runs are the sections above. The page walk also finds class `0x11`, and the window does not paint it. It paints class `0x13` as an angled line, class `0xD` as its bounds, class `0x15` as its stored bitmap, and class `0x19` as its picture. Class `0x12` pies are outside that walk and are not painted. Class `0x17` hotwords are on that walk under their field and are not painted a second time.

## User properties

A `__` name is a system variable the lesson and the four system books declare, such as `system string __studentFirst` in `getFirst` of `nc81recs.sbk`. The reader keeps those names in one in-memory store. A name is case-insensitive. A value lives for the process and nothing is written to a student-record file. A name that was never set reads as nothing, and nothing is `false` or 0 in a condition. Startup, the window, and every page's `enterPage` share the same store. On `9e954d01.tbk` startup leaves `__import` at `false`, because `enterApplication` assigns it. `getFirst` returns `__studentFirst` from the store. When that name is set to `Ada`, the display list for `P10` shows `Hello Ada, this lesson is about:` with the same `Arial` run at offset 0. Empty or unset `__studentFirst` still shows `Hello Student, this lesson is about:`. `__studentRecords` and `openSession` do not change.

## Lesson tests

`python3 -m unittest discover -s tests` passes with no lesson on disk. Every test that reads Logic Families takes the path from `OPENTOOLBOOK_TBK` and skips when that variable is unset or names no file. Nothing from the lesson, `nida81.tbk`, or the `nc81*.sbk` books is checked in. A test reads a companion with `tests/lesson.py` `companion`, which is `find_file` over `search_roots` of the lesson: the lesson directory, then its parent, case-insensitive, the same shelf `open_book` uses. A disc copy with `NC81RECS.SBK` in upper case beside the lesson and `NIDA81.TBK` one directory up passes the same tests as a flat lower-case copy. When the shelf has no such file, `companion` returns the path beside the lesson, so the test's own `is_file` check fails or skips as before. A test that builds a `Navigator` on the logo book and follows a name back to the lesson passes `lesson=`, the same shelf the window keeps, because on a disc copy the lesson is in `Lessons/` below the logo book and not on the logo book's own shelf. A file name a test compares is compared in lower case.

## Statement walker

Opening the book, `enterPage`, and `buttonClick` walk a handler with one loop, in `walk.py`. `if`, `else`, `end if`, `break`, and `return` are that loop. `end` and `end if` both close an `if`, so `if error = 1 then` closed by `end` in `selection1` of `P10001` through `P10004` is one block. An `if` line with no `then`, such as `if sysLevel = reader` in `Next` of `P1270`, is a block. An `if` line with `then` and a statement after it is one line, not a block. A missing `sysLevel` is `reader` in all three. A condition the caller cannot decide runs neither branch, in all three. `break` and `return` stop the handler. A `linkDLL` block is not called. `forward` has no body. `end` at the top of a handler, such as `end buttonClick`, ends it.

A click used to read every line of both branches. It now skips a branch whose condition it cannot decide. `P300`, the opening page, and every `enterPage` field write on `9e954d01.tbk` and `nida81.tbk` are unchanged. Three clicks change: `Retry` on `P12000`, `P12002`, and `P12003` of `nida81.tbk` read `go to page "p12050"` inside `if ntries = 4 then`. That branch is not taken now, so each click names `P12060` of `nida71.tbk`, the quoted page under `when it is 60` before that `if`. `conditions` and `when` are not statements yet.

## Logo page click

`P0` of `nida81.tbk` has no button. The page paints the background, field `Page#`, field `Copyright`, and one unnamed field. Its only handler is the page's own `buttonClick`: `system lastbook`, `system nextpage`, `go to page (nextpage) of book(lastbook)`. It has no `enterPage`; the book `enterPage` sets `page#` to `P0`. A click that hits no button, or a button with no `buttonClick`, goes to the page's `buttonClick`. So the way off logo `P0` is a click anywhere on the page.

`go to page (name) of book(name)` reads those two system variables. When a handler this runner executed assigned both a string, the window opens that page of that book, with the book found by the click search. A page id matches regardless of case. With `--show P0` no handler has assigned them, so the click stays on `P0`. The page the click opens is whatever `nextpage` and `lastbook` hold; the logo page quotes none.

## Back to the lesson from the logo book

`P0` of `9e954d01.tbk` runs `lastbook = name of this book` and `nextpage = "p10"` in its `enterPage`, before `go to page "P0" of book getLogoBook()`. Startup runs that handler, so `lastbook` is `9e954d01.tbk` and `nextpage` is `p10`. The system variables startup assigned stay on the window. A click on logo `P0` of `nida81.tbk` then runs `go to page (nextpage) of book(lastbook)` and opens `P10` of `9e954d01.tbk`, found with the lesson's shelf. With `nida81.tbk` and the system books in `--home/courses` and the lesson in another folder, the bare command opens `P0` of `nida81.tbk`, and one click on that page lands on `P10` of the lesson.

## Cross-book fixtures

A page whose byte at `+0x30` has low bits 0 stores its script inline. The word at `+0x2A` is a near pointer into the page's segment. At that pointer is a skip word, that many bytes, a count word, and that many bytes that expand to the source. The block's end word, at the pointer minus 4, is the pointer plus 2, the skip, 2, the count, and 1 or 2 more bytes. That holds on all 18 inline page scripts in `9e954d01.tbk` and the one in `nida81.tbk`, and the class word at the pointer minus 2 is 0 on all 19. A byte below `0x80` expands to itself and a 0 byte ends the handler.

`tests/fixtures/otb_cross_a.tbk` and `tests/fixtures/otb_cross_b.tbk` are `otb-line-rect.tbk` with one change each, written by `tests/crossbook.py`. B's empty page id at `+6` is `P0`. A's page has an inline `enterPage` with skip 0 and plain characters: `go to page "P0" of book "otb_cross_b.tbk"`. Its segment record is copied to the end of the file with that block appended, and the leaf entry names the new position and length. `opening_page` on A opens `P0` of B. B is found by the shelf, so it may sit beside A or in A's parent, in any case. With no B, the error names `otb_cross_b.tbk` and `P0`. The display list, the page records, and the record count are the line-rect book's. The names use `_` because the report reads a file name as letters, digits, and `_`. ToolBook has not opened these two books.

## `it`

`it` is the value of the last `get`. `get name()` stores what that handler returns. `get 1`, `get "text"`, `get true`, and `get` of a name the handler already assigned store that value. Another `get` replaces it. `if it is 1` and `if it = 1` compare against that value. A quoted value compares without case. `it` that was never set is 0. `openSession` returns 0 when `__studentRecords` is unset, so `if it is 1` in `enterSystem` does not run and `gotoPageList` does not run. After `get` of an expression the reader cannot evaluate, `it` is unset again.

## Name of this page and this book

`name of this page` is the page id. `name of this book` is the book's file name, such as `9e954d01.tbk`. Startup, a startup `get` handler's `return`, and `enterPage` field text read both from one function in `walk.py`. `enterPage` on the display list does not know the file, so there `name of this book` stays the source text, as before. The book `enterPage` of `9e954d01.tbk` says `set text of field "page#" of parent of this page to name of this page`, so field `Page#` on `P300` reads `P300` from that expression. No page id is special-cased.

## Send to the system books

`send name` looks for that handler in the open book, then in `nc81base.sbk`, `nc81recs.sbk`, `nc81test.sbk`, and `nc81trnr.sbk`, in that order. The first book that has the name wins. The system books are found with the same search as the book report. On `9e954d01.tbk` no handler name is in more than one of the four system books. The lesson and `nida81.tbk` share `enterPage`, `keyUp`, `enterApplication`, `author`, and `enterBook`, and the open book's copy wins. A handler whose body has a `linkDLL` or `linkDLL32` line returns without running, so no DLL is called. 75 handlers in the lesson, `nida81.tbk`, and the four system books link a DLL this way, among them `initializeBase`, `openSession`, `setSection`, `setupQuizEx`, `initializeTest`, and `initializeTrnr`. Every other handler runs with the same statement walker as startup. `send getLogoBook` runs the handler in `nc81base.sbk` and returns `nida81.tbk`, or `logo81.tbk` / `mrj81.tbk` when the search finds that file, the same book the window opens. Startup builds its handler map in this order too. `get name()` is unchanged and still runs a handler that links a DLL without calling the DLL.


## fileExists32

`fileExists32("name")` is the shelf. It is 1 when the book report's search finds that name, ignoring case, and 0 when it does not: the book's directory, its parent, `--home`, `--home/courses`, then `--home/Nida98/Lessons`. `tbfile32.dll`, the library `initializeBase` links it from, is not called. The same function answers `fileExists32("x") = 1`, `fileExists32("x") <> 1`, a bare `if fileExists32("x")`, `found = fileExists32("x")`, and `get fileExists32("x")`, so `getLogoBook` and the search cannot disagree. A lesson folder with `nc81base.sbk` and `nida81.tbk` beside it, and neither `logo81.tbk` nor `mrj81.tbk`, opens `P0` of `nida81.tbk`. Add `mrj81.tbk` and the same lesson opens `P0` of `mrj81.tbk`. Add `logo81.tbk` and `getLogoBook` returns `logo81.tbk`.

## Next page of last book

A click handler line `name = "text"`, `name = name of this book`, or `name = name of this page` assigns that system variable, and the window keeps it. Another right-hand side assigns nothing. `go to page nextpage of book lastbook` and `go to page nextpage` read those variables the same way as the parenthesized form. `Selection1` on `P300` of `9e954d01.tbk` assigns `lastbook` = `9e954d01.tbk` and `nextpage` = `P300` before it opens `P310` of `nida81.tbk`. `Next` and `Back` on `P310` say `go to page (nextpage) of book(lastbook)`, and `Next` and `Back` on `P340` say `go to page nextpage of book lastbook`. Each opens `P300` of the lesson, found with the lesson's shelf. With nothing assigned, the click on `P340` stays.

## Request and beep

`beep`, `beep 1`, and `beep(1)` do nothing and return. `request "text"`, with or without `with "Yes" or "No"`, records that text and does not change the page. A click returns the requests in order and the number of beeps. The window rings the bell once for a click that beeps and shows each request in a message box, and the page stays unless the handler goes to another page. The `Skip` branch of `handleQuizClick` in `nc81test.sbk`, when `getQuizResponse()` is not empty, runs `beep(1)` and `request "Do you want to discard your answer?" with "Yes" or "No"`. The reader takes that text from the handler, not from a copy. On `__quizPass` 8 with a letter checked, `Skip` on `P10210` returns that request string, a beep, and `P10210`. The reader does not show a dialog. Nobody answers `Yes`, so the page stays. With no letter checked, `Skip` goes to the next page and returns no request.

## Enter page after a click

The page a click lands on runs its `enterPage` the way the opening page does, in its own book and after a book switch. Its field writes are in the display list, and the book `enterPage` that sets background field `page#` runs for that page. On `P300` that field reads `P300`. `Next` from `P300` opens `P400`, and `page#` reads `P400`. `Back` from `P100` opens `P10`, and field `First` reads `Hello Student, this lesson is about:`. `Selection1` from `P300` opens `P310` of `nida81.tbk`, and `page#` reads `P310`.

A quoted `go to page` in the landing page's `enterPage`, in a branch the reader takes, moves the window again, at most four times. The handlers it calls are the book's own and those of the books it names, found with the click search. Landing on `P0` of `9e954d01.tbk` runs `lastbook = name of this book`, `nextpage = "p10"`, and `go to page "P0" of book getLogoBook()`, so the window moves on to `P0` of `nida81.tbk`. `--show PAGE` still draws the page it is given and does not follow that page's `enterPage` move.

## Background enter page

The background's `enterBackground` and `enterPage` write fields with the same rules as the page's `enterPage`. The page's handler runs first, then the background's, then the book's, the order `forward` passes the message. A later write to the same field wins. Neither `9e954d01.tbk` nor `nida81.tbk` stores an `enterBackground`. The `Test` background of `P10210` through `P10229` has an `enterPage` that sets field `PageText` to the name of the page when `sysLevel` is `author`. A missing `sysLevel` is `reader`, so the window keeps the stored `Testing`. With `sysLevel` `author` the display list for `P10210` shows `P10210` in `PageText`, and `P10211` shows `P10211`. The other backgrounds' `enterPage` handlers call `clearPagelist` and `addToPageList` and write no field.
