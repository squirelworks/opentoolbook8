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

A field is class `0xA`. Its text is word 1 of the block at record `+0x24`: a trailer handle, then a capacity word, a length word, and the characters. The copyright field on page P0 of `9e954d01.tbk` is read that way. The word at `+0x42` is not the text.

## Polygon

A class `0x10` polygon stores its count at `+0x30` and a near pointer to the points at `+0x32`. The source rectangle is four words at `+0x28` and the bounds are four words at `+0x0F`. A point maps as `x' = (x − src.left) × dstW / srcW + dst.left`, and the same for y. Page P430 object 136 has 11 points. Those points are the polygon. They are not the bounds rectangle.

## Button bitmap

A button bitmap is an 8-byte prefix followed by a `BM` file in the huge table. The stored id is the resource id plus 1. Resource 155 of `9e954d01.tbk` is the prefix at file offset `0x50117`. The picture is 580 by 158, 8 bits per pixel.

## Huge-table bitmaps

`9e954d01.tbk` names four bitmaps in the huge table. Resource 148 is at `0x2577`, 581 by 157, 8 bits per pixel. Resource 150 is at `0x18ff7`, 580 by 387, 8 bits per pixel. Resource 155 stays at `0x50117`, 580 by 158, 8 bits per pixel. Resource 164 is at `0x1be627`, 580 by 158, 8 bits per pixel. That count is four.

## Missing files are reported, not fatal

Logic Families names `minstb32.dll`. That file is not in the install list. Opening the book reports `named, not shipped` and still returns the book. A name that is in the install list but absent is `not found`. A starred install-list entry that is absent is `listed, not shipped`. None of the three stops the open.
