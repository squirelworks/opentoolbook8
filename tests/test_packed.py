"""Packed huge-table bytes: counted blocks of repeat and copy codes."""

import unittest

from opentoolbook.packed import unpack


class UnpackTests(unittest.TestCase):
    def test_a_code_below_0xf6_repeats_the_next_byte_three_more_times(self):
        self.assertEqual(unpack(bytes((1, 0, 9, 0xA4))), b"\xa4" * 12)

    def test_a_code_from_0xf6_copies_that_many_bytes_minus_0xf5(self):
        self.assertEqual(unpack(bytes((2, 0, 0xF6, 0x62, 0xF8, 1, 2, 3))), bytes((0x62, 1, 2, 3)))

    def test_the_first_word_counts_the_codes(self):
        with self.assertRaises(ValueError):
            unpack(bytes((2, 0, 9, 0xA4)))
        with self.assertRaises(ValueError):
            unpack(bytes((1, 0, 9, 0xA4, 0)))

    def test_a_new_block_follows_the_last_code(self):
        self.assertEqual(unpack(bytes((1, 0, 0, 7, 1, 0, 0xF6, 8))), bytes((7, 7, 7, 8)))

    def test_a_block_does_not_start_on_the_last_byte_of_a_64k_span(self):
        nine = bytes(range(1, 10))
        codes = (bytes((0xFE,)) + nine) * 6553 + bytes((0xF7, 10, 11))
        first = (6554).to_bytes(2, "little") + codes
        self.assertEqual(len(first), 0xFFFF)
        stored = first + b"\xaa" + bytes((1, 0, 0, 5))
        self.assertEqual(unpack(stored), nine * 6553 + bytes((10, 11)) + b"\x05" * 3)


if __name__ == "__main__":
    unittest.main()
