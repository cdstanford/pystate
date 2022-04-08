"""
Basic functionality for CRC32 codes

This should match a library implementation such as binascii.crc32,
but we also need the more primitive CRC arithmetic operations.
"""

import unittest

# Polynomial:
#   x^32 + x^26 + x^23 + x^22 + x^16
#     + x^12 + x^11 + x^10 + x^8 + x^7
#     + x^5 + x^4 + x^2 + x + 1
POLY_33 = 0b100000100110000010001110110110111
POLY_32  = 0b00000100110000010001110110110111
MAX_32   = 0b11111111111111111111111111111111
assert MAX_32 == 4294967295
assert POLY_32 <= MAX_32
assert POLY_32 + MAX_32 + 1 == POLY_33

"""
Polynomial arithmetic (on 32-bit values)
"""
def crc_add(x, y):
    return x ^ y

def crc_mul(x, y):
    result = 0

    # Multiply stage
    for i in range(32):
        result ^= (y << i) if (x & (1 << i)) else 0

    # Reduce mod 'poly'
    for i in range(31, -1, -1):
        result ^= (POLY_33 << i) if (result & (1 << (32 + i))) else 0

    assert result <= MAX_32
    return result

"""
CRC calculation
"""
def crc(x, init=0):
    result = init ^ MAX_32
    for byte in x:
        result ^= byte
        result = crc_mul(result, POLY_32)
    return result ^ MAX_32

"""
Unit tests
"""
class TestCrc32(unittest.TestCase):
    def test_mul(self):
        # Matching regular multiplication
        assert crc_mul(0, 0) == 0
        assert crc_mul(0, 37) == 0
        assert crc_mul(1, 1) == 1
        assert crc_mul(1, 255) == 255
        assert crc_mul(2, 2) == 4
        assert crc_mul(2, 12) == 24
        assert crc_mul(8, 9) == 72
        assert crc_mul(8, 16) == 128
        assert crc_mul(50, 5) == 250
        assert crc_mul(2, 2**30) == 2**31
        # Matching Nim multiplication, but no overflow
        assert crc_mul(3, 3) == 5
        assert crc_mul(4, 8) == 32
        assert crc_mul(9, 9) == 65
        assert crc_mul(41, 5) == 141
        # Overflow cases
        assert crc_mul(2, 2**31) == POLY_32
        assert crc_mul(2, MAX_32) == POLY_32 ^ MAX_32 ^ 1
        assert crc_mul(3, MAX_32) == POLY_32 ^ 1
        assert crc_mul(8, 2**31) == 4 * POLY_32
        assert crc_mul(128, 2**31) == (64 * POLY_32) ^ POLY_33

    def test_crc32(self):
        # TODO: Failing unit test
        assert crc(b"") == 0
        assert crc(b"a") == 0xe8b7be43
        assert crc(b"abc") == 0x352441c2
        assert crc(b"cat") == 0x9e5e43a8
        assert crc(b"a" * 100) == 0xaf707a64

if __name__ == "__main__":
    # Run unit tests
    unittest.main()
