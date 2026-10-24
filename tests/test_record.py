"""The directory walk and the class-procedure lookup."""

import os
import struct
import unittest

from opentoolbook.record import (
    CLASS_SLOT,
    FOLLOW_UP,
    MESSAGE_AFTER_LOAD,
    Book,
    handler_at,
    procedure_for_message,
)

# The lesson open of 20 October 2026. These are file positions and sizes,
# not the lesson text.
TRACED_POSITION = 0xB7221
TRACED_LENGTH = 0x19C
TRACED_TYPE = 0x25
TRACED_SLOT = 0x1286


def _book_with(body: bytes, flags: int = 0x4001, type_byte: int = 0x11) -> bytes:
    """One real leaf under key 0x1000, plus the header that points at it."""
    key = 0x1000
    length = len(body)
    stored = struct.pack("<HH", key, length - 2) + body[4:]
    # header, three internal nodes, one leaf page, then the body
    header_at = 0
    level0 = 0x200
    level1 = 0x400
    level2 = 0x600
    leaf = 0x800
    body_at = 0xA00
    data = bytearray(body_at + length + FOLLOW_UP)
    data[header_at:header_at + 4] = b"\x03JBO"
    struct.pack_into("<I", data, header_at + 0x10E, level0)
    struct.pack_into("<I", data, level0, level1)
    struct.pack_into("<I", data, level1, level2)
    struct.pack_into("<I", data, level2, leaf)
    # nibble 1 of the top key, so the leaf index is 1 and the key is 0x1000
    slot = leaf + ENTRY_INDEX * 0x18
    struct.pack_into("<I", data, slot, body_at)
    struct.pack_into("<H", data, slot + 8, flags)
    struct.pack_into("<H", data, slot + 0x0C, length)
    data[slot + 0x16] = type_byte
    data[body_at:body_at + length] = stored
    data[body_at + length:body_at + length + FOLLOW_UP] = b"\x01\x00"
    return bytes(data)


ENTRY_INDEX = 1


class DirectoryTests(unittest.TestCase):
    def test_follow_up_is_the_two_bytes_after_the_body(self):
        raw = _book_with(b"\x00\x10" + b"\x00" * 30)
        book = Book(raw)
        self.assertEqual(len(book.records), 1)
        loaded = book.load(book.records[0])
        self.assertEqual(loaded.record.key, 0x1000)
        self.assertTrue(loaded.record.wants_follow_up)
        self.assertTrue(loaded.record.on_disk_status)
        self.assertEqual(loaded.follow_up, b"\x01\x00")
        self.assertEqual(len(loaded.body), 32)

    def test_a_clear_flag_does_not_read_past_the_body(self):
        raw = _book_with(b"\x00\x10" + b"\x00" * 30, flags=0x0001)
        loaded = Book(raw).load(Book(raw).records[0])
        self.assertEqual(loaded.follow_up, b"")

    def test_rejects_a_file_without_the_header(self):
        with self.assertRaises(ValueError):
            Book(b"not a book")


class HandlerTests(unittest.TestCase):
    def test_zero_class_has_no_procedure(self):
        self.assertIsNone(handler_at(0, b"\x00" * 8))

    def test_index_zero_is_the_first_far_pointer_of_the_slot(self):
        # Class 0x25, the type byte of the traced 412-byte record.
        # The captured return for the neighbouring class was 10B0:0000,
        # which is the first pointer of that class, not message 0xE.
        slots = bytearray(0x26 * CLASS_SLOT)
        at = 0x25 * CLASS_SLOT
        struct.pack_into("<HH", slots, at, 0x0000, 0x10B0)
        struct.pack_into("<HH", slots, at + MESSAGE_AFTER_LOAD * 4, 0x1234, 0x10F8)
        self.assertEqual(handler_at(0x25, slots, 0), (0x10B0, 0x0000))
        procedure, message = procedure_for_message(0x25, slots, MESSAGE_AFTER_LOAD)
        self.assertEqual(procedure, (0x10B0, 0x0000))
        self.assertEqual(message, 0xE)


class SpecimenTests(unittest.TestCase):
    def setUp(self):
        path = os.environ.get("OPENTOOLBOOK_TBK")
        if not path or not os.path.isfile(path):
            self.skipTest("set OPENTOOLBOOK_TBK to the lesson book")
        with open(path, "rb") as handle:
            self.book = Book(handle.read())

    def test_traced_record(self):
        match = [item for item in self.book.records if item.position == TRACED_POSITION]
        self.assertEqual(len(match), 1)
        record = match[0]
        self.assertEqual(record.length, TRACED_LENGTH)
        self.assertEqual(record.type_byte, TRACED_TYPE)
        self.assertEqual(record.flags, 0x4001)
        self.assertEqual(record.slot, TRACED_SLOT)
        self.assertEqual(self.book.data[record.slot + 0x14:record.slot + 0x18], b"\x00\x21\x25\x00")
        self.assertTrue(record.wants_follow_up)
        loaded = self.book.load(record)
        self.assertEqual(len(loaded.body), TRACED_LENGTH)
        self.assertEqual(loaded.body[12], TRACED_TYPE)
        self.assertEqual(loaded.follow_up, b"\x01\x00")
        self.assertEqual(len(self.book.records), 206)


if __name__ == "__main__":
    unittest.main()
