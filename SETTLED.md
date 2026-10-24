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

## Polygon

A class `0x10` polygon is 53 bytes. The count is the word at `+0x30` and the near pointer at `+0x32` names the stored points, four bytes each. Every such point list in `9e954d01.tbk` lies inside the source rectangle at `+0x28`. The bounds are four words at `+0x0F`. The reader returns the stored points.

## Button bitmap

A button bitmap is an 8-byte prefix followed by a `BM` file in the huge table. The stored id is the resource id plus 1. Resource 155 of `9e954d01.tbk` is the prefix at file offset `0x50117`. The picture is 580 by 158, 8 bits per pixel.

## Huge-table bitmaps

`9e954d01.tbk` names four bitmaps in the huge table. Resource 148 is at `0x2577`, 581 by 157, 8 bits per pixel. Resource 150 is at `0x18ff7`, 580 by 387, 8 bits per pixel. Resource 155 stays at `0x50117`, 580 by 158, 8 bits per pixel. Resource 164 is at `0x1be627`, 580 by 158, 8 bits per pixel. That count is four.

## Button picture

A class `0x09` button is 43 bytes. The word at `+0x28` is a near pointer to a graphics block. When that word is not 0, the block starts with `0x0202` and the unaligned word at byte `0x15` of the block is the picture id. That id is a type-1 resource id plus one. The reader returns it. On `9e954d01.tbk` the four huge-table bitmaps are named there by their stored ids.

## Page ids

Page ids come from the walk that already finds P0: the page list at book `+0x10`, then the C string at each page record `+6`. That walk includes P0 and P430.

## Background

A class 4 background is the record named by the far reference at page `+0x47`. The class word immediately before that record is 4. The pattern byte is at `+0x4B`. Red, green, and blue are at `+0x5B`, `+0x5C`, and `+0x5D`. On `9e954d01.tbk`, Logo and Definition both use those offsets. Logo is pattern `0xFE` and color 0, 0, 191. Definition is pattern `0xFE` and color 128, 128, 128.

## Quiz question

A quiz question page has fields named `Stem`, `A`, `B`, `C`, and `D`. The trailer slot before each of `Answer`, `QuestionNo`, and `TestNo` is a value: the word `0x0009`, a length, and that many characters. On `9e954d01.tbk` the twenty pages `P10210` through `P10229` use that shape, and their test and question numbers are the same numbers as the `InfoText` field on page `PQINFO`.

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
