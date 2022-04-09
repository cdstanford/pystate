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

SHIFT_FWD1 = 0b00000000000000000000000000000010
SHIFT_BCK1 = 0b10000010011000001000111011011011
SHIFT_FWD8 = 0b00000000000000000000000100000000
SHIFT_BCK8 = 0b10101001110100111110011010100110

SHIFT_BCK_32 = 0xcbf1acda

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
CRC32 calculation
"""
def rev_bits(x, width=32):
    # Reverse-bits function
    x_bin = bin(x)[2:].zfill(width)
    x_bin_rev = ''.join(reversed(x_bin))
    return int(x_bin_rev, 2)

def crc_push(c, byte):
    c ^= byte
    c = crc_mul(c, SHIFT_FWD8)
    return c

def crc_pop(c, byte):
    c = crc_mul(c, SHIFT_BCK8)
    c ^= byte
    return c

# Real CRC32 calculation agreeing with the standard implementation
def crc32(x, init=0):
    result = rev_bits(init ^ MAX_32)
    for byte in x:
        result = crc_push(result, rev_bits(byte))
    return rev_bits(result ^ MAX_32)

# CRC that we use here for convenience
def crc_ours(x, init=0):
    result = init ^ MAX_32
    for byte in x:
        result = crc_push(result, byte)
    return result ^ MAX_32

"""
The core superclass and decorators that do CRC tracking automatically.

- Superclass wrapper which allows calling .get_crc()
- Method decorators which update the stack-based CRC code
"""
class TrackState:
    def __init__(self):
        self._stack_crc = MAX_32

    def get_crc(self):
        return self._stack_crc ^ MAX_32

# Mandatory decorator for the __init__ function
def track_init(f):
    def init_super(self):
        self._stack_crc = MAX_32
        f(self)
    return init_super

# Optional decorator for any function calls to track
def track_stack_calls(f):
    def deco(self, *args, **kwargs):
        self._stack_crc = crc_push(self._stack_crc, *args)
        print(f"Call {args}, CRC {hex(self._stack_crc)}")
        f(self, *args, **kwargs)
        self._stack_crc = crc_pop(self._stack_crc, *args)
        print(f"Return {args}, CRC {hex(self._stack_crc)}")
    return deco

"""
Unit tests
"""
class TestCrc32(unittest.TestCase):
    def test_constants(self):
        assert MAX_32 == 4294967295
        assert POLY_32 <= MAX_32
        assert POLY_32 + MAX_32 + 1 == POLY_33

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

    def test_mul_shift_fwd(self):
        shift1 = 2
        shift2 = crc_mul(shift1, shift1)
        shift4 = crc_mul(shift2, shift2)
        shift8 = crc_mul(shift4, shift4)
        assert shift8 == 256
        assert shift1 == SHIFT_FWD1
        assert shift8 == SHIFT_FWD8

    def test_mul_shift_bck(self):
        shift1 = SHIFT_BCK1
        shift2 = crc_mul(shift1, shift1)
        shift4 = crc_mul(shift2, shift2)
        shift8 = crc_mul(shift4, shift4)
        assert shift8 == SHIFT_BCK8

    def test_mul_inverses(self):
        assert crc_mul(1, 1) == 1
        assert crc_mul(SHIFT_FWD1, SHIFT_BCK1) == 1
        assert crc_mul(SHIFT_FWD8, SHIFT_BCK8) == 1
        assert crc_mul(POLY_32, SHIFT_BCK_32) == 1

    def test_rev_bits(self):
        assert rev_bits(1, 1) == 1
        assert rev_bits(1, 2) == 2
        assert rev_bits(3, 2) == 3
        assert rev_bits(0, 4) == 0
        assert rev_bits(3, 4) == 12
        assert rev_bits(6, 4) == 6
        assert rev_bits(10, 4) == 5

    """
    TODO: Failing unit tests
    """

    def test_crc32_easy(self):
        assert crc32(b"") == 0
        assert crc32(b"\xFF") == 0xff000000

    def test_crc32_medium(self):
        assert crc32(b"\x00") == 0xd202ef8d
        assert crc32(b"a") == 0xe8b7be43
        assert crc32(b"abc") == 0x352441c2
        assert crc32(b"cat") == 0x9e5e43a8

    def test_crc32_hard(self):
        assert crc32(b"a" * 100) == 0xaf707a64

if __name__ == "__main__":
    # Run unit tests
    unittest.main()
