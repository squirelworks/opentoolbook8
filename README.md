# opentoolbook8

Rebuilding Toolbook8 from analysis.

A clean-room reading of how ToolBook II 8 loads one object record.

The behaviour is the lesson-open path in `TB80BAS`: the radix-tree directory, the body read, the two-byte follow-up when the entry asks for one, and the class procedure that message `0xE` is handed to. The procedure is the far pointer at the start of that class's `0x76`-byte slot. The message number is an argument to the procedure. The lookup uses index 0.

```
python -m opentoolbook path/to/book.tbk
python -m unittest tests/test_record.py
```

`OPENTOOLBOOK_TBK` points the extra test at a lesson book. Without it, the tests use a synthetic directory.

On a live stop with the lesson already open, handle `0x0C1E` had class word `0x0001`. The lookup returned `0x2BAF:0000`, the live selector of the class dispatcher, and `ECX` was `0x76`. The 412-byte record (handle `0x0C36` on the October trace) takes the same path. This boot did not reach that return.
