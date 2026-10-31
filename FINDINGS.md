# What the bytes in 9e954d01.tbk repeat

The book on disk is the source. A field is recorded here when two records use it the same way. A value that shows up in only one record is marked as one example.

## Directory records

The file starts with an `MZ` stub. The bytes `03 4A 42 4F` are at file offset `0xc00`. In the next `0x200` bytes, one dword is the root of a four-level tree: each internal node has sixteen children at stride `0x14`, and each leaf page has sixteen entries at stride `0x18`. That dword is at header `+0x10E`. Every leaf that this tree names has a body whose first word is the tree key and whose second word is the stored length minus 2. The walk yields 206 records and their bodies do not overlap.

`nida81.tbk` uses the same rule. Its walk yields 114 records, and every body self-checks the same way.

The word at leaf `+0x08` has bit 14 set on 148 of the 206 records. The bytes after those bodies start with the word 1, then a count, then that many 12-byte headers. The third field of a header is a length, and that many bytes follow the headers. After the blobs come the word 1, a count of 4-byte items, another count, and that many 8-byte slots. This parse finishes inside the gap for all 148. For 144 of them the next directory record starts at that end. For four, more file bytes follow the trailer. The other records sit against the next record, except the last record, whose 84 trailing zero bytes are one example of padding at the end of the file.

## Object records

Inside a directory record the base is 6 bytes before the body. An object is a word at `at - 4` and a class word at `at - 2`. The first word is the object's end, measured from the base, so the object length is that word minus `at - base`. The classes below are the ones where two directory records both contain an object of the same class and the same length.

### Class `0x5`, 81 bytes, 131 records

Every one of these is the first object in a directory record. The object starts 14 bytes into the body. The byte at body offset 9 (object −5) is `0x80` on 129 records and `0x81` on the other two. The next three bytes are `65 00 05` on all 131: the size word is `0x65` and the class word is 5. Word `+0x00` is 514, word `+0x26` is 20, and word `+0x28` is 4352. The C string at `+0x06` is the page id. Two records whose flag byte is `0x80`:

```
0202640300005030007972696768740000000000000000000000000000000000000000000000140000116800a60398032001000000000000008a03ffff0000000000000000000014000051b80300000087
020201040000503100544c45006874000000000000000000000000000000000000000000000014000011000076006800200100010000004c053805ffff0000000000000000000014000071460500000073
```

The first string is `P0`. The second is `P1`.

The two records whose flag byte is `0x81` are `P440` (directory key `0x3200`, file `0xc7dbb`) and `P2920` (key `0xb700`, file `0x2085bf`). The bytes from object −8 through the page id:

```
2b371a816500050002026c0300005034343000
c3382281650005000202c1030000503239323000
```

Both names are in the page-id walk. No other byte of the 81-byte object is shared by these two and absent from the `0x80` pages. `nida81.tbk` has the same split: 43 pages use `0x80`, and `P22100` uses `0x81`, still followed by `65 00 05`. Which page that is in `nida81.tbk` is one example.

`TB80BAS` does not compare those four bytes. The page test in that image is the class word at object −2 equal to 5. The flag byte is outside that compare. The view-page function and the other compares are in `RESEARCH.md`.

The characters in the gap after `P440`'s body, and before the next directory record, start `ICs are classified into logic families based on voltage requirements`. They are not in the `P430` body. The record is a capacity word, a length word, and that many characters, in the trailer heap. On `P440` the words are 128 and 122 at file `0xcbad7`, and the characters start at `0xcbadb`. The stored characters are `\r\n\r\nICs are classified into logic families based on voltage requirements, speed and the number of circuits they can drive.` Every class `0x5` page has that record in the gap after its directory body: all 131 pages in this book, and all 44 pages in `nida81.tbk`. The capacity is not one value. `P400` stores 96 and 80 at file `0xbdffd`, and the characters are `\r\n\r\nDigital circuits and the IC chip are usually thought of as one and the same.` A class `0xA` field names the record on both pages, through word 1 of the block at `+0x24`.

### Class `0x4`, 103 bytes, 14 records that agree

Fourteen records sit at near offset `0x14`, start with the word `0x0202`, and carry a C string at `+0x06`. The byte at `+0x4B` is the pattern and the three bytes at `+0x5B` are red, green, and blue. Logo is pattern 254 and color 0, 0, 191. Definition is pattern 254 and color 128, 128, 128. Overlay is pattern 253 and color 0, 0, 0, so the pattern and the color are fields, not one fixed value.

A fifteenth 103-byte run whose class word is also 4 contains the text `UhandleQuizKey`. It does not start with `0x0202` and it is not at near `0x14`. That run is one example.

### Class `0x8`, 41 bytes, 243 records

Word `+0x02` is 0, word `+0x08` is 65535, and words `+0x20` and `+0x26` are 0. The four signed words at `+0x0F` are an ordered rectangle in all 243. Two records:

```
0c0000001c03ffffffff08000029000b13e30d961efd118080800040404000010000040000fe00004f
250000001400ffffffff08000016006108b60d970eee11fffcf00080808000210000040000fd00002f
```

### Class `0x8` colors

The bytes at `+0x17`, `+0x18`, and `+0x19` are a color, and the byte at `+0x1A` is 0. The bytes at `+0x1B`, `+0x1C`, and `+0x1D` are a color, and the byte at `+0x1E` is 0. The byte at `+0x25` is the pattern. The even scan finds 243 records. The patterns include 254, 33, 253, and 4. The 56 records whose pattern is 33 store color 0, 0, 0 and color 192, 192, 192. The 143 records whose pattern is 254 use more than one color. The first record above is pattern 254, colors 128, 128, 128 and 64, 64, 64. The second is pattern 253, colors 255, 252, 240 and 128, 128, 128.

`nida81.tbk` has 86 records of this class and length. The same two colors and the same pattern byte are present on all 86. The patterns are 254, 253, and 81. The two records whose pattern is 81 store color 240, 240, 240 and color 96, 96, 96. The 75 records whose pattern is 254 use more than one color. Eight records have left equal to right at `+0x0F`. One of them is (6821, 3534, 6821, 3536), colors 255, 255, 255 and 64, 64, 64, pattern 254.

### Class `0x9`, 43 bytes, 398 records

Word `+0x02` is 0 and word `+0x20` is 0. The four signed words at `+0x0F` are an ordered rectangle in all 398. Two records:

```
11000000140005000600080000ffff51014a013e23a41000000000ffffff000300000000ac070901b60005
0b0000005001ffff0f00080000fffffd096900b218ed0300000000ffffff000300000000e20f0a01ca0119
```

The word at `+0x28` is a near pointer from the segment base. It is 0 on two of the 398, and those two do not name a graphics block. On the other 396 the block starts with the word `0x0202`. The unaligned word at byte `0x15` of that block is a picture id. It equals a type-1 resource id plus one on all 396. The type-1 resource ids in this book are 100 through 166 with no gaps, so a stored id from 101 through 166 is also some other resource's id. The value 100, the only resource id that is not a stored id, does not occur. The value 167 is not a resource id, and it occurs on 7 buttons, so the field is the stored id. The stored ids of the four huge-table bitmaps, 149, 151, 156, and 165, occur in this word. 134 occurs 91 times, 131 occurs 84 times, and 116 occurs 23 times. Those three are stored ids of resources 133, 130, and 115, and none of those resources is in the huge table. The words at block `+0x27`, `+0x39`, and `+0x4b` are not stored ids on every button, so they are not this field. The word at `+0x4b` is 148 on six buttons, and on those six the picture id is 146. The word at record `+4` is 156 on two buttons. It is not the picture id. Two blocks, the first with stored id 151 and the second with stored id 167:

```
02020100000000000000000100fc21ad160000000097000000000000000000000000000000000000
02020000000000000000000100210c760200000000a7000000000000000000000000000000000000
```

`nida81.tbk` has 156 class `0x09` records of 43 bytes. The pointer is 0 on 7 of them. The other 149 name a block that starts with `0x0202`, and the word at byte `0x15` is a stored id on all 149. Two of those values, 150 and 152, are not resource ids in that book. Each of those two numbers occurs once.

### Class `0xA`, 61 bytes, 515 records

Word `+0x02` is 0, word `+0x20` is 0, word `+0x2E` is 720, and word `+0x34` is 0. The four signed words at `+0x0F` are an ordered rectangle in all 515. The text of a field is word 1 of the block named by the word at `+0x24`. That read returns both `Copyright ©  Nida Corporation 1997 - 2002` and `Filename: 93954d01.TBK`. Offset `+0x42` is past byte 61, so it is not a field of this record. Two records:

```
0900000014000600ffff0800000900f8009411a6259c18000000004080ff00430000ac07fe030000d002d002d002d00206415200000001000000000003
0000000014000600ffff0800000d0000001e00fb044a01e0e0e0000000bf0003000004066e010000900090009000d002b6495200000001000000000073
```

Word 0 of the block at `+0x24` is a run list on the fields where it is a trailer handle. On the even scan, 518 of these records sit in a segment that has a trailer. That word is `0xFFFF` on 432 of them and 0 on 4, and those 436 have no run list. The other 82 name a block whose second word is a count, followed by that many 11-byte runs. The same shape holds for all 52 handled fields in `nida81.tbk` (190 of its fields are `0xFFFF`, and 4 are 0).

The first word of each run is an offset into that field's text. Inside one block the offsets strictly increase, and each offset is at most the text length. The byte at run `+6` is 0 or 4. The byte at run `+10` is 0. That is all 224 runs in `9e954d01.tbk` and all 131 runs in `nida81.tbk`. The word at run `+2` is not a single value. The word in front of the count is not the count. Two blocks from `9e954d01.tbk`:

```
0300020000003407000000000000001200440400000000000000
080006000000920f0000000000000001002609000000f0f0f0001900920f000000000000001a002609000000f0f0f0003000920f0000000000000031002609000000f0f0f000
```

The first has offsets 0 and 18. The second has offsets 0, 1, 25, 26, 48, and 49.

### Class `0xB`, 49 bytes, 372 records

Words `+0x02`, `+0x1A`, `+0x1C`, and `+0x20` are 0. Word `+0x08` is 65535. Word `+0x22` is 1. Two records:

```
1000000014000e00ffff000000fffffd096900b218ed03000000000000000001000001000200fd096900b218ed03840199
0f0000005001ffffffff000000ffff820c6801fe17fd02000000000000000001000001000200820c6801fe17fd02500265
```

The word at `+0x24` is a count and the word at `+0x2E` is a near pointer to that many 10-byte entries. An entry is a child near offset, then the signed words left, top, right, and bottom. The child's word at `+4` is that group's near offset, on every child of 371 records. One child pointer does not land on an object. That pointer is one example.

The word at `+4` is a near pointer to the parent. On a class `0x9` button it is a page on 294 records, a group on 89, and a background on 15. On these 372 records it is a page on 168 and another group on 203. One group points at a background. That target is one example.

`Selection1` on `P300` is the group at near `0x9C`. The count is 2. The entries:

```
e201e2069204071ecc061002cb070d05a61d4806
```

The children are the button at `0x1E2` and the field at `0x210`. The rectangles are (1762, 1170, 7687, 1740) and (1995, 1293, 7590, 1608), the same words as each child's `+0x0F`. A second group, near `0x754`, is also a button then a field:

```
b008e809cf03c81a27063009aa0b590487197605
```

Those rectangles are (2536, 975, 6856, 1575) and (2986, 1113, 6535, 1398). The button entry equals that button's `+0x0F` on all 89 class `0x9` children. The field entry equals the field's `+0x0F` on 114 of 133 class `0xA` children.

The field entry follows the button entry on all 33 groups where the field rectangle sits inside the button rectangle, and on all 19 such groups in `nida81.tbk`. An inner class `0x13` entry is the later one on 24 lists and the earlier one on 4. Those four are why the list order is not a front byte.

`nida81.tbk` has 94 class `0xB` records of 49 bytes. The count, the pointer, and the 10-byte entries are the same shape, and each child's word at `+4` is the group. One group:

```
5c0b5f072d003a1d7602dc0b8f07a5001f1d0d02
```

The children are a button at `0xB5C` and a field at `0xBDC`. The rectangles are (1887, 45, 7482, 630) and (1935, 165, 7455, 525).

### Class `0xC`, 41 bytes, 45 records

Words `+0x06` and `+0x08` are 65535. Words `+0x02`, `+0x20`, and `+0x26` are 0. The four signed words at `+0x0F` are an ordered rectangle in all 45. Two records:

```
230000001400ffffffff0800001800b0132b111914a31180808000f0f0f000010000040000fe0000bb
180000008402ffffffff08000033000b040d11a104b2110000000080808000010000040000fd000059
```

### Class `0xE`, 53 bytes, 528 records

Same length as class `0x10`, and a different record. Words `+0x06` and `+0x08` are 65535. Words `+0x02` and `+0x20` are 0. Word `+0x32` is 15 in every one of the 528. The four words at `+0x0F` have area in 12 of the 528. On the other 516 one side is equal. Two records:

```
270000001400ffffffff0800001400fa05e10f6108e10ffffcf00080808000210000040000006108e10ffa05e10f00000f000f00a7
290000001400ffffffff0800001300970ee10f4911e10ffffcf00080808000210000040000004911e10f970ee10f00000f000f00e7
```

The four signed words at `+0x26` are the two endpoints. In the first record they are (2145, 4065) and (1530, 4065). In the second they are (4425, 4065) and (3735, 4065). On 520 records the words at `+0x0F` are those endpoints written as bounds, and the flat side is equal. Four of those 520 are diagonal: two lines, each stored in two records, with the endpoints on opposite corners. On the other 8 the long side matches the endpoints and the flat side is 37 past each endpoint. Two of those 8:

```
c90000001400ffffffff0800000a00281c690f721c3b10ffff0000808080000100000400000a4d1c690f4d1c3b1001000f100f00db
0e0000001400ffffffff080000120074138d116216d711fffcf00080808000210000040000006216b2117413b21101100f000f0095
```

The first endpoints are (7245, 3945) and (7245, 4155). The second are (5730, 4530) and (4980, 4530).

`nida81.tbk` has 24 class `0xE` records of 53 bytes. Word `+0x32` is 15, and words `+0x02` and `+0x20` are 0, on all 24. The endpoints are the four signed words at `+0x26`. Nineteen match the bounds. Five keep the long side and put 37 past the endpoints on the flat side. Two records:

```
b10000009003ffffffff000000ffff4803c111301bc11140404000ffffff00010000040000044803c111301bc11100000f000f007b
b20000009003ffffffff000000ffff4803b211301bb21160606000ffffff00010000040000044803b211301bb21100000f000f00b3
```

The first endpoints are (840, 4545) and (6960, 4545). The second are (840, 4530) and (6960, 4530).

### Class `0x10`, 53 bytes, 654 records

Words `+0x06` and `+0x08` are 65535. Words `+0x02`, `+0x20`, and `+0x26` are 0. The four signed words at `+0x0F` are an ordered rectangle in all 654, and so are the four signed words at `+0x28`. The word at `+0x30` is a count and the word at `+0x32` is a near pointer to that many stored pairs. Every stored pair lies in the rectangle at `+0x28`. The counts are not all the same: the records include lists of 11, 6, 4, 3, and 96 points. The reader returns those stored pairs. Two records:

```
0e0000001c03ffffffff0800002700bf13fd115514fc1200000000c0c0c000010000040000fe0000ae15a4104416ee110b000e043b
0f0000001c03ffffffff08000026005415fd11ea15fc1200000000c0c0c000010000040000fe0000ae15a4104416ee110b007604a3
```

### Class `0x11`, 61 bytes, 62 records

Words `+0x06` and `+0x08` are 65535. Words `+0x02` and `+0x20` are 0. Word `+0x22` is 4. Word `+0x34` is 768. Words `+0x38` and `+0x3A` are 15. The four signed words at `+0x0F` are an ordered rectangle in all 62. The signed pairs at `+0x25` and `+0x29` are the stored points. Forty-three records store (5433, 3955) and (5428, 3544). Nineteen store (1866, 5065) and (1815, 4620). One of each:

```
0d0000001c03ffffffff0800002800fd112d0fbf13d11080808000000000000100000400003915730f3415d80d0915a60eff00d2000300000f000f007b
110000008802ffffffff08000026009213c70bae15f20dffffff00ffff00000100000400004a07c91317070c121707ed120e01e1000300000f000f0069
```

### Class `0x11` third pair, and why the window does not paint arcs

The signed pair at `+0x2D` is a third point. On all 62 arcs in `9e954d01.tbk` and both in `nida81.tbk` the three pairs at `+0x25`, `+0x29`, and `+0x2D` are one of three triples, and each triple occurs on arcs whose rectangles at `+0x0F` differ:

| book | count | `+0x25` | `+0x29` | `+0x2D` | words `+0x31`, `+0x33`, `+0x35` |
|---|---|---|---|---|---|
| `9e954d01.tbk` | 43 | (5433, 3955) | (5428, 3544) | (5385, 3750) | 255, 210, 3 |
| `9e954d01.tbk` | 19 | (1866, 5065) | (1815, 4620) | (1815, 4845) | 270, 225, 3 |
| `nida81.tbk` | 2 | (3465, 4126) | (3316, 4320) | (3465, 4320) | 150, 195, 22 |

The words at `+0x37` and `+0x39` are 3840 on all 64. In the first two rows the y of the third pair is within 3 of halfway between the first two (3750 against 3749.5, 4845 against 4842.5). In the third row it is not.

On P1140 objects 17, 65, and 80 store the second triple. Their rectangles are (5010, 3015, 5550, 3570), (2985, 3030, 3525, 3585), and (5010, 3675, 5550, 4230). Drawing the stored pairs would put all three arcs on the same spot, outside every one of those rectangles. The TBKX export's arc `Vertices` sit inside the rectangle: object 80 is `5331,4224,5280,3675`. Against the rectangle's left and top, the export x offsets differ by 51, the same 51 as the stored x values (1866 and 1815). The export y span is 549 where the stored y span is 445, so the y mapping is not a shift. On the first triple the spans are equal (411). The source rectangle that would map the stored pairs onto the rectangle at `+0x0F` is not named by bytes that repeat, so the arc stays off the display list. The words at `+0x31` and `+0x33` may be angles. That is not settled.

### Class `0x13`, 55 bytes, 66 records

Words `+0x06` and `+0x08` are 65535. Word `+0x02` is 0 and word `+0x0A` is 8. The four signed words at `+0x0F` are an ordered rectangle in 64 of the 66. The other two are flat: (5985, 3446, 5998, 3446) and (6678, 3421, 6678, 3446). Two records:

```
1d000000bc03ffffffff0800001b006e17760da017f40d4040ff00bf00000021000004000061177a0d9d17100e06005e0e00000f000f77
1e000000bc03ffffffff0800001a006117760d6e17760d4040ff00bf00000021000004000052177a0d61177a0d0200b40e00000f000fbd
```

The word at `+0x2D` is a count and the word at `+0x2F` is a near pointer to that many signed pairs. On all 66 the pointer is 3 bytes past the record. The count is 3 on 30 records and 4 on 23. The records also include lists of 2, 5, 6, and 7. A list of 8 and a list of 10 are one example each. The two records above are a list of 6 and a list of 2:

```
9d17100e7f17e00d7817dd0d6117bc0d61179b0d61177a0d
61177a0d52177a0d
```

The first pairs are (6045, 3600), (6015, 3552), (6008, 3549), (5985, 3516), (5985, 3483), and (5985, 3450). The second are (5985, 3450) and (5970, 3450). On 61 records the next object's header is the byte after the pairs. On the other five, one byte follows the pairs.

`nida81.tbk` has 14 class `0x13` records of 55 bytes. The word at `+0x2D` is the count and the word at `+0x2F` points 3 bytes past the record, on all 14. Twelve are lists of 3. A list of 2 and a list of 4 are one example each. The next object's header is the byte after the pairs on all 14. Two lists of 3:

```
a2033a11a2031806a71c1806
b1033a11981c3a11981c1806
```

The first pairs are (930, 4410), (930, 1560), and (7335, 1560). The second are (945, 4410), (7320, 4410), and (7320, 1560).

### Class `0x13` bounds

The four signed words at `+0x25` are the minimum x, the minimum y, the maximum x, and the maximum y of those pairs. That holds for all 66 records, and for all 14 in `nida81.tbk`. On the flat record whose `+0x0F` is (5985, 3446, 5998, 3446), the words at `+0x25` are (5970, 3450, 5985, 3450). On the flat record whose `+0x0F` is (6678, 3421, 6678, 3446), the words at `+0x25` are (6795, 3420, 6795, 3450).

### Class `0x15`, 89 bytes, 5 records

Twenty-four words are the same in all five, including `+0x04` = 20, `+0x06` and `+0x08` = 65535, and `+0x1A` = 65280. Two records:

```
020000001400ffffffff080000ffff000000009024e61900000000ffffff0001000001040000fe000020a00c00000000009024e61900000000010000000000000000000000000000000000000004000000dc01000000000005
100000001400ffffffff0000003300eaff0000a724680100000000ffffff000100000f010000fe0000e03a000016150000bd2468010000000001000000000000000000000000000000000000000600a700e8020000000000ad
```

### Class `0x17`, 17 bytes, 5 records

Word `+0x06` is 11, word `+0x08` is 65535, and words `+0x02` and `+0x0E` are 0. Two records:

```
0400000040020b00ffff00a6021000009b
060000009c000b00ffff0002013c0000f7
```

### Class `0x26`, 83 bytes, 2 records

The second record's bytes at `+0x06` are the C string `Key Map`. The first record is zero there. The shared words include `+0x00` = 517, `+0x28` = 65535, `+0x2C` = 5, and `+0x2E` = 5. One class `0x26` record in `nida81.tbk` carries the same string. Two records:

```
0502000000000000000000000000000000000000000000000000000000000000000000000000c800ffff0000050005002025701a11012640200358027702d501ba0014000000000000008400000000008000b7
0502010000004b6579204d6170000000000000000000000000000000000000000000000000005801ffff000005000500b0138016001125002003580270001b00ac001400000000000000860000000000800075
```

### Smaller agreements

Class `0x2B`, 28 bytes, two records. Both start `00000100`, then a length byte and a C string. The strings are `Test2` and `Title`.

Class `0x2D`, 30 bytes, two records. Both start `00000100` and then a C string, `Overlay` and `IntroEnd`. The length byte differs, so the string is the shared field and the length is part of that string.

Class `0x2E`, 128 bytes, two records. Both start with the word 6 and then a page id (`Q1139` and `Q1137`). The rest is a list of the same shape.

Class `0x22`, 140 bytes, two records. The bytes are text. The two runs share the surrounding words and differ in the page ids embedded in the text (`p1311` and `p2241`).

Class `0x23`, 68 bytes, six records. All six are the same bytes:

```
022251011424003b020520402398002b45085e00040a23b6002b423b02051b402390002c09052e40218f0002fcff056a4223980002f8ff3a001100243b02083700040a23
```

## Quiz questions

Twenty pages, `P10210` through `P10229`, each hold five class `0xA` fields named `Stem`, `A`, `B`, `C`, and `D`. In the trailer heap, the slot before a property name holds the value: the word `0x0009`, a length word, and that many characters. `P10210` and `P10211` both use it.

`P10210` answer value and name:

```
0600090001004300770003000000416e7377657200
```

That value is `C`. The same bytes on `P10211` have `42` where `P10210` has `43`, so the value is `B`. The following value slots are `110` and `111`, named `QuestionNo`, then `1` and `1`, named `TestNo`.

Page `PQINFO` has a field named `InfoText`. Its filled rows are page, test, and question. All twenty question pages' `TestNo` and `QuestionNo` are those two columns. The answer letters are not all the same.

The info rows also name a help page. Nineteen question pages contain a length-prefixed `P` plus that number. Page `10215` contains `P1310` where the info row says `30000`, so that string is not the info column.

The same `0x0009` slot holds `SourceQuestionNo`, `SourceTestNo`, and `sourcepage` on all twenty pages. `SourceQuestionNo` is the same characters as `QuestionNo`. `SourceTestNo` is the same characters as `TestNo`. `sourcepage` is the page id, `P10210` through `P10229`.

The name `SourceLesson` is on all twenty pages, and the characters in front of it are `93954302.tbk`. The word before that length is `0x0009` on nineteen pages and `0x0004` on `P10210`.

## One example, no second record

These class words occur on one object only, so none of their fields is recorded as shared: `0x2`, `0x1C`, `0x20`, `0x27`, `0x31`, `0x33`, `0x3E`.

## Small classes in nida81.tbk

`nida81.tbk` has one class `0x15` record of 89 bytes. The constant words match except at `+0x24`, `+0x26`, `+0x3A`, and `+0x3C`. Each of those four values occurs once. The four signed words at `+0x0F` are an ordered rectangle in all five records of `9e954d01.tbk`. Two of them are (0, 0, 9360, 6630) and (-22, 0, 9383, 360). The `nida81.tbk` record is ordered there too, (525, 405, 8835, 6255), and that rectangle is one example.

`nida81.tbk` has no class `0x17` record of 17 bytes. On each of the five records in `9e954d01.tbk`, the word at `+0x04` is a near pointer to a 61-byte class `0xA` field, and that field is named `Text`. On page `P1080` the word is `0x240`. On page `P1082` it is `0x9C`.

`nida81.tbk` has two class `0x26` records of 83 bytes, and those records use the same constant words. One of the two carries the C string `Key Map`. That is a second record with the string.

## Class `0xD` words at +0x28 and +0x2A

All 14 class `0xD` records in `nida81.tbk` are on page `P22100`. The word at `+0x28` equals the word at `+0x2A` on all 14: 27 on two, 56 on eight, and 11 on four. A rounded corner size would fit, but nothing in the repo names it, so the window draws square corners. The bytes `01 00 00 01 00 00` at `+0x1F` through `+0x24` are the same on 10 records; the byte at `+0x1F` is 3 on the four whose pair is 11. Two records:

```
170100009e08ffffffff0000004900721c5010471da31060606000ff000000010000010000fe00001b001b004b
da0000000019ffffffff0000001400161a500d391a9713ffffff0060606000030000010000fe00000b000b008b
```

## Class `0x19`

`nida81.tbk` has 39 class `0x19` records of 89 bytes. `9e954d01.tbk` has none. Word `+0x02` is 0. Words `+0x06` and `+0x08` are 65535. Word `+0x1E` is 256, word `+0x36` is 768, and word `+0x38` is 512. The byte at `+0x26` is 254. The four signed words at `+0x0F` are an ordered rectangle in all 39. The word at `+0x04` is a near pointer to an object. On 31 records it is 20 and names the page. On the other 8 it names a class `0xB` record of 49 bytes. Page `P370` object 38 is one of those eight: the word is `0x9C`. Two records whose pointer is the page:

```
240000001400ffffffff080000ffff3804b103f519f41a00000000ffffff000100000f010000fe0000e08a0400be2902000000000000000300020000000000000073018d01080000000000000006000001f800000000000021
250000001400ffffffff080000ffff28050a05681f801600000000ffffff000100000f010000fe0000a01f04006a83020000000000000003000200000000000000c0012a01080000000000000007000001ec03000000000015
```

The first is object 36 on page `P310`, bounds (1080, 945, 6645, 6900). The second is object 37 on page `P320`, bounds (1320, 1290, 8040, 5760).

## The word at byte 2 of a style run

The book record's word at `+0x28` is a near pointer. The first word of that block is a count, and that many near pointers follow. The count is 63 in `9e954d01.tbk` and 30 in `nida81.tbk`. The second word is 63 in the first book and 24 in the second, so it is not the count.

62 of the 63 pointers in `9e954d01.tbk` address a C string. The strings stored more than once are Arial (28), Nida (9), System (5), MS Sans Serif (5), Times New Roman (4), WP Greek Helve (3), ShelleyAllegro BT (2), and Symbol (2). Pointer `0xe8a` does not start with a C string. That pointer is one example.

26 of the 30 pointers in `nida81.tbk` address a C string. Arial is stored 13 times, MS Sans Serif 5 times, System 3 times, and Nida twice. The other four slots are the pointers `0x620` and `0xb9c`, each stored twice. Neither starts with a C string.

The word at byte 2 of a style run is 1, or it is one of those pointers and the bytes there are a C string. The value 1 is not a pointer in the table. In `9e954d01.tbk` it is 1 on 134 of the 224 runs. Of the other 90, 74 name Arial, 8 name MS Sans Serif, and 7 name Wingdings. One run names MS Shell Dlg, which is one example. The two runs in the first block quoted under class `0xA` name Arial (`0x0734`) and MS Sans Serif (`0x0444`).

In `nida81.tbk` the word is 1 on 61 of the 131 runs and Arial on 69. One run names Times New Roman, which is one example.

The word at `+0x22` of a class `0xA` field is one of the C-string pointers on every such field. In `9e954d01.tbk` that is Arial on 492 fields, MS Sans Serif on 13, System on 10, and Small Fonts on 3. In `nida81.tbk` it is Arial on 225 fields and MS Sans Serif on 21.

## Class `0x0B` rectangle

The four signed words at `+0x0F` are a rectangle on all 372 class `0x0B` records in `9e954d01.tbk` and all 94 in `nida81.tbk`. The right is past the left and the bottom is past the top. The two records in the class `0x0B` section are (2557, 105, 6322, 1005) and (3202, 360, 6142, 765). Two records in `nida81.tbk`:

```
300000001400ffffffff000000ffff8f169f062b208a0c000000000000000001000001000c00f816900694207b0c4c08c5
4c0000001400ffffffff000000ffff5f072d003a1d76020000000000000000010000010002005f072d003a1d7602440b59
```

Those are (5775, 1695, 8235, 3210) and (1887, 45, 7482, 630).

That rectangle is the union of the rectangles at `+0x0F` of the objects in the same segment whose word at `+0x04` names the record. The objects are class `0x8` (41 bytes), `0x9` (43), `0xA` (61), `0xB` (49), `0xC` (41), `0xE` (53), `0x10` (53), `0x11` (61), and `0x13` (55): 1838 objects in `9e954d01.tbk`, and the union matches on all 372. `nida81.tbk` also names 14 class `0xD` records of 45 bytes and the 8 class `0x19` records above. With those included, the union matches on all 94.

One class `0xC` record of 43 bytes and one class `0x10` record of 57 bytes in `nida81.tbk` also name a class `0x0B` record. Each length occurs once. Both lie inside, and the union matches without them.

The rectangles stored in the list at `+0x2E` are not this union. That list's union equals `+0x0F` on 188 of the 372 records and on 44 of the 94. The four words at `+0x26` differ from `+0x0F` on 184 of the 372 and on 50 of the 94.

## Class `0xC` colors

The bytes at `+0x17`, `+0x18`, and `+0x19` are a color, and the byte at `+0x1A` is 0. The bytes at `+0x1B`, `+0x1C`, and `+0x1D` are a color, and the byte at `+0x1E` is 0. The byte at `+0x25` is the pattern. That holds for all 45 class `0xC` records of 41 bytes in `9e954d01.tbk` and all 37 in `nida81.tbk`. The two records in the class `0xC` section are pattern 254, colors 128, 128, 128 and 240, 240, 240, and pattern 253, colors 0, 0, 0 and 128, 128, 128.

In `9e954d01.tbk` the pattern is 253 on 23 records and 254 on 22. Each of those two groups uses more than one color. In `nida81.tbk` the pattern is 254 on all 37, and those records use more than one color. On page `P410` both ellipses use pattern 253 and color 0, 0, 0, the same pattern and the same color as that page's background, and color 128, 128, 128. Their bounds are (1035, 4365, 1185, 4530) and (3375, 6105, 3525, 6270). On page `P310` of `nida81.tbk`, five of the ten ellipses use pattern 254 and color 128, 128, 128, the same pattern and the same color as that page's background, and color 255, 255, 255. Two of those five are (6045, 2010, 6120, 2085) and (6045, 2250, 6120, 2325).

## Class `0x10` colors

The bytes at `+0x17`, `+0x18`, and `+0x19` are a color, and the byte at `+0x1A` is 0. The bytes at `+0x1B`, `+0x1C`, and `+0x1D` are a color, and the byte at `+0x1E` is 0. The byte at `+0x25` is the pattern. That holds for all 654 class `0x10` records of 53 bytes in `9e954d01.tbk` and all 76 in `nida81.tbk`. The two records in the class `0x10` section are pattern 254, colors 0, 0, 0 and 192, 192, 192.

In `9e954d01.tbk` the pattern is 254 on 621 records, 119 on 14, and 105 on 14. A pattern of 12 occurs on 4 records. A pattern of 21 is one example. The 14 records whose pattern is 119 store color 0, 0, 0 and color 64, 128, 64. The 14 whose pattern is 105 store color 0, 0, 0 and color 191, 64, 64. The 621 records whose pattern is 254 use more than one color. In `nida81.tbk` the pattern is 254 on all 76, and those records use more than one color. Seventeen of them store the same color in both triples.

## Picture ids outside the huge table

The type-1 directory is the dword at header `+8 + (1 + 5) * 4`. The same shape of slot with a resource id in place of the type is header `+(id + 5) * 4`, and the reader's own base is header `+8 + (id + 5) * 4`. Neither dword is the file offset of an 8-byte prefix followed by `BM`. That was checked for all 63 type-1 ids in `9e954d01.tbk` that are not in the huge table, and all 23 such ids in `nida81.tbk`.

Resource 133 is stored id 134. `(133 + 5) * 4` is `0x228`. The dword at header `+0x228` is 0, and the dword at header `+8 + 0x228` is 0. Resource 130 is stored id 131. The dword at header `+0x21C` is 0. The dword at header `+8 + 0x21C` is `0x01400006`, past the end of the file.

In `nida81.tbk`, resource 116 is not in the huge table. The dword at header `+(116 + 5) * 4` is `0x00040000`. The 16 bytes at that offset are `74 20 6c 61 77 20 61 6e 64 20 61 6c 6c 20 20 20`. Byte 8 of those is `0x64`, not `BM`. The dword at header `+8 + (116 + 5) * 4` is 0. The same `0x00040000` is the slot for resources 126, 131, 141, and 146, so it is not an offset of resource 116.

## Field words at +0x28, +0x2A, +0x2C, +0x32, and byte +0x36

The field scan finds 518 class `0xA` records of 61 bytes in `9e954d01.tbk`. The class note above says 515. Word `+0x2E` is 720 and word `+0x34` is 0 on all 518. The five values are not one combination. Twenty-seven combinations occur. The ones shared by more than one field:

| count | +0x28 | +0x2A | +0x2C | +0x32 | +0x36 |
|---|---|---|---|---|---|
| 258 | 0 | 0 | 0 | 50 | 1 |
| 86 | 187 | 187 | 0 | 50 | 1 |
| 85 | 360 | 360 | 310 | 50 | 5 |
| 18 | 360 | 360 | 360 | 50 | 4 |
| 16 | 720 | 720 | 720 | 50 | 1 |
| 9 | 144 | 144 | 144 | 50 | 1 |
| 6 | 0 | 0 | 0 | 50 | 5 |
| 6 | 360 | 360 | 360 | 50 | 3 |
| 4 | 0 | 0 | 0 | 82 | 1 |
| 4 | 0 | 0 | 0 | 562 | 1 |
| 3 | 0 | 0 | 0 | 48 | 0 |
| 3 | 144 | 144 | 144 | 82 | 1 |
| 3 | 360 | 360 | 0 | 50 | 1 |
| 2 | 0 | 0 | 0 | 434 | 1 |
| 2 | 360 | 360 | 360 | 58 | 1 |
| 2 | 720 | 720 | 720 | 58 | 3 |

The other eleven combinations occur once. Of the 85 fields on the row 360, 360, 310, 50, 5, 84 are named `Text` and one is named `text`. The `Text` field on `P400` and the `Text` field on `P440` are that row.

`nida81.tbk` has 246 fields of this length. Word `+0x2E` is 720 and word `+0x34` is 0 on all 246. Sixteen combinations occur. The ones shared by more than one field:

| count | +0x28 | +0x2A | +0x2C | +0x32 | +0x36 |
|---|---|---|---|---|---|
| 100 | 0 | 0 | 0 | 50 | 1 |
| 74 | 0 | 0 | 0 | 434 | 1 |
| 19 | 360 | 360 | 310 | 50 | 5 |
| 18 | 144 | 144 | 144 | 50 | 1 |
| 8 | 360 | 360 | 360 | 50 | 1 |
| 7 | 0 | 0 | 0 | 58 | 1 |
| 7 | 360 | 0 | 0 | 82 | 1 |
| 2 | 0 | 0 | 0 | 48 | 1 |
| 2 | 0 | 0 | 0 | 50 | 4 |
| 2 | 0 | 0 | 0 | 50 | 5 |
| 2 | 144 | 144 | 144 | 82 | 1 |

The other five combinations occur once. Of the 19 fields on the row 360, 360, 310, 50, 5, two are named `text` and the other seventeen have no name.

## Style run bytes 4, 5, 7, 8, and 9

`9e954d01.tbk` has 224 runs. `nida81.tbk` has 131.

Byte 4 in the first book is 0 on 219 runs, 238 on 3, and 146 on 2. Byte 5 is 0 on 222 and 2 on 2. The two runs with byte 5 equal to 2 are the two with byte 4 equal to 146, so the word at byte 4 is `0x0292` on those two and 238 on the three. All five have the face word 1. In `nida81.tbk` byte 4 is 0 and byte 5 is 0 on all 131 runs.

Byte 7 in the first book is 255 on 111, 0 on 84, 240 on 20, and 64 on 9. Byte 8 is 0 on 84, 252 on 62, 255 on 49, 240 on 20, and 64 on 9. Byte 9 is 0 on 128, 240 on 82, 255 on 9, 64 on 3, and 191 on 2. In `nida81.tbk` byte 7 is 0 on 81, 255 on 37, and 64 on 13. Byte 8 is 0 on 79, 255 on 27, 252 on 14, 64 on 9, and 128 on 2. Byte 9 is 0 on 93, 255 on 20, 240 on 14, 191 on 2, and 64 on 2.

The seven Wingdings runs in `9e954d01.tbk` store 0 at bytes 4, 5, 7, 8, and 9. `nida81.tbk` has no Wingdings run. The word at byte 4 of an Arial run is 0 on all 74 Arial runs in the first book and all 69 in the second. That is the same word the Wingdings runs store. The word at byte 7 is not one value on the Arial runs. No point size is read from these bytes. The size is in the font-table entry the run's word at byte 2 names; `SETTLED.md` has that read.

## Class `0x15` words that vary

Twenty-four words are the same on all five records, as the class note says. The other twenty words vary. Their offsets are `+0x00`, `+0x0A`, `+0x0C`, `+0x0E`, `+0x10`, `+0x12`, `+0x14`, `+0x16`, `+0x22`, `+0x28`, `+0x2A`, `+0x2C`, `+0x2E`, `+0x30`, `+0x32`, `+0x34`, `+0x4C`, `+0x4E`, `+0x50`, and `+0x52`. The last byte varies too. None of those twenty words is a type-1 resource id, and none is a stored id in 101 through 166.

The word at `+0x00` is 2, 16, 20, 16, 20. The two records whose id is 16 share the word `0xA700` at `+0x4E`. The two whose id is 20 share `0x1D00` there. Reading an unaligned word at `+0x4F` on the first pair yields 167, because byte `+0x4F` is `0xA7` and byte `+0x50` is 0. Resource 166 starts `02 02 07 00`. The bytes `01 02 01 00` and `BM` occur later in that resource, at `+18` and `+26`. That unaligned 167 is not a picture field. It is the palette color count of the class `0x15` paint object, which `SETTLED.md` now reads with the record's huge-table row and info-header pointer.

## Class `0x19` tail

`nida81.tbk` has 39 records. `9e954d01.tbk` has none. The words that stay the same on all 39, beyond the constants already listed, are `+0x20`, `+0x30`, `+0x32`, `+0x34`, `+0x46`, `+0x48`, `+0x4A`, `+0x4E`, `+0x54`, and `+0x56`, each 0. The byte at `+0x26` is 254 on all 39. The word at `+0x26` is 254 on 38. On object 84 it is `0x78FE`, and the low byte is still 254.

The words that vary are `+0x00`, `+0x04`, `+0x0A`, `+0x0C`, `+0x0E`, `+0x10`, `+0x12`, `+0x14`, `+0x16`, `+0x18`, `+0x1A`, `+0x1C`, `+0x22`, `+0x24`, `+0x26`, `+0x28`, `+0x2A`, `+0x2C`, `+0x2E`, `+0x3A`, `+0x3C`, `+0x3E`, `+0x40`, `+0x42`, `+0x44`, `+0x4C`, `+0x50`, and `+0x52`. The last byte varies. `+0x0E` through `+0x14` are the bounds, different on every record. `+0x4C` is different on every record. `+0x44` is 2048 on 25 records and 2049 on 14.

The word at `+0x04` is the near pointer already recorded: a class 5 page on 31 records and a class `0xB` record of 49 bytes on 8. No other word names one class on more than one record.

`SETTLED.md` now reads the record as a picture: `+0x29`, `+0x2D`, `+0x4D`, and the metafile in the huge table. The words at `+0x41` and `+0x43` are within two of the DIB width and height: the DIB is wider by 0 on 29 records and by 1 on 10, and taller by 1 on 29, by 0 on 7, and by 2 on 3. The window does not use them; it uses the metafile window extent. The word at `+0x45` is 8, the DIB depth, on all 39. The word at `+0x51` points at a 40-byte block of zeros followed by a 256-color palette; the reader uses the palette inside the metafile instead. The word at `+0x2A` is 144 on 3 records. The word at `+0x2E` is 147 on 6 records and 0 on 6. 144 and 147 are type-1 resource ids in this book. The dword at header `+(144 + 5) * 4` is `0x0F960000`. The dword at header `+(147 + 5) * 4` is `0x01400006`. Both are past the end of the file. The same slots hold other values on the other records, so neither word is a picture id.

## Page scripts that are not inline

The low two bits of the byte at `+0x30` are 0 on 128 pages of `9e954d01.tbk` and on 40 pages of `nida81.tbk`. They are 2 on the other pages: `P10301`, `P10302`, and `P10303` in the first book, and `P12000`, `P12001`, `P12002`, and `P12003` in the second. The word at `+0x2A` on those pages is `0x175`, `0x176`, `0x177`, and `0x9F`, `0xA0`, `0xA1`, `0xA2`. The `buttonClick` reader does not expand that word. Objects on those pages whose own script is inline are still read.

## nida71.tbk is named, not opened

`nida81.tbk` names `nida71.tbk` from pages `P12000`, `P12001`, `P12002`, and `P12003`. On each of those pages the button `Retry` has the line `go to page "P12060" of book "nida71.tbk"`. Page `P12001` also has `go to page "P12000" of book "nida71.tbk"`. The file is not in this read.

## Names in the four nc81 books

None of `nc81base.sbk`, `nc81recs.sbk`, `nc81test.sbk`, or `nc81trnr.sbk` stores the words `to handle`. The names below are plain text.

In `nc81base.sbk` one run of strings is `P10003`, `P10004`, `__lessonMode`, `gotoQuizPage`, then `__quizPreTest`, `__quizAssessment`, `P10002`, `P900`, `__lessonMode`, `__quizDisableMenuKey`, `P10001`, `getMenuPage`, then `getMenuPage`, `setupMenuPage`, `gotoMenuPage`, then `P902`, `P904`, `P901`, `__lessonMode`, `setupMenuPage`, `P903`, `setupMenuPageLocal`. A later catalog, with no page id on the same line, names `gotoMenuPage()`, `setupMenuPage(`, `clearMenuFlags()`, `setMenuFlag(`, and `getMenuFlag(`. `gotoNextQuestionEx` occurs beside `__lessonMode` and the text `nc81test.sbk`, not beside those page ids. The same page ids occur again as quoted text beside `getMenuPage`. That second copy is not copied out here as a condition tree.

`nc81test.sbk` stores `handleQuizClick` beside `__quizReviewPage`, and again beside `gotoNextQuestionEx`. The catalog that names `gotoNextQuestionEx()` also names `__quizAssessment` and `__quizPreTest`, and it does not put a page id on those lines. `P10301`, `P10302`, and `P10303` sit beside `__quizStartPage`. `P19999` sits beside `getNextQuestion` and `gotoNextQuestion`.

`nc81recs.sbk` has no page id. The plain names are `initializeRecs()`, `openSession()`, `closeSession()`, `bookmarkSession()`, `StartSession()`, and `RestartSession()`, plus `getFirst()`, `getLast()`, `getId()`, `getClass()`, and `getCurrentPath()`.

`nc81trnr.sbk` has no page id in that kind of list. `P366` occurs once, inside a script, and not beside a name. The plain names are `initializeTrnr()`, `getTrainerType()`, `getTrainerPort()`, `startExperiment()`, `endExperiment()`, `checkComm130()`, `saveSettings130()`, `loadSettings130()`, `checkComm130E()`, `startCai130E()`, `endCai130E()`, `readVoltages130E()`, `saveSettings130E()`, `loadSettings130E()`, `checkCommTd2000()`, `startCaiTd2000()`, `endCaiTd2000()`, `readVoltageTd2000()`, `saveSettingsTd2000()`, `loadSettingsTd2000()`, `checkComm5050()`, `clearFaults5050()`, `readMain5050()`, `verifyMain5050()`, `verifyExternal5050()`, `checkComm205E()`, `readFrequency205E()`, `setFrequency205E()`, `readVolume205E()`, `readCard205E()`, `clearFaults205E()`, `flushMessageQueue()`, `readExternal5050()`, and `readcard205E()`.

## Line colors

The bytes at `+0x17`, `+0x18`, and `+0x19` are a color, and the byte at `+0x1A` is 0, on all 528 class `0x0E` records in `9e954d01.tbk` and all 24 in `nida81.tbk`. The bytes at `+0x1B`, `+0x1C`, and `+0x1D` are a color, and the byte at `+0x1E` is 0, on those same records. The two records in the class `0x0E` section store 255, 252, 240 and 128, 128, 128. In `nida81.tbk` the two records in that section store 64, 64, 64 and 255, 255, 255, and 96, 96, 96 and 255, 255, 255.

In `9e954d01.tbk` the first color is 192, 192, 192 on 154 records and 160, 160, 164 on 154. The second color is 255, 255, 255 on 384. Ten color pairs each occur on more than one endpoint pair. Twelve endpoint pairs are stored with more than one color pair, so the colors are not the endpoints. In `nida81.tbk` five color pairs each occur on more than one endpoint pair. No endpoint pair there is stored with two color pairs.

The byte at `+0x25` is 4 on 372 records, 0 on 91, 10 on 63, and 14 on 2. In `nida81.tbk` it is 4 on 18, 14 on 3, 0 on 2, and 10 on 1. The endpoints begin at `+0x26`. A pattern byte on a class `0x8`, `0xC`, or `0x10` record is not 0. This byte is not that pattern.

## Type 10 handler bytes

The type-10 directory is the dword at header `+8 + (10 + 5) * 4`. Its entries are the same 8-byte shape as the type-1 directory. `9e954d01.tbk` lists ids 372, 373, 374, and 376. `nida81.tbk` lists ids 158, 159, 160, 161, and 165. The type-9 directory in each book lists those same ids.

Each type-10 record is 15 bytes, the class word at −2 is `0x2A`, and the record starts `02 02 01 00`. The word at `+6` is 0 and the word at `+0x0B` is `0xFFFF`. The word at `+9` is a near pointer. The word at that pointer is a count, and that many bytes follow. The last of those bytes is 0. Those bytes expand to a handler. In `9e954d01.tbk` three begin `to handle enterPage` and one begins `to handle enterSystem`. In `nida81.tbk` four begin `To handle enterpage` and one begins `to handle enterApplication`.

The word at `+4` of the 15-byte record is not that pointer. On three type-10 records in `nida81.tbk` it is the same value. That address is 1550 bytes into the handler bytes of id 158.

A page whose script-mode byte has low bits 2 stores a word at `+0x2A`. That word minus 1 is one of these type-10 ids, on all three such pages in `9e954d01.tbk` and all four in `nida81.tbk`. Each of those seven words occurs once. The type-9 record with the same id is also 15 bytes and starts `02 02 01 00`. The bytes at its `+9` pointer do not expand to a handler.

## Lesson zip directory

The local file `die0dv03.zip` is one byte, `78`. It is a one-byte stub, the same pattern as `93954302.tbk`, which is also the one byte `78`. The stub does not contain `50 4b 01 02` or `50 4b 05 06`. It is not opened.

Two other archives do contain a central directory. `att-cd.zip` has 449 records and `toolbook-files.zip` has 120. Every record in both begins with the 46-byte header whose shared constant bytes are `50 4b 01 02` at 0, `14 03 14 00` at 4, `00` at 9 and at 11, `5d` at 15, `00` at 23 and at 29, and `18 00 00 00 00 00 00 00 00 00` at 30. Each archive ends with 22 bytes that begin `50 4b 05 06 00 00 00 00` and end `00 00`. The bytes between those differ. `att-cd.zip` names `Nida98/Lessons/nida81.tbk` and does not name a `.zip`. `toolbook-files.zip` names `.c` and `.html` files. Neither archive is the local `die0dv03.zip`.

## Polygon source rectangle and bounds

On a class `0x10` record the four signed words at `+0x28` are the source rectangle and the four signed words at `+0x0F` are the bounds. Those two rectangles are equal on 3 of the 654 records in `9e954d01.tbk`: (3915, 5190, 5565, 6495), (3615, 3435, 5745, 5985), and (3675, 3480, 5655, 3615). They are equal on 2 of the 76 records in `nida81.tbk`: (4395, 3660, 8040, 4605) and (7740, 3660, 8055, 5805). The other records do not share one relationship between the four edges. That is not a scale.

## Group entry union

The union of the rectangles stored in the 10-byte entries equals the group's rectangle at `+0x0F` on 188 of the 372 groups in `9e954d01.tbk` and on 44 of the 94 groups in `nida81.tbk`. The union of the rectangles at `+0x0F` of the objects whose word at `+0x04` names the group equals that rectangle on all 372 and all 94. The 10-byte list is left as stored.

## Class `0x25`

Class `0x25` is a 49-byte record in both books, at near `0x14` of the segment whose key is `0x2100`. The byte at object −5 is `0x80`. The 49 bytes are the same in both files. Words `+0x00` through `+0x22` are 0. Word `+0x24` is 20, word `+0x26` is 4352, word `+0x28` is 72, word `+0x2A` is 2, word `+0x2C` is 0, and word `+0x2E` is 65535. The last byte is `0x53`. The two segments are not the same length.

`nida81.tbk` has no second record of class `0x2`, `0x1C`, `0x20`, `0x27`, `0x31`, `0x33`, or `0x3E`. Those stay one example.

## Pattern bytes

The background pattern is the byte at `+0x4B`. `9e954d01.tbk` has 15 backgrounds: 254 on 12, 253 on 2, and 0 on 1. `nida81.tbk` has 20 backgrounds, and every one is 254.

The pattern on a class `0x8`, `0xC`, or `0x10` record is the byte at `+0x25`. Class `0x8` in `9e954d01.tbk` is 254 on 143, 33 on 56, 253 on 41, and 4 on 3, of 243 records. In `nida81.tbk` it is 254 on 75, 253 on 9, and 81 on 2, of 86 records. Class `0xC` in `9e954d01.tbk` is 253 on 23 and 254 on 22, of 45 records. In `nida81.tbk` all 37 are 254. Class `0x10` in `9e954d01.tbk` is 254 on 621, 105 on 14, 119 on 14, 12 on 4, and 21 on 1, of 654 records. In `nida81.tbk` all 76 are 254.

`0xFE` occurs in both books on all four of those fields. `0xFD` occurs in both books on class `0x8`. `0xFF` does not occur on any of those fields in either book. The other values stay numbers.

## TBKX export of this book

The export is a TB115 naming of `9e954d01`. The bytes below are the TB80 file. A field is listed here when the export name and the bytes already read are the same value on more than one record.

The export object id is the word at the start of the record. Rectangle is class `0x8`, button `0x9`, field `0xA`, group `0xB`, ellipse `0xC`, line `0xE`, irregular polygon `0x10`, arc `0x11`, and angled line `0x13`. Five hotwords are class `0x17`. The field `Review 2` on `P10410` is the last object of its directory record and stores 1 as its end word. The page walk now reads that case, as `SETTLED.md` says.

Field `Text`, with the `{...}` tokens removed, is the character record on 230 named fields. `InfoText` on `PINFO` stores one newline the export does not. That newline is one example. A token such as `{size:18}` is not a character in the record.

On all twenty quiz pages the export `Stem`, `A`, `B`, `C`, `D`, `Answer`, `QuestionNo`, and `TestNo` are the values the reader returns. `SourceQuestionNo`, `SourceTestNo`, and `sourcepage` are those same characters.

A class `0x10` count is the number of pairs in `Vertices`, on all 654. Those pairs are the stored points on 3 records, where the source rectangle equals the bounds. The other stored points are not the export vertices.

A class `0x0E` line's endpoints are `Vertices`, on all 528. The color at `+0x17` is `RgbStroke` and the color at `+0x1B` is `RgbFill`, on all 528.

A button `NormalGraphic` of `bitmap id N` stores N + 1, on all 380 buttons that name a graphic. A `CheckedGraphic` of `bitmap id N` stores N + 1 at byte `0x4b` of that block, on all 301 buttons that name one. The word is 0 on the other 95 blocks. `nida81.tbk` stores a picture id there on 79 blocks and 0 on 70. An `InvertGraphic` of `bitmap id N` stores N + 1 at byte `0x27` of that block, on all 311 buttons that name one. The word is 0 on the other 85 blocks. `nida81.tbk` stores a picture id there on 79 blocks and 0 on 70. A `DisabledGraphic` of `bitmap id N` stores N + 1 at byte `0x39` of that block, on all 17 buttons that name one. The word is 0 on the other 379 blocks, and on all 149 blocks in `nida81.tbk`.

Background `RgbFill` is the first color and `RgbStroke` is the second color, on all 131 pages. `solidFill` is pattern byte 254 and `none` is pattern byte 253.

Field `Indents` are the words at `+0x28`, `+0x2A`, and `+0x2C`, on 386 fields. The rectangle at `+0x0F` is `Bounds` on those 386 fields, on 382 buttons, on 45 ellipses, and on 243 rectangles.

A class `0x13` count is the number of pairs in `Vertices`, on all 66. Those pairs are the stored points on 4 records.

Type 19 resources 100, 101, 102, and 103 are the four shared scripts. Each record is 15 bytes, class `0x2A`, and starts with `0x0202`. The word at `+9` names a payload that starts `01 02 13 00`. The first `80 81` in that payload expands to the script. Resource 102 is `response = answer of this page`, then `score = 100` or `score = 0`.

A button `BorderStyle` is the byte at `+0x27`, on all 382 buttons. `none` is 1, `radioButton3d` is 9, and `pushButton` is 7. `nida81.tbk` stores 1 on 149 of these buttons and 7 on 7. `Enabled` is bit 0 of the byte at `+0x26`, on all 398 buttons. `true` is 1 and `false` is 0. `nida81.tbk` stores 1 on 93 and 0 on 63. `Checked` is bit 4 of that byte, on all 398 buttons. `true` is 1 on 11 and `false` is 0 on the rest. Every button in `nida81.tbk` stores 0. `Transparent` is the same split as `BorderStyle` in this book: every `none` button is `true` and the other 89 are `false`. That is not a second field.

A field `BorderStyle` is the byte at `+0x36`, on 496 fields. `none` is 1, `scrolling` is 2, `shadowed` is 3, `raised` is 4, `inset` is 5, and `rectangle` is 0. One export field is not that record. That field is one example. `nida81.tbk` stores 1 on 222 of these fields, 5 on 22, and 4 on 2.

The export arc `Vertices` are not the stored pairs at `+0x25` and `+0x29`, on any of the 62 arcs.

The words `0x0013` and `0x0068` sit in the 55 bytes after the page record on all twenty quiz pages, and on none of the 91 other pages with that same gap. `0x0068` is 104. The export calls the shared script id 103. That pair occurs once. `HelpPage` is not the `0x0009` value slot. `SourceLesson` is that slot on 19 pages. On `P10210` the word in that place is `0x0004`. That page is one example. Line `LineStyle` is not the byte at `+0x25`.

## Quiz handlers

`nc81test.sbk` type 10 resource 741 is one script of `to get` handlers. `nida81.tbk` does not store these names. The lesson stores the calls.

`to get gotoNextQuestionEx` contains:

```
	if  __quizPass <= 3  and  __quizIndex > 0  then	
		response = getQuizResponse()
		score = 0
		if  response <> ""  then
			if  response = answer of this page  then
				score = 100
			end if
			get storeQuestionResponse(testNo of this page, questionNo of this page, response, score)
		else
			get storeQuestionSkipped(testNo of this page, questionNo of this page)
		end if
	end if
```

`to get gotoPreviousQuestionEx` contains the same pass test, the same `getQuizResponse()`, and the same `response = answer of this page` then `score = 100`. The other branch there is `score = 0`. It calls the same `storeQuestionResponse(testNo of this page, questionNo of this page, response, score)` and does not call `storeQuestionSkipped`.

`to get getQuizScore` and `to get getQuizScorePM` both contain:

```
	step i from 1 to __quizCount
		increment(count)
		score = score + __quizScore[i]	
	end step
```

`getQuizScore` then contains `error = score div count` when `count` is past 0. `getObjectiveScore` uses that same `div` for the entries whose `__quizTestNo[i]` is the objective. `getQuizScorePM` contains `error = score / count`. `to get storeQuestionResponse` is the function that writes `__quizScore[__quizIndex] = score`, `__quizResponse[__quizIndex] = response`, and `__quizAttempted[__quizIndex] = 1`.

`to get startCompletionPass`, `to get startChangePass`, and `to get startCritiquePass` each set `__quizIndex = 0` and call `gotoNextQuestionEx()`. The `__quizPass` values are 2, 3, and 4. `to get handleQuizClick` also calls `gotoNextQuestionEx()` when the button is `OK`, `Skip`, or `Next`. That is six calls.

`to get getNextQuestion` returns `getNextRandomX(__quizNumbers)`. `to get getPreviousQuestion` returns `getPreviousRandomX(__quizNumbers)`. `getNextRandomX` adds 1 to `__xIndex` and returns `numbers[__xIndex]` when the index was below the count. `getPreviousRandomX` subtracts 1 and returns that entry when the index was not 1.

On `9e954d01.tbk` the background `Test` is the one named by pages `P10210` through `P10229`. Its `buttonClick` is `get handleQuizClick(target)`. The three type 10 handlers whose ids are 372, 373, and 374 each contain `get handleQuizKey(key)` when the key is `keyF7`. Group `selection1` on pages `P10001`, `P10002`, `P10003`, and `P10004` each calls `setupQuizEx` with `2`, `"P10301"`, `"P10302"`, and `"P10303"`. The first argument is `Assessment`, `Pre-Test`, `Post-Test`, or `Quiz`. After that call the same four scripts contain `get clearpool()`, `addObjectiveToPool(1, 110, 119, 6)`, `addObjectiveToPool(2, 120, 129, 4)`, `setuppool()`, and `get gotoNextQuestionEx()`. Each of the four ends with the line `end buttonClick`.

`to get getquizResponse` is one function. It walks `ansiToChar(96 + i)` and keeps the name of a checked button. `to get processQuizScore` in `nc81base.sbk` is one function. It writes the score into `NIDAREC.INI`. `to get handleQuizKey` is one function.

## Class `0x12` in otb-pie.tbk

`otb-pie.tbk` is a blank native book saved by ToolBook II Instructor 8.1. The page id is empty. Instructor reports two pie objects on that page, ids 0 and 2, and one ellipse, id 1. `9e954d01.tbk` and `nida81.tbk` have no class `0x12` record of this length. The ellipse is the class `0xC` record already described. These notes are the pie records only.

Both pies are class `0x12`. The length formula used for the other draw objects, the end word minus the near offset of the id word, is 59 on pie id 0. Pie id 2 is the last object in that directory record, so it has no following end word inside the record. Its bytes match the first 58 bytes of pie id 0 in the slots below. The 59th byte of pie id 0 is `0x0D`, which is the low byte of the next object's end word.

The two records use the same bytes at `+0x02` through `+0x0E`: `00 00 14 00 ff ff ff ff 08 00 00 ff ff`. Word `+0x04` is `0x14`, the page's near offset. They use the same bytes at `+0x17` through `+0x24`: `00 00 00 00 00 00 00 00 01 00 00 04 32 0f`. They use the same bytes at `+0x36` through `+0x39`: `fe 3e 07 00`.

The four signed words at `+0x0F` are the bounds. Pie id 0 is `(600, 600, 3000, 3000)`. Pie id 2 is `(-1400, 500, 2400, 500)`. Those two rectangles are not the same, so the slot is the one that changes with the object. The top and bottom of pie id 2 are both 500.

The bytes at `+0x25` through `+0x35` are not the same in the two records. Pie id 0, drawn `from 1500,1500 to 3500,3500 to 1500,3500` and then given the bounds above, stores signed words `1500, 3500, 1500, 1500, 1500, 3500, 0, 2000` from `+0x25`. Pie id 2, drawn `from 2400,500 to 1500,2200 to 500,500`, stores `500, 500, 2400, 500, 500, 500, 1900, 0`. The second `to` point of pie id 2, `1500, 2200`, is not one of those words. That region is two examples, not a settled point list. Both examples store the third point, the first point, the third point again, and the per-axis distance from the first to the third (`SETTLED.md`, "Pie wedge refused"). A pie whose second point is not on an axis through the third, saved once and again after Reshape Pie, would show where the end of the wedge is stored.

An ellipse in the same book is 41 bytes and puts its pattern byte at `+0x25`. A pie is longer, and `+0x25` is the first of the words above, not that pattern byte. Class `0x11` is 61 bytes and class `0x10` is 53. Neither length is 59.

## Version FileVersion

The version-resource string `FileVersion` is not one value. `otb-line-rect.tbk` and `nida81.tbk` store `8.1.0.0`. `9e954d01.tbk`, `nc81base.sbk`, `nc81recs.sbk`, `nc81test.sbk`, and `nc81trnr.sbk` store `8.1.0.664`. The fixed file-version low dword in that block is 0 for the first pair and 664 for the second. `FileDescription`, `InternalName`, `OriginalFilename`, `ProductVersion`, and `CompanyName` are the same bytes in all seven files.

