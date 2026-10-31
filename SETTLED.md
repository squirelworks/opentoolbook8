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

## Book handlers

A handler whose body is in an `.sbk` is a column-0 line `to get` or `to handle` in that book's type 10 source. The reader returns the handler name and the book. It does not call the handler, and it does not read a DLL. `nc81base.sbk` holds 46 `to get` handlers, from `initializeBase` through `getCurrentPath`. `nc81recs.sbk` holds 17 `to get` handlers, from `initializeRecs` through `GetVar`. `nc81test.sbk` holds 89 `to get` handlers and `to handle timerNotify`. `nc81trnr.sbk` holds 63 `to get` handlers, plus `to handle linkMemFunctions32` and `to handle unlinkMemFunctions32`. None of the four books has a `to set` line.

## Handler split

Each of those handler lines splits into a name, an argument list, and the start of the body. The name is the word after `to get` or `to handle`. The argument list is the rest of that line, with the spaces around it removed. Nothing left is no arguments. The body starts on the next line. The reader returns that split. It does not call the handler. `initializeBase` in `nc81base.sbk` takes `cmdLine`, and `specifyMenuColors` takes `color1, color2`. `writeResponse` in `nc81recs.sbk` takes `int testno, int questionno, string response, int score`. `timerNotify` in `nc81test.sbk` takes `timerId`, `clearRandomSetX` takes `int numbers[] by reference`, and `getNextQuestion` takes no arguments. `linkMemFunctions32` in `nc81trnr.sbk` takes no arguments, and `sendFaults130` takes `string faults`. `getExternalValue` is followed by a blank line, and that blank line is where its body starts.

## Export module name

The bytes before the object store are a PE file. Data directory 0 is the export directory. The reader returns the C string its Name field points at. On `otb-line-rect.tbk` that string is `MINSTB32.dll` at file offset `0x258`, and the directory lists zero exports. `nida81.tbk` and `9e954d01.tbk` store the same name at that offset. `nida81.tbk` has no other `.dll` name.

## Page size

The book record stores the page width at `+0x20` and the page height at `+0x1E`. Both are signed words. On `otb-line-rect.tbk` and `otb-pie.tbk` they are 9000 and 6000. On `9e954d01.tbk` and `nida81.tbk` they are 9360 and 6624. On `nc81base.sbk`, `nc81recs.sbk`, `nc81test.sbk`, and `nc81trnr.sbk` they are 9345 and 6630. One page unit is 1/20 point. One point is 96/72 pixels at 96 dpi. The fit scale multiplies that pixel size once.

## Page window

`python3 -m opentoolbook --show P300 path/to/9e954d01.tbk` opens that page. The display list is the same list without a screen. The background is painted from the class 4 reader. Pattern 254 is a solid fill of the color at `+0x5B`. Pattern 253 paints no fill. A rectangle, ellipse, or polygon uses the color at `+0x1B` as its fill and the color at `+0x17` as its stroke. A line is the two endpoints at `+0x26`, in the stroke color. A polygon is the stored points. A field paints its text, its bounds, and the style-run faces. A button paints its bounds and the picture at byte `0x15` of the graphics block. The picture at byte `0x4B` is drawn only when bit 4 of button `+0x26` is set. On `P10210` the A button is not checked, so the window uses picture 116 and not picture 118. A field whose bounds contain a non-text shape is painted under that shape. A label whose bounds contain no shape is painted in front of a later shape or button that contains the label. On `P300` the selection text is in front of `MenuFrame`. On `P400` the part number is in front of the chip rectangle. On `P410` the label stored behind the chip rectangle is painted in front of it. On `P1110` the field that contains a line is painted under that line, and the label that contains nothing is painted in front of the ellipse.

An inline type-1 picture stores a `BM` file eight bytes after `01 02 01 00`. On `9e954d01.tbk` that marker is at byte 18 of all 63 inline pictures. On `nida81.tbk` it is at byte 18 of 21 pictures and at byte 36 of the other 2. A huge-table picture keeps the `BM` file after the 8-byte prefix.

## Enter page greeting

On `P10` of `9e954d01.tbk` the `enterPage` handler sets the text of field `First` to `"Hello" && getFirst() & ", this lesson is about:"` when `sysLevel` is `reader`, and to `"Hello, this lesson is about:"` otherwise. The field's stored name is `first`. A missing `sysLevel` is `reader`. `getFirst` in `nc81recs.sbk` returns `__studentFirst`. The reader strips the ends of that variable, and returns `Student` when it is empty. `&&` is one operator and is recognized before `&`. `&&` concatenates with a space. `&` concatenates. The display list for `P10` shows `Hello Student, this lesson is about:`. The one style run at offset 0, face `Arial`, covered the stored string and covers the new string. The field `Text` stays `LOGIC FAMILIES`.

`get setSection("Intro")` calls `setSection` in `nc81base.sbk`. That handler writes through `kernel32.dll`. The reader does not call the DLL, and the greeting does not use the return. `forward` has no handler body in the lesson or the four system books. The reader does not invent one.

On `PINFO` and `PQINFO` the handler sets field `version` to `"Version: " & __nidaVersion of this book`. That value still contains `__` and `of this book`, so it is not written. The stored line `Version: 2.003.0001` stays.

## Quiz page click

The background a page names is painted under the page. Its fields and buttons use the same readers as the page. Class `0x15` records on that background are not painted. On the `Test` background the buttons are `Back`, `OK`, `Help`, `Skip`, and `Next`, and each has an up picture. The book `enterPage` sets field `page#` to the name of the page when that field is on the background. On `P300` that field reads `P300`.

`P10210` is a question page. Its letter buttons keep the up picture. The checked picture stays off the page while no letter is checked. The rectangle named `Correct` sits on the answer and its pattern is 253. It is not painted. No quiz pass has shown it, and a letter is not drawn as the correct answer. Shared script 103 and the `Test` background both call `handleQuizClick`. In `nc81test.sbk` that handler, when `__quizPass` is in `1,2` and `getQuizResponse()` is empty, runs `beep(1)` and `return 0`. The page stays. A checked letter on that pass does not beep, and it does not change the page: `gotoNextQuestionEx` calls `getNextQuestion`, and that returns `getNextRandomX` of the pool. The pool is not a page id.

A list-opened question page has no quiz running. `OK`, `Next`, and `Skip` go to the next page in the stored page list. `Back` goes to the previous page. On `9e954d01.tbk` those pages around `P10210` are `P10004` and `P10211`. A letter click stays. `__quizPass` 8 is the same next and previous pages: `gotoNextQuestionEx` runs `send next`, and `gotoPreviousQuestionEx` runs `send previous`. `Skip` on that pass, when a letter is checked, runs `beep(1)` and a request, so the page stays.

## Button click

A `buttonClick` handler is the text the reader already returns. A quoted `go to page` opens that page. A quoted `of book` names that file. The window opens that filename from the directory of the book passed to `--show`. It does not search the parent, and it does not ignore case. `break` stops the handler, so the `send next` after it does not run. `send next` and `send previous` are the next and previous pages in the stored page list. On `P300` of `9e954d01.tbk`, `Next` opens `P400`, `Back` opens `P100`, and `Selection1` opens `P310` of `nida81.tbk`. `go to page nextpage of book lastbook` has no quotes, so it is not a page. A button with no handler does not change the page, except the quiz buttons whose background calls `handleQuizClick`.

## Version strings

Resource type 16 in the PE resource directory is a version resource. The reader returns `FileDescription`, `InternalName`, `OriginalFilename`, `ProductVersion`, and `CompanyName` from that resource. On `otb-line-rect.tbk`, `nida81.tbk`, and `9e954d01.tbk` those strings are `Toolbook II`, `TB80`, `TB80.EXE`, `8.10.131`, and `Click2learn, Inc.`. The same five strings are in `nc81base.sbk`, `nc81recs.sbk`, `nc81test.sbk`, and `nc81trnr.sbk`.

## Opening the book

`python3 -m opentoolbook path/to/book.tbk` opens a Tk window on the book's opening page. `enterSystem` runs, then `enterApplication`, when the book defines them. A `get` call in a branch the reader takes runs that handler when its body is in the book or in a companion the report's search finds. A quoted `go to page` in a taken branch is the page. A missing `sysLevel` is `reader`, so `sysLevel = "reader"` is the branch that runs. `forward` is not executed. A `linkDLL` line is not called.

`openSession` returns 0 when `__studentRecords` has not been set. `if it is 1` does not run, so `gotoPageList` does not run. `gotoPageList` says `go to page(pagename) of book(bookname)`. Those names are not quoted. The list is filled by the session DLL, which is not called. A resumed session is not the page the window opens.

When the startup handlers do not name a page, the opening page is the first page in the page list at book `+0x10`. That page's `enterPage` is read the same way. On `P0` of `9e954d01.tbk` the reader branch is `go to page "P0" of book getLogoBook()`. `getLogoBook` in `nc81base.sbk` sets the book to `nida81.tbk`, then to `logo81.tbk` when that file is found, otherwise to `mrj81.tbk` when that file is found. `fileExists32` is not called. The quoted name is found by the same search as the report: the lesson directory, its parent, then `--home`, `--home/courses`, and `--home/Nida98/Lessons`. The window opens on `P0` of that book. `otb-line-rect.tbk` has no such handlers. Its one stored page is the opening page, and that page id is empty.

A book with no startup page and no stored page is an error. The error names the book. A handler that does not return a book name is an error. The error names the handler and the page. A book file the search does not find is an error. The error names that file and the page.

`python3 -m opentoolbook path/to/book.tbk --report` prints the record count, the follow-up reads, the files the book names, and the startup call names. It does not open a window. `--report path/to/book.tbk` prints the same report. `--home` with a book and without `--report` opens the book and searches that install. It does not print the install list. `--home` without a book still prints the install folder.

`python3 -m opentoolbook --show P300 path/to/book.tbk` opens a Tk window on the page id in the command. It does not follow those startup handlers to the book's opening page. The paint and the OpenScript that window runs are the sections above. The page walk also finds classes `0xD`, `0x11`, `0x13`, `0x15`, and `0x19`, and the window does not paint those. Class `0x12` pies and class `0x17` records are outside that walk and are not painted.

## User properties

A `__` name is a system variable the lesson and the four system books declare, such as `system string __studentFirst` in `getFirst` of `nc81recs.sbk`. The reader keeps those names in one in-memory store. A name is case-insensitive. A value lives for the process and nothing is written to a student-record file. A name that was never set reads as nothing, and nothing is `false` or 0 in a condition. Startup, the window, and every page's `enterPage` share the same store. On `9e954d01.tbk` startup leaves `__import` at `false`, because `enterApplication` assigns it. `getFirst` returns `__studentFirst` from the store. When that name is set to `Ada`, the display list for `P10` shows `Hello Ada, this lesson is about:` with the same `Arial` run at offset 0. Empty or unset `__studentFirst` still shows `Hello Student, this lesson is about:`. `__studentRecords` and `openSession` do not change.

## Statement walker

Opening the book, `enterPage`, and `buttonClick` walk a handler with one loop, in `walk.py`. `if`, `else`, `end if`, `break`, and `return` are that loop. `end` and `end if` both close an `if`, so `if error = 1 then` closed by `end` in `selection1` of `P10001` through `P10004` is one block. An `if` line with no `then`, such as `if sysLevel = reader` in `Next` of `P1270`, is a block. An `if` line with `then` and a statement after it is one line, not a block. A missing `sysLevel` is `reader` in all three. A condition the caller cannot decide runs neither branch, in all three. `break` and `return` stop the handler. A `linkDLL` block is not called. `forward` has no body. `end` at the top of a handler, such as `end buttonClick`, ends it.

A click used to read every line of both branches. It now skips a branch whose condition it cannot decide. `P300`, the opening page, and every `enterPage` field write on `9e954d01.tbk` and `nida81.tbk` are unchanged. Three clicks change: `Retry` on `P12000`, `P12002`, and `P12003` of `nida81.tbk` read `go to page "p12050"` inside `if ntries = 4 then`. That branch is not taken now, so each click names `P12060` of `nida71.tbk`, the quoted page under `when it is 60` before that `if`. `conditions` and `when` are not statements yet.

## Send to the system books

`send name` looks for that handler in the open book, then in `nc81base.sbk`, `nc81recs.sbk`, `nc81test.sbk`, and `nc81trnr.sbk`, in that order. The first book that has the name wins. The system books are found with the same search as the book report. On `9e954d01.tbk` no handler name is in more than one of the four system books. The lesson and `nida81.tbk` share `enterPage`, `keyUp`, `enterApplication`, `author`, and `enterBook`, and the open book's copy wins. A handler whose body has a `linkDLL`, `linkDLL32`, or `unlinkDLL` line returns without running, so no DLL is called. 76 handlers in the lesson, `nida81.tbk`, and the four system books link or unlink a DLL this way, among them `initializeBase`, `openSession`, `setSection`, `setupQuizEx`, `initializeTest`, and `initializeTrnr`. Every other handler runs with the same statement walker as startup. `send getLogoBook` runs the handler in `nc81base.sbk` and returns `nida81.tbk`, or `logo81.tbk` / `mrj81.tbk` when the search finds that file, the same book the window opens. Startup builds its handler map in this order too. `get name()` is unchanged and still runs a handler that links a DLL without calling the DLL.


## initializeBase literals

`initializeBase(cmdLine)` in `nc81base.sbk` runs its literal assignments only. An assignment runs when its right side is a whole or decimal number, a quoted string, `true`, `false`, the `cmdLine` parameter, or a name the handler or the store already holds. A `__` name goes to the in-memory store, and any other name is local to the handler. Every other line is skipped, and the skip is named: `linkDLL tbfile32.dll`, `linkDLL32 kernel32.dll`, and `linkDLL32 user32.dll` by library, a call by the name it calls (`clearMenuFlags`, `specifyMenuColors`, `clearExperimentFlags`, `WritePrivateProfileStringA`, `GetPrivateProfileIntA`, `placeLesson`), `set saveOnClose of this book` and `set sysChangesDB` by property, and the `/Quester` `conditions` block under `if wordcount(__cmdline) >= 2` by its condition. `setSection` is not called. With an empty command line the store holds `__pageIndex` 0, `__pageListCleared` 0, `__quizDisableMenuKey` 0, and `__cmdLine` empty. `__lessonMode` comes from `GetPrivateProfileIntA` on `NIDAREC.INI`, so it stays unset, and `if __lessonMode = 5` and `= 6` run neither branch. `__nidaVersion` is not assigned there. `if sysLevel = reader` is taken. A condition on a value the handler holds is decided, and any other condition runs neither branch and is named. The walker skips a whole `conditions`, `step`, or `while` block when its caller asks, as this one does. Startup does not call this yet: `enterSystem` guards `get initializebase(cmdLine)` with `if "nc81base.sbk" is not in sysBooks`, and the reader does not decide `sysBooks`.

## initializeTrnr literals

`initializeTrnr` in `nc81trnr.sbk` runs the same way as `initializeBase`. The store gets `__experimentActive`, `__trainerAddress`, `__trainerAc1`, `__trainerDc1`, `__trainerAc2`, `__trainerDc2`, `__trainerSp3`, `__trainerDc3`, and `__trainerFilament` as 0, and `__trainerNlv` and `__trainerPlv` as 0.0. It skips `linkDLL32 kernel32.dll` and six `GetPrivateProfileIntA` calls, so `__trainerType`, `__trainerPort`, `__plcType`, `__plcPort`, `__205Type`, and `__205Port` stay unset.

A handler outside the four `initialize*` handlers runs only when it reaches no DLL and its body is only assignments. A handler reaches a DLL when it links or unlinks one, or calls a handler in the send chain that does. The skipped names are:

- `linkMemFunctions32` links `kernel32.dll`.
- `unlinkMemFunctions32` runs `unlinkDLL "kernel32.dll"`.
- `sendFaults130(string faults)` calls `sendFaultsTd2000`, which links a DLL.
- `getExternalValue(string exname)` in `nc81base.sbk` links `kernel32.dll` and calls `GetPrivateProfileStringA`. Its body starts on the blank line after the header, and that body is not only assignments.

`unlinkDLL` now counts as a DLL line for `send` too.
