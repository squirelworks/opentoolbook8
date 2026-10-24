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

On open, those filenames are looked up in this order: the book's directory, `--home`, `--home/courses`, then `--home/Nida98/Lessons`. The match ignores case. The report prints the path that was found. The book still opens when `minstb32.dll`, `93954302.tbk`, or `93954d01.tbk` is absent.

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

## Button picture

A class `0x09` button is 43 bytes. The word at `+0x28` is a near pointer to a graphics block. When that word is not 0, the block starts with `0x0202` and the unaligned word at byte `0x15` of the block is the picture id. That id is a type-1 resource id plus one. The reader returns it. On `9e954d01.tbk` the four huge-table bitmaps are named there by their stored ids.

## Button bounds

A class `0x09` button is 43 bytes. The four signed words at `+0x0F` are a rectangle. The reader returns that rectangle. On `9e954d01.tbk` the Next button on `P300` is (8907, 6210, 9342, 6630) and the A button on `P10210` is (2430, 1635, 2715, 1920). The same read holds for every such button in `nida81.tbk`.

## Button checked picture

A class `0x09` button's word at `+0x28` names a graphics block that starts with `0x0202`. The unaligned word at byte `0x4b` of that block is the checked picture. It is a type-1 resource id plus one, or 0 when there is no checked picture. The reader returns it. On `9e954d01.tbk` the A button on `P10210` is 118, the stored id of bitmap 117. The MenuFrame button on `P300` is 0. The same word is a stored id or 0 on every such block in `nida81.tbk`.

## Button invert picture

A class `0x09` button's graphics block starts with `0x0202`. The unaligned word at byte `0x27` of that block is the invert picture. It is a type-1 resource id plus one, or 0 when there is no invert picture. The reader returns it. On `9e954d01.tbk` the A button on `P10210` is 117, the stored id of bitmap 116. The MenuFrame button on `P300` is 0. The same word is a stored id or 0 on every such block in `nida81.tbk`. The border byte at the button record's `+0x27` is a different field.

## Button disabled picture

A class `0x09` button's graphics block starts with `0x0202`. The unaligned word at byte `0x39` of that block is the disabled picture. It is a type-1 resource id plus one, or 0 when there is no disabled picture. The reader returns it. On `9e954d01.tbk` the A button on `P10301` is 128, the stored id of bitmap 127. The MenuFrame button on `P300` is 0. Every such block in `nida81.tbk` is 0.

## Button border

A class `0x09` button is 43 bytes. The byte at `+0x27` is the border. The reader returns that byte. On `9e954d01.tbk` the Next button on `P300` is 1 and the A button on `P10210` is 9. The export calls 1 `none`, 9 `radioButton3d`, and 7 `pushButton`. In `nida81.tbk` every such button is 1 or 7.

## Button enabled

A class `0x09` button is 43 bytes. Bit 0 of the byte at `+0x26` is enabled. The reader returns that bit. On `9e954d01.tbk` the Next button on `P300` is 1 and the A button on `P10302` is 0. The export calls 1 `true` and 0 `false`. The same bit is 1 on 93 buttons in `nida81.tbk` and 0 on 63.

## Button checked

A class `0x09` button is 43 bytes. Bit 4 of the byte at `+0x26` is checked. The reader returns that bit. On `9e954d01.tbk` the B button on `P10211` is 1 and the A button on `P10210` is 0. The export calls 1 `true` and 0 `false`. Every such button in `nida81.tbk` is 0. The checked picture at byte `0x4b` of the graphics block is a different field.

## Page ids

Page ids come from the walk that already finds P0: the page list at book `+0x10`, then the C string at each page record `+6`. That walk includes P0 and P430.

## Background

A class 4 background is the record named by the far reference at page `+0x47`. The class word immediately before that record is 4. The pattern byte is at `+0x4B`. Red, green, and blue are at `+0x5B`, `+0x5C`, and `+0x5D`. On `9e954d01.tbk`, Logo and Definition both use those offsets. Logo is pattern `0xFE` and color 0, 0, 191. Definition is pattern `0xFE` and color 128, 128, 128.

## Quiz question

A quiz question page has fields named `Stem`, `A`, `B`, `C`, and `D`. The trailer slot before each of `Answer`, `QuestionNo`, `TestNo`, `SourceQuestionNo`, `SourceTestNo`, and `sourcepage` is a value: the word `0x0009`, a length, and that many characters. The reader returns those six values. On `9e954d01.tbk` the twenty pages `P10210` through `P10229` use that shape. Their test and question numbers are the same numbers as the `InfoText` field on page `PQINFO`. `SourceQuestionNo` is that question number, `SourceTestNo` is that test number, and `sourcepage` is the page id.

## Polyline

A class `0x13` record is 55 bytes. The count is the word at `+0x2D` and the near pointer at `+0x2F` names the stored points, four bytes each. The four signed words at `+0x25` are the minimum x, the minimum y, the maximum x, and the maximum y of those points. The reader returns the stored points. The same read holds for every such record in `9e954d01.tbk` and in `nida81.tbk`.

## Arc

Class `0x11` object 80 on page P1140 of `9e954d01.tbk` stores two points, the signed pairs at `+0x25` and `+0x29`: (1866, 5065) and (1815, 4620). Those are the points in the record. The arc is not filled.

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

## Class `0x0B`

A class `0x0B` record is 49 bytes. The four signed words at `+0x0F` are a rectangle. It is the union of the rectangles at `+0x0F` of the objects whose word at `+0x04` names the record. The reader returns that rectangle. On `9e954d01.tbk` the two records in `FINDINGS.md` are (2557, 105, 6322, 1005) and (3202, 360, 6142, 765). The same read holds for every such record in `nida81.tbk`.

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

## Open handlers

A handler whose body is in an `.sbk` is a column-0 line `to get` or `to handle` in that book's type 10 source. The reader returns the handler name and the book. It does not call the handler, and it does not read a DLL. `nc81base.sbk` holds 46 `to get` handlers, from `initializeBase` through `getCurrentPath`. `nc81recs.sbk` holds 17 `to get` handlers, from `initializeRecs` through `GetVar`. `nc81test.sbk` holds 89 `to get` handlers and `to handle timerNotify`. `nc81trnr.sbk` holds 63 `to get` handlers, plus `to handle linkMemFunctions32` and `to handle unlinkMemFunctions32`. None of the four books has a `to set` line.

## Handler split

Each of those handler lines splits into a name, an argument list, and the start of the body. The name is the word after `to get` or `to handle`. The argument list is the rest of that line, with the spaces around it removed. Nothing left is no arguments. The body starts on the next line. The reader returns that split. It does not call the handler. `initializeBase` in `nc81base.sbk` takes `cmdLine`, and `specifyMenuColors` takes `color1, color2`. `writeResponse` in `nc81recs.sbk` takes `int testno, int questionno, string response, int score`. `timerNotify` in `nc81test.sbk` takes `timerId`, `clearRandomSetX` takes `int numbers[] by reference`, and `getNextQuestion` takes no arguments. `linkMemFunctions32` in `nc81trnr.sbk` takes no arguments, and `sendFaults130` takes `string faults`. `getExternalValue` is followed by a blank line, and that blank line is where its body starts.
