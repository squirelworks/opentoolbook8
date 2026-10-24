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

The sentence `ICs are classified into logic families based on voltage requirements` is one example of text in the gap after `P440`'s body and before the next directory record. It is not in the `P430` body.

### Class `0x4`, 103 bytes, 14 records that agree

Fourteen records sit at near offset `0x14`, start with the word `0x0202`, and carry a C string at `+0x06`. The byte at `+0x4B` is the pattern and the three bytes at `+0x5B` are red, green, and blue. Logo is pattern 254 and color 0, 0, 191. Definition is pattern 254 and color 128, 128, 128. Overlay is pattern 253 and color 0, 0, 0, so the pattern and the color are fields, not one fixed value.

A fifteenth 103-byte run whose class word is also 4 contains the text `UhandleQuizKey`. It does not start with `0x0202` and it is not at near `0x14`. That run is one example.

### Class `0x8`, 41 bytes, 241 records

Word `+0x02` is 0, word `+0x08` is 65535, and words `+0x20` and `+0x26` are 0. The four signed words at `+0x0F` are an ordered rectangle in all 241. Two records:

```
0c0000001c03ffffffff08000029000b13e30d961efd118080800040404000010000040000fe00004f
250000001400ffffffff08000016006108b60d970eee11fffcf00080808000210000040000fd00002f
```

### Class `0x9`, 43 bytes, 398 records

Word `+0x02` is 0 and word `+0x20` is 0. The four signed words at `+0x0F` are an ordered rectangle in all 398. Two records:

```
11000000140005000600080000ffff51014a013e23a41000000000ffffff000300000000ac070901b60005
0b0000005001ffff0f00080000fffffd096900b218ed0300000000ffffff000300000000e20f0a01ca0119
```

### Class `0xA`, 61 bytes, 515 records

Word `+0x02` is 0, word `+0x20` is 0, word `+0x2E` is 720, and word `+0x34` is 0. The four signed words at `+0x0F` are an ordered rectangle in all 515. The text of a field is word 1 of the block named by the word at `+0x24`. That read returns both `Copyright ©  Nida Corporation 1997 - 2002` and `Filename: 93954d01.TBK`. Offset `+0x42` is past byte 61, so it is not a field of this record. Two records:

```
0900000014000600ffff0800000900f8009411a6259c18000000004080ff00430000ac07fe030000d002d002d002d00206415200000001000000000003
0000000014000600ffff0800000d0000001e00fb044a01e0e0e0000000bf0003000004066e010000900090009000d002b6495200000001000000000073
```

### Class `0xB`, 49 bytes, 369 records

Words `+0x02`, `+0x1A`, `+0x1C`, and `+0x20` are 0. Word `+0x08` is 65535. Word `+0x22` is 1. Two records:

```
1000000014000e00ffff000000fffffd096900b218ed03000000000000000001000001000200fd096900b218ed03840199
0f0000005001ffffffff000000ffff820c6801fe17fd02000000000000000001000001000200820c6801fe17fd02500265
```

### Class `0xC`, 41 bytes, 45 records

Words `+0x06` and `+0x08` are 65535. Words `+0x02`, `+0x20`, and `+0x26` are 0. The four signed words at `+0x0F` are an ordered rectangle in all 45. Two records:

```
230000001400ffffffff0800001800b0132b111914a31180808000f0f0f000010000040000fe0000bb
180000008402ffffffff08000033000b040d11a104b2110000000080808000010000040000fd000059
```

### Class `0xE`, 53 bytes, 526 records

Same length as class `0x10`, and a different record. Words `+0x06` and `+0x08` are 65535. Words `+0x02` and `+0x20` are 0. Word `+0x32` is 15 in every one of the 526. The four words at `+0x0F` are an ordered rectangle in 12 of them, so that rectangle is not a field of this class. Two records:

```
270000001400ffffffff0800001400fa05e10f6108e10ffffcf00080808000210000040000006108e10ffa05e10f00000f000f00a7
290000001400ffffffff0800001300970ee10f4911e10ffffcf00080808000210000040000004911e10f970ee10f00000f000f00e7
```

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

### Class `0x13`, 55 bytes, 65 records

Words `+0x06` and `+0x08` are 65535. Word `+0x02` is 0 and word `+0x0A` is 8. The four signed words at `+0x0F` are an ordered rectangle in 64 of the 65. The one that is not is one example. Two records that have the rectangle:

```
1d000000bc03ffffffff0800001b006e17760da017f40d4040ff00bf00000021000004000061177a0d9d17100e06005e0e00000f000f77
1e000000bc03ffffffff0800001a006117760d6e17760d4040ff00bf00000021000004000052177a0d61177a0d0200b40e00000f000fbd
```

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

The second record's bytes at `+0x04` are the C string `Key Map`. The first record is zero there. The shared words include `+0x00` = 517, `+0x28` = 65535, `+0x2C` = 5, and `+0x2E` = 5. The name is one example until a third record carries one. Two records:

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

## One example, no second record

These class words occur on one object only, so none of their fields is recorded as shared: `0x2`, `0x1C`, `0x20`, `0x25`, `0x27`, `0x31`, `0x33`, `0x3E`.
